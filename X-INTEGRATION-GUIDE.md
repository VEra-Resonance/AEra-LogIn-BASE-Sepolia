# 📘 VEra-Resonance for X (Twitter) - Complete Integration Guide

## 🎯 What you will achieve

By the end of this guide, you will have:
- ✅ A private X account with VEra-Resonance
- ✅ Automatic proof-of-human verification for followers
- ✅ Bot-free, authentic community
- ✅ Complete control over your followers

---

## 📋 Prerequisites

### **Technical:**
- ✅ VEra-Resonance server running (port 8820)
- ✅ ngrok or fixed domain
- ✅ MetaMask or compatible wallet

### **X account:**
- ✅ Existing X/Twitter account
- ✅ Access to account settings
- ✅ Willingness to set account to private

---

## 🚀 Part 1: Server setup

### **Step 1.1: Start server**

```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
python3 server.py
```

**Expected output:**
```
✓ VEra-Resonance Server started
🌐 Public URL: http://localhost:8820
📍 Host: 0.0.0.0:8820
```

### **Step 1.2: Set up ngrok tunnel**

```bash
ngrok http 8820
```

**Important:** Note your public URL:
```
https://[your-unique-url].ngrok-free.dev
```

### **Step 1.3: Test server**

Open in your browser:
```
https://[your-url]/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "VEra-Resonance v0.1",
  "database": "connected"
}
```

✅ **Server is running!** Continue to part 2.

---

## 🔒 Part 2: Set X account to private

### **Step 2.1: Open account settings**

1. Go to **X.com**
2. Click your **profile picture** (top left)
3. Select **"Settings and privacy"**

### **Step 2.2: Privacy settings**

1. Navigate to: **"Privacy and safety"**
2. Then to: **"Audience and tagging"**
3. Enable: **"Protect your posts"** (or "Protect your Tweets")

### **Step 2.3: Confirm**

- ✅ You will be warned that your tweets are only visible to followers
- ✅ Confirm with **"Protect"**

**Result:**
- 🔒 Your account is now private
- 🔒 New followers must request
- 🔒 You must manually approve each follower

---

## 📝 Part 3: Bio with VEra-Resonance link

### **Step 3.1: Edit bio**

1. Go to your **profile**
2. Click **"Edit profile"**
3. Scroll to **"Bio"**

### **Step 3.2: Choose template**

Select a suitable template from `X-BIO-TEMPLATES.md`, e.g.:

```
🔒 Protected Account - Real Humans Only

Want to follow? Prove you're human:
👉 https://[your-url].ngrok-free.dev

✓ No bots | ✓ No spam | ✓ Real conversations
Powered by VEra-Resonance

#ProofOfHuman #Web3Social
```

### **Step 3.3: Insert URL**

Replace `[your-url]` with your real ngrok URL:
```
👉 https://ronna-unmagnetised-unaffrightedly.ngrok-free.dev
```

### **Step 3.4: Save**

- ✅ Click **"Save"**
- ✅ Check that the link is clickable

---

## 📌 Part 4: Create pinned tweet

### **Step 4.1: Create tweet**

Create a new tweet with this guide:

```
🔐 IMPORTANT: How to follow this account

1️⃣ Click the link in my bio
2️⃣ Connect your wallet (MetaMask)
3️⃣ Sign the message (free, no gas)
4️⃣ Achieve Resonance Score ≥50
5️⃣ Send follow request to X
6️⃣ I approve within 24h

Why? Because I want ONLY real humans as followers.
No bots. No fakes. Only authentic connections.

🔗 Verify now: https://[your-url]

#ProofOfHuman #VEraResonance
```

### **Step 4.2: Pin tweet**

1. Click the **three dots** on the tweet
2. Select **"Pin to your profile"**
3. Confirm

✅ **The tweet is now pinned at the top!**

---

## 👥 Part 5: Verify first followers

### **Step 5.1: User perspective (testing)**

Test the flow yourself:

1. **Open your X profile** (in incognito tab)
2. **Click the bio link**
3. **Verify yourself** with MetaMask
4. **Check your score**

### **Step 5.2: Send follow request**

After successful verification:

1. User goes back to your X profile
2. User clicks **"Follow"**
3. X shows: **"Follow request sent"**

### **Step 5.3: Accept follow request**

You as account owner:

1. Go to **"Notifications"**
2. See the **"Follow request"**
3. Open VEra-Resonance dashboard:
   ```
   https://[your-url]/api/user/[wallet-address]
   ```
4. Check the **Resonance Score**
5. If score ≥50: **"Accept"** on X
6. If score <50: **"Decline"**

---

## 🎛️ Part 6: Follow management workflow

### **Workflow:**

```
1. User sees your X profile (private)
   ↓
2. User clicks bio link → VEra-Resonance
   ↓
3. User verifies with wallet
   ↓
4. VEra-Resonance creates/updates Resonance Score
   ↓
5. User goes back to X
   ↓
6. User sends follow request
   ↓
7. You check score in VEra system
   ↓
8. Score ≥50? → Accept
   Score <50? → Decline
   ↓
9. User is now follower (or not)
```

### **Best practices:**

#### ✅ **Accept when:**
- Resonance Score ≥50
- First login more than 24h ago
- Natural activity pattern
- No mass requests from similar wallets

#### ❌ **Decline when:**
- Resonance Score <50
- Suspicious wallet pattern
- Too many requests in short time
- Unnatural on-chain activity

---

## 📊 Part 7: Monitoring & Analytics

### **Dashboard URLs:**

#### **1. Server health:**
```
https://[your-url]/api/health
```

#### **2. Overall statistics:**
```
https://[your-url]/api/stats
```

**Shows:**
- Total Users
- Average Score
- Total Logins

#### **3. Individual user:**
```
https://[your-url]/api/user/0x[wallet-address]
```

**Shows:**
- Resonance Score
- First Seen
- Last Login
- Login Count

#### **4. User events:**
```
https://[your-url]/api/events/0x[wallet-address]
```

**Shows:**
- Login history
- Score changes
- Event timeline

### **ngrok web interface:**

For live monitoring of all requests:
```
http://127.0.0.1:4040
```

**Shows:**
- All incoming requests
- Timestamps
- Response codes
- Request/response bodies

---

## 🔧 Part 8: Advanced configuration

### **Adjust minimum score**

Edit `.env`:
```bash
INITIAL_SCORE=50
MIN_SCORE_FOR_FOLLOW=50  # Add this line
```

### **Auto-approval (optional)**

For fully automatic approval, you could create a bot that:
1. Fetches follow requests from X
2. Matches wallet address with score
3. Automatically sends accept/decline

**Note:** Requires X API access (paid)

### **Enable UTM tracking**

Use in your bio:
```
https://[your-url]?source=x&campaign=bio&account=[your-handle]
```

In the server code you can then track where users come from.

---

## 🚨 Part 9: Troubleshooting

### **Problem: Link doesn't work**

**Solution:**
```bash
# Check if server is running:
ps aux | grep "python3 server.py"

# Check if ngrok is running:
ps aux | grep ngrok

# Restart:
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
python3 server.py &
ngrok http 8820
```

### **Problem: Wallet connection fails**

**Solution:**
- Check MetaMask extension
- Check browser console (F12)
- Check CORS settings in `.env`

### **Problem: Score not displayed**

**Solution:**
```bash
# Check database:
sqlite3 /home/karlheinz/krypto/aera-token/webside-wallet-login/aera.db
sqlite> SELECT * FROM users;
sqlite> .quit
```

### **Problem: ngrok URL changes constantly**

**Solution:**
- Option 1: Paid ngrok plan (fixed URL)
- Option 2: Own domain with Cloudflare Tunnel
- Option 3: VPS with fixed IP

---

## 📈 Part 10: Scaling & optimization

### **When you have >100 follow requests:**

1. **Create bulk-check tool:**
   ```bash
   # Script that checks all pending requests
   # and outputs score list
   ```

2. **Increase minimum score:**
   ```
   MIN_SCORE_FOR_FOLLOW=60  # or 70
   ```

3. **Add time gate:**
   ```
   # Only wallets that are >7 days old
   ```

### **Automation:**

Create a dashboard that:
- ✅ Shows all follow requests
- ✅ Scores next to each request
- ✅ One-click accept/decline
- ✅ Bulk actions

---

## 🎯 Part 11: Marketing & community building

### **Announce:**

**Twitter thread:**
```
🧵 Thread: Why my account is now private

1/5 Starting today, my account is private. BUT different than usual.
I only let verified humans in.

2/5 How? Through wallet signature. No KYC, no data.
Just proof that you're a real human.

3/5 Why? Because I don't want bots, fakes, or spam.
Only real connections, real conversations.

4/5 How do you follow me?
→ Link in bio
→ Connect wallet
→ Give signature (free)
→ Send follow request

5/5 Welcome to the future of social media.
Human-verified. Bot-free. Real.

#ProofOfHuman #VEraResonance
```

### **Cross-promotion:**

- Post in crypto communities
- Share in Discord servers
- Mention in podcasts
- Create case study

---

## ✅ Checklist: Ready for go-live?

- [ ] Server running and reachable
- [ ] ngrok tunnel active
- [ ] X account set to private
- [ ] Bio updated with VEra-Resonance link
- [ ] Pinned tweet created
- [ ] Self-tested (with second wallet)
- [ ] Dashboard URLs working
- [ ] Monitoring running (ngrok web interface)
- [ ] Backup plan for outage (server restart script)
- [ ] Community informed

---

## 🎉 Congratulations!

You have successfully set up the **first proof-of-human gate for X**!

**Your community is now:**
- ✅ Bot-free
- ✅ Authentic
- ✅ Valuable
- ✅ Unique

---

## 📞 Support & updates

**Check server logs:**
```bash
tail -f /tmp/server_8820.log
```

**Check database status:**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
sqlite3 aera.db "SELECT COUNT(*) FROM users;"
```

**Check ngrok status:**
```bash
curl http://127.0.0.1:4040/api/tunnels
```

---

**Good luck with your VEra-Resonance! 🚀**

*Created for VEra-Resonance - The first proof-of-human gate for social media*

© 2025 Karlheinz Beismann — Apache License 2.0
