# 🚀 Album Multi-Downloader - Schnellstart

## 1-Minute Setup für Album-Downloads

### ⚡ Schnellstart

1. **Spotify API Setup** (einmalig):
   ```bash
   python album_config.py
   ```
   
2. **Album Download starten**:
   ```bash
   python album_multi_downloader.py
   ```

Das war's! 🎉

---

## 📋 Was passiert:

1. **Konfiguration**: Beim ersten Start wirst du nach Spotify API-Schlüsseln gefragt
2. **JSON-Analyse**: Das Programm liest `YourLibrary.json` 
3. **Album-Erkennung**: Gruppiert deine Songs nach Alben
4. **Download**: Lädt jedes Album vollständig herunter
5. **Organisation**: Erstellt saubere Ordnerstruktur (Künstler/Album)

## 🎯 Beispiel

Aus dieser JSON:
```json
{
  "tracks": [
    {"artist": "Queen", "album": "News of the World", "track": "We Will Rock You"},
    {"artist": "Queen", "album": "News of the World", "track": "We Are the Champions"},
    {"artist": "Queen", "album": "A Night at the Opera", "track": "Bohemian Rhapsody"}
  ]
}
```

Wird das:
```
📁 Downloads/
  └── Queen/
      ├── News of the World/        ← Ganzes Album heruntergeladen
      │   ├── 01 - We Will Rock You.mp3
      │   ├── 02 - We Are the Champions.mp3
      │   └── ... (alle anderen Album-Songs)
      └── A Night at the Opera/     ← Ganzes Album heruntergeladen  
          ├── 01 - Death on Two Legs.mp3
          ├── 02 - Lazing on a Sunday Afternoon.mp3
          ├── 03 - Bohemian Rhapsody.mp3
          └── ... (alle anderen Album-Songs)
```

## 🔧 Erste Hilfe

**Problem**: "Konfigurationsdatei nicht gefunden"
**Lösung**: `python album_config.py` ausführen

**Problem**: "Album nicht gefunden"  
**Lösung**: Prüfe Schreibweise in der JSON-Datei

**Problem**: "Spotify API Fehler"
**Lösung**: API-Schlüssel in der Konfiguration überprüfen

## 💡 Profi-Tipps

- **Große Bibliotheken**: Das Programm läuft automatisch durch alle Alben
- **Neustart sicher**: Bereits heruntergeladene Alben werden übersprungen  
- **Eigene JSON**: `python album_multi_downloader.py meine_musik.json`
- **Tracking**: In `downloaded_albums.json` siehst du den Fortschritt

---

**Vollständige Dokumentation**: [ALBUM_MULTI_DOWNLOADER.md](ALBUM_MULTI_DOWNLOADER.md)
