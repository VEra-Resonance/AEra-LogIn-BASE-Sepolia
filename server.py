"""
VEra-Resonance Backend - FastAPI Server
Creator: Karlheinz Beismann
Project: VEra-Resonance — Decentralized Proof-of-Human Architecture
License: Apache 2.0 (see LICENSE file)
© 2025 VEra-Resonance Project

Verifies wallet addresses and manages Resonance Scores
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import time
import json
import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
import hashlib
import secrets

# ===== IMPORT CUSTOM LOGGER =====
from logger import logger, api_logger, db_logger, wallet_logger, airdrop_logger, log_activity

# Load environment variables
load_dotenv()

# Config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
INITIAL_SCORE = int(os.getenv("INITIAL_SCORE", 50))
MAX_SCORE = int(os.getenv("MAX_SCORE", 100))
SCORE_INCREMENT = int(os.getenv("SCORE_INCREMENT", 1))
TOKEN_SECRET = os.getenv("TOKEN_SECRET", "aera-secret-key-change-in-production")
TOKEN_EXPIRY_DAYS = int(os.getenv("TOKEN_EXPIRY_DAYS", 7))

# Airdrop Configuration
ADMIN_WALLET = os.getenv("ADMIN_WALLET", "")
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY", "")
AERA_CONTRACT = "0x5032206396A6001eEaD2e0178C763350C794F69e"
AIRDROP_AMOUNT = 0.5  # AEra Tokens
SEPOLIA_RPC = os.getenv("SEPOLIA_RPC_URL", "https://sepolia.infura.io/v3/YOUR_INFURA_KEY")

app = FastAPI(
    title="VEra-Resonance API",
    description="Decentralized Proof-of-Human System",
    version="0.1"
)


# CORS-Middleware für Browser-Zugriff (mit Environment-Variablen konfigurierbar)
allowed_origins = [origin.strip() for origin in CORS_ORIGINS]
if "*" in allowed_origins:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

logger.info(f"✓ CORS Konfiguration: {allowed_origins}")

# Registriere Static Files (CSS, JS, etc.)
static_dir = os.path.join(os.path.dirname(__file__))
try:
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"✓ Static Files mounted: {static_dir}")
except Exception as e:
    logger.warning(f"⚠️ Static Files konnten nicht gemountet werden: {e}")

# Templates für dynamische Landing Pages
templates = Jinja2Templates(directory=static_dir)

# Datenbank-Konfiguration
DB_PATH = os.path.join(os.path.dirname(__file__), "aera.db")

# Platform-Konfiguration für dynamisches Styling
PLATFORM_CONFIG = {
    "twitter": {
        "name": "X / Twitter",
        "color": "#1DA1F2",
        "gradient": "linear-gradient(135deg, #1DA1F2 0%, #0D8BD9 100%)",
        "emoji": "𝕏",
        "badge": "FROM X/TWITTER"
    },
    "telegram": {
        "name": "Telegram",
        "color": "#0088cc",
        "gradient": "linear-gradient(135deg, #0088cc 0%, #006699 100%)",
        "emoji": "✈️",
        "badge": "FROM TELEGRAM"
    },
    "discord": {
        "name": "Discord",
        "color": "#5865F2",
        "gradient": "linear-gradient(135deg, #5865F2 0%, #4752C4 100%)",
        "emoji": "💬",
        "badge": "FROM DISCORD"
    },
    "instagram": {
        "name": "Instagram",
        "color": "#E1306C",
        "gradient": "linear-gradient(135deg, #833AB4 0%, #FD1D1D 50%, #FCAF45 100%)",
        "emoji": "📷",
        "badge": "FROM INSTAGRAM"
    },
    "facebook": {
        "name": "Facebook",
        "color": "#1877F2",
        "gradient": "linear-gradient(135deg, #1877F2 0%, #0D5DBF 100%)",
        "emoji": "👥",
        "badge": "FROM FACEBOOK"
    },
    "linkedin": {
        "name": "LinkedIn",
        "color": "#0A66C2",
        "gradient": "linear-gradient(135deg, #0A66C2 0%, #084D92 100%)",
        "emoji": "👔",
        "badge": "FROM LINKEDIN"
    },
    "reddit": {
        "name": "Reddit",
        "color": "#FF4500",
        "gradient": "linear-gradient(135deg, #FF4500 0%, #CC3700 100%)",
        "emoji": "🤖",
        "badge": "FROM REDDIT"
    },
    "youtube": {
        "name": "YouTube",
        "color": "#FF0000",
        "gradient": "linear-gradient(135deg, #FF0000 0%, #CC0000 100%)",
        "emoji": "📺",
        "badge": "FROM YOUTUBE"
    },
    "tiktok": {
        "name": "TikTok",
        "color": "#000000",
        "gradient": "linear-gradient(135deg, #000000 0%, #FF0050 100%)",
        "emoji": "🎵",
        "badge": "FROM TIKTOK"
    },
    "direct": {
        "name": "Direct",
        "color": "#667eea",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "emoji": "⚡",
        "badge": "DIRECT ACCESS"
    }
}

def get_db_connection():
    """Erstelle Datenbankverbindung mit WAL-Modus für Concurrency"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA cache_size = -64000")  # 64MB Cache
    conn.execute("PRAGMA busy_timeout=10000")  # 10s Timeout
    db_logger.debug(f"DB Connection established: {DB_PATH}")
    return conn

def extract_referrer_source(referrer: str) -> str:
    """
    Extrahiert die Quelle aus dem Referrer (z.B. 'twitter', 'telegram', 'direct')
    """
    if not referrer:
        return "direct"
    
    referrer_lower = referrer.lower()
    
    # Social Media Platforms
    if "twitter.com" in referrer_lower or "x.com" in referrer_lower or "t.co" in referrer_lower:
        return "twitter"
    elif "telegram" in referrer_lower or "t.me" in referrer_lower:
        return "telegram"
    elif "facebook.com" in referrer_lower or "fb.com" in referrer_lower:
        return "facebook"
    elif "instagram.com" in referrer_lower:
        return "instagram"
    elif "reddit.com" in referrer_lower:
        return "reddit"
    elif "discord" in referrer_lower:
        return "discord"
    elif "youtube.com" in referrer_lower or "youtu.be" in referrer_lower:
        return "youtube"
    elif "linkedin.com" in referrer_lower:
        return "linkedin"
    elif "tiktok.com" in referrer_lower:
        return "tiktok"
    
    # Search Engines
    elif "google" in referrer_lower:
        return "google"
    elif "bing" in referrer_lower:
        return "bing"
    elif "duckduckgo" in referrer_lower:
        return "duckduckgo"
    
    # Crypto/Web3
    elif "etherscan" in referrer_lower:
        return "etherscan"
    elif "opensea" in referrer_lower:
        return "opensea"
    
    # Other
    elif "localhost" in referrer_lower or "127.0.0.1" in referrer_lower:
        return "localhost"
    elif "ngrok" in referrer_lower:
        return "ngrok-test"
    else:
        return "other"

def init_db():
    """Initialisiert Datenbank mit notwendigen Tabellen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users-Tabelle
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        address TEXT PRIMARY KEY,
        first_seen INTEGER,
        last_login INTEGER,
        score INTEGER DEFAULT 50,
        login_count INTEGER DEFAULT 0,
        created_at TEXT,
        first_referrer TEXT,
        last_referrer TEXT
    )
    """)
    
    # Events-Tabelle für Audit-Trail (erweitert mit referrer)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        event_type TEXT,
        score_before INTEGER,
        score_after INTEGER,
        timestamp INTEGER,
        created_at TEXT,
        referrer TEXT,
        user_agent TEXT,
        ip_address TEXT
    )
    """)
    
    # Airdrops-Tabelle für Tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airdrops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT UNIQUE,
        amount REAL,
        tx_hash TEXT,
        status TEXT,
        created_at TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"✓ Datenbank initialisiert: {DB_PATH}")

def generate_token(address: str, duration_hours = None) -> str:
    """
    Generiert einen JWT-ähnlichen Token
    
    Args:
        address: Wallet-Adresse
        duration_hours: Token-Gültigkeitsdauer in Stunden (None = Standard TOKEN_EXPIRY_DAYS)
    """
    if duration_hours is None:
        duration_hours = TOKEN_EXPIRY_DAYS * 24
    elif duration_hours == 0:
        # 0 = kein Ablaufdatum, Token gilt bis manuelles Abmelden
        duration_hours = 365 * 24  # 1 Jahr als Maximum
    
    expiry = (datetime.utcnow() + timedelta(hours=int(duration_hours))).timestamp()
    token_data = f"{address}:{expiry}"
    signature = hashlib.sha256((token_data + TOKEN_SECRET).encode()).hexdigest()
    token = f"{token_data}:{signature}"
    
    log_activity("DEBUG", "TOKEN", "Generated new token", address=address[:10], duration_hours=duration_hours, expiry_timestamp=expiry)
    return token

def verify_token(token: str) -> dict:
    """Verifiziert und dekodiert einen Token"""
    try:
        parts = token.split(":")
        if len(parts) != 3:
            wallet_logger.warning(f"Invalid token format received")
            return {"valid": False, "error": "Invalid token format"}
        
        address, expiry_str, signature = parts
        expected_sig = hashlib.sha256((f"{address}:{expiry_str}" + TOKEN_SECRET).encode()).hexdigest()
        
        if signature != expected_sig:
            wallet_logger.warning(f"Token signature mismatch for {address[:10]}")
            return {"valid": False, "error": "Invalid signature"}
        
        expiry = float(expiry_str)
        if datetime.utcfromtimestamp(expiry) < datetime.utcnow():
            wallet_logger.warning(f"Token expired for {address[:10]}")
            return {"valid": False, "error": "Token expired"}
        
        log_activity("DEBUG", "TOKEN", "Token verified", address=address[:10])
        return {"valid": True, "address": address, "expiry": expiry}
    except Exception as e:
        wallet_logger.error(f"Token verification error: {str(e)}")
        return {"valid": False, "error": str(e)}

async def trigger_airdrop(address: str) -> dict:
    """
    Trigger Airdrop via Telegram Bot API mit Retry-Logik
    Die echte Ausführung passiert im Telegram Bot Service
    """
    address = address.lower()
    max_retries = 3
    retry_delay = 0.5  # 500ms
    
    for attempt in range(max_retries):
        try:
            # Prüfe ob Wallet bereits Airdrop bekommen hat
            conn = get_db_connection()
            conn.execute("PRAGMA busy_timeout=5000")  # 5 Sekunden Timeout
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM airdrops WHERE address=?", (address,))
            existing_airdrop = cursor.fetchone()
            
            if existing_airdrop:
                conn.close()
                logger.info(f"⚠️ Airdrop already received for {address}")
                return {"triggered": False, "message": "Airdrop already received"}
            
            # Bestimme Status basierend auf Admin-Credentials
            if not ADMIN_WALLET or not ADMIN_PRIVATE_KEY:
                status = "pending_admin"
                logger.warning(f"⚠️ Airdrop pending (waiting for admin approval): {address}")
            else:
                status = "pending_execution"
                logger.info(f"✓ Airdrop queued for execution: {address}")
            
            # Registriere Airdrop in Datenbank
            cursor.execute(
                """INSERT INTO airdrops (address, amount, status, created_at)
                   VALUES (?, ?, ?, ?)""",
                (address, AIRDROP_AMOUNT, status, datetime.utcnow().isoformat())
            )
            conn.commit()
            conn.close()
            
            return {
                "triggered": True,
                "address": address,
                "amount": AIRDROP_AMOUNT,
                "status": status,
                "message": f"Airdrop of {AIRDROP_AMOUNT} AERA registered with status: {status}"
            }
            
        except Exception as e:
            if 'conn' in locals():
                conn.close()
            
            if attempt < max_retries - 1 and "database is locked" in str(e):
                logger.warning(f"⏳ Airdrop retry {attempt + 1}/{max_retries}: {str(e)}")
                await asyncio.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                continue
            
            logger.error(f"❌ Airdrop error (attempt {attempt + 1}): {str(e)}")
            return {"triggered": False, "message": f"Airdrop failed: {str(e)}"}
    
    return {"triggered": False, "message": "Airdrop failed after retries"}

@app.on_event("startup")
def startup_event():
    """App-Start: Initialisiere Datenbank"""
    init_db()
    logger.info("🚀 VEra-Resonance Server gestartet")
    logger.info(f"   🌐 Öffentliche URL: {PUBLIC_URL}")
    logger.info(f"   📍 Host: {HOST}:{PORT}")
    logger.info(f"   🔐 CORS Origins: {CORS_ORIGINS}")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Dynamic Landing Page - Adapts styling based on referrer platform
    Only ONE template, dynamically styled!
    """
    referrer = request.headers.get("referer", request.headers.get("referrer", ""))
    referrer_source = extract_referrer_source(referrer)
    
    # Get platform config or default
    platform = PLATFORM_CONFIG.get(referrer_source, PLATFORM_CONFIG["direct"])
    
    logger.info(f"✓ Serving dynamic landing for: {referrer_source} ({platform['name']})")
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "platform_source": referrer_source,
        "platform_name": platform["name"],
        "platform_color": platform["color"],
        "platform_gradient": platform["gradient"],
        "platform_emoji": platform["emoji"],
        "platform_badge": platform["badge"]
    })

@app.get("/api/health")
async def health_check():
    """Health-Check Endpoint"""
    return {
        "status": "healthy",
        "service": "VEra-Resonance v0.1",
        "timestamp": int(time.time()),
        "database": "connected" if os.path.exists(DB_PATH) else "disconnected",
        "database_path": DB_PATH
    }

@app.get("/api/debug")
async def debug_info(req: Request):
    """Debug Info für Troubleshooting"""
    client_host = req.client.host if req.client else "unknown"
    return {
        "server": "VEra-Resonance v0.1",
        "timestamp": int(time.time()),
        "client_ip": client_host,
        "database": {
            "path": DB_PATH,
            "exists": os.path.exists(DB_PATH),
            "size_mb": os.path.getsize(DB_PATH) / (1024 * 1024) if os.path.exists(DB_PATH) else 0
        },
        "cors": "enabled",
        "endpoints": {
            "health": "/api/health",
            "verify": "POST /api/verify",
            "user": "GET /api/user/{address}",
            "stats": "GET /api/stats",
            "events": "GET /api/events/{address}"
        }
    }

@app.post("/api/nonce")
async def get_nonce(req: Request):
    """
    Generiert eine Nonce für Message-Signing
    Diese Nonce muss vom Client mit MetaMask signiert werden
    """
    try:
        data = await req.json()
        address = data.get("address", "").lower()
        
        if not address or not address.startswith("0x") or len(address) != 42:
            log_activity("ERROR", "AUTH", "Invalid nonce request", address=address[:10] if address else "unknown")
            return {"error": "Invalid address", "success": False}
        
        # Generiere zufällige Nonce
        nonce = secrets.token_hex(16)
        log_activity("DEBUG", "AUTH", "Nonce generated", address=address[:10], nonce=nonce[:16])
        
        return {
            "success": True,
            "address": address,
            "nonce": nonce,
            "message": f"Signiere diese Nachricht um dich bei AEra anzumelden:\nNonce: {nonce}"
        }
    except Exception as e:
        log_activity("ERROR", "AUTH", f"Nonce error: {str(e)}")
        return {"error": str(e), "success": False}

@app.post("/api/verify")
async def verify(req: Request):
    """
    Verifiziert eine Wallet-Adresse mit MetaMask-Signatur (PROOF OF HUMAN)
    
    Request:
        {
            "address": "0x...",
            "nonce": "...",
            "signature": "0x..."
        }
    
    Response:
        {
            "is_human": true,
            "address": "0x...",
            "resonance_score": 50-100,
            "message": "..."
        }
    """
    try:
        data = await req.json()
        address = data.get("address", "").lower()
        nonce = data.get("nonce", "")
        signature = data.get("signature", "")
        token_duration_hours = data.get("token_duration_hours", None)
        
        # ===== EXTRACT REFERRER & USER-AGENT =====
        referrer = req.headers.get("referer", req.headers.get("referrer", ""))
        user_agent = req.headers.get("user-agent", "")
        client_ip = req.client.host if req.client else "unknown"
        referrer_source = extract_referrer_source(referrer)
        
        log_activity("INFO", "AUTH", "Verify request received", 
                    address=address[:10], 
                    has_signature=bool(signature),
                    referrer_source=referrer_source,
                    ip=client_ip[:15])
        
        # ===== KRITISCH: SIGNATURE VALIDIERUNG =====
        if not signature:
            log_activity("ERROR", "AUTH", "No signature provided - REJECTING", address=address[:10])
            return {"error": "No signature provided - MetaMask sign required!", "is_human": False}
        
        if not nonce:
            log_activity("ERROR", "AUTH", "No nonce provided", address=address[:10])
            return {"error": "No nonce", "is_human": False}
        
        # Validiere Adresse
        if not address or not address.startswith("0x") or len(address) != 42:
            log_activity("ERROR", "AUTH", "Invalid address format", address=address[:10])
            return {"error": "Invalid address format", "is_human": False}
        
        # ===== VALIDIERE SIGNATURE MIT web3.py =====
        try:
            from eth_account.messages import encode_defunct
            from eth_account import Account
            
            message_text = f"Signiere diese Nachricht um dich bei AEra anzumelden:\nNonce: {nonce}"
            message = encode_defunct(text=message_text)
            
            # Verifiziere Signature
            recovered_address = Account.recover_message(message, signature=signature)
            
            if recovered_address.lower() != address:
                log_activity("ERROR", "AUTH", "Signature verification FAILED", address=address[:10], recovered=recovered_address[:10])
                return {"error": "Signature verification failed", "is_human": False}
            
            log_activity("INFO", "AUTH", "✓✓✓ Signature VERIFIED", address=address[:10])
            
        except ImportError:
            log_activity("WARNING", "AUTH", "eth_account not available - skipping signature check")
        except Exception as e:
            log_activity("ERROR", "AUTH", f"Signature verification error: {str(e)}", address=address[:10])
            return {"error": f"Signature error: {str(e)}", "is_human": False}
        
        # ===== BENUTZER-LOGIN (nach Signature-Verifizierung) =====
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Benutzer suchen
        cursor.execute("SELECT * FROM users WHERE address=?", (address,))
        user = cursor.fetchone()
        
        current_timestamp = int(time.time())
        current_iso = datetime.utcnow().isoformat()
        
        if user:
            # Benutzer existiert bereits
            old_score = user['score']
            new_score = min(user['score'] + 1, 100)
            login_count = user['login_count'] + 1
            
            cursor.execute(
                """UPDATE users 
                   SET last_login=?, score=?, login_count=?, last_referrer=?
                   WHERE address=?""",
                (current_timestamp, new_score, login_count, referrer_source, address)
            )
            
            cursor.execute(
                """INSERT INTO events 
                   (address, event_type, score_before, score_after, timestamp, created_at, referrer, user_agent, ip_address)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (address, "login", old_score, new_score, current_timestamp, current_iso, referrer_source, user_agent[:200], client_ip)
            )
            
            first_seen = user['first_seen']
            message = f"Welcome back! Score increased to {new_score}/100"
            log_activity("INFO", "AUTH", "Existing user login", 
                        address=address[:10], 
                        old_score=old_score, 
                        new_score=new_score, 
                        login_count=login_count,
                        referrer=referrer_source)
            
        else:
            # Neuer Benutzer
            initial_score = 50
            cursor.execute(
                """INSERT INTO users 
                   (address, first_seen, last_login, score, login_count, created_at, first_referrer, last_referrer)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (address, current_timestamp, current_timestamp, initial_score, 1, current_iso, referrer_source, referrer_source)
            )
            
            cursor.execute(
                """INSERT INTO events 
                   (address, event_type, score_before, score_after, timestamp, created_at, referrer, user_agent, ip_address)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (address, "signup", 0, initial_score, current_timestamp, current_iso, referrer_source, user_agent[:200], client_ip)
            )
            
            first_seen = current_timestamp
            new_score = initial_score
            message = f"Welcome! Your initial Resonance Score is {initial_score}/100"
            log_activity("INFO", "AUTH", "New user registered", 
                        address=address[:10], 
                        initial_score=initial_score,
                        referrer=referrer_source)
        
        conn.commit()
        conn.close()
        
        # Trigger Airdrop NACH Commit
        if not user:
            airdrop_result = await trigger_airdrop(address)
            message += f" | {airdrop_result['message']}"
        
        # Generiere Token
        token = generate_token(address, token_duration_hours)
        
        log_activity("INFO", "AUTH", "✓ Verify successful (SIGNATURE VERIFIED)", address=address[:10], score=new_score)
        
        return {
            "is_human": True,
            "address": address,
            "resonance_score": new_score,
            "first_seen": first_seen,
            "last_login": current_timestamp,
            "login_count": user['login_count'] + 1 if user else 1,
            "message": message,
            "token": token
        }
        
    except Exception as e:
        log_activity("ERROR", "AUTH", f"Verification error: {str(e)}")
        return {
            "error": str(e),
            "is_human": False
        }

@app.get("/api/user/{address}")
async def get_user(address: str):
    """
    Ruft Benutzerdaten ab (ohne Sicherheitscheck - nur Demo!)
    """
    try:
        address = address.lower()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE address=?", (address,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return {"error": "User not found"}
        
        return {
            "address": user['address'],
            "resonance_score": user['score'],
            "first_seen": user['first_seen'],
            "last_login": user['last_login'],
            "login_count": user['login_count'],
            "created_at": user['created_at']
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/stats")
async def get_stats():
    """
    Gibt Statistiken aus (öffentlich)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']
        
        cursor.execute("SELECT AVG(score) as avg_score FROM users")
        avg_score = cursor.fetchone()['avg_score']
        
        cursor.execute("SELECT COUNT(*) as total FROM events WHERE event_type='login'")
        total_logins = cursor.fetchone()['total']
        
        conn.close()
        
        return {
            "total_users": total_users,
            "average_score": round(avg_score, 2) if avg_score else 0,
            "total_logins": total_logins,
            "timestamp": int(time.time())
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/events/{address}")
async def get_user_events(address: str):
    """
    Ruft Login-Ereignisse eines Benutzers ab
    """
    try:
        address = address.lower()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT * FROM events 
               WHERE address=? 
               ORDER BY timestamp DESC 
               LIMIT 50""",
            (address,)
        )
        events = cursor.fetchall()
        conn.close()
        
        return {
            "address": address,
            "events": [dict(event) for event in events]
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/referrer-stats")
async def get_referrer_stats():
    """
    Gibt Statistiken über Referrer-Quellen zurück
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Neue User pro Referrer
        cursor.execute("""
            SELECT first_referrer, COUNT(*) as count
            FROM users
            WHERE first_referrer IS NOT NULL
            GROUP BY first_referrer
            ORDER BY count DESC
        """)
        new_users_by_referrer = cursor.fetchall()
        
        # Alle Events pro Referrer
        cursor.execute("""
            SELECT referrer, COUNT(*) as count
            FROM events
            WHERE referrer IS NOT NULL
            GROUP BY referrer
            ORDER BY count DESC
        """)
        events_by_referrer = cursor.fetchall()
        
        # Top Referrer letzte 24h
        yesterday = int(time.time()) - (24 * 3600)
        cursor.execute("""
            SELECT referrer, COUNT(*) as count
            FROM events
            WHERE referrer IS NOT NULL AND timestamp > ?
            GROUP BY referrer
            ORDER BY count DESC
            LIMIT 10
        """, (yesterday,))
        top_24h = cursor.fetchall()
        
        conn.close()
        
        return {
            "new_users_by_source": [dict(r) for r in new_users_by_referrer],
            "total_events_by_source": [dict(r) for r in events_by_referrer],
            "top_sources_24h": [dict(r) for r in top_24h],
            "timestamp": int(time.time())
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/verify-token")
async def verify_token_endpoint(req: Request):
    """
    Verifiziert einen gespeicherten Token (für Auto-Login) MIT SIGNATUR-VERIFIZIERUNG
    
    Request:
        {
            "token": "address:expiry:signature",
            "address": "0x...",
            "nonce": "...",
            "message": "...",
            "signature": "0x..."
        }
    
    Response:
        {
            "valid": true,
            "address": "0x...",
            "resonance_score": 55,
            "message": "Auto-logged in"
        }
    """
    try:
        data = await req.json()
        token = data.get("token", "")
        address = data.get("address", "").lower()
        nonce = data.get("nonce", "")
        message_to_verify = data.get("message", "")
        signature = data.get("signature", "")
        
        if not token:
            return {"valid": False, "error": "No token provided"}
        
        # ===== NEUE SIGNATUR-VERIFIZIERUNG FÜR AUTO-LOGIN =====
        log_activity("INFO", "AUTH", "Auto-login with token - signature verification", address=address[:10] if address else "unknown")
        
        if not signature:
            log_activity("ERROR", "AUTH", "Auto-login: No signature provided - REJECTING", address=address[:10])
            return {"valid": False, "error": "No signature provided - MetaMask sign required for auto-login!"}
        
        if not nonce:
            log_activity("ERROR", "AUTH", "Auto-login: No nonce provided", address=address[:10])
            return {"valid": False, "error": "No nonce provided"}
        
        # Validiere Adresse
        if not address or not address.startswith("0x") or len(address) != 42:
            log_activity("ERROR", "AUTH", "Auto-login: Invalid address format", address=address[:10])
            return {"valid": False, "error": "Invalid address format"}
        
        # ===== VALIDIERE SIGNATURE MIT web3.py =====
        try:
            from eth_account.messages import encode_defunct
            from eth_account import Account
            
            message = encode_defunct(text=message_to_verify)
            
            # Verifiziere Signature
            recovered_address = Account.recover_message(message, signature=signature)
            
            if recovered_address.lower() != address:
                log_activity("ERROR", "AUTH", "Auto-login: Signature verification FAILED", address=address[:10], recovered=recovered_address[:10])
                return {"valid": False, "error": "Signature verification failed", "is_human": False}
            
            log_activity("INFO", "AUTH", "✓✓✓ Auto-login: Signature VERIFIED", address=address[:10])
            
        except ImportError:
            log_activity("WARNING", "AUTH", "Auto-login: eth_account not available - skipping signature check")
        except Exception as e:
            log_activity("ERROR", "AUTH", f"Auto-login: Signature verification error: {str(e)}", address=address[:10])
            return {"valid": False, "error": f"Signature error: {str(e)}", "is_human": False}
        
        # ===== NACH SIGNATUR-VERIFIZIERUNG: TOKEN VERIFIZIEREN =====
        result = verify_token(token)
        
        if not result["valid"]:
            return result
        
        # Validiere dass Token-Adresse mit Request-Adresse übereinstimmt
        if result["address"].lower() != address:
            log_activity("ERROR", "AUTH", "Auto-login: Address mismatch between token and request", token_addr=result["address"][:10], req_addr=address[:10])
            return {"valid": False, "error": "Address mismatch"}
        
        # Hole aktuelle Daten aus Datenbank
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE address=?", (address,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return {"valid": False, "error": "User not found"}
        
        log_activity("INFO", "AUTH", "✓ Auto-login SUCCESSFUL (signature + token verified)", address=address[:10], score=user['score'])
        
        return {
            "valid": True,
            "address": address,
            "resonance_score": user['score'],
            "login_count": user['login_count'],
            "first_seen": user['first_seen'],
            "message": "Auto-logged in successfully (signature verified)"
        }
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

@app.get("/api/airdrop-status/{address}")
async def get_airdrop_status(address: str):
    """
    Prüft den Airdrop-Status einer Wallet
    """
    try:
        address = address.lower()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM airdrops WHERE address=?", (address,))
        airdrop = cursor.fetchone()
        conn.close()
        
        if not airdrop:
            return {
                "address": address,
                "status": "not_registered",
                "message": "No airdrop record found"
            }
        
        return {
            "address": address,
            "status": airdrop['status'],
            "amount": airdrop['amount'],
            "tx_hash": airdrop['tx_hash'],
            "created_at": airdrop['created_at']
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
