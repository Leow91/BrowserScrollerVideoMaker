# Examples

Dieser Ordner enthält Beispiel-Skripte für die Verwendung des Scroll Video Generators.

## Verfügbare Beispiele

### 1. run_examples.sh

Ein Bash-Skript, das mehrere Beispiel-Videos mit verschiedenen Konfigurationen erstellt.

**Verwendung:**
```bash
cd examples
chmod +x run_examples.sh
./run_examples.sh
```

**Was es tut:**
- Erstellt ein einfaches Scroll-Video von example.com
- Erstellt ein HD-Video von Hacker News
- Erstellt ein Video mit Text-Overlay von GitHub

### 2. batch_process.py

Ein Python-Skript für die Batch-Verarbeitung mehrerer URLs.

**Verwendung:**
```bash
cd examples
python batch_process.py
```

**Anpassung:**

Bearbeiten Sie `batch_process.py` und ändern Sie die `urls_config` Liste:

```python
urls_config = [
    # (url, duration_seconds, output_filename, text_overlay)
    ("https://example.com", 10, "example_com.mp4", "Example.com"),
    ("https://ihre-url.de", 20, "output.mp4", "Ihr Text"),
    # Fügen Sie weitere URLs hinzu...
]
```

## Einzelne Beispiel-Befehle

### Minimales Beispiel

```bash
python ../scroll_video_generator.py \
    --url https://example.com \
    --duration 10 \
    --output simple.mp4
```

### Mit Text-Overlay

```bash
python ../scroll_video_generator.py \
    --url https://github.com \
    --duration 15 \
    --output github_tour.mp4 \
    --text_overlay "GitHub Homepage"
```

### Mit Logo

Erstellen Sie zuerst ein Logo (z.B. `logo.png`) und führen Sie dann aus:

```bash
python ../scroll_video_generator.py \
    --url https://example.com \
    --duration 20 \
    --output branded.mp4 \
    --logo_path logo.png
```

### Vollständiges Beispiel

```bash
python ../scroll_video_generator.py \
    --url https://example.com \
    --duration 30 \
    --output complete.mp4 \
    --logo_path logo.png \
    --text_overlay "Website Demo 2024" \
    --width 1920 \
    --height 1080
```

## Hinweise

- Videos werden im aktuellen Verzeichnis (`examples/`) gespeichert
- Stellen Sie sicher, dass Sie die Abhängigkeiten installiert haben
- FFmpeg muss systemweit verfügbar sein
