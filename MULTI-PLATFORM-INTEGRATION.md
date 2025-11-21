# 🌐 VEra-Resonance Multi-Platform Integration Guide

## Complete Guide for ALL Social Media Platforms

---

## 🎯 Universal Setup (applies to all platforms)

### **Step 1: Prepare server**
```bash
# Server runs on port 8820
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
python3 server.py

# ngrok tunnel (already active)
# URL: https://ronna-unmagnetised-unaffrightedly.ngrok-free.dev
```

### **Step 2: Verification link**
```
Your Universal URL:
https://ronna-unmagnetised-unaffrightedly.ngrok-free.dev
```

**With tracking:**
```
https://[your-url]?source=[platform]

Examples:
- twitter:   ?source=twitter
- telegram:  ?source=telegram
- discord:   ?source=discord
- instagram: ?source=instagram
```

---

## 📱 Platform-specific guides

---

# 𝕏 X / Twitter

## Setup (5 minutes)

### **1. Set account to private**
```
Settings → Privacy and safety → Audience → ✅ Protect your posts
```

### **2. Update bio**
```
🔒 Protected Account - Real Humans Only

Want to follow? Prove you're human:
👉 https://[your-url]?source=twitter

✓ No bots | ✓ No spam
#ProofOfHuman
```

### **3. Pinned tweet**
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

### **4. Follow-request management**
```
User sends follow request
   ↓
You open: https://[your-url]/api/user/[wallet-address]
   ↓
Score ≥50? → Accept
Score <50? → Decline
```

**Workflow:** See `X-INTEGRATION-GUIDE.md` for details

---

# 📱 Telegram

## Setup (10 minutes)

### **1. Create private group**
```
1. Open Telegram
2. New Chat → New Group
3. Name & add members
4. Group Info → Group type → "Private Group"
```

### **2. Group description**
```
🔒 Verified Humans Only

Join: https://[your-url]?source=telegram

✅ No bots | ✅ Score ≥50 required
Powered by VEra-Resonance
```

### **3. Welcome message (via bot or pinned)**
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

### **4. Member approval workflow**

#### **Manual:**
```
1. User sends PM with wallet address
2. You check: https://[your-url]/api/user/[address]
3. Score ≥50? → Send invite link
```

#### **With bot (optional):**
```python
# Telegram Bot Code (Python)
@bot.command('/verify')
async def verify_command(ctx):
    await ctx.send(f"Verify here: {VERIFICATION_URL}?source=telegram")

@bot.command('/request')
async def request_invite(ctx, wallet_address):
    # Check VEra API
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

## Setup (15 minutes)

### **1. Set server to invite-only**
```
Server Settings
  → Moderation
  → Verification Level: High
  → Remove all public invite links
```

### **2. Server description**
```
🔐 Human-Verified Server

Join: https://[your-url]?source=discord

How:
1. Verify your humanity
2. Get Score ≥50
3. Receive invite link
4. Welcome!

No bots allowed.
```

### **3. Welcome channel**
```
# 🚪 welcome

Welcome to [Server Name]!

You're here because you're **verified human**! 🎉

## Your Resonance Score
Check your score: https://[your-url]/api/user/[your-wallet]

## Server Rules
1. Be respectful
2. No spam (seriously, you're human!)
3. Enjoy bot-free conversations

Questions? Ask @Admin
```

### **4. Verification channel (optional)**
```
# 🔐 verification

## Want to join this server?

**Step 1:** Verify your humanity
👉 https://[your-url]?source=discord

**Step 2:** DM an admin with your wallet address
Format: `!verify 0xYourWalletAddress`

**Step 3:** Admin checks score & sends invite

**Requirements:**
✅ Resonance Score ≥50
✅ Accept server rules
```

### **5. Discord bot for auto-invite**

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
    
    # Check VEra API
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

## Setup (5 minutes)

### **1. Private account**
```
Settings → Privacy → Private Account ✅
```

### **2. Bio**
```
🔒 Humans Only | Verify ↓
```

### **3. Link in bio**
```
Linktree/Beacons with:
🔐 Verify to Follow
→ https://[your-url]?source=instagram
```

### **4. Story highlights "How to follow"**

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

### **5. Follow-request approval**
```
1. User sends follow request
2. You receive notification
3. Check: https://[your-url]/api/user/[wallet]
4. Score ≥50? → Accept
```

---

# 👔 LinkedIn

## Setup (10 minutes)

### **1. Create private group**
```
LinkedIn → Groups → Create Group
→ "Members must be approved by an admin" ✅
```

### **2. Group description**
```
🏢 Professional Network | Human-Verified

Join: https://[your-url]?source=linkedin

Requirements:
✅ Wallet verification
✅ Score ≥50
✅ Professional conduct

Quality > Quantity
```

### **3. Pinned post**
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

### **4. Approval workflow**
```
1. User requests membership
2. LinkedIn notifies you
3. Check user's wallet score
4. Approve if ≥50
```

---

# 🔴 YouTube

## Setup (10 minutes)

### **1. Channel description**
```
🎥 Human-Verified Channel

Comment/Member verification:
👉 https://[your-url]?source=youtube

✅ No spam comments
✅ Real viewers only

#ProofOfHuman
```

### **2. Community post**
```
🔐 NEW: Comment verification!

To comment or become a member:
1. Visit: [link]
2. Verify humanity
3. Get Score ≥50
4. Comment freely!

Why? 90% of YouTube comments are bots.
This channel is different. Real people only.

Already verified? You're good! ✅
```

### **3. Pinned comment (on every video)**
```
🔒 Verified humans only!

Want to comment? Verify here: [link]

This channel uses VEra-Resonance to keep discussions authentic.
No bots. No spam. Real viewers.

Questions? Read pinned community post.
```

### **4. Comment moderation**
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

## Setup (5 minutes)

### **1. Private account**
```
Settings → Privacy → Private Account ✅
```

### **2. Bio**
```
🔒 Real humans only
Verify ↓ [Link in Bio]
#ProofOfHuman
```

### **3. Link in bio**
```
Linktree with:
🔐 Verify to Follow
→ https://[your-url]?source=tiktok
```

### **4. Pinned video**

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

## Setup (10 minutes)

### **1. Create private subreddit**
```
Create Community
→ Community type: Private ✅
```

### **2. Description & sidebar**
```
🔒 r/YourSubreddit - Human-Verified

Join: https://[your-url]?source=reddit

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

# Why human verification?

- No bot accounts
- No vote manipulation
- Quality over quantity

# Rules

1. Be respectful
2. No spam
3. Contribute meaningfully
```

### **3. Moderator note**
```
When user requests to join:
1. User sends modmail with wallet address
2. Check: /api/user/[address]
3. Score ≥50? → Approve
4. Welcome message: "You're in! Your score: X/100"
```

---

# 📘 Facebook

## Setup (10 minutes)

### **1. Create private group**
```
Facebook → Groups → Create Group
→ Privacy: Private ✅
→ Membership approval required ✅
```

### **2. Group description**
```
🔒 Human-Verified Community

Join: https://[your-url]?source=facebook

✅ No bots
✅ No fake accounts
✅ Real conversations

Score ≥50 required
```

### **3. Pinned post**
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
Powered by VEra-Resonance
```

### **4. Approval workflow**
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

### **Universal API check function**

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
            headers={"User-Agent": f"VEra-Bot/{platform}"}
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

## 📊 Multi-Platform Dashboard (concept)

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

## ✅ Universal checklist

### **Per platform:**
- [ ] Account/Group set to private
- [ ] Add VEra-Resonance link (with ?source= parameter)
- [ ] Create welcome/info post
- [ ] Define approval workflow
- [ ] Test with own account
- [ ] Manually review first 10 users
- [ ] Optional: set up bot for automation

### **Tracking:**
- [ ] Check referrer stats: `/api/referrer-stats`
- [ ] Identify best platform
- [ ] Measure conversion rates
- [ ] Identify cross-platform users

---

## 🎯 Pro tips

### **1. Platform priority**
Start with platforms where you already have an audience:
1. X/Twitter (easiest start)
2. Telegram (tech-savvy audience)
3. Discord (gaming/Web3)
4. Instagram (creators)
5. LinkedIn (professional)

### **2. Cross-promotion**
```
"Verified on X/Twitter? You're already verified for:
- Telegram group
- Discord server
- Instagram account

Same wallet, instant access everywhere!"
```

### **3. Score boost for multi-platform**
```python
# In server.py - bonus for cross-platform users
platforms_used = len(set([event['referrer'] for event in user_events]))
if platforms_used >= 3:
    bonus_score = 5
    new_score += bonus_score
```

---

## 🚀 Next steps

1. **Choose 2-3 main platforms**
2. **Perform setup in parallel**
3. **Cross-promote between platforms**
4. **Measure & optimize**

---

**🌐 VEra-Resonance: One gateway, all platforms!**

*Version 1.0 | November 21, 2025*

© 2025 Karlheinz Beismann — Apache License 2.0
