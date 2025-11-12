# Automated Web Scroll Video Creator

Ein robustes Python-Skript zum automatischen Erstellen von Scroll-Videos von Webseiten mit optionalen Logo- und Text-Overlays.

## Features

- Automatisches Scrollen durch beliebige Webseiten
- Aufzeichnung des Scroll-Vorgangs als Video
- Konfigurierbare Scroll-Dauer
- Optional: Logo-Overlay (obere rechte Ecke)
- Optional: Text-Overlay (unten zentriert)
- Anpassbare Viewport-Größe
- Flüssiges Scrollen mit 30 FPS
- CLI-basierte Konfiguration

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

## Verwendung

### Basis-Syntax

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

## Erweiterte Verwendung

### Batch-Verarbeitung mehrerer URLs

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
