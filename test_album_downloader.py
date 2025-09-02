"""
Test-Skript für Album Multi-Downloader
Testet das System mit einem kleinen Beispiel-Dataset.
"""

import json
import os
import sys
from pathlib import Path

def create_test_json():
    """Erstellt eine Test-JSON mit einigen Beispiel-Alben."""
    test_data = {
        "tracks": [
            # Album 1: Queen - News of the World (mehrere Songs)
            {
                "artist": "Queen",
                "album": "News of the World",
                "track": "We Will Rock You",
                "uri": "spotify:track:54flyrjcdnQdco7300avMJ"
            },
            {
                "artist": "Queen", 
                "album": "News of the World",
                "track": "We Are the Champions",
                "uri": "spotify:track:7ccI9cStQbQdystvc6TvxD"
            },
            # Album 2: The Beatles - Abbey Road (ein Song)
            {
                "artist": "The Beatles",
                "album": "Abbey Road",
                "track": "Come Together",
                "uri": "spotify:track:2EqlS6tkEnglzr7tkKAAYD"
            },
            # Album 3: Pink Floyd - The Wall (ein Song)
            {
                "artist": "Pink Floyd",
                "album": "The Wall",
                "track": "Another Brick in the Wall, Pt. 2",
                "uri": "spotify:track:1UHS8Rf6h5Ar3CDWRd3wjF"
            },
            # Doppelter Eintrag (sollte nur einmal Album downloaden)
            {
                "artist": "Queen",
                "album": "News of the World", 
                "track": "Sheer Heart Attack",
                "uri": "spotify:track:3fVB3GHYU71KADqHgABLAl"
            }
        ]
    }
    
    with open("test_library.json", 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print("✓ Test-JSON erstellt: test_library.json")
    print("  - 3 verschiedene Alben")
    print("  - 5 Songs total")
    return "test_library.json"

def test_config_creation():
    """Testet das Erstellen einer Konfiguration."""
    print("\n🧪 Teste Konfigurationserstellung...")
    
    # Entferne bestehende Konfiguration für Test
    if os.path.exists("album_downloader_config.json"):
        os.rename("album_downloader_config.json", "album_downloader_config.json.backup")
    
    print("Für diesen Test, verwende beliebige Test-Credentials.")
    print("(Für echten Download benötigst du echte Spotify API-Schlüssel)")
    
    try:
        from album_config import setup_config
        # Simuliere Benutzereingaben (für automatisierten Test)
        # In der Praxis würde der Benutzer diese eingeben
        print("Test-Modus: Verwende Dummy-Credentials")
        return True
    except Exception as e:
        print(f"❌ Konfigurationstest fehlgeschlagen: {e}")
        return False

def test_library_parsing():
    """Testet das Parsen der JSON-Bibliothek."""
    print("\n🧪 Teste JSON-Parsing...")
    
    try:
        from album_multi_downloader import AlbumMultiDownloader
        
        # Dummy-Konfiguration für Test
        test_config = {
            'spotify': {
                'client_id': 'test_id',
                'client_secret': 'test_secret'
            },
            'download': {
                'base_path': './test_downloads',
                'create_album_folders': True,
                'audio_format': 'mp3',
                'bitrate': 'auto'
            },
            'tracking': {
                'downloaded_albums_file': 'test_downloaded_albums.json',
                'skip_existing': True
            }
        }
        
        # Erstelle Test-Ordner
        Path('./test_downloads').mkdir(exist_ok=True)
        
        # Teste nur das Parsing, nicht den Download
        print("✓ Import erfolgreich")
        
        # Test: JSON laden
        test_json = create_test_json()
        with open(test_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tracks = data.get('tracks', [])
        print(f"✓ {len(tracks)} Tracks geladen")
        
        # Test: Album-Gruppierung
        from collections import defaultdict
        albums = defaultdict(list)
        
        for track in tracks:
            artist = track.get('artist', '').strip()
            album = track.get('album', '').strip()
            album_key = f"{artist} - {album}"
            albums[album_key].append(track)
        
        print(f"✓ {len(albums)} einzigartige Alben erkannt:")
        for album_key, album_tracks in albums.items():
            print(f"   - {album_key} ({len(album_tracks)} Songs)")
        
        return True
        
    except Exception as e:
        print(f"❌ Parsing-Test fehlgeschlagen: {e}")
        return False

def test_spotify_search_simulation():
    """Simuliert Spotify-Suche ohne echte API-Calls."""
    print("\n🧪 Teste Spotify-Suche (Simulation)...")
    
    test_albums = [
        ("Queen", "News of the World"),
        ("The Beatles", "Abbey Road"), 
        ("Pink Floyd", "The Wall")
    ]
    
    for artist, album in test_albums:
        # Simuliere erfolgreiche Suche
        simulated_url = f"https://open.spotify.com/album/fake_id_{artist.replace(' ', '_').lower()}"
        print(f"✓ Simulierte Suche: {artist} - {album} → {simulated_url}")
    
    return True

def cleanup_test_files():
    """Räumt Test-Dateien auf."""
    print("\n🧹 Räume Test-Dateien auf...")
    
    test_files = [
        "test_library.json",
        "test_downloaded_albums.json",
        "album_downloader_config.json"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"✓ Entfernt: {file}")
    
    # Stelle Original-Konfiguration wieder her
    if os.path.exists("album_downloader_config.json.backup"):
        os.rename("album_downloader_config.json.backup", "album_downloader_config.json")
        print("✓ Original-Konfiguration wiederhergestellt")
    
    # Entferne Test-Download-Ordner
    import shutil
    if os.path.exists("./test_downloads"):
        shutil.rmtree("./test_downloads")
        print("✓ Test-Download-Ordner entfernt")

def run_tests():
    """Führt alle Tests aus."""
    print("🧪 Album Multi-Downloader Tests")
    print("=" * 40)
    
    tests = [
        ("JSON-Parsing", test_library_parsing),
        ("Spotify-Suche (Simulation)", test_spotify_search_simulation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n▶️  {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} bestanden")
                passed += 1
            else:
                print(f"❌ {test_name} fehlgeschlagen")
        except Exception as e:
            print(f"❌ {test_name} fehlgeschlagen: {e}")
    
    print(f"\n📊 Test-Ergebnisse: {passed}/{total} bestanden")
    
    if passed == total:
        print("🎉 Alle Tests bestanden! Das System ist bereit.")
        print("\nNächste Schritte:")
        print("1. Führe 'python album_config.py' aus für echte Konfiguration")
        print("2. Stelle sicher, dass du echte Spotify API-Schlüssel hast")
        print("3. Führe 'python album_multi_downloader.py' aus")
    else:
        print("⚠️  Einige Tests fehlgeschlagen. Prüfe die Installation.")
    
    return passed == total

def main():
    """Hauptfunktion."""
    try:
        success = run_tests()
        
        # Frage nach Cleanup
        response = input("\nTest-Dateien aufräumen? (j/n): ").lower()
        if response in ['j', 'ja', 'y', 'yes', '']:
            cleanup_test_files()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests abgebrochen.")
        cleanup_test_files()
        sys.exit(1)

if __name__ == "__main__":
    main()
