"""
Album Multi-Downloader Configuration Setup
Dieses Modul erstellt und verwaltet die Konfigurationsdatei für den Album-Downloader.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

CONFIG_FILE = "album_downloader_config.json"

def create_config() -> Dict[str, Any]:
    """
    Erstellt eine neue Konfigurationsdatei durch Benutzereingaben.
    
    Returns:
        Dict mit Konfigurationsdaten
    """
    config = {}
    
    print("=== Album Multi-Downloader Konfiguration ===")
    print()
    
    # Spotify API Credentials
    print("Spotify API Credentials benötigt:")
    print("(Siehe: https://developer.spotify.com/dashboard/)")
    
    client_id = input("Spotify Client ID: ").strip()
    while not client_id:
        print("Client ID ist erforderlich!")
        client_id = input("Spotify Client ID: ").strip()
    
    client_secret = input("Spotify Client Secret: ").strip()
    while not client_secret:
        print("Client Secret ist erforderlich!")
        client_secret = input("Spotify Client Secret: ").strip()
    
    config["spotify"] = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    # Download Ordner
    print()
    print("Download-Ordner Konfiguration:")
    default_path = os.path.join(os.path.expanduser("~"), "Music", "Spotify_Albums")
    
    download_path = input(f"Download-Ordner [{default_path}]: ").strip()
    if not download_path:
        download_path = default_path
    
    # Erstelle Ordner falls er nicht existiert
    Path(download_path).mkdir(parents=True, exist_ok=True)
    
    config["download"] = {
        "base_path": download_path,
        "create_album_folders": True,
        "audio_format": "mp3",
        "bitrate": "auto"
    }
    
    # Tracking-Datei für bereits heruntergeladene Alben
    config["tracking"] = {
        "downloaded_albums_file": "downloaded_albums.json",
        "skip_existing": True
    }
    
    # Speichere Konfiguration
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"Konfiguration gespeichert in: {CONFIG_FILE}")
    return config

def load_config() -> Dict[str, Any]:
    """
    Lädt die Konfigurationsdatei.
    
    Returns:
        Dict mit Konfigurationsdaten
        
    Raises:
        FileNotFoundError: Wenn Konfigurationsdatei nicht gefunden wird
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Konfigurationsdatei {CONFIG_FILE} nicht gefunden. Führe setup aus.")
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_config(updates: Dict[str, Any]) -> None:
    """
    Aktualisiert die Konfigurationsdatei.
    
    Args:
        updates: Dictionary mit Updates
    """
    config = load_config()
    config.update(updates)
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def setup_config() -> Dict[str, Any]:
    """
    Setup-Funktion für die Konfiguration.
    
    Returns:
        Konfigurationsdaten
    """
    if os.path.exists(CONFIG_FILE):
        response = input(f"Konfigurationsdatei {CONFIG_FILE} bereits vorhanden. Überschreiben? (j/n): ")
        if response.lower() not in ['j', 'ja', 'y', 'yes']:
            return load_config()
    
    return create_config()

if __name__ == "__main__":
    try:
        config = setup_config()
        print("Konfiguration erfolgreich erstellt!")
        print(f"Download-Ordner: {config['download']['base_path']}")
    except KeyboardInterrupt:
        print("\nSetup abgebrochen.")
    except Exception as e:
        print(f"Fehler beim Setup: {e}")
