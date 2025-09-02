#!/usr/bin/env python3
"""
Demo des Album Multi-Downloaders
Zeigt die Funktionsweise mit einem kleinen Beispiel-Dataset.
"""

import json
import os
import sys
from pathlib import Path

def create_demo_library():
    """Erstellt eine Demo-Bibliothek mit bekannten Alben."""
    demo_library = {
        "tracks": [
            # Queen - News of the World
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
            
            # The Beatles - Abbey Road
            {
                "artist": "The Beatles",
                "album": "Abbey Road",
                "track": "Come Together",
                "uri": "spotify:track:2EqlS6tkEnglzr7tkKAAYD"
            },
            {
                "artist": "The Beatles",
                "album": "Abbey Road", 
                "track": "Something",
                "uri": "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
            },
            
            # Led Zeppelin - Led Zeppelin IV
            {
                "artist": "Led Zeppelin",
                "album": "Led Zeppelin IV",
                "track": "Stairway to Heaven",
                "uri": "spotify:track:5CQ30WqJwcep0pYcV4AMNc"
            },
            
            # Pink Floyd - The Dark Side of the Moon
            {
                "artist": "Pink Floyd", 
                "album": "The Dark Side of the Moon",
                "track": "Money",
                "uri": "spotify:track:0vFOzaXqZHahrZp6enQwQb"
            }
        ]
    }
    
    # Speichere Demo-Bibliothek
    demo_file = "demo_library.json"
    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(demo_library, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Demo-Bibliothek erstellt: {demo_file}")
    return demo_file

def show_demo_info():
    """Zeigt Informationen über die Demo."""
    print("🎵 Album Multi-Downloader Demo")
    print("=" * 50)
    print()
    print("Diese Demo zeigt, wie der Album Multi-Downloader funktioniert.")
    print()
    print("Die Demo-Bibliothek enthält Songs aus 4 berühmten Alben:")
    print("• Queen - News of the World (2 Songs)")
    print("• The Beatles - Abbey Road (2 Songs)")  
    print("• Led Zeppelin - Led Zeppelin IV (1 Song)")
    print("• Pink Floyd - The Dark Side of the Moon (1 Song)")
    print()
    print("Das Programm wird:")
    print("1. Diese 4 Alben auf Spotify finden")
    print("2. Jedes Album VOLLSTÄNDIG herunterladen")
    print("3. Ordner nach Künstler/Album organisieren")
    print("4. Bereits heruntergeladene Alben beim nächsten Mal überspringen")
    print()

def run_demo():
    """Führt die Demo aus."""
    show_demo_info()
    
    # Prüfe ob spotDL verfügbar ist
    try:
        import spotdl
        print("✓ spotDL gefunden")
    except ImportError:
        print("❌ spotDL nicht gefunden. Installation erforderlich:")
        print("   pip install spotdl")
        return False
    
    # Erstelle Demo-Bibliothek
    demo_file = create_demo_library()
    
    # Prüfe Konfiguration
    config_exists = os.path.exists("album_downloader_config.json")
    
    if not config_exists:
        print()
        print("⚠️  Noch keine Konfiguration vorhanden.")
        print()
        choice = input("Möchtest du jetzt die Konfiguration einrichten? (j/n): ").lower()
        
        if choice in ['j', 'ja', 'y', 'yes']:
            print()
            print("Führe aus: python album_config.py")
            print("Danach: python demo_album_downloader.py")
            return True
        else:
            print("Demo abgebrochen. Konfiguration erforderlich.")
            return False
    
    print()
    print("✓ Konfiguration gefunden")
    print()
    choice = input("Demo starten? (Downloads werden durchgeführt!) (j/n): ").lower()
    
    if choice not in ['j', 'ja', 'y', 'yes']:
        print("Demo abgebrochen.")
        return True
    
    print()
    print("🚀 Starte Album Multi-Downloader...")
    print()
    
    # Führe den Album-Downloader aus
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 
            "album_multi_downloader.py", 
            demo_file
        ], check=True)
        
        print()
        print("🎉 Demo erfolgreich abgeschlossen!")
        print()
        print("Überprüfe deinen Download-Ordner für die heruntergeladenen Alben.")
        
        # Zeige Statistiken
        if os.path.exists("downloaded_albums.json"):
            with open("downloaded_albums.json", 'r', encoding='utf-8') as f:
                tracking_data = json.load(f)
                downloaded = tracking_data.get('downloaded_albums', [])
                print(f"📊 {len(downloaded)} Alben heruntergeladen")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Ausführen der Demo: {e}")
        return False
    except FileNotFoundError:
        print("❌ album_multi_downloader.py nicht gefunden")
        return False

def cleanup_demo():
    """Räumt Demo-Dateien auf."""
    demo_files = [
        "demo_library.json",
        "downloaded_albums.json"
    ]
    
    print()
    choice = input("Demo-Dateien aufräumen? (j/n): ").lower()
    
    if choice in ['j', 'ja', 'y', 'yes']:
        for file in demo_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"✓ Entfernt: {file}")

def main():
    """Hauptfunktion der Demo."""
    try:
        success = run_demo()
        
        if success:
            cleanup_demo()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo abgebrochen.")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()
