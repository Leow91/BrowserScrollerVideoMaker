# Quick Start Guide

Schnellanleitung zum Erstellen Ihres ersten Scroll-Videos in 5 Minuten!

## Schritt 1: Installation (3 Minuten)

```bash
# 1. FFmpeg installieren (falls noch nicht vorhanden)
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# 2. Python-Pakete installieren
pip install -r requirements.txt

# 3. Browser herunterladen
playwright install chromium
```

## Schritt 2: Erstes Video erstellen (1 Minute)

```bash
python scroll_video_generator.py \
    --url https://example.com \
    --duration 10 \
    --output mein_erstes_video.mp4
```

## Schritt 3: Ergebnis ansehen

```bash
# Das Video sollte jetzt als 'mein_erstes_video.mp4' im aktuellen Verzeichnis sein
# Öffnen Sie es mit Ihrem Video-Player!
```

## Nächste Schritte

### Text hinzufügen

```bash
python scroll_video_generator.py \
    --url https://github.com \
    --duration 15 \
    --output github.mp4 \
    --text_overlay "Meine GitHub Tour"
```

### Logo hinzufügen

```bash
# Erstellen Sie zuerst ein Logo (logo.png)
python scroll_video_generator.py \
    --url https://example.com \
    --duration 20 \
    --output branded.mp4 \
    --logo_path logo.png
```

### Beide Overlays

```bash
python scroll_video_generator.py \
    --url https://example.com \
    --duration 20 \
    --output complete.mp4 \
    --logo_path logo.png \
    --text_overlay "Website Demo"
```

## Fehlerbehebung

### FFmpeg nicht gefunden

```bash
# Testen Sie:
ffmpeg -version

# Falls nicht installiert, siehe Schritt 1
```

### Playwright-Browser nicht gefunden

```bash
# Führen Sie erneut aus:
playwright install chromium
```

## Hilfe

```bash
python scroll_video_generator.py --help
```

Für detaillierte Informationen siehe [README.md](README.md).
