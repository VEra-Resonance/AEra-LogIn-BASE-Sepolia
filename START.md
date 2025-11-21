# 🚀 VEra-Resonance – START HERE

## Quick Links

| Link | Description |
|------|-------------|
| 📖 [README.md](README.md) | Complete Documentation |
| ⚙️ [INSTALLATION.md](INSTALLATION.md) | Step-by-Step Setup |
| 📱 [MOBILE-SETUP.md](MOBILE-SETUP.md) | Mobile & QR Code Setup |
| 🌍 [GLOBAL-DEPLOYMENT.md](GLOBAL-DEPLOYMENT.md) | Make it globally accessible |
| ✅ [CHECKLIST.md](CHECKLIST.md) | Feature Checklist |

---

## 60-Second Quick Start

```bash
# 1. Navigate to folder
cd /home/karlheinz/krypto/aera-token/webside-wallet-login

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start the server
uvicorn server:app --host 0.0.0.0 --port 8820 --reload

# 4. Open in browser
# http://localhost:8820
```

---

## What Should Work?

✅ **QR Code visible** – In the "📱 QR Code" tab  
✅ **URL displayed** – Below QR code  
✅ **Wallet connectable** – Desktop with MetaMask  
✅ **Verification works** – Score is calculated  
✅ **Logins counted** – On multiple verifications  

---

## Troubleshooting

1. **QR Code not visible?**
   - Open browser F12 → Console
   - Should show logs
   - Reload page (Ctrl+R)

2. **Wallet won't connect?**
   - MetaMask installed?
   - MetaMask unlocked?
   - Test on http://localhost:8820

3. **API not reachable?**
   - `curl http://localhost:8820/api/health`
   - Server running?
   - Port 8820 available?

---

## File Structure

```
webside-wallet-login/
├── index.html                    # Frontend (HTML+JS)
├── server.py                     # Backend (FastAPI)
├── aera.db                       # SQLite Database
├── .env                          # Configuration
├── requirements.txt              # Python Dependencies
├── venv/                         # Virtual Environment
│
├── README.md                     # Complete Docs
├── INSTALLATION.md               # Installation Guide
├── MOBILE-SETUP.md              # Mobile Setup
├── GLOBAL-DEPLOYMENT.md         # Production Deployment
├── CHECKLIST.md                 # Feature Tests
└── START.md                      # This file
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Frontend HTML |
| GET | `/api/health` | Health Check |
| POST | `/api/verify` | Verify Wallet |
| GET | `/api/user/{address}` | User Data |
| GET | `/api/stats` | Statistics |
| GET | `/api/events/{address}` | Login History |

---

## Environment Configuration

Most important `.env` variables:

```env
# Server
HOST=0.0.0.0          # 0.0.0.0 = externally accessible
PORT=8820
PUBLIC_URL=http://localhost:8820

# For Production
PUBLIC_URL=https://vera-resonance.example.com

# CORS
CORS_ORIGINS=*        # "*" for development
```

---

## Next Steps

1. ✅ Start locally (`http://localhost:8820`)
2. ✅ Verify QR code & URL
3. ✅ Connect wallet & verify
4. ✅ Make globally accessible with ngrok
5. ✅ Go through [CHECKLIST.md](CHECKLIST.md)
6. ✅ Deploy to production

---

## Support

**View Logs:**
```bash
# In server terminal
# Press Ctrl+C to stop
# Restart with debug logging:
uvicorn server:app --host 0.0.0.0 --port 8820 --log-level debug
```

**Browser Console:**
```
F12 → Console
Should show logs with [VEra-Resonance] prefix
```

**API Test:**
```bash
curl http://localhost:8820/api/health | python3 -m json.tool
```

---

## License

Apache License 2.0 – See [LICENSE](LICENSE)

---

**VEra-Resonance © 2025 Karlheinz Beismann**  
*Decentralized Proof-of-Human – No KYC, No Identity Theft*
