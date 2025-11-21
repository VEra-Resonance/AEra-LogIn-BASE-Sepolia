# 🚀 VEra-Resonance API - Features Overview

**Status:** ✅ Production-Ready v0.1  
**Backend:** FastAPI + SQLite  
**Authentication:** MetaMask Wallet Signature (EIP-191)  

---

## 📋 Current Features

### 1️⃣ **Wallet Login System** ✅
- **MetaMask Integration**: Sign-in with wallet signature
- **Signature Verification**: EIP-191 standard message signing
- **Non-Custodial**: No private keys stored on server
- **Nonce-Based**: Replay attack protection

#### Endpoints:
```
POST /api/nonce
  → Generate random nonce for signing
  
POST /api/verify
  → Verify signed message + create login session
```

**Example Flow:**
```bash
# 1. Get Nonce
curl -X POST http://localhost:8820/api/nonce \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'

# Response:
{
  "success": true,
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "nonce": "a1b2c3d4...",
  "message": "Signiere diese Nachricht um dich bei AEra anzumelden:\nNonce: a1b2c3d4..."
}

# 2. Sign with MetaMask, then POST signature
curl -X POST http://localhost:8820/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
    "nonce": "a1b2c3d4...",
    "signature": "0x..."
  }'

# Response:
{
  "is_human": true,
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "resonance_score": 50,
  "first_seen": 1700334000,
  "last_login": 1700334120,
  "login_count": 1,
  "message": "Welcome! Your initial Resonance Score is 50/100",
  "token": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE:1700340120:signature..."
}
```

---

### 2️⃣ **Resonance Score System** ✅
- **Initial Score**: 50 points for new users
- **Max Score**: 100 points
- **Increment**: +1 point per login (capped at 100)
- **Persistent**: Tracked in SQLite database
- **Audit Trail**: All changes logged

#### Logic:
```
New User     → 50 points
Each Login   → +1 point (max 100)
Events Table → All changes recorded with timestamp
```

---

### 3️⃣ **User Data API** ✅
```
GET /api/user/{address}
```

Returns user profile:
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "resonance_score": 51,
  "first_seen": 1700334000,
  "last_login": 1700334120,
  "login_count": 2,
  "created_at": "2025-11-18T10:00:00"
}
```

---

### 4️⃣ **Statistics API** ✅
```
GET /api/stats
```

Returns public statistics:
```json
{
  "total_users": 42,
  "average_score": 65.5,
  "total_logins": 128,
  "timestamp": 1700334000
}
```

---

### 5️⃣ **Event History API** ✅
```
GET /api/events/{address}
```

Returns login events (up to 50 most recent):
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "events": [
    {
      "id": 1,
      "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
      "event_type": "signup",
      "score_before": 0,
      "score_after": 50,
      "timestamp": 1700334000,
      "created_at": "2025-11-18T10:00:00",
      "referrer": "direct",
      "user_agent": "Mozilla/5.0...",
      "ip_address": "192.168.1.1"
    }
  ]
}
```

---

### 6️⃣ **Referrer Tracking** ✅
```
GET /api/referrer-stats
```

Returns:
- New users by source (Twitter, Discord, Telegram, etc.)
- Total events per source
- Top sources in last 24 hours

```json
{
  "new_users_by_source": [
    {"first_referrer": "twitter", "count": 15},
    {"first_referrer": "discord", "count": 8}
  ],
  "total_events_by_source": [
    {"referrer": "twitter", "count": 42},
    {"referrer": "direct", "count": 28}
  ],
  "top_sources_24h": [
    {"referrer": "twitter", "count": 12}
  ],
  "timestamp": 1700334000
}
```

---

### 7️⃣ **Auto-Login Token System** ✅
```
POST /api/verify-token
```

Verify stored token for auto-login (with signature verification):
```json
{
  "token": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE:1700340120:signature...",
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "signature": "0x..."
}
```

Returns:
```json
{
  "valid": true,
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "resonance_score": 55,
  "message": "Auto-logged in"
}
```

---

### 8️⃣ **Airdrop System** ✅
- **Trigger**: Automatically on first signup
- **Token**: 0.5 AEra tokens
- **Contract**: `0x5032206396A6001eEaD2e0178C763350C794F69e`
- **Network**: Sepolia testnet
- **Status Tracking**: pending_admin → completed/failed

#### Airdrop Status:
- ✅ New signup → Airdrop triggered
- ⏳ pending_admin: Waiting for admin approval
- ✅ completed: Tokens sent to wallet
- ❌ failed: Error during transaction

---

### 9️⃣ **System Health & Debug** ✅

```
GET /api/health
```

Health check:
```json
{
  "status": "healthy",
  "service": "VEra-Resonance v0.1",
  "timestamp": 1700334000,
  "database": "connected",
  "database_path": "/path/to/aera.db"
}
```

```
GET /api/debug
```

Debug info:
```json
{
  "server": "VEra-Resonance v0.1",
  "timestamp": 1700334000,
  "client_ip": "192.168.1.1",
  "database": {
    "path": "/path/to/aera.db",
    "exists": true,
    "size_mb": 1.23
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
```

---

## 🎯 Platform Support

Dynamic landing page adapts to referrer source:

| Platform | Color | Emoji | Badge |
|----------|-------|-------|-------|
| **X / Twitter** | #1DA1F2 | 𝕏 | FROM X/TWITTER |
| **Telegram** | #0088cc | ✈️ | FROM TELEGRAM |
| **Discord** | #5865F2 | 🎮 | FROM DISCORD |
| **GitHub** | #333333 | 🐙 | FROM GITHUB |
| **Reddit** | #FF4500 | 🤖 | FROM REDDIT |
| **LinkedIn** | #0077B5 | 💼 | FROM LINKEDIN |
| **Bluesky** | #1185FE | 🦋 | FROM BLUESKY |
| **Mastodon** | #563ACC | 🐘 | FROM MASTODON |
| **Direct** | #666666 | 🌐 | DIRECT ACCESS |

---

## 📊 Database Schema

### Table: `users`
| Column | Type | Purpose |
|--------|------|---------|
| `address` | TEXT (PK) | Wallet address |
| `first_seen` | INTEGER | First login timestamp |
| `last_login` | INTEGER | Last login timestamp |
| `score` | INTEGER | Resonance score (0-100) |
| `login_count` | INTEGER | Total logins |
| `created_at` | TEXT | ISO timestamp |
| `first_referrer` | TEXT | Source of first visit |
| `last_referrer` | TEXT | Source of last visit |

### Table: `events`
| Column | Type | Purpose |
|--------|------|---------|
| `id` | INTEGER (PK) | Event ID |
| `address` | TEXT | Wallet address |
| `event_type` | TEXT | "signup" or "login" |
| `score_before` | INTEGER | Score before event |
| `score_after` | INTEGER | Score after event |
| `timestamp` | INTEGER | Unix timestamp |
| `created_at` | TEXT | ISO timestamp |
| `referrer` | TEXT | Source platform |
| `user_agent` | TEXT | Client browser info |
| `ip_address` | TEXT | Client IP (privacy: truncated) |

---

## 🔐 Security Features

✅ **Signature Verification** - EIP-191 standard (MetaMask)  
✅ **Nonce Protection** - Prevents replay attacks  
✅ **Non-Custodial** - No private keys stored  
✅ **CORS Middleware** - Configurable origins  
✅ **Error Handling** - Comprehensive try-catch blocks  
✅ **Audit Trail** - All actions logged with timestamps  
✅ **Privacy-First** - Only wallet address + score, no personal data  
✅ **Rate Limiting** - (Ready for implementation)  

---

## 🚀 Deployment Ready

✅ FastAPI ASGI server  
✅ SQLite persistence  
✅ Environment-based configuration  
✅ Structured logging  
✅ Error handling  
✅ Production-grade middleware  

### Quick Start:
```bash
# Install
pip install -r requirements.txt

# Run
python3 server.py &

# Public tunnel (ngrok)
ngrok http 8820
```

---

## 📝 What's NOT Yet Implemented

❌ Admin Dashboard (for account owners to see followers)  
❌ Rate limiting  
❌ Token refresh mechanism  
❌ Leaderboard  
❌ Badge system  
❌ Delegation system (accounts can link sub-accounts)  
❌ Mobile app  

---

## 🎯 Next Steps

**Priority 1:** Add Admin Dashboard for follower verification visibility  
**Priority 2:** Implement rate limiting  
**Priority 3:** Add leaderboard/badge system  

Want to implement any of these? 🚀
