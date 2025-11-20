# ngrok Setup für AEra Server (Port 8820)

## 🚀 Schnellstart

### 1. ngrok Account erstellen
1. Gehen Sie zu: **https://dashboard.ngrok.com/signup**
2. Registrieren Sie sich (kostenlos mit GitHub, Google oder Email)
3. Bestätigen Sie Ihre Email-Adresse

### 2. Authtoken holen
1. Nach dem Login gehen Sie zu: **https://dashboard.ngrok.com/get-started/your-authtoken**
2. Kopieren Sie Ihren Authtoken (sieht aus wie: `2abc...xyz`)

### 3. Authtoken konfigurieren
```bash
ngrok config add-authtoken IHR_TOKEN_HIER
```

### 4. Server über ngrok freigeben
```bash
ngrok http 8820
```

## 📋 Vollständige Anleitung

### Schritt-für-Schritt

**1. Server starten (falls noch nicht läuft)**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
nohup python3 server.py > /tmp/server_8820.log 2>&1 &
```

**2. Authtoken einmalig konfigurieren**
```bash
# Ersetzen Sie <IHR_TOKEN> mit Ihrem echten Token
ngrok config add-authtoken <IHR_TOKEN>
```

**3. ngrok starten**
```bash
ngrok http 8820
```

**4. Öffentliche URL verwenden**
Nach dem Start zeigt ngrok Ihnen eine URL an, z.B.:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8820
```

Diese URL können Sie dann von überall verwenden!

## 🔧 Automatisiertes Start-Script

Nach der Konfiguration des Authtokens können Sie dieses Script verwenden:

```bash
#!/bin/bash
# start_server_with_ngrok.sh

# Server im Hintergrund starten
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
nohup python3 server.py > /tmp/server_8820.log 2>&1 &

# Kurz warten, bis Server bereit ist
sleep 3

# ngrok starten (blockiert Terminal, zeigt Live-Status)
ngrok http 8820
```

## 🌐 Zugriffsmöglichkeiten nach ngrok-Setup

1. **Lokal:** `http://localhost:8820`
2. **LAN:** `http://192.168.178.50:8820`
3. **Tailscale:** `http://[tailscale-ip]:8820`
4. **Internet (ngrok):** `https://xyz.ngrok.io` (die URL, die ngrok anzeigt)

## 🔐 Sicherheitshinweise

⚠️ **WICHTIG:** Mit ngrok ist Ihr Server öffentlich zugänglich!

- ✅ Stellen Sie sicher, dass Ihre Authentifizierung funktioniert
- ✅ Verwenden Sie HTTPS (ngrok macht das automatisch)
- ✅ Überwachen Sie die Logs: `tail -f /tmp/server_8820.log`
- ✅ Beachten Sie die CORS-Einstellungen
- ⚠️ Teilen Sie die ngrok-URL nur mit vertrauenswürdigen Personen

## 📱 ngrok Alternativen

Falls Sie einen dauerhaften Tunnel brauchen, gibt es auch:
- **ngrok bezahlter Account** (feste URL, mehrere Tunnel)
- **Tailscale** (VPN, bereits installiert)
- **Cloudflare Tunnel** (kostenlos)
- **Portainer** mit Reverse Proxy

## 🛠️ Troubleshooting

### "ERR_NGROK_4018"
→ Authtoken nicht konfiguriert. Siehe Schritt 2 oben.

### Server nicht erreichbar
```bash
# Prüfen Sie, ob Server läuft:
ps aux | grep "python3 server.py"

# Prüfen Sie, ob Port offen ist:
ss -tlnp | grep 8820
```

### ngrok Tunnel beenden
Drücken Sie `Ctrl+C` im Terminal wo ngrok läuft.

## 📚 Weitere Ressourcen

- ngrok Dashboard: https://dashboard.ngrok.com/
- ngrok Dokumentation: https://ngrok.com/docs
- ngrok Download: https://ngrok.com/download
