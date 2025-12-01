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
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import hashlib
import secrets

# ===== IMPORT CUSTOM LOGGER =====
from logger import logger, api_logger, db_logger, wallet_logger, airdrop_logger, log_activity

# ===== IMPORT BLOCKCHAIN SERVICE =====
from web3_service import web3_service
from blockchain_sync import sync_score_after_update

# Load environment variables
load_dotenv()

# Config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8840))
PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")
NGROK_URL = os.getenv("NGROK_URL", "")  # NEW: Explicit ngrok URL
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# NEW: Tailscale Support
TAILSCALE_ENABLED = os.getenv("TAILSCALE_ENABLED", "false").lower() == "true"
TAILSCALE_IP = os.getenv("TAILSCALE_IP", "")

# NEW: Deployment Mode (local, tailscale, ngrok)
DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "local")  # local, tailscale, ngrok

INITIAL_SCORE = int(os.getenv("INITIAL_SCORE", 50))
MAX_SCORE = int(os.getenv("MAX_SCORE", 100))
SCORE_INCREMENT = int(os.getenv("SCORE_INCREMENT", 1))
TOKEN_SECRET = os.getenv("TOKEN_SECRET", "aera-secret-key-change-in-production")
TOKEN_EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES", 2))  # 2 Minuten Standard

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
DATABASE_NAME = os.getenv("DATABASE_PATH", "./aera.db")
DB_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME.replace("./", ""))

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
    
    # Users-Tabelle (erweitert mit owner_wallet für Follower-Tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        address TEXT PRIMARY KEY,
        first_seen INTEGER,
        last_login INTEGER,
        score INTEGER DEFAULT 50,
        login_count INTEGER DEFAULT 0,
        created_at TEXT,
        first_referrer TEXT,
        last_referrer TEXT,
        owner_wallet TEXT,
        is_verified_follower INTEGER DEFAULT 0,
        display_name TEXT
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
        ip_address TEXT,
        owner_wallet TEXT
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
    
    # Followers-Tabelle: Link Owner <-> Follower
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_wallet TEXT NOT NULL,
        follower_address TEXT NOT NULL,
        follower_score INTEGER,
        follower_display_name TEXT,
        verified_at TEXT,
        source_platform TEXT,
        verified BOOLEAN DEFAULT 1,
        follow_confirmed BOOLEAN DEFAULT 0,
        confirmed_at TEXT,
        UNIQUE(owner_wallet, follower_address),
        FOREIGN KEY(owner_wallet) REFERENCES users(address),
        FOREIGN KEY(follower_address) REFERENCES users(address)
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"✓ Datenbank initialisiert: {DB_PATH}")

def generate_token(address: str, duration_minutes = None) -> str:
    """
    Generiert einen JWT-ähnlichen Token
    
    Args:
        address: Wallet-Adresse
        duration_minutes: Token-Gültigkeitsdauer in Minuten (None = Standard TOKEN_EXPIRY_MINUTES = 2 Min)
    """
    if duration_minutes is None:
        duration_minutes = TOKEN_EXPIRY_MINUTES
    elif duration_minutes == 0:
        # 0 = kein Ablaufdatum, Token gilt bis manuelles Abmelden
        duration_minutes = 525600  # 1 Jahr als Maximum
    
    expiry = (datetime.utcnow() + timedelta(minutes=int(duration_minutes))).timestamp()
    token_data = f"{address}:{expiry}"
    signature = hashlib.sha256((token_data + TOKEN_SECRET).encode()).hexdigest()
    token = f"{token_data}:{signature}"
    
    log_activity("DEBUG", "TOKEN", "Generated new token", address=address[:10], duration_minutes=duration_minutes, expiry_timestamp=expiry)
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
async def startup_event():
    """App-Start: Initialisiere Datenbank und Blockchain Services"""
    init_db()
    logger.info("🚀 VEra-Resonance Server gestartet")
    logger.info(f"   🌐 Öffentliche URL: {PUBLIC_URL}")
    logger.info(f"   📍 Host: {HOST}:{PORT}")
    logger.info(f"   🔐 CORS Origins: {CORS_ORIGINS}")
    
    # Starte Blockchain Sync Queue Processor
    from blockchain_sync import start_sync_queue_processor, add_to_sync_queue, should_sync_score
    asyncio.create_task(start_sync_queue_processor())
    logger.info("   ⛓️  Blockchain Sync Queue gestartet")
    
    # Starte NFT Mint Confirmation Checker
    from nft_confirmation import start_nft_confirmation_checker
    asyncio.create_task(start_nft_confirmation_checker())
    logger.info("   🎨 NFT Mint Confirmation Checker gestartet")
    
    # Initial Scan: Füge alle User mit Score ≥10 zur Sync-Queue hinzu
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT address, score, blockchain_score
            FROM users
            WHERE score >= 10
            ORDER BY score DESC
        """)
        users = cursor.fetchall()
        conn.close()
        
        added_count = 0
        for address, db_score, blockchain_score in users:
            blockchain_score = blockchain_score or 0
            if should_sync_score(db_score, blockchain_score):
                add_to_sync_queue(address, db_score)
                added_count += 1
        
        if added_count > 0:
            logger.info(f"   📊 {added_count} users added to initial sync queue")
    except Exception as e:
        logger.error(f"   ❌ Failed to scan users for initial sync: {e}")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Dynamic Landing Page - Adapts styling based on referrer platform
    Only ONE template, dynamically styled!
    """
    referrer = request.headers.get("referer", request.headers.get("referrer", ""))
    
    # WICHTIG: URL-Parameter "source" hat PRIORITÄT vor Referrer-Header!
    url_source = request.query_params.get("source", "").strip().lower()
    referrer_source = url_source if url_source else extract_referrer_source(referrer)
    
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

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Admin Follower Dashboard"""
    with open(os.path.join(os.path.dirname(__file__), "dashboard.html"), "r") as f:
        return f.read()

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard_html():
    """Admin Follower Dashboard (with .html extension)"""
    with open(os.path.join(os.path.dirname(__file__), "dashboard.html"), "r") as f:
        return f.read()

@app.get("/blockchain-dashboard.js")
async def blockchain_dashboard_js():
    """Blockchain Dashboard JavaScript Module"""
    from fastapi.responses import FileResponse
    js_path = os.path.join(os.path.dirname(__file__), "blockchain-dashboard.js")
    return FileResponse(js_path, media_type="application/javascript")

@app.get("/blockchain-test.html", response_class=HTMLResponse)
async def blockchain_test():
    """Blockchain Integration Test Page"""
    with open(os.path.join(os.path.dirname(__file__), "blockchain-test.html"), "r") as f:
        return f.read()

@app.get("/blockchain-direct-test.html", response_class=HTMLResponse)
async def blockchain_direct_test():
    """Direct Blockchain API Test Page"""
    with open(os.path.join(os.path.dirname(__file__), "blockchain-direct-test.html"), "r") as f:
        return f.read()

@app.get("/api/health")
async def health_check():
    """Health-Check Endpoint with deployment info"""
    # NEW: Try to detect Tailscale IP
    tailscale_ip = None
    try:
        import socket
        hostname = socket.gethostname()
        # Tailscale IPs start with 100.
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip.startswith('100.'):
                tailscale_ip = ip
                break
    except:
        pass
    
    return {
        "status": "healthy",
        "service": "VEra-Resonance v0.1",
        "timestamp": int(time.time()),
        "database": "connected" if os.path.exists(DB_PATH) else "disconnected",
        "database_path": DB_PATH,
        "deployment": {
            "mode": DEPLOYMENT_MODE,
            "local_url": f"http://localhost:{PORT}",
            "tailscale_ip": tailscale_ip,
            "tailscale_url": f"http://{tailscale_ip}/dashboard" if tailscale_ip else None,
            "public_url": PUBLIC_URL
        }
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
        token_duration_minutes = data.get("token_duration_minutes", None)  # Token-Gültigkeitsdauer in Minuten
        owner_wallet = data.get("owner", "").lower()  # NEW: Owner for follower tracking
        display_name = data.get("display_name", "").strip()  # NEW: User-provided display name
        
        # ===== EXTRACT REFERRER & USER-AGENT =====
        referrer = req.headers.get("referer", req.headers.get("referrer", ""))
        user_agent = req.headers.get("user-agent", "")
        client_ip = req.client.host if req.client else "unknown"
        
        # PRIORITÄT: POST-Body "source" > URL-Parameter "source" > Referrer-Header
        source_from_body = data.get("source", "").strip().lower()
        url_source = req.query_params.get("source", "").strip().lower()
        referrer_source = source_from_body if source_from_body else (url_source if url_source else extract_referrer_source(referrer))
        
        log_activity("INFO", "AUTH", "Verify request received", 
                    address=address[:10], 
                    has_signature=bool(signature),
                    referrer_source=referrer_source,
                    owner_wallet=owner_wallet[:10] if owner_wallet else "none",
                    ip=client_ip[:15])
        
        # ===== VALIDATE OWNER WALLET IF PROVIDED =====
        if owner_wallet and (not owner_wallet.startswith("0x") or len(owner_wallet) != 42):
            log_activity("ERROR", "AUTH", "Invalid owner wallet format", address=address[:10])
            return {"error": "Invalid owner wallet format", "is_human": False}
        
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
            
            # BLOCKCHAIN: Check if score sync needed (every 10 points)
            await sync_score_after_update(address, new_score, conn)
            
            first_seen = user['first_seen']
            message = f"Welcome back! Score increased to {new_score}/100"
            log_activity("INFO", "AUTH", "Existing user login", 
                        address=address[:10], 
                        old_score=old_score, 
                        new_score=new_score, 
                        login_count=login_count,
                        referrer=referrer_source)
            
            # NEW: Auch bei existierenden User-Logins: Follower-Eintrag erstellen wenn owner_wallet vorhanden
            if owner_wallet:
                try:
                    # Prüfe ob dieser Follower auf dieser Plattform bereits existiert
                    cursor.execute(
                        """SELECT id FROM followers 
                           WHERE owner_wallet = ? AND follower_address = ? AND source_platform = ?""",
                        (owner_wallet, address, referrer_source)
                    )
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Update: Nur Score und Timestamp aktualisieren
                        cursor.execute(
                            """UPDATE followers 
                               SET follower_score = ?, verified_at = ?
                               WHERE owner_wallet = ? AND follower_address = ? AND source_platform = ?""",
                            (new_score, current_iso, owner_wallet, address, referrer_source)
                        )
                        log_activity("INFO", "FOLLOWER", "✓ Follower score updated", 
                                    owner=owner_wallet[:10], 
                                    follower=address[:10], 
                                    source=referrer_source)
                    else:
                        # Insert: Neuer Follower-Eintrag für diese Plattform
                        cursor.execute(
                            """INSERT INTO followers 
                               (owner_wallet, follower_address, follower_score, follower_display_name, verified_at, source_platform, verified)
                               VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            (owner_wallet, address, new_score, display_name or None, current_iso, referrer_source, 1)
                        )
                        log_activity("INFO", "FOLLOWER", "✓ New follower registered (multi-platform)", 
                                    owner=owner_wallet[:10], 
                                    follower=address[:10], 
                                    source=referrer_source)
                except Exception as e:
                    log_activity("WARNING", "FOLLOWER", f"Could not create/update follower entry: {str(e)}")
            
        else:
            # Neuer Benutzer
            initial_score = 50
            cursor.execute(
                """INSERT INTO users 
                   (address, first_seen, last_login, score, login_count, created_at, first_referrer, last_referrer, owner_wallet, is_verified_follower, display_name)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (address, current_timestamp, current_timestamp, initial_score, 1, current_iso, referrer_source, referrer_source, owner_wallet or None, 1 if owner_wallet else 0, display_name or None)
            )
            
            cursor.execute(
                """INSERT INTO events 
                   (address, event_type, score_before, score_after, timestamp, created_at, referrer, user_agent, ip_address, owner_wallet)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (address, "signup", 0, initial_score, current_timestamp, current_iso, referrer_source, user_agent[:200], client_ip, owner_wallet or None)
            )
            
            # NEW: Wenn Owner vorhanden, registriere als Follower
            if owner_wallet:
                try:
                    cursor.execute(
                        """INSERT INTO followers 
                           (owner_wallet, follower_address, follower_score, follower_display_name, verified_at, source_platform, verified)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (owner_wallet, address, initial_score, display_name or None, current_iso, referrer_source, 1)
                    )
                    log_activity("INFO", "FOLLOWER", "✓ Follower registered", 
                                owner=owner_wallet[:10], 
                                follower=address[:10], 
                                source=referrer_source)
                except Exception as e:
                    log_activity("WARNING", "FOLLOWER", f"Could not register follower: {str(e)}")
            
            first_seen = current_timestamp
            new_score = initial_score
            message = f"Welcome! Your initial Resonance Score is {initial_score}/100"
            if owner_wallet:
                message += f" | Registered as follower"
            log_activity("INFO", "AUTH", "New user registered", 
                        address=address[:10], 
                        initial_score=initial_score,
                        referrer=referrer_source,
                        owner=owner_wallet[:10] if owner_wallet else "none")
            
            # BLOCKCHAIN: Check if score sync needed (initial score 50)
            await sync_score_after_update(address, new_score, conn)
            
            # DELAY: Wait 2 seconds to prevent nonce conflict between score sync and NFT mint
            await asyncio.sleep(2)
        
        # ===== BLOCKCHAIN: IDENTITY NFT INTEGRATION =====
        try:
            # Check current identity status from DB
            cursor.execute("SELECT identity_status, identity_nft_token_id FROM users WHERE address=?", (address,))
            identity_result = cursor.fetchone()
            db_identity_status = identity_result[0] if identity_result else 'pending'
            db_token_id = identity_result[1] if identity_result else None
            
            # Prüfe ob User bereits Identity NFT hat
            has_identity = await web3_service.has_identity_nft(address)
            
            # RETRY LOGIC: If status is 'failed' or 'pending' (old users), try minting again
            if not has_identity and db_identity_status in ['failed', 'pending']:
                log_activity("INFO", "BLOCKCHAIN", "🎨 Starting Identity NFT mint", address=address[:10])
                success, result = await web3_service.mint_identity_nft(address)
                
                if success:
                    tx_hash = result
                    # Set status to 'minting' with tx_hash - background task will confirm later
                    cursor.execute(
                        """UPDATE users 
                           SET identity_status='minting', identity_mint_tx_hash=?, identity_minted_at=?
                           WHERE address=?""",
                        (tx_hash, current_iso, address)
                    )
                    
                    log_activity("INFO", "BLOCKCHAIN", "📤 Identity NFT mint transaction sent", 
                                address=address[:10], 
                                tx_hash=tx_hash[:16] + "...")
                    message += f" | Identity NFT minting (TX: {tx_hash[:10]}...)"
                else:
                    error_msg = result
                    log_activity("WARNING", "BLOCKCHAIN", f"NFT minting failed: {error_msg}", address=address[:10])
                    # Nicht-kritischer Fehler - fahre fort
                    cursor.execute(
                        """UPDATE users 
                           SET identity_status='failed'
                           WHERE address=?""",
                        (address,)
                    )
            else:
                # User hat bereits NFT - hole Token ID
                token_id = await web3_service.get_identity_token_id(address)
                if token_id is not None:
                    # Update DB falls noch nicht gespeichert
                    cursor.execute(
                        """UPDATE users 
                           SET identity_nft_token_id=?, identity_status='active'
                           WHERE address=? AND identity_nft_token_id IS NULL""",
                        (token_id, address)
                    )
                    log_activity("INFO", "BLOCKCHAIN", "✓ Identity NFT verified", 
                                address=address[:10], 
                                token_id=token_id)
        
        except Exception as e:
            log_activity("WARNING", "BLOCKCHAIN", f"Identity NFT error (non-critical): {str(e)}", address=address[:10])
            # Nicht-kritischer Fehler - System funktioniert weiter ohne Blockchain
        
        conn.commit()
        conn.close()
        
        # Trigger Airdrop NACH Commit
        if not user:
            airdrop_result = await trigger_airdrop(address)
            message += f" | {airdrop_result['message']}"
        
        # Generiere Token
        token = generate_token(address, token_duration_minutes)
        
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


# ===== BLOCKCHAIN API ENDPOINTS =====

@app.get("/api/blockchain/identity/{address}")
async def get_blockchain_identity(address: str):
    """
    Get Identity NFT information for a user
    
    Returns:
        {
            "has_identity": true,
            "token_id": 123,
            "status": "active",
            "minted_at": "2024-11-30T14:30:00",
            "contract_address": "0x...",
            "basescan_url": "https://sepolia.basescan.org/nft/0x..."
        }
    """
    try:
        address = address.lower()
        
        # Get DB info
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT identity_nft_token_id, identity_status, identity_minted_at, identity_mint_tx_hash
               FROM users WHERE address=?""",
            (address,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return {
                "has_identity": False,
                "identity_status": "not_found",
                "token_id": None,
                "mint_tx_hash": None,
                "minted_at": None,
                "contract_address": None,
                "basescan_url": None
            }
        
        # Get blockchain info
        # Primary: Trust DB if status is 'active' (already verified)
        db_token_id = user['identity_nft_token_id']
        db_status = user['identity_status']
        
        if db_status == 'active' and db_token_id is not None:
            # User has verified NFT in DB
            has_identity = True
            token_id = db_token_id
        else:
            # Check blockchain for pending/failed cases
            has_identity = await web3_service.has_identity_nft(address)
            token_id = await web3_service.get_identity_token_id(address) if has_identity else db_token_id
        
        contract_address = os.getenv("IDENTITY_NFT_ADDRESS", "")
        tx_hash = user['identity_mint_tx_hash']
        basescan_url = f"https://sepolia.basescan.org/nft/{contract_address}/{token_id}" if token_id else None
        tx_url = f"https://sepolia.basescan.org/tx/{tx_hash}" if tx_hash else None
        
        return {
            "has_identity": has_identity,
            "identity_status": user['identity_status'],  # pending, minting, active, failed
            "token_id": token_id,
            "mint_tx_hash": tx_hash,
            "minted_at": user['identity_minted_at'],
            "contract_address": contract_address,
            "basescan_url": basescan_url,
            "tx_url": tx_url
        }
        
    except Exception as e:
        log_activity("ERROR", "API", f"Blockchain identity error: {str(e)}")
        return {"error": str(e), "has_identity": False}


@app.get("/api/blockchain/score/{address}")
async def get_blockchain_score(address: str):
    """
    Get Resonance Score comparison (DB vs Blockchain)
    
    Returns:
        {
            "address": "0x...",
            "db_score": 55,
            "blockchain_score": 50,
            "sync_pending": 5,
            "last_sync": "2024-11-30T14:30:00",
            "next_sync_at": 60,
            "contract_address": "0x...",
            "basescan_url": "https://sepolia.basescan.org/address/0x..."
        }
    """
    try:
        address = address.lower()
        
        # Get DB info
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT score, blockchain_score, blockchain_score_synced_at, last_blockchain_sync
               FROM users WHERE address=?""",
            (address,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return {"error": "User not found"}
        
        # Get blockchain score
        blockchain_score = await web3_service.get_blockchain_score(address)
        
        db_score = user['score']
        sync_pending = db_score - (blockchain_score or 0)
        
        # Calculate next sync milestone
        next_sync_at = ((db_score // 10) + 1) * 10 if db_score < 100 else 100
        
        contract_address = os.getenv("RESONANCE_SCORE_ADDRESS", "")
        basescan_url = f"https://sepolia.basescan.org/address/{contract_address}"
        
        return {
            "address": address,
            "db_score": db_score,
            "blockchain_score": blockchain_score,
            "sync_pending": sync_pending,
            "last_sync": user['last_blockchain_sync'],
            "next_sync_at": next_sync_at,
            "contract_address": contract_address,
            "basescan_url": basescan_url
        }
        
    except Exception as e:
        log_activity("ERROR", "API", f"Blockchain score error: {str(e)}")
        return {"error": str(e)}


@app.get("/api/blockchain/interactions/{address}")
async def get_blockchain_interactions(address: str, offset: int = 0, limit: int = 10):
    """
    Get user's interaction history from blockchain
    
    Query Parameters:
        offset: Pagination offset (default 0)
        limit: Results per page (default 10, max 50)
    
    Returns:
        {
            "address": "0x...",
            "interactions": [
                {
                    "initiator": "0x...",
                    "responder": "0x...",
                    "interaction_type": 0,
                    "interaction_type_name": "FOLLOW",
                    "timestamp": 1701360000,
                    "dashboard_link": "https://...",
                    "basescan_url": "https://sepolia.basescan.org/tx/0x..."
                }
            ],
            "total": 5,
            "offset": 0,
            "limit": 10
        }
    """
    try:
        address = address.lower()
        limit = min(limit, 50)  # Max 50 per request
        
        # Get interactions from blockchain
        interactions = await web3_service.get_user_interactions(address, offset, limit)
        
        # Map interaction types
        type_names = {
            0: "FOLLOW",
            1: "SHARE",
            2: "ENGAGE",
            3: "COLLABORATE",
            4: "MILESTONE"
        }
        
        # Enhance with type names and Basescan URLs
        enhanced_interactions = []
        for interaction in interactions:
            enhanced_interactions.append({
                "initiator": interaction["initiator"],
                "responder": interaction["responder"],
                "interaction_type": interaction["interaction_type"],
                "interaction_type_name": type_names.get(interaction["interaction_type"], "UNKNOWN"),
                "timestamp": interaction["timestamp"],
                "dashboard_link": interaction["dashboard_link"],
                "basescan_url": f"https://sepolia.basescan.org/tx/{interaction.get('tx_hash', '')}" if interaction.get("tx_hash") else None
            })
        
        return {
            "address": address,
            "interactions": enhanced_interactions,
            "total": len(interactions),
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        log_activity("ERROR", "API", f"Blockchain interactions error: {str(e)}")
        return {"error": str(e), "interactions": []}


@app.get("/api/blockchain/stats")
async def get_blockchain_stats():
    """
    Get blockchain system statistics and health
    
    Returns:
        {
            "blockchain_health": {
                "connected": true,
                "chain_id": 84532,
                "latest_block": 12345678,
                "gas_price_gwei": 0.5
            },
            "contracts": {
                "identity_nft": "0x...",
                "resonance_score": "0x...",
                "registry": "0x..."
            },
            "stats": {
                "total_identities": 150,
                "total_interactions": 420,
                "total_score_synced": 7500
            },
            "basescan_base_url": "https://sepolia.basescan.org"
        }
    """
    try:
        # Get blockchain health
        health = await web3_service.get_blockchain_health()
        
        # Get DB stats
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE identity_status='active'")
        total_identities = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE blockchain_score > 0")
        users_with_score = cursor.fetchone()['count']
        
        cursor.execute("SELECT SUM(blockchain_score) as total FROM users")
        total_score_synced = cursor.fetchone()['total'] or 0
        
        conn.close()
        
        # Get interaction count (estimate from blockchain if available)
        # For now use DB follower count as proxy
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM followers WHERE follow_confirmed=1")
        total_interactions = cursor.fetchone()['count']
        conn.close()
        
        return {
            "blockchain_health": health,
            "contracts": {
                "identity_nft": os.getenv("IDENTITY_NFT_ADDRESS", ""),
                "resonance_score": os.getenv("RESONANCE_SCORE_ADDRESS", ""),
                "registry": os.getenv("REGISTRY_ADDRESS", "")
            },
            "stats": {
                "total_identities": total_identities,
                "total_interactions": total_interactions,
                "total_score_synced": total_score_synced,
                "users_with_blockchain_score": users_with_score
            },
            "basescan_base_url": "https://sepolia.basescan.org"
        }
        
    except Exception as e:
        log_activity("ERROR", "API", f"Blockchain stats error: {str(e)}")
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

# 🔐 SECURITY: Challenge-Response Authentication for Dashboard
# Requires ACTIVE MetaMask confirmation via personal_sign
dashboard_challenges = {}  # {address: {nonce, timestamp}}

@app.post("/admin/challenge")
async def get_dashboard_challenge(data: dict):
    """
    🔐 SECURITY: Get a challenge to sign with MetaMask (personal_sign)
    
    This requires:
    - ACTIVE MetaMask confirmation (cannot be bypassed)
    - User MUST click "Sign" in MetaMask every time
    - Even if MetaMask is unlocked
    
    Request body: {"owner": "0x..."}
    Response: {"success": true, "nonce": "...", "message": "..."}
    """
    try:
        import secrets
        
        owner = data.get("owner", "").lower()
        
        if not owner or not owner.startswith("0x") or len(owner) != 42:
            return {"success": False, "error": "Invalid owner wallet"}
        
        # Generate unique nonce
        nonce = secrets.token_hex(16)
        
        # Store challenge with timestamp (5 min expiry)
        dashboard_challenges[owner] = {
            "nonce": nonce,
            "timestamp": time.time(),
            "expiry": 300
        }
        
        log_activity("INFO", "AUTH", "Dashboard challenge created", owner=owner[:10], nonce=nonce[:10])
        
        return {
            "success": True,
            "nonce": nonce,
            "message": "🔐 Sign this in MetaMask to access your dashboard"
        }
    except Exception as e:
        log_activity("ERROR", "AUTH", "Challenge creation failed", error=str(e))
        return {"success": False, "error": str(e)}

@app.post("/admin/verify-signature")
async def verify_dashboard_signature(data: dict):
    """
    🔐 SECURITY: Verify personal_sign signature
    
    Request body:
        {
            "owner": "0x...",
            "signature": "0x...",
            "nonce": "..."
        }
    
    Response:
        {
            "success": true,
            "verified": true,
            "message": "✓ Verified"
        }
    """
    try:
        from eth_account.messages import encode_defunct
        from eth_account import Account
        
        owner = data.get("owner", "").lower()
        signature = data.get("signature", "")
        nonce = data.get("nonce", "")
        
        if not owner or not signature or not nonce:
            return {"success": False, "error": "owner, signature, and nonce required"}
        
        # Get stored challenge
        if owner not in dashboard_challenges:
            log_activity("WARNING", "AUTH", "No challenge found", owner=owner[:10])
            return {"success": False, "error": "No challenge found. Request a new one."}
        
        challenge_data = dashboard_challenges[owner]
        
        # Verify nonce matches
        if challenge_data["nonce"] != nonce:
            log_activity("WARNING", "AUTH", "Nonce mismatch", owner=owner[:10])
            return {"success": False, "error": "Invalid nonce"}
        
        # Check if challenge expired (5 minutes)
        if time.time() - challenge_data["timestamp"] > challenge_data["expiry"]:
            del dashboard_challenges[owner]
            log_activity("WARNING", "AUTH", "Challenge expired", owner=owner[:10])
            return {"success": False, "error": "Challenge expired"}
        
        # Verify signature
        try:
            messageToSign = f"VEra-Resonance Dashboard Access\n\nNonce: {nonce}\n\nBitte bestätigen Sie in MetaMask um auf Ihr Dashboard zuzugreifen."
            message = encode_defunct(text=messageToSign)
            recovered_address = Account.recover_message(message, signature=signature).lower()
        except Exception as e:
            log_activity("ERROR", "AUTH", "Signature recovery failed", owner=owner[:10], error=str(e))
            return {"success": False, "error": f"Invalid signature: {str(e)}"}
        
        # Check if signature matches owner
        if recovered_address != owner:
            log_activity("WARNING", "AUTH", "Signature mismatch", expected=owner[:10], got=recovered_address[:10])
            return {"success": False, "error": "Signature mismatch"}
        
        # Verified! Delete challenge (one-time use)
        del dashboard_challenges[owner]
        
        log_activity("INFO", "AUTH", "✓ Dashboard signature verified", owner=owner[:10])
        
        # ===== NFT RETRY LOGIC + NEW USER REGISTRATION =====
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT identity_status, identity_mint_tx_hash, score FROM users WHERE address=?", (owner,))
            result = cursor.fetchone()
            
            if not result:
                # ===== NEW USER: First-time Dashboard access =====
                log_activity("INFO", "AUTH", "🆕 First-time dashboard user - creating account", address=owner[:10])
                
                # Create user with initial score
                current_iso = datetime.now(timezone.utc).isoformat()
                cursor.execute(
                    """INSERT INTO users (address, score, created_at, identity_status)
                       VALUES (?, ?, ?, ?)""",
                    (owner, INITIAL_SCORE, current_iso, 'pending')
                )
                conn.commit()
                
                # Sync initial score to blockchain
                log_activity("INFO", "BLOCKCHAIN", "🔄 Syncing initial score", address=owner[:10])
                await sync_score_after_update(owner, INITIAL_SCORE, conn)
                
                # Wait 2 seconds (nonce conflict prevention)
                await asyncio.sleep(2)
                
                # Mint NFT for new user
                log_activity("INFO", "BLOCKCHAIN", "🎨 Starting Identity NFT mint for new dashboard user", address=owner[:10])
                success, mint_result = await web3_service.mint_identity_nft(owner)
                
                if success:
                    new_tx_hash = mint_result
                    cursor.execute(
                        """UPDATE users 
                           SET identity_status='minting', identity_mint_tx_hash=?, identity_minted_at=?
                           WHERE address=?""",
                        (new_tx_hash, current_iso, owner)
                    )
                    conn.commit()
                    log_activity("INFO", "BLOCKCHAIN", "✅ NFT mint transaction sent for new user", 
                                address=owner[:10], 
                                tx_hash=new_tx_hash[:16] + "...")
                else:
                    error_msg = mint_result
                    cursor.execute("UPDATE users SET identity_status='failed' WHERE address=?", (owner,))
                    conn.commit()
                    log_activity("WARNING", "BLOCKCHAIN", f"NFT minting failed for new user: {error_msg}", address=owner[:10])
            
            elif result:
                # ===== EXISTING USER: Check for retry =====
                db_identity_status = result[0]
                tx_hash = result[1]
                
                # RETRY if status is 'minting' without tx_hash OR 'failed'
                if db_identity_status in ['failed', 'pending'] or (db_identity_status == 'minting' and not tx_hash):
                    log_activity("INFO", "BLOCKCHAIN", "🔄 Retry: NFT mint for dashboard login", address=owner[:10])
                    
                    # Check if user already has NFT on-chain
                    has_identity = await web3_service.has_identity_nft(owner)
                    
                    if not has_identity:
                        # Attempt NFT mint
                        success, mint_result = await web3_service.mint_identity_nft(owner)
                        
                        if success:
                            new_tx_hash = mint_result
                            cursor.execute(
                                """UPDATE users 
                                   SET identity_status='minting', identity_mint_tx_hash=?, identity_minted_at=?
                                   WHERE address=?""",
                                (new_tx_hash, datetime.now(timezone.utc).isoformat(), owner)
                            )
                            conn.commit()
                            log_activity("INFO", "BLOCKCHAIN", "✅ NFT mint retry successful", 
                                        address=owner[:10], 
                                        tx_hash=new_tx_hash[:16] + "...")
                        else:
                            error_msg = mint_result
                            cursor.execute("UPDATE users SET identity_status='failed' WHERE address=?", (owner,))
                            conn.commit()
                            log_activity("WARNING", "BLOCKCHAIN", f"NFT retry failed: {error_msg}", address=owner[:10])
                    else:
                        # User already has NFT - update status
                        token_id = await web3_service.get_identity_token_id(owner)
                        if token_id is not None:
                            cursor.execute(
                                """UPDATE users 
                                   SET identity_nft_token_id=?, identity_status='active'
                                   WHERE address=?""",
                                (token_id, owner)
                            )
                            conn.commit()
                            log_activity("INFO", "BLOCKCHAIN", "✓ NFT already minted, status updated", 
                                        address=owner[:10], token_id=token_id)
            
            conn.close()
        except Exception as e:
            log_activity("WARNING", "BLOCKCHAIN", f"NFT retry check failed: {str(e)}", address=owner[:10])
        # ===== END NFT RETRY LOGIC =====
        
        return {
            "success": True,
            "verified": True,
            "message": "✓ Verified - Dashboard access granted"
        }
    except Exception as e:
        log_activity("ERROR", "AUTH", "Signature verification failed", error=str(e))
        return {"success": False, "error": str(e)}

@app.get("/admin/followers")
async def get_followers_dashboard(req: Request):
    """
    Admin Dashboard - Shows all verified followers for an owner
    
    Query Parameters:
        owner: Owner wallet address (required)
        token: Optional signature for verification
    
    Returns:
        {
            "owner": "0x...",
            "total_followers": 42,
            "followers": [
                {
                    "follower_address": "0x...",
                    "resonance_score": 51,
                    "verified_at": "2025-11-21T10:00:00",
                    "source_platform": "twitter",
                    "verified": true
                }
            ],
            "statistics": {
                "average_score": 65.5,
                "verified_count": 42,
                "by_platform": {"twitter": 15, "discord": 8}
            }
        }
    """
    try:
        # Get owner from query params
        owner_wallet = req.query_params.get("owner", "").lower()
        
        if not owner_wallet:
            return {"error": "owner parameter required", "success": False}
        
        if not owner_wallet.startswith("0x") or len(owner_wallet) != 42:
            return {"error": "Invalid owner wallet format", "success": False}
        
        log_activity("INFO", "ADMIN", "Dashboard requested", owner=owner_wallet[:10])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all followers for this owner
        cursor.execute("""
            SELECT 
                f.id,
                f.follower_address,
                f.follower_score,
                f.follower_display_name,
                f.verified_at,
                f.source_platform,
                f.verified,
                u.login_count,
                u.last_login,
                u.created_at
            FROM followers f
            LEFT JOIN users u ON f.follower_address = u.address
            WHERE f.owner_wallet = ?
            ORDER BY f.verified_at DESC
        """, (owner_wallet,))
        
        followers = cursor.fetchall()
        
        # Calculate statistics
        if followers:
            total_verified = len(followers)
            avg_score = sum(f['follower_score'] if f['follower_score'] else 0 for f in followers) / len(followers)
            
            # Group by platform
            platform_counts = {}
            for f in followers:
                platform = f['source_platform'] or 'unknown'
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
        else:
            total_verified = 0
            avg_score = 0
            platform_counts = {}
        
        # Get owner stats
        cursor.execute("SELECT score, login_count, created_at FROM users WHERE address=?", (owner_wallet,))
        owner_data = cursor.fetchone()
        
        conn.close()
        
        log_activity("INFO", "ADMIN", "Dashboard returned", 
                    owner=owner_wallet[:10], 
                    followers_count=total_verified)
        
        return {
            "success": True,
            "owner": owner_wallet,
            "owner_score": owner_data['score'] if owner_data else None,
            "total_followers": total_verified,
            "followers": [
                {
                    "follower_address": f['follower_address'],
                    "display_name": f['follower_display_name'],
                    "resonance_score": f['follower_score'],
                    "verified_at": f['verified_at'],
                    "source_platform": f['source_platform'],
                    "verified": bool(f['verified']),
                    "login_count": f['login_count'] or 0,
                    "last_login": f['last_login']
                }
                for f in followers
            ],
            "statistics": {
                "average_score": round(avg_score, 2),
                "verified_count": total_verified,
                "by_platform": platform_counts,
                "timestamp": int(time.time())
            }
        }
        
    except Exception as e:
        log_activity("ERROR", "ADMIN", f"Dashboard error: {str(e)}")
        return {"error": str(e), "success": False}

@app.get("/admin/follower-link")
async def generate_follower_link(req: Request):
    """
    Generate a custom follower link for an owner
    
    Query Parameters:
        owner: Owner wallet address (required)
        source: Social media platform (optional: twitter, discord, telegram, etc.)
    
    Returns:
        {
            "owner": "0x...",
            "follower_link": "https://ngrok.url/?owner=0x...&source=twitter",
            "qr_code": "data:image/png;base64,..."
        }
    """
    try:
        owner_wallet = req.query_params.get("owner", "").lower()
        source = req.query_params.get("source", "direct")
        
        if not owner_wallet or not owner_wallet.startswith("0x") or len(owner_wallet) != 42:
            return {"error": "Invalid owner wallet", "success": False}
        
        # Use ngrok URL if available, otherwise fall back to PUBLIC_URL
        base_url = NGROK_URL if NGROK_URL else PUBLIC_URL
        
        # If ngrok URL not set, try to detect from ngrok API
        if not base_url or base_url == PUBLIC_URL:
            try:
                import urllib.request
                ngrok_response = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2)
                import json as json_lib
                tunnels_data = json_lib.loads(ngrok_response.read().decode())
                tunnels = tunnels_data.get("tunnels", [])
                for tunnel in tunnels:
                    if tunnel.get("proto") == "https":
                        base_url = tunnel.get("public_url", base_url)
                        break
            except:
                # Fall back to PUBLIC_URL if ngrok API not available
                base_url = PUBLIC_URL
        
        # Build follower link
        follower_link = f"{base_url}/?owner={owner_wallet}&source={source}"
        
        log_activity("INFO", "ADMIN", "Follower link generated", 
                    owner=owner_wallet[:10], 
                    source=source,
                    base_url=base_url)
        
        return {
            "success": True,
            "owner": owner_wallet,
            "source": source,
            "follower_link": follower_link,
            "base_url": base_url,
            "instructions": {
                "step1": "Share this link with your followers",
                "step2": "They click the link and verify with their wallet",
                "step3": "They appear in your dashboard at /admin/followers?owner=" + owner_wallet,
                "step4": "Track their Resonance Score and engagement"
            }
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

@app.post("/admin/confirm-follower")
async def confirm_follower(req: Request):
    """
    Confirm a follower from the follower's side (after MetaMask verification)
    
    Request Body:
        {
            "owner": "0x...",
            "follower": "0x..."
        }
    
    Updates followers table to set follow_confirmed = 1
    """
    try:
        data = await req.json()
        owner = data.get("owner", "").lower()
        follower = data.get("follower", "").lower()
        
        if not owner or not owner.startswith("0x") or len(owner) != 42:
            return {"error": "Invalid owner wallet", "success": False}
        
        if not follower or not follower.startswith("0x") or len(follower) != 42:
            return {"error": "Invalid follower wallet", "success": False}
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if follower record exists
        cursor.execute(
            "SELECT * FROM followers WHERE owner_wallet = ? AND follower_address = ?",
            (owner, follower)
        )
        follower_record = cursor.fetchone()
        
        if not follower_record:
            conn.close()
            return {"error": "Follower record not found", "success": False}
        
        # Update to mark as confirmed
        cursor.execute(
            "UPDATE followers SET follow_confirmed = 1, confirmed_at = datetime('now') WHERE owner_wallet = ? AND follower_address = ?",
            (owner, follower)
        )
        conn.commit()
        conn.close()
        
        log_activity("INFO", "ADMIN", "Follow confirmed",
                    owner=owner[:10],
                    follower=follower[:10])
        
        # ===== BLOCKCHAIN: RECORD INTERACTION =====
        try:
            # Record follow interaction on-chain (Type 0 = FOLLOW)
            dashboard_link = f"{PUBLIC_URL}/dashboard?owner={owner}"
            success, result = await web3_service.record_interaction(
                initiator=follower,         # Follower initiates the follow
                responder=owner,            # Owner receives the follow
                interaction_type=0,         # 0 = FOLLOW
                dashboard_link=dashboard_link
            )
            
            if success:
                tx_hash = result
                log_activity("INFO", "BLOCKCHAIN", "✓ Interaction recorded on-chain",
                            initiator=follower[:10],
                            responder=owner[:10],
                            type="FOLLOW",
                            tx_hash=tx_hash[:20] if tx_hash else "unknown")
            else:
                error_msg = result
                log_activity("WARNING", "BLOCKCHAIN", f"Interaction recording failed: {error_msg}",
                            initiator=follower[:10],
                            responder=owner[:10])
        
        except Exception as e:
            log_activity("WARNING", "BLOCKCHAIN", f"Interaction recording error (non-critical): {str(e)}",
                        initiator=follower[:10],
                        responder=owner[:10])
        
        return {
            "success": True,
            "message": "Follow request confirmed",
            "owner": owner,
            "follower": follower
        }
        
    except Exception as e:
        logger.error(f"❌ confirm_follower error: {str(e)}")
        return {"error": str(e), "success": False}


# ===== BLOCKCHAIN SYNC DEBUG ENDPOINTS =====

@app.get("/api/blockchain/sync-queue")
async def get_sync_queue():
    """Debug: Zeigt aktuelle Sync Queue"""
    from blockchain_sync import sync_queue
    return {
        "queue_size": len(sync_queue),
        "items": [
            {
                "address": item["address"][:10] + "...",
                "score": item["score"],
                "attempts": item["attempts"],
                "last_attempt": item["last_attempt"].isoformat() if item.get("last_attempt") else None
            }
            for item in sync_queue
        ]
    }

@app.post("/api/blockchain/trigger-sync/{address}")
async def trigger_sync(address: str):
    """Debug: Triggert manuellen Sync für User"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT score, blockchain_score FROM users WHERE LOWER(address) = LOWER(?)", (address,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {"error": "User not found", "success": False}
        
        db_score, blockchain_score = result
        blockchain_score = blockchain_score or 0
        
        from blockchain_sync import add_to_sync_queue, should_sync_score
        
        if should_sync_score(db_score, blockchain_score):
            add_to_sync_queue(address, db_score)
            return {
                "success": True,
                "message": f"Added {address[:10]}... to sync queue",
                "db_score": db_score,
                "blockchain_score": blockchain_score
            }
        else:
            return {
                "success": False,
                "message": "User does not meet sync criteria",
                "db_score": db_score,
                "blockchain_score": blockchain_score,
                "next_milestone": ((db_score // 10) + 1) * 10
            }
    
    except Exception as e:
        logger.error(f"❌ trigger_sync error: {str(e)}")
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
