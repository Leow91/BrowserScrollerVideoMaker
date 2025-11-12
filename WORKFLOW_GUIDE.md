# Workflow Guide

Komplette Anleitung für das Erstellen und Ausführen von Video-Workflows mit automatischer Link-Erkennung, interaktiver Auswahl und Sequenzierung.

## 🎯 Überblick

Das Workflow-System ermöglicht es Ihnen:

1. **Automatisch Links zu finden** - Erkennt Links auf Webseiten oder aus sitemap.xml
2. **Interaktiv auszuwählen** - Checkbox-Interface zum Auswählen gewünschter Seiten
3. **Workflows zu nummerieren** - Erstellt nummerierte Sequenzen
4. **Workflows zu speichern** - Wiederverwendbare JSON-Konfigurationen
5. **Batch-Verarbeitung** - Führt mehrere Videos automatisch aus

## 🚀 Schnellstart

### Schritt 1: Workflow erstellen

```bash
python workflow_builder.py
```

Das interaktive Tool führt Sie durch:
- URL-Eingabe der Haupt-Website
- Automatische Link-Erkennung (sitemap.xml oder Scraping)
- Kategorieauswahl mit Checkboxen
- Konfiguration der Video-Einstellungen
- Nummerierung und Speicherung

### Schritt 2: Workflow ausführen

```bash
python workflow_runner.py workflows/my_workflow.json
```

## 📖 Detaillierte Anleitung

### 1. Link-Erkennung

Das System bietet drei Modi zur Link-Erkennung:

#### A) Sitemap.xml (Empfohlen)

Versucht automatisch `sitemap.xml` zu finden und zu parsen:

```bash
# Automatisch
python link_finder.py https://example.com
```

Standardmäßig probiert es:
- `https://example.com/sitemap.xml`
- `https://example.com/sitemap_index.xml`
- `https://example.com/sitemap1.xml`

**Vorteile:**
- Vollständige URL-Liste
- Kategorisierung nach URL-Struktur
- Schnell und zuverlässig

#### B) Homepage-Scraping

Scrapt Links direkt von der Homepage:

```bash
python link_finder.py https://example.com
```

**Vorteile:**
- Funktioniert ohne Sitemap
- Erkennt Navigation und Kategorien
- Intelligent kategorisiert (Navigation, Footer, etc.)

#### C) Manuelle Eingabe

URLs manuell eingeben:

```bash
python workflow_builder.py
# Wählen Sie dann "Manual entry"
```

**Vorteile:**
- Vollständige Kontrolle
- Für spezifische Seiten
- Keine automatische Erkennung nötig

### 2. Interaktive Workflow-Erstellung

#### Starten Sie den Workflow Builder

```bash
python workflow_builder.py
```

#### Schritt-für-Schritt

**1. URL eingeben**
```
Enter the base URL of the website:
> https://example.com
```

**2. Erkennungsmethode wählen**
```
How would you like to discover pages?
  🗺️  Try sitemap.xml first (recommended)
  🔍 Scrape from homepage
  ✍️  Manual entry (enter URLs manually)
```

**3. Kategorien auswählen**

Das System zeigt gefundene Kategorien:
```
Select categories to include:
  ☐ 📁 Products (15 links)
  ☐ 📁 Blog (8 links)
  ☐ 📁 About (3 links)
  ☐ 📁 Navigation (12 links)
```

Verwenden Sie:
- `Leertaste` zum An-/Abwählen
- `a` zum Alle auswählen
- `Enter` zum Bestätigen

**4. Spezifische Links auswählen**

Pro Kategorie:
```
📁 Category: Products
Select all 15 links from 'Products'? (y/N)

# Falls Nein:
Select links from 'Products':
  ☐ 1. Product A - https://example.com/products/a
  ☐ 2. Product B - https://example.com/products/b
  ☐ 3. Product C - https://example.com/products/c
```

**5. Video-Einstellungen konfigurieren**

```
Use default settings for all videos? (y/N)
> y

Default settings: duration: 15s, 1920x1080

Add logo overlay to all videos? (y/N)
> y
Path to logo file (PNG):
> /path/to/logo.png

Add text overlay to all videos? (y/N)
> y
Use page title as text overlay? (y/N)
> y
```

**Oder individuell pro Video:**

```
Video 1/3: Product A
─────────────────────────────────────────
Duration (seconds): 20
Width (pixels): 1920
Height (pixels): 1080
Add logo overlay? (y/N): y
Path to logo file: logo.png
Add text overlay? (y/N): y
Text overlay: Product A Overview
```

**6. Reihenfolge anpassen (optional)**

```
Would you like to reorder the sequence? (y/N)
> y

Current order:
  1. Product A
  2. Product B
  3. Product C

Select items in the desired order:
  ☐ 1. Product A
  ☐ 2. Product B
  ☐ 3. Product C
```

**7. Workflow speichern**

```
Save this workflow to a file? (Y/n)
> y

Workflow filename:
> my_website_tour.json

✓ Workflow saved to: workflows/my_website_tour.json
```

### 3. Workflow-Struktur

Gespeicherte Workflows sind JSON-Dateien:

```json
{
  "base_url": "https://example.com",
  "steps": [
    {
      "number": 1,
      "url": "https://example.com/products/a",
      "description": "Product A",
      "duration": 15,
      "width": 1920,
      "height": 1080,
      "output": "001_Product_A.mp4",
      "logo_path": "logo.png",
      "text_overlay": "Product A"
    },
    {
      "number": 2,
      "url": "https://example.com/products/b",
      "description": "Product B",
      "duration": 20,
      "width": 1920,
      "height": 1080,
      "output": "002_Product_B.mp4",
      "logo_path": "logo.png",
      "text_overlay": "Product B"
    }
  ]
}
```

### 4. Workflows ausführen

#### Gesamten Workflow ausführen

```bash
python workflow_runner.py workflows/my_workflow.json
```

#### Workflow-Info anzeigen (ohne Ausführung)

```bash
python workflow_runner.py workflows/my_workflow.json --info
```

Ausgabe:
```
📋 WORKFLOW INFORMATION
══════════════════════════════════════════════════════════════════════

File: workflows/my_workflow.json
Base URL: https://example.com
Total steps: 3

Step   1: Product A
  URL:      https://example.com/products/a
  Duration: 15s
  Output:   001_Product_A.mp4
  Logo:     logo.png
  Text:     Product A

...
```

#### Teilweise ausführen

**Nur Schritte 3-5:**
```bash
python workflow_runner.py workflows/my_workflow.json --start 3 --end 5
```

**Ab Schritt 10:**
```bash
python workflow_runner.py workflows/my_workflow.json --start 10
```

#### Benutzerdefiniertes Output-Verzeichnis

```bash
python workflow_runner.py workflows/my_workflow.json --output-dir my_videos
```

### 5. Ausgabe und Ergebnisse

#### Während der Ausführung

```
══════════════════════════════════════════════════════════════════════
🎬 EXECUTING WORKFLOW (3 steps)
══════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════
Step 1/3 (#1): Product A
══════════════════════════════════════════════════════════════════════

Starting browser and loading https://example.com/products/a...
Loading page...
Page height: 4500px
Viewport height: 1080px
Scrolling 3420px over 15 seconds...
Scroll complete. Finalizing recording...
Raw video saved as temp_raw_scroll.webm
Applying overlays with FFmpeg...
Video successfully created: output/001_Product_A.mp4

✓ Step 1 completed successfully!
```

#### Nach Abschluss

```
📊 WORKFLOW EXECUTION SUMMARY
══════════════════════════════════════════════════════════════════════
Total steps:      3
Successful:       3 ✓
Failed:           0 ✗
Execution time:   125.4s (~2m 5s)
Output directory: /home/user/BrowserScrollerVideoMaker/output
══════════════════════════════════════════════════════════════════════
```

#### Output-Struktur

```
output/
├── 001_Product_A.mp4
├── 002_Product_B.mp4
└── 003_Product_C.mp4
```

## 🎨 Erweiterte Verwendung

### Workflows manuell bearbeiten

Sie können gespeicherte Workflows direkt bearbeiten:

```bash
nano workflows/my_workflow.json
```

Ändern Sie z.B.:
- URLs
- Dauer
- Text-Overlays
- Reihenfolge (number-Feld)

### Workflows kombinieren

Kombinieren Sie mehrere Workflows:

```python
import json

# Workflow 1 laden
with open("workflows/workflow1.json") as f:
    wf1 = json.load(f)

# Workflow 2 laden
with open("workflows/workflow2.json") as f:
    wf2 = json.load(f)

# Kombinieren
combined = {
    "base_url": wf1["base_url"],
    "steps": wf1["steps"] + wf2["steps"]
}

# Nummern neu zuweisen
for i, step in enumerate(combined["steps"], 1):
    step["number"] = i
    step["output"] = f"{i:03d}_{step['output'][4:]}"

# Speichern
with open("workflows/combined.json", "w") as f:
    json.dump(combined, f, indent=2)
```

### Workflow-Vorlagen

Erstellen Sie Vorlagen für häufige Szenarien:

**template_blog.json:**
```json
{
  "base_url": "https://YOUR-SITE.com",
  "steps": [
    {
      "number": 1,
      "url": "https://YOUR-SITE.com/blog",
      "description": "Blog Overview",
      "duration": 10,
      "width": 1920,
      "height": 1080,
      "output": "001_blog_overview.mp4",
      "logo_path": "logo.png",
      "text_overlay": "Blog"
    }
  ]
}
```

Dann anpassen und ausführen.

## 🔧 Tipps und Tricks

### 1. Optimale Scroll-Dauer

- **Kurze Seiten** (< 3000px): 5-10 Sekunden
- **Mittlere Seiten** (3000-8000px): 15-20 Sekunden
- **Lange Seiten** (> 8000px): 25-40 Sekunden

### 2. Performance-Optimierung

Für große Workflows:
- Führen Sie in Batches aus (`--start` und `--end`)
- Nutzen Sie niedrigere Auflösungen für Tests (1280x720)
- Schließen Sie andere Browser-Fenster

### 3. Fehlerbehandlung

Bei Fehlern:
1. Workflow-Runner zeigt Fehler an
2. Fragt nach 5 Sekunden, ob fortgesetzt werden soll
3. Drücken Sie Ctrl+C zum Abbrechen

Neustart ab fehlgeschlagenem Schritt:
```bash
python workflow_runner.py workflows/my_workflow.json --start 5
```

### 4. Logo-Optimierung

Empfohlene Logo-Größe:
- **1920x1080 Videos**: 200-300px Breite
- **PNG mit Transparenz**
- Position: Automatisch oben rechts

### 5. Text-Overlay Best Practices

- **Kurze Texte** (< 50 Zeichen) für bessere Lesbarkeit
- Nutzen Sie Seiten-Titel automatisch
- Vermeiden Sie Sonderzeichen (`:`, `'`, etc.)

## 📋 Beispiel-Workflows

### Beispiel 1: E-Commerce-Produktkatalog

```bash
python workflow_builder.py
```

1. URL: `https://shop.example.com`
2. Methode: Sitemap.xml
3. Kategorien auswählen: `Products`, `New Arrivals`
4. Settings: 15s, Logo, Auto-Text
5. Speichern als: `product_catalog.json`

Ausführen:
```bash
python workflow_runner.py workflows/product_catalog.json --output-dir product_videos
```

### Beispiel 2: Blog-Post-Serie

```bash
python workflow_builder.py
```

1. URL: `https://blog.example.com`
2. Methode: Scrape from homepage
3. Kategorie: `Blog Posts`
4. Alle Posts auswählen
5. Settings: 20s, mit Text-Overlay (Titel)
6. Reihenfolge: Neueste zuerst

### Beispiel 3: Dokumentations-Seiten

```bash
python workflow_builder.py
```

1. URL: `https://docs.example.com`
2. Methode: Sitemap.xml
3. Kategorien: `Getting Started`, `Tutorials`, `API Reference`
4. Settings: 25s (lange Seiten), ohne Logo, mit Text
5. Nummerierung: Logische Reihenfolge (Getting Started → Tutorials → API)

## 🔍 Fehlerbehebung

### Links werden nicht gefunden

**Problem**: Keine Links bei automatischer Erkennung

**Lösungen:**
1. Versuchen Sie Homepage-Scraping statt Sitemap
2. Nutzen Sie manuelle Eingabe
3. Prüfen Sie, ob `robots.txt` Zugriff blockiert

### Sitemap.xml nicht gefunden

**Problem**: `No sitemap found`

**Lösungen:**
1. Prüfen Sie manuell: `https://example.com/sitemap.xml`
2. Suchen Sie in `robots.txt` nach Sitemap-URL
3. Verwenden Sie Scraping oder manuelle Eingabe

### Kategorisierung ungenau

**Problem**: Links in falschen Kategorien

**Lösung:**
- Bei manueller Eingabe werden alle als "Manual" kategorisiert
- Bei Sitemap: Kategorien basieren auf URL-Struktur
- Sie können Workflows manuell bearbeiten

### Workflow-Ausführung abbricht

**Problem**: Fehler bei einem Schritt stoppt Workflow

**Lösungen:**
1. Warten Sie 5 Sekunden, Workflow fährt automatisch fort
2. Oder drücken Sie Ctrl+C zum Abbrechen
3. Starten Sie neu ab dem fehlgeschlagenen Schritt

## 📚 Weitere Ressourcen

- [README.md](README.md) - Haupt-Dokumentation
- [QUICKSTART.md](QUICKSTART.md) - Schnelleinstieg
- [examples/](examples/) - Beispiel-Skripte
