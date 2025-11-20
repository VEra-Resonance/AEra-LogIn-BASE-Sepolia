# 🌐 AEra-Gate Multi-Platform Integration Guide

## Komplette Anleitung für ALLE Social Media Plattformen

---

## 🎯 Universal Setup (gilt für alle Plattformen)

### **Schritt 1: Server bereit machen**
```bash
# Server läuft auf Port 8820
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
python3 server.py

# ngrok Tunnel (bereits aktiv)
# URL: https://ronna-unmagnetised-unaffrightedly.ngrok-free.dev
```

### **Schritt 2: Verification Link**
```
Ihre Universal-URL:
https://ronna-unmagnetised-unaffrightedly.ngrok-free.dev
```

**Mit Tracking:**
```
https://[ihre-url]?source=[platform]

Beispiele:
- twitter:   ?source=twitter
- telegram:  ?source=telegram
- discord:   ?source=discord
- instagram: ?source=instagram
```

---

## 📱 Plattform-spezifische Anleitungen

---

# 𝕏 X / Twitter

## Setup (5 Minuten)

### **1. Account auf privat**
```
Settings → Privacy and safety → Audience → ✅ Protect your posts
```

### **2. Bio aktualisieren**
```
🔒 Protected Account - Real Humans Only

Want to follow? Prove you're human:
👉 https://[ihre-url]?source=twitter

✓ No bots | ✓ No spam
#ProofOfHuman
```

### **3. Pinned Tweet**
```
🔐 How to follow this account:

1. Click link in bio
2. Connect wallet
3. Sign message (free!)
4. Get Score ≥50
5. Send follow request
6. I approve within 24h

Only real humans allowed! 🤝
```

### **4. Follow-Request-Management**
```
User sendet Follow-Request
   ↓
Sie öffnen: https://[ihre-url]/api/user/[wallet-address]
   ↓
Score ≥50? → Accept
Score <50? → Decline
```

**Workflow:** Siehe `X-INTEGRATION-GUIDE.md` für Details

---

# 📱 Telegram

## Setup (10 Minuten)

### **1. Private Group erstellen**
```
1. Telegram öffnen
2. Neuer Chat → Neue Gruppe
3. Name & Teilnehmer hinzufügen
4. Gruppen-Info → Gruppentyp → "Private Gruppe"
```

### **2. Group Description**
```
🔒 Verified Humans Only

Join: https://[ihre-url]?source=telegram

✅ No bots | ✅ Score ≥50 required
Powered by AEra-Gate
```

### **3. Welcome Message (via Bot oder Pinned)**
```
Welcome to [Group Name]! 🎉

This group is BOT-FREE.

To join:
1. Visit: [verification-link]
2. Verify with wallet
3. Get Score ≥50
4. Request invite below
5. Admin approves you

Type /verify to get link
```

### **4. Member Approval Workflow**

#### **Manual:**
```
1. User schickt PM mit Wallet-Address
2. Sie prüfen: https://[ihre-url]/api/user/[address]
3. Score ≥50? → Invite Link senden
```

#### **Mit Bot (Optional):**
```python
# Telegram Bot Code (Python)
@bot.command('/verify')
async def verify_command(ctx):
    await ctx.send(f"Verify here: {VERIFICATION_URL}?source=telegram")

@bot.command('/request')
async def request_invite(ctx, wallet_address):
    # Check AEra API
    response = requests.get(f"{API_URL}/api/user/{wallet_address}")
    data = response.json()
    
    if data['resonance_score'] >= 50:
        invite_link = await ctx.channel.create_invite(max_uses=1)
        await ctx.send(f"✅ Verified! Join: {invite_link}")
    else:
        await ctx.send(f"❌ Score too low: {data['resonance_score']}/100")
```

---

# 💬 Discord

## Setup (15 Minuten)

### **1. Server auf Invite-Only**
```
Server Settings
  → Moderation
  → Verification Level: High
  → Remove all public invite links
```

### **2. Server Description**
```
🔐 Human-Verified Server

Join: https://[ihre-url]?source=discord

How:
1. Verify your humanity
2. Get Score ≥50
3. Receive invite link
4. Welcome!

No bots allowed.
```

### **3. Welcome Channel**
```
# 🚪 welcome

Welcome to [Server Name]!

You're here because you're **verified human**! 🎉

## Your Resonance Score
Check your score: https://[ihre-url]/api/user/[your-wallet]

## Server Rules
1. Be respectful
2. No spam (seriously, you're human!)
3. Enjoy bot-free conversations

Questions? Ask @Admin
```

### **4. Verification Channel (Optional)**
```
# 🔐 verification

## Want to join this server?

**Step 1:** Verify your humanity
👉 https://[ihre-url]?source=discord

**Step 2:** DM an admin with your wallet address
Format: `!verify 0xYourWalletAddress`

**Step 3:** Admin checks score & sends invite

**Requirements:**
✅ Resonance Score ≥50
✅ Accept server rules
```

### **5. Discord Bot für Auto-Invite**

```python
# Discord Bot (Python with discord.py)
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix='!')

AERA_API = "https://your-url"
MIN_SCORE = 50

@bot.command()
async def verify(ctx, wallet_address: str):
    """Check if user is verified and send invite"""
    
    # Check AEra API
    try:
        response = requests.get(f"{AERA_API}/api/user/{wallet_address}")
        data = response.json()
        
        score = data.get('resonance_score', 0)
        
        if score >= MIN_SCORE:
            # Create invite link
            invite = await ctx.channel.create_invite(
                max_uses=1,
                max_age=3600,  # 1 hour
                unique=True
            )
            
            await ctx.author.send(
                f"✅ Verified! Your score: {score}/100\n"
                f"Join the server: {invite.url}\n"
                f"This link expires in 1 hour."
            )
            
            await ctx.send(f"✅ Invite sent to {ctx.author.mention}")
            
        else:
            await ctx.send(
                f"❌ Score too low: {score}/100 (need ≥{MIN_SCORE})\n"
                f"Try again after more logins!"
            )
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

bot.run('YOUR_BOT_TOKEN')
```

---

# 📷 Instagram

## Setup (5 Minuten)

### **1. Private Account**
```
Settings → Privacy → Private Account ✅
```

### **2. Bio**
```
🔒 Humans Only | Verify ↓
```

### **3. Link in Bio**
```
Linktree/Beacons mit:
🔐 Verify to Follow
→ https://[ihre-url]?source=instagram
```

### **4. Story Highlights "How to Follow"**

**Slide 1:**
```
🔐 This account is protected

Bot-free zone!
```

**Slide 2:**
```
How to follow:

1. Tap link in bio
2. Connect wallet
3. Verify (30 sec)
4. Send follow request
```

**Slide 3:**
```
Why verify?

✅ No bots
✅ No fake followers
✅ Real engagement only
```

**Slide 4:**
```
Questions?

DM me after verifying!
```

### **5. Follow-Request Approval**
```
1. User sendet Follow-Request
2. Sie erhalten Notification
3. Prüfen: https://[ihre-url]/api/user/[wallet]
4. Score ≥50? → Accept
```

---

# 👔 LinkedIn

## Setup (10 Minuten)

### **1. Private Group erstellen**
```
LinkedIn → Groups → Create Group
→ "Members must be approved by an admin" ✅
```

### **2. Group Description**
```
🏢 Professional Network | Human-Verified

Join: https://[ihre-url]?source=linkedin

Requirements:
✅ Wallet verification
✅ Score ≥50
✅ Professional conduct

Quality > Quantity
```

### **3. Pinned Post**
```
👋 Welcome to [Group Name]

This is a HUMAN-VERIFIED professional group.

To join:
1. Visit link in group description
2. Verify with wallet (safe, no personal data)
3. Get Score ≥50
4. Request membership
5. Admin approval within 48h

Why? Because professionals deserve spam-free networking.

Questions? Message admin.
```

### **4. Approval Workflow**
```
1. User requests membership
2. LinkedIn notifies you
3. Check user's wallet score
4. Approve if ≥50
```

---

# 🔴 YouTube

## Setup (10 Minuten)

### **1. Channel Description**
```
🎥 Human-Verified Channel

Comment/Member verification:
👉 https://[ihre-url]?source=youtube

✅ No spam comments
✅ Real viewers only

#ProofOfHuman
```

### **2. Community Post**
```
🔐 NEW: Comment Verification!

To comment or become a member:
1. Visit: [link]
2. Verify humanity
3. Get Score ≥50
4. Comment freely!

Why? 90% of YouTube comments are bots.
This channel is different. Real people only.

Already verified? You're good! ✅
```

### **3. Pinned Comment (on every video)**
```
🔒 Verified humans only!

Want to comment? Verify here: [link]

This channel uses AEra-Gate to keep discussions authentic.
No bots. No spam. Real viewers.

Questions? Read pinned community post.
```

### **4. Comment Moderation**
```
YouTube Studio → Comments → Hold for review
   ↓
New comment appears
   ↓
Check commenter's wallet: /api/user/[address]
   ↓
Score ≥50? → Approve
Score <50? → Hold/Delete
```

---

# 🎵 TikTok

## Setup (5 Minuten)

### **1. Private Account**
```
Settings → Privacy → Private Account ✅
```

### **2. Bio**
```
🔒 Real humans only
Verify ↓ [Link in Bio]
#ProofOfHuman
```

### **3. Link in Bio**
```
Linktree mit:
🔐 Verify to Follow
→ https://[ihre-url]?source=tiktok
```

### **4. Pinned Video**

**Script:**
```
"Why is my TikTok private? 🤔

Simple: I only want REAL followers.

Here's how to follow:
1. Click link in bio
2. Prove you're human (30 sec)
3. Send follow request
4. I approve you!

No bots. No fakes. Just real people. 🤝

Link in bio! 👆"
```

---

# 📰 Reddit

## Setup (10 Minuten)

### **1. Private Subreddit erstellen**
```
Create Community
→ Community type: Private ✅
```

### **2. Description & Sidebar**
```
🔒 r/YourSubreddit - Human-Verified

Join: https://[ihre-url]?source=reddit

Requirements:
✅ Wallet verification
✅ Score ≥50
✅ Follow rules

No bots. Quality discussions.
```

**Sidebar:**
```
# How to Join

1. Visit verification link
2. Connect wallet & sign
3. Get Score ≥50
4. Message mods with wallet address
5. Approval within 24h

# Why Human Verification?

- No bot accounts
- No vote manipulation
- Quality over quantity

# Rules

1. Be respectful
2. No spam
3. Contribute meaningfully
```

### **3. Moderator Note**
```
When user requests to join:
1. User sends modmail with wallet address
2. Check: /api/user/[address]
3. Score ≥50? → Approve
4. Welcome message: "You're in! Your score: X/100"
```

---

# 📘 Facebook

## Setup (10 Minuten)

### **1. Private Group erstellen**
```
Facebook → Groups → Create Group
→ Privacy: Private ✅
→ Membership approval required ✅
```

### **2. Group Description**
```
🔒 Human-Verified Community

Join: https://[ihre-url]?source=facebook

✅ No bots
✅ No fake accounts
✅ Real conversations

Score ≥50 required
```

### **3. Pinned Post**
```
🛡️ Welcome to [Group Name]!

HOW TO JOIN:
1. Click link in group description
2. Connect wallet & sign (free, safe)
3. Get Resonance Score
4. Request membership
5. Admin approval

WHY?
No bots. No spam. Quality community.

QUESTIONS?
Message admins.

---
Powered by AEra-Gate
```

### **4. Approval Workflow**
```
User requests to join
   ↓
Facebook notifies you
   ↓
Ask user for wallet address (via PM or screening questions)
   ↓
Check: /api/user/[address]
   ↓
Score ≥50? → Approve
```

---

## 🔧 Advanced: Cross-Platform Bot/Integration

### **Universal API Check Function**

```python
import requests

AERA_API = "https://your-url"
MIN_SCORE = 50

def check_user_verified(wallet_address, platform="unknown"):
    """
    Universal function to check if user is verified
    Works for ALL platforms
    """
    try:
        response = requests.get(
            f"{AERA_API}/api/user/{wallet_address}",
            headers={"User-Agent": f"AEra-Bot/{platform}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            score = data.get('resonance_score', 0)
            
            return {
                "verified": score >= MIN_SCORE,
                "score": score,
                "login_count": data.get('login_count', 0),
                "first_referrer": data.get('first_referrer', 'unknown')
            }
        else:
            return {"verified": False, "error": "User not found"}
            
    except Exception as e:
        return {"verified": False, "error": str(e)}

# Usage:
result = check_user_verified("0xabc...xyz", platform="telegram")
if result["verified"]:
    print(f"✅ User verified! Score: {result['score']}")
else:
    print(f"❌ Not verified: {result.get('error')}")
```

---

## 📊 Multi-Platform Dashboard (Concept)

```
User: 0xabc...xyz

Verified on:
✅ X/Twitter (first seen: 2025-11-20)
✅ Telegram (joined: 2025-11-21)
✅ Discord (joined: 2025-11-22)
⏳ Instagram (pending)
❌ LinkedIn (not verified)

Resonance Score: 62/100
Total Logins: 12
Active Platforms: 3

Recommendation: APPROVE for all platforms
```

---

## ✅ Universal Checklist

### **Per Platform:**
- [ ] Account/Group auf privat
- [ ] AEra-Link hinzufügen (mit ?source= parameter)
- [ ] Welcome/Info Post erstellen
- [ ] Approval-Workflow definieren
- [ ] Test mit eigenem Account
- [ ] Erste 10 User manuell prüfen
- [ ] Optional: Bot für Automatisierung

### **Tracking:**
- [ ] Referrer-Stats prüfen: `/api/referrer-stats`
- [ ] Beste Plattform identifizieren
- [ ] Conversion-Raten messen
- [ ] Cross-Platform-User identifizieren

---

## 🎯 Pro-Tipps

### **1. Plattform-Priorität**
Starten Sie mit den Plattformen, wo Sie bereits Audience haben:
1. X/Twitter (einfachster Start)
2. Telegram (tech-savvy Audience)
3. Discord (Gaming/Web3)
4. Instagram (Creator)
5. LinkedIn (Professional)

### **2. Cross-Promotion**
```
"Verified on X/Twitter? You're already verified for:
- Telegram Group
- Discord Server
- Instagram Account

Same wallet, instant access everywhere!"
```

### **3. Score-Boost für Multi-Platform**
```python
# In server.py - bonus for cross-platform users
platforms_used = len(set([event['referrer'] for event in user_events]))
if platforms_used >= 3:
    bonus_score = 5
    new_score += bonus_score
```

---

## 🚀 Next Steps

1. **Wählen Sie 2-3 Haupt-Plattformen**
2. **Setup parallel durchführen**
3. **Cross-promote zwischen Plattformen**
4. **Messen & optimieren**

---

**🌐 AEra-Gate: Ein Gate, alle Plattformen!**

*Version 1.0 | 20. November 2025*
