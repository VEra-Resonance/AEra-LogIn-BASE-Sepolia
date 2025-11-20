# 🔍 AEra-Gate Server-Erweiterung: X-Referrer-Tracking

## ✅ Implementiert

Die Server-Erweiterung ist jetzt vollständig implementiert und trackt automatisch, von wo User kommen!

---

## 📊 Was wurde hinzugefügt?

### **1. Erweiterte Datenbank-Schema**

#### Users-Tabelle (erweitert):
```sql
CREATE TABLE users (
    address TEXT PRIMARY KEY,
    first_seen INTEGER,
    last_login INTEGER,
    score INTEGER DEFAULT 50,
    login_count INTEGER DEFAULT 0,
    created_at TEXT,
    first_referrer TEXT,      -- NEU: Erste Quelle
    last_referrer TEXT         -- NEU: Letzte Quelle
);
```

#### Events-Tabelle (erweitert):
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    address TEXT,
    event_type TEXT,
    score_before INTEGER,
    score_after INTEGER,
    timestamp INTEGER,
    created_at TEXT,
    referrer TEXT,             -- NEU: Quelle (twitter, telegram, etc.)
    user_agent TEXT,           -- NEU: Browser/Device-Info
    ip_address TEXT            -- NEU: IP für Sybil-Detection
);
```

---

## 🎯 Automatische Quellen-Erkennung

### **Funktion: `extract_referrer_source()`**

Erkennt automatisch die Quelle aus dem HTTP-Referer-Header:

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

#### **Suchmaschinen:**
- `google.com` → `"google"`
- `bing.com` → `"bing"`
- `duckduckgo.com` → `"duckduckgo"`

#### **Web3:**
- `etherscan.io` → `"etherscan"`
- `opensea.io` → `"opensea"`

#### **Sonstiges:**
- Kein Referer → `"direct"`
- Unbekannte Quelle → `"other"`

---

## 🔄 Automatisches Tracking

### **Bei jedem Login/Signup:**

```python
# Server extrahiert automatisch:
referrer = req.headers.get("referer")           # HTTP-Header
user_agent = req.headers.get("user-agent")      # Browser-Info
client_ip = req.client.host                     # IP-Adresse
referrer_source = extract_referrer_source(referrer)  # z.B. "twitter"

# Speichert in Events:
INSERT INTO events (
    address, event_type, score_before, score_after,
    timestamp, created_at,
    referrer, user_agent, ip_address          -- NEU
) VALUES (...)

# Bei Neu-Registrierung auch in Users:
INSERT INTO users (
    address, first_seen, last_login, score, login_count,
    created_at, first_referrer, last_referrer  -- NEU
) VALUES (...)
```

---

## 📡 Neue API-Endpoints

### **1. `/api/referrer-stats` - Referrer-Statistiken**

```bash
curl https://[ihre-url]/api/referrer-stats
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

### **2. `/api/user/{address}` - Erweiterte User-Info**

Jetzt mit Referrer-Daten:

```bash
curl https://[ihre-url]/api/user/0xabc...xyz
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
  "first_referrer": "twitter",     // NEU
  "last_referrer": "telegram"      // NEU
}
```

### **3. `/api/events/{address}` - Erweiterte Event-Info**

Events enthalten jetzt Referrer-Daten:

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
      "referrer": "telegram",              // NEU
      "user_agent": "Mozilla/5.0...",      // NEU
      "ip_address": "192.168.1.100"        // NEU
    }
  ]
}
```

---

## 🎨 Verwendung der Daten

### **1. X-Follower identifizieren**

```sql
-- Alle User die von X kamen:
SELECT address, score, login_count
FROM users
WHERE first_referrer = 'twitter'
ORDER BY score DESC;
```

### **2. Beste Traffic-Quelle finden**

```sql
-- Top Traffic-Quellen:
SELECT first_referrer, COUNT(*) as users, AVG(score) as avg_score
FROM users
GROUP BY first_referrer
ORDER BY users DESC;
```

### **3. User-Journey analysieren**

```sql
-- User der von X kam, aber jetzt von Telegram kommt:
SELECT *
FROM users
WHERE first_referrer = 'twitter'
  AND last_referrer = 'telegram';
```

### **4. Conversion-Rate per Quelle**

```sql
-- Signups vs. Logins per Quelle:
SELECT 
    referrer,
    SUM(CASE WHEN event_type='signup' THEN 1 ELSE 0 END) as signups,
    SUM(CASE WHEN event_type='login' THEN 1 ELSE 0 END) as logins
FROM events
GROUP BY referrer;
```

---

## 🔍 Dashboard-Queries

### **Für Ihr Follow-Management:**

```sql
-- Zeige alle X-User mit Score ≥50 die heute verifiziert wurden:
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

### **Traffic-Analyse:**

```sql
-- Stündliche Traffic-Verteilung von X:
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

## 🚀 Erweiterte Features (möglich)

### **1. UTM-Parameter-Tracking**

Erweitern Sie die URL in Ihrer X-Bio:
```
https://[ihre-url]?utm_source=twitter&utm_campaign=bio&utm_medium=social
```

Dann im Server extrahieren:
```python
utm_source = request.query_params.get("utm_source")
utm_campaign = request.query_params.get("utm_campaign")
# Speichern in Events
```

### **2. Bonus-Score für X-Referrals**

```python
if referrer_source == "twitter":
    initial_score = 55  # +5 Bonus
    message = "Welcome from X! Bonus score: +5"
```

### **3. Source-Specific Landing Pages**

```python
if referrer_source == "twitter":
    return FileResponse("index-x.html")
elif referrer_source == "telegram":
    return FileResponse("index-telegram.html")
```

### **4. Anti-Sybil via IP-Clustering**

```sql
-- Finde verdächtige Wallets (mehrere von gleicher IP):
SELECT ip_address, COUNT(DISTINCT address) as wallet_count
FROM events
WHERE timestamp > (unixepoch() - 3600)
GROUP BY ip_address
HAVING wallet_count > 5;
```

---

## 🔧 Migration für bestehende DB

Falls Ihre Datenbank bereits User hat, führen Sie aus:

```sql
-- Füge neue Spalten hinzu (falls noch nicht vorhanden):
ALTER TABLE users ADD COLUMN first_referrer TEXT;
ALTER TABLE users ADD COLUMN last_referrer TEXT;

ALTER TABLE events ADD COLUMN referrer TEXT;
ALTER TABLE events ADD COLUMN user_agent TEXT;
ALTER TABLE events ADD COLUMN ip_address TEXT;

-- Setze Default-Werte für bestehende User:
UPDATE users SET first_referrer = 'unknown' WHERE first_referrer IS NULL;
UPDATE users SET last_referrer = 'unknown' WHERE last_referrer IS NULL;
```

**Hinweis:** Beim nächsten Server-Start wird `init_db()` automatisch die neuen Spalten erstellen (falls noch nicht vorhanden).

---

## 📊 Beispiel-Auswertung

### **Nach 1 Woche mit X-Bio-Link:**

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

**Insight:** Telegram-User haben höheren Score und bessere Conversion!

---

## ✅ Testing

### **Test 1: Von X kommend**

```bash
curl -X POST https://[ihre-url]/api/verify \
  -H "Content-Type: application/json" \
  -H "Referer: https://twitter.com/your-profile" \
  -d '{
    "address": "0xtest123...",
    "nonce": "abc123",
    "signature": "0xsig..."
  }'
```

**Erwartete DB-Einträge:**
- `users.first_referrer = "twitter"`
- `events.referrer = "twitter"`

### **Test 2: Direkter Zugriff**

```bash
curl -X POST https://[ihre-url]/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xtest456...",
    "nonce": "def456",
    "signature": "0xsig2..."
  }'
```

**Erwartete DB-Einträge:**
- `users.first_referrer = "direct"`
- `events.referrer = "direct"`

---

## 🎯 Nächste Schritte

1. ✅ **Server neu starten** (um neue DB-Spalten zu erstellen)
2. ✅ **Erste Verifikation testen** (prüfe Referrer in DB)
3. ✅ **Statistiken abrufen** (`/api/referrer-stats`)
4. ✅ **Dashboard bauen** (optional)

---

## 📝 Logging

Alle Referrer-Aktivitäten werden geloggt:

```
[INFO] AUTH: Verify request received | address=0xabc...xyz | referrer_source=twitter
[INFO] AUTH: New user registered | address=0xabc...xyz | referrer=twitter
[INFO] AUTH: Existing user login | address=0xdef...uvw | referrer=telegram
```

---

**🚀 Server-Erweiterung komplett! Jetzt wissen Sie immer, woher Ihre User kommen!**

*Erstellt für AEra-Gate - Tracking für authentische Communities*
