# 📊 AEra Logger - Übersicht

Der umfassende Logger protokolliert **ALLES** was im System passiert!

## 📁 Log-Dateien

```
logs/
├── aera.log          📄 Hauptlog - ALLES (Debug, Info, Warning, Error)
├── aera.json         📊 JSON-Format - für strukturierte Analyse
├── activity.log      📝 Activity Log - nur wichtige Events
├── errors.log        ❌ Error Log - nur Fehler
```

## 📖 Log-Dateien lesen

### Alle Aktivitäten (Main Log)
```bash
tail -100 logs/aera.log
tail -f logs/aera.log  # Live-Verfolgung
```

### Nur wichtige Events
```bash
tail -50 logs/activity.log
```

### Nur Fehler
```bash
tail -30 logs/errors.log
```

### JSON (strukturiert)
```bash
cat logs/aera.json | python3 -m json.tool
```

### Spezifische Suche
```bash
grep "AUTH" logs/aera.log          # Authentifizierung
grep "WEB3" logs/aera.log          # Blockchain
grep "AIRDROP" logs/aera.log       # Airdrop Events
grep "ERROR" logs/aera.log         # Fehler
```

## 📊 Logger-Kategorien

| Kategorie | Beschreibung |
|-----------|------------|
| `AUTH` | Benutzer-Authentifizierung, Logins, Registrierungen |
| `TOKEN` | Token-Generierung und Verifikation |
| `WALLET` | Wallet-Operationen |
| `WEB3` | Blockchain-Interaktionen |
| `AIRDROP` | Airdrop-Verteilungen |
| `DATABASE` | Datenbank-Operationen |

## 🔍 Fehler-Tracking

### Live-Fehler-Verfolgung
```bash
tail -f logs/errors.log
```

### Fehler mit Kontext
```bash
grep -A 3 -B 3 "ERROR" logs/aera.log
```

## 📈 Performance

### Größe der Logs überprüfen
```bash
du -sh logs/
ls -lh logs/
```

### Logs archivieren (Speichern)
```bash
cp logs/aera.log logs/aera_$(date +%Y%m%d_%H%M%S).log
> logs/aera.log  # Clear
```

### Alte Logs löschen
```bash
# Logs älter als 7 Tage löschen
find logs -type f -mtime +7 -delete
```

## 💡 Wichtige Log-Meldungen

### Erfolgreiche Registrierung
```
[INFO] [AUTH] New user registered | address=0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5 | initial_score=50
```

### Erfolgreicher Login
```
[INFO] [AUTH] Existing user login | address=0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5 | old_score=50 | new_score=51 | login_count=2
```

### Token-Fehler
```
[ERROR] [TOKEN] Token verification error | error=Token expired
```

### Airdrop Execution
```
[INFO] [AIRDROP] Airdrop transaction sent | address=0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5 | tx_hash=0x...
```

## 🎯 Anwendungs-Szenarien

### Benutzer-Aktivität verfolgen
```bash
grep "0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5" logs/aera.log
```

### Alle Neukunden heute
```bash
grep "$(date +%Y-%m-%d)" logs/aera.log | grep "New user registered"
```

### Fehler-Rate
```bash
grep "ERROR" logs/aera.log | wc -l
```

### Durchschnittliche Response-Zeit
```bash
grep "duration" logs/aera.json | python3 -c "import json, sys; times = [json.loads(l).get('duration', 0) for l in sys.stdin]; print(f'Avg: {sum(times)/len(times):.2f}ms')"
```

---

**Logging aktiv seit:** Server-Start
**Logger-Komponenten:** 6 (Main, Auth, Web3, Database, Wallet, Airdrop)
