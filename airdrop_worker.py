"""
AEra Airdrop Worker - Automatische Token-Versendung
Überwacht die airdrop-Tabelle und versendet Tokens
"""

import sqlite3
import time
import logging
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from web3 import Web3
import sys

# Load environment variables
load_dotenv()

# Logging Setup
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "info").upper(),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "aera.db")
ADMIN_WALLET = os.getenv("ADMIN_WALLET", "")
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY", "")
# Nutze Fallback zu Alchemy wenn SEPOLIA_RPC_URL nicht konfiguriert
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL", "https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY")
AERA_CONTRACT = "0x5032206396A6001eEaD2e0178C763350C794F69e"
AIRDROP_AMOUNT = 0.5  # AEra Tokens
AIRDROP_AMOUNT_WEI = int(AIRDROP_AMOUNT * 10**18)  # Convert to Wei

# Minimal ERC-20 Transfer ABI
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

def get_db_connection():
    """Stellt Datenbankverbindung her"""
    conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")
    return conn

def check_credentials():
    """Überprüfe ob Admin-Credentials vorhanden sind"""
    if not ADMIN_WALLET or not ADMIN_PRIVATE_KEY:
        logger.error("❌ FEHLER: ADMIN_WALLET oder ADMIN_PRIVATE_KEY nicht konfiguriert!")
        logger.error("   Setze diese in der .env Datei:")
        logger.error(f"   ADMIN_WALLET={ADMIN_WALLET or 'YOUR_ADMIN_WALLET'}")
        logger.error(f"   ADMIN_PRIVATE_KEY={'***' if ADMIN_PRIVATE_KEY else 'YOUR_PRIVATE_KEY'}")
        return False
    
    if ADMIN_WALLET.startswith("0x") and len(ADMIN_WALLET) == 42:
        logger.info(f"✓ Admin Wallet: {ADMIN_WALLET[:6]}...{ADMIN_WALLET[-4:]}")
        return True
    else:
        logger.error(f"❌ Ungültige Admin-Wallet Adresse: {ADMIN_WALLET}")
        return False

def connect_web3():
    """Verbinde zu Sepolia Testnet"""
    try:
        w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
        
        if not w3.is_connected():
            logger.error(f"❌ Kann nicht zu Sepolia verbinden: {SEPOLIA_RPC_URL}")
            return None
        
        logger.info(f"✓ Verbunden zu Sepolia (Block: {w3.eth.block_number})")
        return w3
    except Exception as e:
        logger.error(f"❌ Web3-Verbindungsfehler: {str(e)}")
        return None

def send_airdrop(w3, recipient_address: str, amount_wei: int) -> dict:
    """
    Sendet Token an die Empfänger-Adresse
    
    Returns:
        {
            "success": bool,
            "tx_hash": str or None,
            "error": str or None
        }
    """
    try:
        # Prüfe Adressen
        if not Web3.is_address(recipient_address):
            return {"success": False, "tx_hash": None, "error": "Invalid recipient address"}
        
        recipient_address = Web3.to_checksum_address(recipient_address)
        admin_wallet = Web3.to_checksum_address(ADMIN_WALLET)
        contract_address = Web3.to_checksum_address(AERA_CONTRACT)
        
        logger.info(f"📤 Versende {amount_wei / 10**18} AERA zu {recipient_address[:6]}...{recipient_address[-4:]}")
        
        # Verbinde zum Contract
        contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)
        
        # Hole Nonce für Admin-Wallet
        nonce = w3.eth.get_transaction_count(admin_wallet)
        
        # Baue Transaction
        tx = contract.functions.transfer(
            recipient_address,
            amount_wei
        ).build_transaction({
            'from': admin_wallet,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 11155111  # Sepolia Chain ID
        })
        
        # Signiere Transaction
        signed_tx = w3.eth.account.sign_transaction(
            tx,
            ADMIN_PRIVATE_KEY
        )
        
        # Versende Transaction (kompatibel mit web3.py v6+)
        try:
            # web3.py v6+ Stil
            raw_tx = signed_tx.raw_transaction
        except AttributeError:
            try:
                # Alternative für manche Versionen
                raw_tx = signed_tx.raw
            except AttributeError:
                # Fallback: nutze bytes() auf SignedTransaction
                raw_tx = bytes(signed_tx)
        
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        tx_hash_str = tx_hash.hex()
        
        logger.info(f"✓ Transaction versendet: {tx_hash_str}")
        
        return {
            "success": True,
            "tx_hash": tx_hash_str,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"❌ Airdrop-Fehler: {str(e)}")
        return {
            "success": False,
            "tx_hash": None,
            "error": str(e)
        }

def process_pending_airdrops(w3):
    """Verarbeitet alle pending Airdrops"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hole alle pending Airdrops
        cursor.execute(
            "SELECT id, address, amount FROM airdrops WHERE status='pending_execution' LIMIT 10"
        )
        pending = cursor.fetchall()
        
        if not pending:
            logger.debug("ℹ️ Keine pending Airdrops gefunden")
            conn.close()
            return
        
        logger.info(f"⏳ Verarbeite {len(pending)} pending Airdrops...")
        
        for airdrop in pending:
            airdrop_id = airdrop['id']
            address = airdrop['address']
            amount = airdrop['amount']
            
            # Konvertiere zu Wei
            amount_wei = int(amount * 10**18)
            
            # Versende Token
            result = send_airdrop(w3, address, amount_wei)
            
            if result["success"]:
                # Update Status auf completed
                cursor.execute(
                    """UPDATE airdrops 
                       SET status='completed', tx_hash=?
                       WHERE id=?""",
                    (result["tx_hash"], airdrop_id)
                )
                logger.info(f"✅ Airdrop #{airdrop_id} abgeschlossen: {result['tx_hash'][:10]}...")
                
            else:
                # Update Status auf failed
                cursor.execute(
                    """UPDATE airdrops 
                       SET status='failed', tx_hash=?
                       WHERE id=?""",
                    (result["error"], airdrop_id)
                )
                logger.error(f"❌ Airdrop #{airdrop_id} fehlgeschlagen: {result['error']}")
            
            conn.commit()
        
        conn.close()
        logger.info(f"✓ Airdrop-Verarbeitung abgeschlossen")
        
    except Exception as e:
        logger.error(f"❌ Fehler bei Airdrop-Verarbeitung: {str(e)}")

def main():
    """Hauptschleife des Airdrop-Workers"""
    logger.info("=" * 60)
    logger.info("🚀 AEra Airdrop Worker gestartet")
    logger.info("=" * 60)
    
    # Überprüfe Credentials
    if not check_credentials():
        logger.error("❌ Kann nicht ohne Admin-Credentials starten!")
        sys.exit(1)
    
    # Verbinde zu Web3
    w3 = connect_web3()
    if not w3:
        logger.error("❌ Kann nicht zu Sepolia verbinden!")
        sys.exit(1)
    
    # Hauptschleife
    logger.info("⏳ Überwache Airdrop-Anfragen (drücke Ctrl+C zum Beenden)...")
    
    try:
        while True:
            try:
                process_pending_airdrops(w3)
                time.sleep(10)  # Überprüfe alle 10 Sekunden
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logger.error(f"❌ Fehler in Hauptschleife: {str(e)}")
                time.sleep(10)
    
    except KeyboardInterrupt:
        logger.info("\n⏹️ Worker beendet (SIGINT)")
        sys.exit(0)

if __name__ == "__main__":
    main()
