# 👥 Owner-Follower System Documentation

**Feature:** Track verified followers and their Resonance Scores  
**Status:** ✅ Live & Production-Ready  
**Version:** v0.1

---

## 🎯 Overview

The Owner-Follower system allows account owners (from X, Discord, Telegram, etc.) to:

1. **Generate custom links** to share with their followers
2. **Track follower verification** - see who verified with their Resonance wallet
3. **View follower scores** - monitor community authenticity
4. **Analyze engagement** - by platform and time

---

## 🚀 Quick Start

### Step 1: Get Your Admin Dashboard Link

```
https://your-app.example.com/dashboard
```

### Step 2: Enter Your Wallet Address

```
Wallet Address: 0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE
```

### Step 3: Generate Follower Link

Select your platform (Twitter, Discord, etc.) and copy the link:

```
https://your-app.example.com/?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE&source=twitter
```

### Step 4: Share with Followers

Post the link on your social media account:

```
"Verify your humanity! Click the link below to get your Resonance Score:
[Link]
Only takes 30 seconds with your wallet!"
```

### Step 5: View Results

Go back to your dashboard - followers will appear in real-time!

---

## 🔌 API Endpoints

### 1. Generate Follower Link

```http
GET /admin/follower-link?owner=0x...&source=twitter
```

**Parameters:**
- `owner` (required) - Your wallet address (0x...)
- `source` (optional) - Platform: twitter, discord, telegram, facebook, reddit, direct

**Response:**
```json
{
  "success": true,
  "owner": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "source": "twitter",
  "follower_link": "https://app.example.com/?owner=0x742d...&source=twitter",
  "instructions": {
    "step1": "Share this link with your followers",
    "step2": "They click the link and verify with their wallet",
    "step3": "They appear in your dashboard",
    "step4": "Track their Resonance Score"
  }
}
```

### 2. Get Followers Dashboard Data

```http
GET /admin/followers?owner=0x...
```

**Parameters:**
- `owner` (required) - Your wallet address

**Response:**
```json
{
  "success": true,
  "owner": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "owner_score": 55,
  "total_followers": 42,
  "followers": [
    {
      "follower_address": "0x1234567890123456789012345678901234567890",
      "resonance_score": 51,
      "verified_at": "2025-11-21T10:00:00",
      "source_platform": "twitter",
      "verified": true,
      "login_count": 2,
      "last_login": 1700334120
    }
  ],
  "statistics": {
    "average_score": 65.5,
    "verified_count": 42,
    "by_platform": {
      "twitter": 15,
      "discord": 8,
      "direct": 19
    },
    "timestamp": 1700334000
  }
}
```

---

## 💾 Database Schema

### New Table: `followers`

Tracks the owner ↔ follower relationship:

```sql
CREATE TABLE followers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_wallet TEXT NOT NULL,
    follower_address TEXT NOT NULL,
    follower_score INTEGER,
    verified_at TEXT,
    source_platform TEXT,
    verified BOOLEAN DEFAULT 1,
    UNIQUE(owner_wallet, follower_address),
    FOREIGN KEY(owner_wallet) REFERENCES users(address),
    FOREIGN KEY(follower_address) REFERENCES users(address)
);
```

### Extended `users` Table

Added follower tracking:

```sql
ALTER TABLE users ADD COLUMN owner_wallet TEXT;
ALTER TABLE users ADD COLUMN is_verified_follower INTEGER DEFAULT 0;
```

### Extended `events` Table

Added owner tracking:

```sql
ALTER TABLE events ADD COLUMN owner_wallet TEXT;
```

---

## 🔐 How It Works

### Flow Diagram

```
Account Owner (e.g., Twitter)
        ↓
    [Generate Link]
    /dashboard?owner=0x...&source=twitter
        ↓
    [Share on Twitter]
    "Verify your humanity: https://..."
        ↓
    Follower clicks link
        ↓
    [Follower verifies wallet]
    MetaMask signature
        ↓
    [Backend creates user]
    - Sets owner_wallet = 0x...
    - Sets is_verified_follower = 1
    - Creates entry in followers table
        ↓
    [Owner sees in dashboard]
    /admin/followers?owner=0x...
        ↓
    Shows: "42 verified followers, avg score: 65.5"
```

### Data Flow (Backend)

```
POST /api/verify
{
  "address": "0xFollower...",
  "signature": "0x...",
  "owner": "0xOwner..."  ← NEW
}
        ↓
    Check signature
        ↓
    Create user (first time)
        ↓
    Set owner_wallet = "0xOwner..."
        ↓
    Insert into followers table:
    - owner_wallet: 0xOwner...
    - follower_address: 0xFollower...
    - follower_score: 50
    - verified_at: NOW()
    - source_platform: "twitter"
        ↓
    Return to client with message:
    "Registered as follower"
```

---

## 📊 Dashboard Features

### Live Dashboard UI

Access at: `https://your-app.example.com/dashboard`

**Features:**
- ✅ Enter wallet address and load followers
- ✅ View follower statistics (count, avg score)
- ✅ Generate custom links per platform
- ✅ Copy link to clipboard
- ✅ Live follower table with:
  - Wallet address (shortened)
  - Resonance score badge
  - Platform source
  - Verification date
  - Login count

### Example: Twitter Account Owner

```
Owner Wallet: 0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE

Stats:
  - 42 Verified Followers
  - Average Score: 65.5
  - Your Score: 55

Platform Distribution:
  - Twitter: 15 followers
  - Discord: 8 followers
  - Direct: 19 followers

Top Followers:
  0x1234...7890: Score 95 (verified Nov 21, 2 logins)
  0xabcd...ef12: Score 87 (verified Nov 21, 1 login)
  0x5678...9012: Score 72 (verified Nov 20, 3 logins)
```

---

## 🎛️ Configuration

### Environment Variables

Add to `.env`:

```bash
# Owner-Follower system
ENABLE_FOLLOWER_TRACKING=true  # Enable/disable feature
OWNER_DASHBOARD_URL=/dashboard  # Dashboard path
```

### Customization

**Change dashboard styling:**
Edit `dashboard.html` - currently uses purple gradient

**Add more platforms:**
Edit `index.html` and `dashboard.html` - add to platform selector

**Change platform icon/name:**
Edit `server.py` - `PLATFORM_CONFIG` dictionary

---

## 🔒 Security Considerations

### What's NOT Stored

- ❌ Personal information
- ❌ Passwords
- ❌ Email addresses
- ❌ Social media usernames
- ❌ Private keys

### What IS Stored

- ✅ Wallet addresses (public)
- ✅ Resonance scores (generated)
- ✅ Verification timestamps
- ✅ Platform source (public referrer)
- ✅ Login counts

### Authentication

- ✅ All actions verified via wallet signature (EIP-191)
- ✅ Nonce-based (prevents replay attacks)
- ✅ No credentials stored on server

---

## 📈 Use Cases

### 1. Social Media Influencer

**Goal:** Verify authentic followers, fight bots

```
Influencer posts on Twitter:
"Get verified! Click the link and prove you're human:
https://vera-app.com/?owner=0x1234...&source=twitter"

Results:
- 1,000 clicks
- 450 complete verification
- 89% have score >= 50
- Can see which followers are "most authentic"
```

### 2. DAO Community Manager

**Goal:** Track verified community members

```
Discord server:
- Post verification link in #verify channel
- 5,000 members join
- 2,100 verify with VEra
- Can see avg score by country/region via platform
```

### 3. Gaming Community

**Goal:** Anti-bot verification for tournaments

```
Esports team wants verified players:
"Only players with VEra score >= 80 can join tournament"

Team owner:
- Shares link: https://vera-app.com/?owner=0xTeam...&source=discord
- 150 players verify
- 120 meet threshold (score >= 80)
- 30 filtered as likely bots (score < 50)
```

### 4. Forum/Discussion Platform

**Goal:** Community trust & reputation

```
Forum user profiles show:
- ✓ Verified with VEra
- Score: 75/100
- 45 verified logins
- Joined: Nov 2025

Admin tools:
- View all members by score
- Flag accounts < 50 for moderation
```

---

## 🚀 Roadmap

### v0.2 (Next)
- [ ] Batch export followers to CSV
- [ ] Leaderboard (top followers by score)
- [ ] Email notifications on new follower
- [ ] Webhook for integrations

### v0.3
- [ ] Advanced analytics (score trends, engagement)
- [ ] Follower reputation badges
- [ ] Integration with Discord bot
- [ ] Telegram bot for verification

### v1.0
- [ ] On-chain score storage (NFT)
- [ ] Multi-wallet support (link sub-accounts)
- [ ] API rate limiting & quotas
- [ ] Admin moderation tools

---

## 📞 Support

**Questions?**

- 📖 Read API docs: `/README.md`
- 🐛 Report bugs: GitHub Issues
- 💬 Get help: Community Discord

**Example URL:**

```
Owner's Twitter:
@yourhandle: "Verify your humanity! https://vera-resonance.example.com/?owner=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE&source=twitter"

Follower clicks link:
→ Sees VEra-Resonance login page
→ Connects MetaMask wallet
→ Signs message (EIP-191)
→ Gets Resonance Score (50-100)
→ Registered as your follower

Check dashboard:
→ Go to /dashboard
→ Enter your wallet: 0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE
→ See: "42 followers, avg score: 65.5"
→ Table shows all verified followers with scores
```

---

## 🎯 Key Metrics

Tracked per owner:

| Metric | Description |
|--------|-------------|
| **Total Followers** | Count of verified followers |
| **Average Score** | Mean Resonance Score of followers |
| **Platform Distribution** | Followers by source (Twitter, Discord, etc.) |
| **Growth Rate** | New followers per day/week |
| **Authenticity %** | % of followers with score >= 50 |
| **Engagement** | Avg logins per follower |

---

**Version:** 0.1  
**Last Updated:** Nov 21, 2025  
**Status:** ✅ Production Ready
