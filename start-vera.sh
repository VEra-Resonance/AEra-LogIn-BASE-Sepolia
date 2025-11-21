#!/bin/bash

# VEra-Resonance — Auto-Start Script
# Supports: Local, Tailscale, and ngrok

set -e

PROJECT_DIR="/home/karlheinz/krypto/aera-token/webside-wallet-login"
LOG_DIR="$PROJECT_DIR/logs"
TUNNEL_LOG="$LOG_DIR/tunnel-url.txt"

# Create logs directory
mkdir -p "$LOG_DIR"

echo "🚀 VEra-Resonance — Multi-Access Launcher"
echo "==========================================="
echo ""

# Parse arguments
DEPLOYMENT_MODE="${1:-local}"
NGROK_ENABLED="${2:-yes}"

case $DEPLOYMENT_MODE in
    local|tailscale|ngrok)
        echo "✓ Deployment mode: $DEPLOYMENT_MODE"
        ;;
    *)
        echo "❌ Invalid mode. Use: local | tailscale | ngrok"
        echo "Usage: ./start-vera.sh [local|tailscale|ngrok] [ngrok-yes/no]"
        exit 1
        ;;
esac

# Kill old processes
echo "🧹 Cleaning up old processes..."
pkill -f "python3.*server.py" || true
pkill -f "ngrok" || true
sleep 1

# Start FastAPI server
echo "🚀 Starting FastAPI server..."
cd "$PROJECT_DIR"

export DEPLOYMENT_MODE=$DEPLOYMENT_MODE
export TAILSCALE_ENABLED=$([ "$DEPLOYMENT_MODE" = "tailscale" ] && echo "true" || echo "false")

python3 server.py &
SERVER_PID=$!
echo "✓ Server started (PID: $SERVER_PID)"

# Wait for server to start
sleep 2

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    echo "❌ Server failed to start!"
    exit 1
fi

# Start ngrok if enabled
if [ "$NGROK_ENABLED" = "yes" ] && [ "$DEPLOYMENT_MODE" != "local" ]; then
    echo "🌐 Starting ngrok tunnel..."
    
    if ! command -v ngrok &> /dev/null; then
        echo "❌ ngrok not found. Install: apt install ngrok"
        exit 1
    fi
    
    ngrok http 8840 &
    NGROK_PID=$!
    
    # Wait for ngrok to start and get URL
    sleep 3
    
    # Try to get ngrok URL from API
    NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -z "$NGROK_URL" ]; then
        echo "⚠️  Could not get ngrok URL. Check: http://127.0.0.1:4040"
    else
        echo "✓ ngrok tunnel: $NGROK_URL"
        echo "$NGROK_URL" > "$TUNNEL_LOG"
    fi
fi

# Get Tailscale IP if available
if [ "$DEPLOYMENT_MODE" = "tailscale" ]; then
    echo "🔍 Detecting Tailscale IP..."
    TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "")
    
    if [ -n "$TAILSCALE_IP" ]; then
        echo "✓ Tailscale IP: $TAILSCALE_IP"
        echo "✓ Dashboard: http://$TAILSCALE_IP:8000/dashboard"
        echo "http://$TAILSCALE_IP:8000/dashboard" > "$TUNNEL_LOG"
    else
        echo "⚠️  Tailscale IP not found. Make sure Tailscale is running:"
        echo "    tailscale status"
    fi
fi

echo ""
echo "==========================================="
echo "✅ VEra-Resonance is RUNNING!"
echo ""
echo "📍 Access URLs:"
echo "   Local:    http://localhost:8840/dashboard"

if [ -f "$TUNNEL_LOG" ]; then
    URL=$(cat "$TUNNEL_LOG")
    echo "   Tunnel:   $URL"
fi

echo ""
echo "📊 Health Check:"
echo "   curl http://localhost:8840/api/health"
echo ""
echo "🛑 Stop: pkill -f 'python3.*server.py' && pkill -f ngrok"
echo ""

# Keep running
wait $SERVER_PID
