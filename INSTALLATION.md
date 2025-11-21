# 🚀 VEra-Resonance – Installation & Quick Start Guide

Complete guide to start the VEra-Resonance system.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Step-by-Step](#installation-step-by-step)
3. [Starting the Server](#starting-the-server)
4. [Testing & Verification](#testing--verification)
5. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Required
- **Python 3.9+** (or 3.11)
- **pip** (Python Package Manager)
- **Git** (for cloning, optional)
- **MetaMask** or another EVM-compatible wallet (for frontend testing)

### Recommended
- **Virtual Environment** (venv) – for isolation
- **Postman or cURL** – for API testing
- **VS Code or IDE** – for editing

### Optional
- **Docker** – for containerized deployment
- **PostgreSQL** – for production (instead of SQLite)

---

## 📦 Installation Step-by-Step

### Step 1: Clone Repository / Navigate to Folder

```bash
# If not already in webside-wallet-login folder:
cd /path/to/webside-wallet-login
```

### Step 2: Create Virtual Environment (RECOMMENDED)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows (CMD)
python -m venv venv
venv\Scripts\activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

**Output should look like:**
```
(venv) user@machine ~/webside-wallet-login $
```

### Step 3: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 4: Install Dependencies

**Option A: Using requirements.txt**
```bash
pip install -r requirements.txt
```

**Option B: Manual**
```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install pydantic==2.5.0
pip install python-dotenv==1.0.0
```

**Output should show:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 pydantic-2.5.0 ...
```

### Step 5: Verify Installation

```bash
python -c "import fastapi; import uvicorn; print('✓ All imports OK')"
```

**Expected:** `✓ All imports OK`

---

## 🚀 Starting the Server

### Method A: Simple (Recommended)

```bash
# Make sure your venv is activated
source venv/bin/activate  # or equivalent for your OS

# Start the server
uvicorn server:app --reload --port 8820
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8820
INFO:     Application startup complete
```

### Method B: Using Shell Script

```bash
./start.sh
```

(Script activates venv automatically)

### Method C: Without Auto-Reload

```bash
uvicorn server:app --port 8820
```

(Faster, but code changes require restart)

---

## 🧪 Testing & Verification

### Test 1: Health Check (Terminal)

```bash
# Open a NEW terminal tab/window
curl http://localhost:8820/api/health | python -m json.tool
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "VEra-Resonance v0.1",
  "timestamp": 1234567890
}
```

---

### Test 2: Open Frontend (Browser)

Go to: **http://localhost:8820**

You should see:
- ✅ VEra-Resonance logo
- ✅ "Connect Wallet" button
- ✅ "Decentralized Proof-of-Human" text

---

### Test 3: Wallet Connection (Browser)

1. **Open MetaMask** – Make sure MetaMask is installed
2. **Click "Connect Wallet"**
3. **Approve in MetaMask**
4. You should see your wallet address ✓

---

### Test 4: Verification (Browser)

1. **After successful wallet connection:** Click "Verify" button
2. **Server responds with score:** e.g. "Score: 50/100" ✓
3. **View details:** Address, network, score

---

### Test 5: API Calls (cURL)

```bash
# Verify wallet address
curl -X POST http://localhost:8820/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```

**Expected:**
```json
{
  "is_human": true,
  "address": "0x742d35cc6634c0532925a3b844bc59e7e6d6e0de",
  "resonance_score": 50,
  "first_seen": 1234567890,
  "login_count": 1,
  "message": "Welcome! Your initial Resonance Score is 50/100"
}
```

---

### Test 6: Multiple Verifications

Run the same curl command again:

```bash
curl -X POST http://localhost:8820/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```

**Expected:** Score is now **51** (increased by 1) ✓

---

## 🛠️ Troubleshooting

### Problem: "Port 8820 already in use"

**Solution A:** Kill other processes on port 8820
```bash
# Linux/Mac
lsof -ti:8820 | xargs kill -9

# or use a different port
uvicorn server:app --port 8821
```

**Solution B:** Open browser on new port
```
http://localhost:8821
```

---

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Activate virtual environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Then install dependencies again
pip install -r requirements.txt
```

---

### Problem: "Connection refused" during cURL test

**Solution:** Server is not running
```bash
# Check if server is running
ps aux | grep uvicorn

# If not, restart it
uvicorn server:app --port 8820
```

---

### Problem: MetaMask Connect button doesn't work

**Solution 1:** Install MetaMask extension
- Chrome: https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn

**Solution 2:** Check developer console
- Browser: F12 → Console
- Look for error messages

**Solution 3:** Clear browser cache
```
Ctrl+Shift+Delete → Cookies & Cache
```

---

### Problem: CORS errors in browser

**Sign:**
```
Access to XMLHttpRequest at 'http://localhost:8820/api/verify' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:** CORS is already enabled in `server.py`. If problem persists:
```python
# Check after line 16 in server.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← must be like this
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Problem: Database errors

**Sign:** `sqlite3.OperationalError`

**Solution:** Reset database
```bash
# Delete old database
rm aera.db

# Restart server
uvicorn server:app --reload --port 8820
```

Database will be automatically recreated.

---

## 📊 Logs & Debugging

### Server Logs in Detail

```bash
# With more debug info
uvicorn server:app --reload --port 8820 --log-level debug
```

### Browser Console

```javascript
// In browser open: F12 → Console
// Then test:
fetch('http://localhost:8820/api/health')
  .then(r => r.json())
  .then(d => console.log('✓ Server OK:', d))
  .catch(e => console.error('✗ Error:', e))
```

### Inspect SQLite Database

```bash
# Open SQLite CLI
sqlite3 aera.db

# Then in console:
> SELECT * FROM users;
> SELECT * FROM events;
> .quit
```

---

## ✅ Checklist: Everything Running?

- [ ] Python 3.9+ installed
- [ ] Virtual environment created & activated
- [ ] `pip install -r requirements.txt` successful
- [ ] `uvicorn server:app --reload --port 8820` starts
- [ ] `curl http://localhost:8820/api/health` responds
- [ ] Browser opens `http://localhost:8820`
- [ ] Connect Wallet button visible
- [ ] MetaMask wallet connected ✓
- [ ] Verification works
- [ ] Score increases with multiple verifications

---

## 🎉 Done!

You have successfully installed VEra-Resonance! 🚀

### Next Steps:

1. **Integration into other platforms** – Use the `/api/verify` endpoint
2. **Customization** – Adjust colors, logo, scoring logic
3. **Production Deployment** – See `README.md` → Deployment section
4. **On-Chain Integration** – Connect with VEra-Resonance Token Smart Contract

---

## 📞 Support & Links

- **GitHub:** [VEra-Resonance/AEra-LogIn](https://github.com/VEra-Resonance/AEra-LogIn)
- **Docs:** See `README.md`
- **License:** Apache License 2.0 (see `LICENSE`)
- **Contact:** Karlheinz Beismann (2025)

---

**VEra-Resonance © 2025 Karlheinz Beismann** ⸻ *Decentralized Proof-of-Human – No KYC, No Identity Theft*
