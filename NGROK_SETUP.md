# ngrok Setup for VEra-Resonance Server (Port 8820)

## 🚀 Quick Start

### 1. Create ngrok account
1. Go to: **https://dashboard.ngrok.com/signup**
2. Sign up (free with GitHub, Google, or Email)
3. Verify your email address

### 2. Get your authtoken
1. After login, go to: **https://dashboard.ngrok.com/get-started/your-authtoken**
2. Copy your authtoken (looks like: `2abc...xyz`)

### 3. Configure authtoken
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

### 4. Expose server through ngrok
```bash
ngrok http 8820
```

## 📋 Complete Instructions

### Step-by-step

**1. Start server (if not already running)**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
nohup python3 server.py > /tmp/server_8820.log 2>&1 &
```

**2. Configure authtoken (one time)**
```bash
# Replace <YOUR_TOKEN> with your actual token
ngrok config add-authtoken <YOUR_TOKEN>
```

**3. Start ngrok**
```bash
ngrok http 8820
```

**4. Use public URL**
After startup, ngrok will show you a URL, e.g.:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8820
```

You can use this URL from anywhere!

## 🔧 Automated Start Script

After configuring your authtoken, you can use this script:

```bash
#!/bin/bash
# start_server_with_ngrok.sh

# Start server in background
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
nohup python3 server.py > /tmp/server_8820.log 2>&1 &

# Wait briefly for server to be ready
sleep 3

# Start ngrok (blocks terminal, shows live status)
ngrok http 8820
```

## 🌐 Access options after ngrok setup

1. **Local:** `http://localhost:8820`
2. **LAN:** `http://192.168.178.50:8820`
3. **Tailscale:** `http://[tailscale-ip]:8820`
4. **Internet (ngrok):** `https://xyz.ngrok.io` (the URL ngrok displays)

## 🔐 Security notes

⚠️ **IMPORTANT:** With ngrok, your server is publicly accessible!

- ✅ Make sure your authentication works
- ✅ Use HTTPS (ngrok does this automatically)
- ✅ Monitor logs: `tail -f /tmp/server_8820.log`
- ✅ Check CORS settings
- ⚠️ Only share the ngrok URL with trusted people

## 📱 ngrok alternatives

If you need a permanent tunnel, there are also:
- **ngrok paid account** (fixed URL, multiple tunnels)
- **Tailscale** (VPN, already installed)
- **Cloudflare Tunnel** (free)
- **Portainer** with reverse proxy

## 🛠️ Troubleshooting

### "ERR_NGROK_4018"
→ Authtoken not configured. See Step 2 above.

### Server not reachable
```bash
# Check if server is running:
ps aux | grep "python3 server.py"

# Check if port is open:
ss -tlnp | grep 8820
```

### Stop ngrok tunnel
Press `Ctrl+C` in the terminal where ngrok is running.

## 📚 Further resources

- ngrok Dashboard: https://dashboard.ngrok.com/
- ngrok Documentation: https://ngrok.com/docs
- ngrok Download: https://ngrok.com/download
