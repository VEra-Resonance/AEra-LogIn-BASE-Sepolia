# 🔍 VEra-Resonance Server Extension: X Referrer Tracking

## ✅ Implemented

The server extension is now fully implemented and automatically tracks where users come from!

---

## 📊 What was added?

### **1. Extended Database Schema**

#### Users table (extended):
```sql
CREATE TABLE users (
    address TEXT PRIMARY KEY,
    first_seen INTEGER,
    last_login INTEGER,
    score INTEGER DEFAULT 50,
    login_count INTEGER DEFAULT 0,
    created_at TEXT,
    first_referrer TEXT,      -- NEW: First source
    last_referrer TEXT         -- NEW: Last source
);
```

#### Events table (extended):
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    address TEXT,
    event_type TEXT,
    score_before INTEGER,
    score_after INTEGER,
    timestamp INTEGER,
    created_at TEXT,
    referrer TEXT,             -- NEW: Source (twitter, telegram, etc.)
    user_agent TEXT,           -- NEW: Browser/device info
    ip_address TEXT            -- NEW: IP for sybil detection
);
```

---

## 🎯 Automatic Source Detection

### **Function: `extract_referrer_source()`**

Automatically detects source from HTTP referer header:

#### **Social Media:**
- `twitter.com`, `x.com`, `t.co` → `"twitter"`
- `t.me`, `telegram.me` → `"telegram"`
- `facebook.com`, `fb.com` → `"facebook"`
- `instagram.com` → `"instagram"`
- `reddit.com` → `"reddit"`
- `discord.gg` → `"discord"`
- `youtube.com`, `youtu.be` → `"youtube"`
- `linkedin.com` → `"linkedin"`
- `tiktok.com` → `"tiktok"`

#### **Search Engines:**
- `google.com` → `"google"`
- `bing.com` → `"bing"`
- `duckduckgo.com` → `"duckduckgo"`

#### **Web3:**
- `etherscan.io` → `"etherscan"`
- `opensea.io` → `"opensea"`

#### **Other:**
- No referer → `"direct"`
- Unknown source → `"other"`

---

## 🔄 Automatic Tracking

### **On every login/signup:**

```python
# Server automatically extracts:
referrer = req.headers.get("referer")           # HTTP header
user_agent = req.headers.get("user-agent")      # Browser info
client_ip = req.client.host                     # IP address
referrer_source = extract_referrer_source(referrer)  # e.g. "twitter"

# Stores in events:
INSERT INTO events (
    address, event_type, score_before, score_after,
    timestamp, created_at,
    referrer, user_agent, ip_address          -- NEW
) VALUES (...)

# On registration also in users:
INSERT INTO users (
    address, first_seen, last_login, score, login_count,
    created_at, first_referrer, last_referrer  -- NEW
) VALUES (...)
```

---

## 📡 New API Endpoints

### **1. `/api/referrer-stats` - Referrer Statistics**

```bash
curl https://[your-url]/api/referrer-stats
```

**Response:**
```json
{
  "new_users_by_source": [
    {"first_referrer": "twitter", "count": 127},
    {"first_referrer": "telegram", "count": 89},
    {"first_referrer": "direct", "count": 34}
  ],
  "total_events_by_source": [
    {"referrer": "twitter", "count": 452},
    {"referrer": "telegram", "count": 298},
    {"referrer": "direct", "count": 156}
  ],
  "top_sources_24h": [
    {"referrer": "twitter", "count": 45},
    {"referrer": "telegram", "count": 23}
  ],
  "timestamp": 1700000000
}
```

### **2. `/api/user/{address}` - Extended User Info**

Now with referrer data:

```bash
curl https://[your-url]/api/user/0xabc...xyz
```

**Response:**
```json
{
  "address": "0xabc...xyz",
  "resonance_score": 55,
  "first_seen": 1700000000,
  "last_login": 1700001000,
  "login_count": 5,
  "created_at": "2025-11-20T18:30:00",
  "first_referrer": "twitter",     // NEW
  "last_referrer": "telegram"      // NEW
}
```

### **3. `/api/events/{address}` - Extended Event Info**

Events now contain referrer data:

```json
{
  "address": "0xabc...xyz",
  "events": [
    {
      "id": 123,
      "address": "0xabc...xyz",
      "event_type": "login",
      "score_before": 54,
      "score_after": 55,
      "timestamp": 1700001000,
      "created_at": "2025-11-20T18:45:00",
      "referrer": "telegram",              // NEW
      "user_agent": "Mozilla/5.0...",      // NEW
      "ip_address": "192.168.1.100"        // NEW
    }
  ]
}
```

---

## 🎨 Using the Data

### **1. Identify X followers**

```sql
-- All users who came from X:
SELECT address, score, login_count
FROM users
WHERE first_referrer = 'twitter'
ORDER BY score DESC;
```

### **2. Find best traffic source**

```sql
-- Top traffic sources:
SELECT first_referrer, COUNT(*) as users, AVG(score) as avg_score
FROM users
GROUP BY first_referrer
ORDER BY users DESC;
```

### **3. Analyze user journey**

```sql
-- User who came from X but now from Telegram:
SELECT *
FROM users
WHERE first_referrer = 'twitter'
  AND last_referrer = 'telegram';
```

### **4. Conversion rate per source**

```sql
-- Signups vs. logins per source:
SELECT 
    referrer,
    SUM(CASE WHEN event_type='signup' THEN 1 ELSE 0 END) as signups,
    SUM(CASE WHEN event_type='login' THEN 1 ELSE 0 END) as logins
FROM events
GROUP BY referrer;
```

---

## 🔍 Dashboard Queries

### **For your follow management:**

```sql
-- Show all X users with score ≥50 verified today:
SELECT 
    u.address, 
    u.score, 
    u.login_count,
    e.timestamp
FROM users u
JOIN events e ON u.address = e.address
WHERE e.referrer = 'twitter'
  AND e.event_type = 'signup'
  AND e.timestamp > (unixepoch() - 86400)
  AND u.score >= 50
ORDER BY e.timestamp DESC;
```

### **Traffic analysis:**

```sql
-- Hourly traffic distribution from X:
SELECT 
    strftime('%H:00', datetime(timestamp, 'unixepoch')) as hour,
    COUNT(*) as visits
FROM events
WHERE referrer = 'twitter'
  AND timestamp > (unixepoch() - 86400)
GROUP BY hour
ORDER BY hour;
```

---

## 🚀 Advanced Features (possible)

### **1. UTM parameter tracking**

Extend URL in your X bio:
```
https://[your-url]?utm_source=twitter&utm_campaign=bio&utm_medium=social
```

Then extract in server:
```python
utm_source = request.query_params.get("utm_source")
utm_campaign = request.query_params.get("utm_campaign")
# Store in events
```

### **2. Bonus score for X referrals**

```python
if referrer_source == "twitter":
    initial_score = 55  # +5 bonus
    message = "Welcome from X! Bonus score: +5"
```

### **3. Source-specific landing pages**

```python
if referrer_source == "twitter":
    return FileResponse("index-x.html")
elif referrer_source == "telegram":
    return FileResponse("index-telegram.html")
```

### **4. Anti-sybil via IP clustering**

```sql
-- Find suspicious wallets (multiple from same IP):
SELECT ip_address, COUNT(DISTINCT address) as wallet_count
FROM events
WHERE timestamp > (unixepoch() - 3600)
GROUP BY ip_address
HAVING wallet_count > 5;
```

---

## 🔧 Migration for existing DB

If your database already has users, run:

```sql
-- Add new columns (if not already present):
ALTER TABLE users ADD COLUMN first_referrer TEXT;
ALTER TABLE users ADD COLUMN last_referrer TEXT;

ALTER TABLE events ADD COLUMN referrer TEXT;
ALTER TABLE events ADD COLUMN user_agent TEXT;
ALTER TABLE events ADD COLUMN ip_address TEXT;

-- Set default values for existing users:
UPDATE users SET first_referrer = 'unknown' WHERE first_referrer IS NULL;
UPDATE users SET last_referrer = 'unknown' WHERE last_referrer IS NULL;
```

**Note:** On next server restart, `init_db()` will automatically create new columns (if not already present).

---

## 📊 Example Report

### **After 1 week with X bio link:**

```
Total Users: 234
├─ Twitter: 187 (80%)
├─ Direct: 23 (10%)
├─ Telegram: 15 (6%)
└─ Other: 9 (4%)

Average Score by Source:
├─ Twitter: 58.3
├─ Telegram: 62.1
└─ Direct: 51.2

Conversion Rate:
├─ Twitter → Follow Request: 73%
├─ Telegram → Follow Request: 89%
└─ Direct → Follow Request: 45%
```

**Insight:** Telegram users have higher score and better conversion!

---

## ✅ Testing

### **Test 1: Coming from X**

```bash
curl -X POST https://[your-url]/api/verify \
  -H "Content-Type: application/json" \
  -H "Referer: https://twitter.com/your-profile" \
  -d '{
    "address": "0xtest123...",
    "nonce": "abc123",
    "signature": "0xsig..."
  }'
```

**Expected DB entries:**
- `users.first_referrer = "twitter"`
- `events.referrer = "twitter"`

### **Test 2: Direct access**

```bash
curl -X POST https://[your-url]/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xtest456...",
    "nonce": "def456",
    "signature": "0xsig2..."
  }'
```

**Expected DB entries:**
- `users.first_referrer = "direct"`
- `events.referrer = "direct"`

---

## 🎯 Next Steps

1. ✅ **Restart server** (to create new DB columns)
2. ✅ **Test first verification** (check referrer in DB)
3. ✅ **Get statistics** (`/api/referrer-stats`)
4. ✅ **Build dashboard** (optional)

---

## 📝 Logging

All referrer activities are logged:

```
[INFO] AUTH: Verify request received | address=0xabc...xyz | referrer_source=twitter
[INFO] AUTH: New user registered | address=0xabc...xyz | referrer=twitter
[INFO] AUTH: Existing user login | address=0xdef...uvw | referrer=telegram
```

---

**🚀 Server extension complete! Now you'll always know where your users come from!**

*Built for VEra-Resonance - Tracking for authentic communities*
