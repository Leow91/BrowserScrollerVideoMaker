# Automated Web Scroll Video Creator

🎬 **Production-Ready** | 🌐 **Web GUI** | 📱 **13 Social Platforms** | 🚀 **Scalable** | 📦 **Docker Support** | ⚖️ **MIT License**

Ein professionelles, produktionsreifes System zum automatischen Erstellen von Scroll-Videos von Webseiten mit Web-GUI, Workflow-Management, Social-Media-Optimierung und Enterprise-Features.

## ✨ Highlights

- ✅ **Modern Web GUI** - Intuitive Gradio-basierte Benutzeroberfläche
- ✅ **13 Social Media Presets** - Instagram, TikTok, YouTube, Facebook, LinkedIn & mehr
- ✅ **Workflow-System** - Automatische Link-Erkennung und Batch-Verarbeitung
- ✅ **Production-Ready** - Logging, Konfiguration, Error Handling
- ✅ **Docker Support** - Einfaches Deployment mit Docker & Kubernetes
- ✅ **Skalierbar** - Modular, erweiterbar, gut dokumentiert
- ✅ **Kommerziell nutzbar** - MIT License, alle Dependencies kompatibel

## Features

### 🎯 Core Features
- Automatisches Scrollen durch beliebige Webseiten
- Aufzeichnung des Scroll-Vorgangs als Video (30 FPS)
- Logo-Overlay (obere rechte Ecke)
- Text-Overlay (unten zentriert)
- Anpassbare Viewport-Größe (640x480 bis 3840x2160)
- Konfigurierbare Scroll-Dauer (1-300 Sekunden)
- FFmpeg-Integration für professionelle Video-Kodierung

### 🌐 Web GUI
- **Modern & Intuitiv** - Gradio-basiertes Interface
- **🆕 Platform Dropdown** - Wähle Instagram, TikTok, YouTube & mehr
- **Auto-Konfiguration** - Einstellungen passen sich automatisch an
- **Echtzeit-Feedback** - Progress-Tracking während Video-Generierung
- **7 Tabs** - Single Video, Link Discovery, Workflow Builder, Runner, Library, Platform Guide, Settings
- **Platform Guide** - Komplette Übersicht aller Social Media Specs
- **Library Management** - Übersicht über Workflows und generierte Videos

### 🔄 Workflow-System
- **🔍 Automatische Link-Erkennung** - Sitemap.xml oder Homepage-Scraping
- **✅ Interaktive Auswahl** - Checkbox-Interface (Web GUI & CLI)
- **🔢 Nummerierte Sequenzen** - Automatische Nummerierung (001, 002, ...)
- **💾 Wiederverwendbare Workflows** - JSON-basierte Konfiguration
- **🎯 Batch-Verarbeitung** - Mehrere Videos automatisch generieren
- **📊 Kategorisierung** - Intelligente Link-Gruppierung

### 🏗️ Production Features
- **Centralized Configuration** - Pydantic-basierte Config mit .env Support
- **Structured Logging** - Rich-formatierte Logs mit Rotation
- **Error Handling** - Comprehensive Exception Handling
- **Docker Support** - Production-ready Dockerfile & docker-compose
- **Health Checks** - Systemüberwachung und Status-Checks
- **Resource Management** - Konfigurierbare Limits und Caching

### 📱 Social Media Platforms (NEU!)
- **Instagram** - Feed (1:1), Story (9:16), Reel (9:16)
- **Facebook** - Feed (16:9), Story (9:16)
- **TikTok** - Vertical (9:16), max 3min
- **YouTube** - Shorts (9:16), Videos (16:9)
- **WhatsApp** - Status (9:16), max 30s
- **LinkedIn** - Posts (16:9), max 10min
- **Twitter/X** - Posts (16:9), max 2:20
- **Pinterest** - Pins (9:16), max 60s
- **Snapchat** - Snaps (9:16), max 60s
- **Custom** - Beliebige Einstellungen

### 📚 Documentation
- [README.md](README.md) - Hauptdokumentation (diese Datei)
- [SOCIAL_MEDIA_GUIDE.md](SOCIAL_MEDIA_GUIDE.md) - **🆕 Social Media Platform Guide**
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Workflow-System Details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production Deployment Guide
- [CODE_REVIEW.md](CODE_REVIEW.md) - Code-Review & Lizenz-Analyse
- [QUICKSTART.md](QUICKSTART.md) - 5-Minuten Quick Start

## Voraussetzungen

### System-Anforderungen

1. **Python 3.7 oder höher**
2. **FFmpeg** - Muss systemweit installiert sein

#### FFmpeg Installation

**Windows:**
```bash
# Mit Chocolatey
choco install ffmpeg

# Oder von https://ffmpeg.org/download.html herunterladen
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

### Überprüfen der FFmpeg-Installation

```bash
ffmpeg -version
```

## Installation

### 1. Repository klonen

```bash
git clone <repository-url>
cd BrowserScrollerVideoMaker
```

### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Playwright-Browser installieren

```bash
playwright install chromium
```

Dies lädt den Chromium-Browser herunter, der für die Videoaufnahme benötigt wird.

## 🚀 Quick Start

### Option 1: Web GUI (Empfohlen)

```bash
# 1. Installation
make setup
# oder manuell:
pip install -r requirements.txt
playwright install chromium

# 2. Web GUI starten
make gui
# oder:
python web_gui.py
```

**Öffnen Sie:** http://localhost:7860

### Option 2: Docker (Production)

```bash
# Start mit Docker Compose
docker-compose up -d

# Zugriff auf http://localhost:7860

# Logs anzeigen
docker-compose logs -f

# Stoppen
docker-compose down
```

### Option 3: CLI (Advanced)

```bash
# Einzelnes Video
python scroll_video_generator.py --url https://example.com --duration 15 --output video.mp4

# Workflow Builder
python workflow_builder.py

# Workflow ausführen
python workflow_runner.py workflows/my_workflow.json
```

## Verwendung

### 🌐 Web GUI

Die Web GUI bietet die komfortabelste Möglichkeit, Videos zu erstellen:

**Tabs:**
1. **📹 Single Video** - Einzelne Videos erstellen
2. **🔍 Link Discovery** - Automatisch Links finden
3. **⚙️ Workflow Builder** - Workflows aus Links erstellen
4. **▶️ Workflow Runner** - Gespeicherte Workflows ausführen
5. **📚 Library** - Workflows und Videos verwalten
6. **⚙️ Settings** - Konfiguration anzeigen

**Screenshot-Beispiele:**

```
┌──────────────────────────────────────────────┐
│  🎬 Scroll Video Generator                  │
├──────────────────────────────────────────────┤
│  📹 Single Video  🔍 Discover  ⚙️ Builder    │
├──────────────────────────────────────────────┤
│                                              │
│  Website URL: https://example.com            │
│  Duration: [====15s====]                     │
│  Width: 1920  Height: 1080                   │
│  Logo: [Upload PNG]                          │
│  Text: My Website Tour                       │
│                                              │
│  [ 🎬 Generate Video ]                       │
│                                              │
│  Status: ✅ Video generated!                 │
│  [Video Player]                              │
└──────────────────────────────────────────────┘
```

### Modus 1: Einzelnes Video (CLI)

#### Basis-Syntax

```bash
python scroll_video_generator.py --url <URL> --duration <SEKUNDEN> --output <DATEINAME>
```

### Beispiele

#### 1. Einfaches Scroll-Video

```bash
python scroll_video_generator.py \
    --url https://example.com \
    --duration 15 \
    --output mein_video.mp4
```

#### 2. Mit Logo-Overlay

```bash
python scroll_video_generator.py \
    --url https://example.com \
    --duration 20 \
    --output mein_video.mp4 \
    --logo_path logo.png
```

#### 3. Mit Text-Overlay

```bash
python scroll_video_generator.py \
    --url https://example.com \
    --duration 10 \
    --output mein_video.mp4 \
    --text_overlay "Website Tour 2024"
```

#### 4. Mit Logo und Text

```bash
python scroll_video_generator.py \
    --url https://github.com \
    --duration 30 \
    --output github_tour.mp4 \
    --logo_path company_logo.png \
    --text_overlay "GitHub Homepage"
```

#### 5. Mit benutzerdefinierter Auflösung

```bash
python scroll_video_generator.py \
    --url https://example.com \
    --duration 15 \
    --output video_4k.mp4 \
    --width 3840 \
    --height 2160
```

### Verfügbare Parameter

| Parameter | Erforderlich | Beschreibung | Standard |
|-----------|--------------|--------------|----------|
| `--url` | Ja | URL der zu scrollenden Webseite | - |
| `--duration` | Ja | Dauer des Scrollens in Sekunden | - |
| `--output` | Ja | Name der Ausgabe-Videodatei | - |
| `--logo_path` | Nein | Pfad zur Logo-PNG-Datei | - |
| `--text_overlay` | Nein | Text für Overlay | - |
| `--width` | Nein | Browser-Viewport-Breite | 1920 |
| `--height` | Nein | Browser-Viewport-Höhe | 1080 |

## Wie es funktioniert

### 1. Scroll-Berechnung

Das Skript:
- Lädt die Webseite im Browser
- Ermittelt die Gesamthöhe der Seite (`document.body.scrollHeight`)
- Berechnet die notwendige Scroll-Geschwindigkeit basierend auf:
  - Gesamthöhe der Seite
  - Gewünschter Dauer
  - 30 FPS für flüssiges Scrollen

### 2. Video-Aufnahme mit Playwright

- Startet Chromium im Headless-Modus mit aktivierter Videoaufnahme
- Führt JavaScript-Code aus, der die Seite pixelweise scrollt
- Verwendet `window.scrollTo()` in kleinen Schritten für flüssige Bewegung
- Speichert das Roh-Video als WebM-Datei

### 3. Video-Komposition mit FFmpeg

Nach der Aufnahme verwendet das Skript FFmpeg um:
- **Logo-Overlay**: Positioniert das Logo in der oberen rechten Ecke (10px Abstand)
- **Text-Overlay**: Platziert Text zentriert am unteren Rand mit:
  - Weißer Schriftfarbe
  - Schwarzem Rahmen für bessere Lesbarkeit
  - Schriftgröße 48pt
- Das finale Video als MP4 (H.264) zu kodieren

### 4. Aufräumen

- Löscht temporäre Dateien
- Gibt nur das finale Video aus

## Technische Details

- **Browser**: Chromium (über Playwright)
- **Video-Codec**: H.264 (libx264)
- **Video-Format**: MP4
- **Scroll-FPS**: 30
- **CRF-Qualität**: 23 (gute Balance zwischen Qualität und Dateigröße)

## Fehlerbehebung

### "FFmpeg is not installed or not in PATH"

**Lösung**: Installieren Sie FFmpeg (siehe oben) und stellen Sie sicher, dass es im PATH ist.

```bash
# Testen
ffmpeg -version
```

### "Logo file not found"

**Lösung**: Überprüfen Sie den Pfad zur Logo-Datei. Verwenden Sie absolute oder relative Pfade.

```bash
# Absoluter Pfad (empfohlen)
--logo_path /home/user/images/logo.png

# Relativer Pfad
--logo_path ./logo.png
```

### Video ist zu kurz oder zu lang

**Lösung**: Das Skript versucht, die exakte Dauer einzuhalten. Bei sehr kurzen oder sehr langen Seiten kann es Abweichungen geben.

### Seite wird nicht vollständig geladen

**Lösung**: Das Skript wartet auf "networkidle". Bei problematischen Seiten können Sie das Timeout anpassen, indem Sie den Code modifizieren:

```python
await page.goto(self.url, wait_until="networkidle", timeout=120000)  # 120 Sekunden
```

### Playwright-Browser nicht gefunden

**Lösung**: Führen Sie erneut aus:

```bash
playwright install chromium
```

## Beispiel-Workflow

```bash
# 1. Installation
pip install -r requirements.txt
playwright install chromium

# 2. Video erstellen
python scroll_video_generator.py \
    --url https://news.ycombinator.com \
    --duration 20 \
    --output hackernews_scroll.mp4 \
    --text_overlay "Hacker News - Daily Feed"

# 3. Ergebnis prüfen
ls -lh hackernews_scroll.mp4
```

### Modus 2: Workflow-System (NEU!)

Das Workflow-System ermöglicht die Erstellung von Video-Sequenzen mit automatischer Link-Erkennung.

#### Schnellstart Workflow

```bash
# 1. Interaktiven Workflow Builder starten
python workflow_builder.py

# 2. Folgen Sie den Anweisungen:
#    - URL eingeben
#    - Automatische Link-Erkennung (Sitemap oder Scraping)
#    - Kategorien und Seiten per Checkbox auswählen
#    - Video-Einstellungen konfigurieren
#    - Workflow speichern

# 3. Workflow ausführen
python workflow_runner.py workflows/mein_workflow.json
```

#### Workflow-Features im Überblick

**Automatische Link-Erkennung:**
```bash
# Probiert automatisch sitemap.xml
python link_finder.py https://example.com
```

**Workflow-Info anzeigen:**
```bash
python workflow_runner.py workflows/mein_workflow.json --info
```

**Teilweise ausführen:**
```bash
# Nur Schritte 5-10
python workflow_runner.py workflows/mein_workflow.json --start 5 --end 10
```

**Vollständige Dokumentation:**
- Siehe [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) für detaillierte Anleitung
- Umfasst: Link-Erkennung, Kategorisierung, Nummerierung, Batch-Verarbeitung

## Erweiterte Verwendung

### Batch-Verarbeitung mehrerer URLs (Manuell)

Erstellen Sie ein Bash-Skript:

```bash
#!/bin/bash

urls=(
    "https://example.com"
    "https://github.com"
    "https://stackoverflow.com"
)

for i in "${!urls[@]}"; do
    python scroll_video_generator.py \
        --url "${urls[$i]}" \
        --duration 15 \
        --output "video_$i.mp4"
done
```

### Anpassung der Video-Qualität

Bearbeiten Sie `scroll_video_generator.py` und ändern Sie den CRF-Wert:

```python
"-crf", "18",  # Höhere Qualität (größere Datei)
"-crf", "28",  # Niedrigere Qualität (kleinere Datei)
```

## Lizenz

MIT License

## Beiträge

Beiträge sind willkommen! Bitte öffnen Sie ein Issue oder Pull Request.

## Support

Bei Problemen oder Fragen öffnen Sie bitte ein Issue im GitHub-Repository.
