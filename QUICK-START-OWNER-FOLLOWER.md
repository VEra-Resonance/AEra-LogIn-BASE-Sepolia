# ⚡ Quick Start - Owner-Follower System

## 🚀 3-Minute Setup

### 1. Start Server

```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
python3 server.py &
```

**Expected output:**
```
✓ Datenbank initialisiert: /path/to/aera.db
🚀 VEra-Resonance Server gestartet
   🌐 Öffentliche URL: http://0.0.0.0:8000
   📍 Host: 0.0.0.0:8000
```

### 2. Open Dashboard

```
Browser: http://localhost:8000/dashboard
```

You should see:
- Input field for wallet address
- "Load Dashboard" button
- Statistics cards
- Link generation section

### 3. Test with Your Wallet

```
Your wallet: 0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE

1. Copy and paste into dashboard
2. Click "Load Dashboard"
3. Should show: "0 followers" (initially)
```

### 4. Generate Follower Link

```
1. Select platform: "Twitter"
2. Click "Generate Link"
3. You'll see:

https://localhost:8000/?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE&source=twitter

4. Copy link
```

### 5. Test Follower Verification

**Open in INCOGNITO mode:**
```
https://localhost:8000/?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE&source=twitter
```

Then:
1. Click "Connect Wallet"
2. Choose a DIFFERENT wallet (or use test wallet)
3. Click "Verify"
4. Sign with MetaMask
5. You should see: "Registered as follower"

### 6. Check Dashboard Again

```
1. Go back to /dashboard
2. Enter YOUR wallet (0x742d35...)
3. Click "Load Dashboard"
4. NOW you should see:

   ✓ 1 Verified Followers
   ✓ Average Score: 50
   ✓ Table showing the follower
```

---

## 🔧 Troubleshooting

### Error: Database not initialized

```bash
# Check if aera.db exists
ls -la aera.db

# If not, restart server - it auto-creates:
python3 server.py
```

### Error: followers table doesn't exist

```bash
# The table is created on first server start
# If you get an error, restart:

# Kill old process
pkill -f "python3.*server.py"

# Start fresh
python3 server.py
```

### Browser shows blank page

```bash
# Check server is running:
curl http://localhost:8000/dashboard

# If error, check logs in terminal where you started server
```

### Follower not appearing in dashboard

```bash
# Make sure:
1. Follower link includes ?owner=0x... parameter
2. Follower used DIFFERENT wallet than owner
3. Wait 1-2 seconds after verification
4. Refresh dashboard and re-load
```

---

## 📊 Database Inspection

### Check Tables Created

```bash
# Open database
sqlite3 aera.db

# List all tables
.tables
# Should show: airdrops events followers users

# Check followers table
SELECT * FROM followers;

# Check users with owner_wallet
SELECT address, owner_wallet, is_verified_follower FROM users;
```

### Example Output

```sql
sqlite> SELECT * FROM followers;

id  | owner_wallet                         | follower_address                     | follower_score | verified_at
----|--------------------------------------|--------------------------------------|----------------|--------------------
1   | 0x742d35Cc6634C0532925a3b844Bc59... | 0x1234567890abcdef1234567890abcdef12  | 50             | 2025-11-21...

sqlite> SELECT address, owner_wallet FROM users;

address                                  | owner_wallet
-----------------------------------------|--------------------------------------
0x742d35Cc6634C0532925a3b844Bc59e7e...  | (null)
0x1234567890abcdef1234567890abcdef12    | 0x742d35Cc6634C0532925a3b844Bc59e7e...
```

---

## 🧪 API Testing with curl

### Test 1: Generate Follower Link

```bash
curl "http://localhost:8000/admin/follower-link?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE&source=twitter"
```

**Response:**
```json
{
  "success": true,
  "owner": "0x742d35cc6634c0532925a3b844bc59e7e6d6e0de",
  "source": "twitter",
  "follower_link": "http://localhost:8000/?owner=0x742d35cc6634c0532925a3b844bc59e7e6d6e0de&source=twitter",
  "instructions": { ... }
}
```

### Test 2: Get Followers Dashboard

```bash
curl "http://localhost:8000/admin/followers?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"
```

**Response:**
```json
{
  "success": true,
  "owner": "0x742d35cc6634c0532925a3b844bc59e7e6d6e0de",
  "total_followers": 1,
  "followers": [
    {
      "follower_address": "0x1234567890abcdef1234567890abcdef12345678",
      "resonance_score": 50,
      "verified_at": "2025-11-21T10:00:00",
      "source_platform": "twitter",
      "verified": true,
      "login_count": 0,
      "last_login": null
    }
  ],
  "statistics": {
    "average_score": 50.0,
    "verified_count": 1,
    "by_platform": {"twitter": 1}
  }
}
```

---

## 📱 Mobile Testing

### Dashboard on Mobile

```
Open on phone:
http://your-ngrok-url.ngrok-free.dev/dashboard

Should work:
✓ Enter wallet address
✓ View followers list
✓ Generate links
✓ Copy links (tap copy button)
```

### Verification on Mobile

```
Open on phone:
http://your-ngrok-url.ngrok-free.dev/?owner=0x...&source=twitter

Should work:
✓ See login page
✓ Connect MetaMask (mobile)
✓ Sign and verify
✓ Get score
```

---

## 🎯 Live Deployment (ngrok)

### 1. Get Public Tunnel

```bash
ngrok http 8000
```

Output:
```
Forwarding                    https://abc123def456.ngrok-free.dev -> http://localhost:8000
```

### 2. Share Dashboard Link

```
Your dashboard:
https://abc123def456.ngrok-free.dev/dashboard

Follower link example:
https://abc123def456.ngrok-free.dev/?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE&source=twitter
```

### 3. Test from Another Device

```
Open dashboard on phone/tablet:
https://abc123def456.ngrok-free.dev/dashboard

Enter wallet → Should work!
```

---

## ✅ Verification Checklist

Before declaring it "working":

- [ ] Server started without errors
- [ ] Dashboard loads at `/dashboard`
- [ ] Can enter wallet address
- [ ] Can generate follower link
- [ ] Follower link includes owner parameter
- [ ] Follower verification works
- [ ] Follower appears in dashboard
- [ ] Statistics update correctly
- [ ] API endpoints respond with data

---

## 🐛 Debug Mode

### Enable Verbose Logging

Add to server.py before starting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Database Changes

Monitor in real-time:

```bash
# Terminal 1: Watch database
watch -n 1 'sqlite3 aera.db "SELECT COUNT(*) as users, (SELECT COUNT(*) FROM followers) as followers FROM users;"'

# Terminal 2: Start server
python3 server.py

# Terminal 3: Test verifications
# Each follower registration should increase counts
```

---

## 📞 Getting Help

**Problem:**
- Dashboard blank → Check server logs
- Followers not appearing → Check ?owner parameter
- Database error → Restart server
- API 404 → Make sure endpoints are spelled correctly

**Solution:**
1. Restart server: `pkill -f server.py && python3 server.py`
2. Delete old database: `rm aera.db && python3 server.py`
3. Check logs: Look at terminal output
4. Test API: Use curl commands above

---

## 🎉 You're Ready!

```bash
# Start
python3 server.py &

# Test
curl http://localhost:8000/dashboard

# Share
ngrok http 8000
# → https://xxx.ngrok-free.dev/dashboard

# Done! 🚀
```

**Next:** Go to `/dashboard` and try it! 🎯
