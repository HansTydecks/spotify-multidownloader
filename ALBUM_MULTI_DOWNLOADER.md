# Album Multi-Downloader

Ein auf **spotDL** basierendes Programm zum automatischen Herunterladen ganzer Alben basierend auf einer JSON-Datei mit einzelnen Liedern.

## 🎯 Überblick

Dieses Programm erweitert das bestehende spotDL-System um die Fähigkeit, automatisch ganze Alben herunterzuladen, anstatt nur einzelne Songs. Es analysiert eine JSON-Datei mit Song-Informationen, gruppiert diese nach Alben und lädt dann systematisch jedes Album vollständig herunter.

## ✨ Features

- **Automatische Album-Erkennung**: Gruppiert Songs aus JSON nach Album und Künstler
- **Spotify API Integration**: Findet Alben über die Spotify API
- **Intelligentes Tracking**: Verhindert doppelte Downloads bereits heruntergeladener Alben
- **Organisierte Ordnerstruktur**: Erstellt automatisch Ordner nach Künstler/Album
- **Konfigurationsmanagement**: Einmalige Einrichtung von API-Schlüsseln und Einstellungen
- **Fortschritts-Verfolgung**: Detaillierte Statistiken und Fortschrittsanzeige
- **Fehlerbehandlung**: Robuste Fehlerbehandlung mit aussagekräftigen Meldungen

## 📋 Voraussetzungen

1. **Python 3.8+** installiert
2. **spotDL** bereits im System vorhanden (dieses Repository)
3. **Spotify Developer Account** für API-Zugang
4. **FFmpeg** installiert (für Audio-Konvertierung)

## 🚀 Installation & Setup

### 1. Spotify API Credentials erstellen

1. Besuche https://developer.spotify.com/dashboard/
2. Erstelle eine neue App
3. Notiere dir `Client ID` und `Client Secret`

### 2. Konfiguration einrichten

Führe das Konfigurationsskript aus:

```bash
python album_config.py
```

Das Programm fragt nach:
- Spotify Client ID
- Spotify Client Secret  
- Download-Ordner (Standard: `~/Music/Spotify_Albums`)

Die Konfiguration wird in `album_downloader_config.json` gespeichert.

### 3. JSON-Datei vorbereiten

Deine Musikbibliothek sollte im folgenden Format vorliegen:

```json
{
  "tracks": [
    {
      "artist": "Murray Head",
      "album": "Emotions",
      "track": "One Night in Bangkok",
      "uri": "spotify:track:6erBowZaW6Ur3vNOWhS2zM"
    },
    {
      "artist": "T. Rex",
      "album": "Electric Warrior", 
      "track": "Get It On",
      "uri": "spotify:track:0LoQuiekvzqx7n8flgEKzF"
    }
  ]
}
```

## 🎵 Verwendung

### Basis-Download

```bash
python album_multi_downloader.py
```

Das Programm sucht standardmäßig nach `YourLibrary.json`.

### Eigene JSON-Datei verwenden

```bash
python album_multi_downloader.py meine_musik.json
```

### Was passiert beim Download:

1. **JSON-Analyse**: Lädt und analysiert die Musikbibliothek
2. **Album-Gruppierung**: Gruppiert Songs nach Künstler und Album
3. **Spotify-Suche**: Findet jedes Album über die Spotify API
4. **Download**: Lädt alle Songs des Albums in organisierten Ordnern herunter
5. **Tracking**: Markiert erfolgreich heruntergeladene Alben

## 📁 Ordnerstruktur

Die heruntergeladenen Alben werden so organisiert:

```
~/Music/Spotify_Albums/
├── Murray Head/
│   └── Emotions/
│       ├── 01 - One Night in Bangkok.mp3
│       ├── 02 - Nobody's Fool.mp3
│       └── ...
├── T. Rex/
│   └── Electric Warrior/
│       ├── 01 - Mambo Sun.mp3
│       ├── 02 - Cosmic Dancer.mp3
│       ├── 03 - Get It On.mp3
│       └── ...
```

## 🔧 Konfiguration

Die Konfigurationsdatei `album_downloader_config.json` enthält:

```json
{
  "spotify": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
  },
  "download": {
    "base_path": "/path/to/downloads",
    "create_album_folders": true,
    "audio_format": "mp3",
    "bitrate": "auto"
  },
  "tracking": {
    "downloaded_albums_file": "downloaded_albums.json",
    "skip_existing": true
  }
}
```

### Einstellungen ändern:

- **base_path**: Download-Ordner ändern
- **audio_format**: Format ändern (mp3, flac, ogg, etc.)
- **skip_existing**: `false` setzen um Alben erneut zu downloaden

## 📊 Tracking System

Das Programm verfolgt bereits heruntergeladene Alben in `downloaded_albums.json`:

```json
{
  "downloaded_albums": [
    "Murray Head - Emotions",
    "T. Rex - Electric Warrior"
  ],
  "last_updated": "2025-09-02 15:30:45"
}
```

## 🛠️ Troubleshooting

### Häufige Probleme:

**"Spotify client not created"**
- Prüfe deine API-Credentials in der Konfiguration
- Stelle sicher, dass die Spotify App aktiv ist

**"Album nicht auf Spotify gefunden"**
- Künstler-/Album-Namen in JSON könnten abweichen
- Manuell nach dem Album auf Spotify suchen und Namen anpassen

**"Keine Songs konnten heruntergeladen werden"**
- Internetverbindung prüfen
- FFmpeg Installation überprüfen
- YouTube-Verfügbarkeit der Songs prüfen

### Debug-Modus:

Für detailliertere Fehlermeldungen spotDL direkt verwenden:

```bash
python -m spotdl download "spotify:album:album_id" --output "test_folder"
```

## 📈 Beispiel-Output

```
🎵 Album Multi-Downloader gestartet
📁 Download-Ordner: /Users/hans/Music/Spotify_Albums
📊 Bereits heruntergeladen: 5 Alben

📖 Lade Bibliothek aus YourLibrary.json...
🎵 150 Tracks gefunden
💿 25 einzigartige Alben identifiziert

[1/25] 📀 Album: Murray Head - Emotions
🔍 Suche Album auf Spotify...
📥 Lade Album-Information...
🎵 Gefunden: 10 Songs
⬇️  Lade Songs herunter...
✅ 10/10 Songs erfolgreich heruntergeladen

[2/25] ⏭️  Album bereits heruntergeladen: T. Rex - Electric Warrior

...

============================================================
📊 Download-Statistiken:
   ✅ Erfolgreich: 18
   ⏭️  Übersprungen: 5
   ❌ Fehlgeschlagen: 2
   📊 Gesamt: 25
============================================================
```

## 🤝 Basiert auf spotDL

Dieses Programm nutzt die bestehende spotDL-Infrastruktur:
- Song-Suche und Download-Logik
- Metadata-Extraktion
- Audio-Qualität und Formate
- YouTube-Integration

Siehe [spotDL Dokumentation](README.md) für weitere Details zu den zugrundeliegenden Funktionen.

## 📄 Lizenz

Dieses Projekt steht unter der gleichen Lizenz wie spotDL (MIT License).
