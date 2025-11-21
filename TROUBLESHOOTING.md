# 🔧 VEra-Resonance – Troubleshooting Guide

Solutions for common problems.

---

## ❌ Problem: Website won't open

### Symptom
- Browser shows "This site can't be reached"
- or "Connection refused"

### Solution

**Step 1: Check if server is running**
```bash
ps aux | grep uvicorn | grep -v grep
```

If nothing is shown → Server is not running!

**Step 2: Start the server**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8820 --reload
```

**Step 3: Test with curl**
```bash
curl http://localhost:8820
```

Should return HTML (not an error).

**Step 4: Browser URL correct?**
- ✅ Correct: `http://localhost:8820`
- ❌ Wrong: `http://localhost:8820/index.html`
- ❌ Wrong: `localhost:8820` (missing http://)
- ❌ Wrong: `http://localhost:3000` (wrong port)

---

## ❌ Problem: QR code not visible

### Symptom
- Website loads
- But QR code is empty
- Or only text visible

### Solution

**Step 1: Open browser console**
```
F12 → Console (bottom)
```

**Step 2: Should show logs:**
```
[VEra-Resonance] === VEra-Resonance started ===
[VEra-Resonance] URL: http://localhost:8820/
[VEra-Resonance] QR code generated for: http://localhost:8820/
```

If not → JavaScript is not loading!

**Step 3: Reload page**
```
Ctrl+R  (Windows/Linux)
Cmd+R   (Mac)
```

**Step 4: Clear cache**
```
Ctrl+Shift+Delete → Delete cookies & cache
```

**Step 5: Brand new browser tab**
```
Ctrl+T → Enter http://localhost:8820
```

---

## ❌ Problem: URL not displayed

### Symptom
- QR code visible but empty
- URL box shows "loading..."
- Or "—"

### Solution

Probably a CSS issue. Try:

```javascript
// Enter in browser console (F12):
console.log('PUBLIC_URL:', window.location.href);
document.getElementById('urlDisplay').textContent = window.location.href;
```

If that works → CSS/layout bug.

---

## ❌ Problem: "Connect Wallet" doesn't work

### Symptom
- Button is clickable but nothing happens
- Or error message
- Or MetaMask popup doesn't open

### Solution A: MetaMask installed?

```
Chrome: https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn
Firefox: https://addons.mozilla.org/en-US/firefox/addon/ether-metamask/
```

### Solution B: MetaMask unlocked?

1. Click MetaMask icon in top right
2. If "Locked" → enter password

### Solution C: Correct chain?

MetaMask might be on the wrong chain:
1. Open MetaMask
2. Click "Ethereum Mainnet" at top
3. Select test network or Sepolia

### Solution D: Console errors?

```
F12 → Console → Look at red errors
```

Common errors:
```
❌ "Cannot read property 'ethereum' of undefined"
   → MetaMask not installed

❌ "User denied account access"
   → MetaMask popup was rejected

❌ "eth_requestAccounts" failed
   → MetaMask error, restart MetaMask
```

---

## ❌ Problem: Verification doesn't work

### Symptom
- Wallet connected
- "Verify" button is clickable
- But nothing happens after clicking
- Or error: "Verification failed"

### Solution

**Step 1: API reachable?**
```bash
curl http://localhost:8820/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```

Should return JSON with `"is_human": true`.

If error → API is not running!

**Step 2: Database OK?**
```bash
sqlite3 aera.db "SELECT COUNT(*) FROM users;"
```

Should return a number (e.g. 0 or 5).

If error → Database is corrupted!

**Step 3: Check browser console**
```
F12 → Console
Should show: [INFO] Response Data: {...}
```

---

## ❌ Problem: External IP not reachable

### Symptom
- Locally works: `http://localhost:8820`
- But from phone: `http://192.168.1.100:8820` doesn't work

### Solution

**Step 1: Bind server to 0.0.0.0**
```bash
# WRONG:
uvicorn server:app --host 127.0.0.1 --port 8820

# CORRECT:
uvicorn server:app --host 0.0.0.0 --port 8820
```

**Step 2: Find external IP**
```bash
hostname -I
# e.g. 192.168.1.100
```

**Step 3: Test from phone**
```
http://192.168.1.100:8820
```

**Step 4: Check firewall**
```bash
# Allow port 8820
sudo ufw allow 8820
```

or

```bash
# Disable firewall completely (testing only!)
sudo ufw disable
```

---

## ❌ Problem: Port 8820 already in use

### Symptom
```
bind() exception: Address already in use
ERROR:     Uvicorn server failed to start. A server process is probably running already on port 8820.
```

### Solution

**Step 1: Find old processes**
```bash
ps aux | grep 8820
# or
lsof -ti:8820
```

**Step 2: Kill process**
```bash
# Gently:
kill <PID>

# Forced:
kill -9 <PID>

# Or directly:
lsof -ti:8820 | xargs kill -9
```

**Step 3: Restart**
```bash
uvicorn server:app --host 0.0.0.0 --port 8820
```

**Step 4: Use different port**
```bash
uvicorn server:app --host 0.0.0.0 --port 8821
# Then: http://localhost:8821
```

---

## ❌ Problem: Python import error

### Symptom
```
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'uvicorn'
```

### Solution

**Step 1: Activate virtual environment**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
source venv/bin/activate
```

Should look like: `(venv) user@machine ~$`

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Restart**
```bash
uvicorn server:app --host 0.0.0.0 --port 8820
```

---

## ❌ Problem: CORS error

### Symptom
```
Access to XMLHttpRequest at 'http://localhost:8820/api/verify' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

### Solution

CORS is already enabled in `server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Allows all origins
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If problem persists:

**Step 1: Check .env**
```bash
cat .env | grep CORS
```

Should show:
```
CORS_ORIGINS=*
```

**Step 2: Restart server**
```bash
pkill -f uvicorn
uvicorn server:app --host 0.0.0.0 --port 8820
```

---

## ❌ Problem: Database error

### Symptom
```
sqlite3.OperationalError: unable to open database file
sqlite3.DatabaseError: database disk image is malformed
```

### Solution

**Step 1: Delete database**
```bash
rm aera.db
```

**Step 2: Restart server**
```bash
uvicorn server:app --host 0.0.0.0 --port 8820
```

The database will be automatically recreated.

**Step 3: Check if new database was created**
```bash
ls -la aera.db
```

Should show the file.

---

## ✅ Quick debug checklist

```bash
# 1. Server running?
ps aux | grep uvicorn

# 2. Responds to requests?
curl http://localhost:8820

# 3. API reachable?
curl http://localhost:8820/api/health

# 4. Database OK?
sqlite3 aera.db "SELECT 1;"

# 5. Ports free?
lsof -i :8820

# 6. venv activated?
which python  # Should show venv/bin/python

# 7. View logs?
# Open new terminal
cd webside-wallet-login
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8820 --log-level debug
```

---

## 🎯 Advanced debugging

### Full log capture
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8820 --log-level debug 2>&1 | tee server.log
```

Then open page → view logs in `server.log`.

### Browser network tab
```
F12 → Network Tab
Then click each request for details:
- Status code?
- Response?
- Headers?
```

### API test with Postman/Insomnia
```
POST http://localhost:8820/api/verify
Headers: Content-Type: application/json
Body: {"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}
```

---

## 📞 If nothing works

1. **Export logs:**
   ```bash
   curl http://localhost:8820/api/debug | python3 -m json.tool > debug.json
   ```

2. **Browser console screenshot** (F12)

3. **Copy terminal output:**
   ```bash
   ps aux | grep uvicorn
   sqlite3 aera.db ".tables"
   ```

4. **Post all info together** with problem description

---

**VEra-Resonance Troubleshooting © 2025 Karlheinz Beismann** ⸻ Apache License 2.0
