"""
Album Multi-Downloader
Lädt ganze Alben basierend auf einer JSON-Datei mit einzelnen Liedern herunter.
Nutzt die bestehende spotDL-Infrastruktur.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import time

try:
    from spotdl import Spotdl
    from spotdl.types.album import Album
    from spotdl.utils.spotify import SpotifyClient
except ImportError as e:
    print(f"❌ Fehler beim Import von spotDL: {e}")
    print("Stelle sicher, dass spotDL installiert ist: pip install spotdl")
    sys.exit(1)

from album_config import load_config, setup_config

class AlbumTracker:
    """Verwaltet bereits heruntergeladene Alben."""
    
    def __init__(self, tracking_file: str):
        self.tracking_file = tracking_file
        self.downloaded_albums: Set[str] = self._load_tracking()
    
    def _load_tracking(self) -> Set[str]:
        """Lädt die Liste bereits heruntergeladener Alben."""
        if os.path.exists(self.tracking_file):
            try:
                with open(self.tracking_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('downloaded_albums', []))
            except Exception as e:
                print(f"Warnung: Fehler beim Laden der Tracking-Datei: {e}")
        return set()
    
    def _save_tracking(self) -> None:
        """Speichert die Liste heruntergeladener Alben."""
        data = {
            'downloaded_albums': list(self.downloaded_albums),
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def is_downloaded(self, album_key: str) -> bool:
        """Prüft ob Album bereits heruntergeladen wurde."""
        return album_key in self.downloaded_albums
    
    def mark_downloaded(self, album_key: str) -> None:
        """Markiert Album als heruntergeladen."""
        self.downloaded_albums.add(album_key)
        self._save_tracking()
    
    def get_downloaded_count(self) -> int:
        """Gibt Anzahl heruntergeladener Alben zurück."""
        return len(self.downloaded_albums)

class AlbumMultiDownloader:
    """Hauptklasse für den Album-Multi-Downloader."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.tracker = AlbumTracker(config['tracking']['downloaded_albums_file'])
        self.spotdl: Optional[Spotdl] = None
        self._initialize_spotdl()
    
    def _initialize_spotdl(self) -> None:
        """Initialisiert spotDL mit Konfiguration."""
        try:
            self.spotdl = Spotdl(
                client_id=self.config['spotify']['client_id'],
                client_secret=self.config['spotify']['client_secret'],
                downloader_settings={
                    'output': self.config['download']['base_path'],
                    'format': self.config['download']['audio_format'],
                    'threads': 4,
                    'bitrate': self.config['download']['bitrate']
                }
            )
            print("✓ SpotDL erfolgreich initialisiert")
        except Exception as e:
            print(f"Fehler beim Initialisieren von SpotDL: {e}")
            sys.exit(1)
    
    def _load_library_json(self, json_file: str) -> List[Dict[str, Any]]:
        """Lädt die JSON-Datei mit der Musikbibliothek."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('tracks', [])
        except Exception as e:
            print(f"Fehler beim Laden der JSON-Datei: {e}")
            sys.exit(1)
    
    def _group_tracks_by_album(self, tracks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Gruppiert Tracks nach Album und Künstler."""
        albums = defaultdict(list)
        
        for track in tracks:
            artist = track.get('artist', '').strip()
            album = track.get('album', '').strip()
            
            if not artist or not album:
                continue
            
            # Erstelle eindeutigen Album-Schlüssel
            album_key = f"{artist} - {album}"
            albums[album_key].append(track)
        
        return dict(albums)
    
    def _search_album_on_spotify(self, artist: str, album: str) -> Optional[str]:
        """Sucht Album auf Spotify und gibt die Album-URL zurück."""
        try:
            spotify_client = SpotifyClient()
            
            # Erste Suche: Kombinierte Suche
            query = f"artist:{artist} album:{album}"
            results = spotify_client.search(q=query, type='album', limit=10)
            
            if results and results['albums']['items']:
                for album_result in results['albums']['items']:
                    # Prüfe ob Artist und Album-Name übereinstimmen
                    album_artists = [artist['name'].lower() for artist in album_result['artists']]
                    if (artist.lower() in album_artists and 
                        album.lower() in album_result['name'].lower()):
                        return album_result['external_urls']['spotify']
                
                # Falls keine exakte Übereinstimmung, nehme das erste Ergebnis
                first_result = results['albums']['items'][0]
                print(f"⚠️  Keine exakte Übereinstimmung. Verwende: {first_result['artists'][0]['name']} - {first_result['name']}")
                return first_result['external_urls']['spotify']
            
            # Zweite Suche: Nur Album-Name
            query = f'"{album}"'
            results = spotify_client.search(q=query, type='album', limit=5)
            
            if results and results['albums']['items']:
                for album_result in results['albums']['items']:
                    album_artists = [artist['name'].lower() for artist in album_result['artists']]
                    if artist.lower() in album_artists:
                        print(f"⚠️  Gefunden mit vereinfachter Suche: {album_result['artists'][0]['name']} - {album_result['name']}")
                        return album_result['external_urls']['spotify']
            
            return None
        except Exception as e:
            print(f"Fehler bei Spotify-Suche für {artist} - {album}: {e}")
            return None
    
    def _create_album_folder(self, artist: str, album: str) -> Path:
        """Erstellt Ordner für Album."""
        # Bereinige Namen für Dateisystem
        safe_artist = "".join(c for c in artist if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_album = "".join(c for c in album if c.isalnum() or c in (' ', '-', '_')).strip()
        
        album_folder = Path(self.config['download']['base_path']) / safe_artist / safe_album
        album_folder.mkdir(parents=True, exist_ok=True)
        return album_folder
    
    def _download_album(self, album_key: str, tracks: List[Dict[str, Any]]) -> bool:
        """Lädt ein Album herunter."""
        print(f"\n📀 Album: {album_key}")
        
        # Parse Artist und Album Namen
        try:
            artist, album = album_key.split(' - ', 1)
        except ValueError:
            print(f"❌ Ungültiges Album-Format: {album_key}")
            return False
        
        # Prüfe ob bereits heruntergeladen
        if self.config['tracking']['skip_existing'] and self.tracker.is_downloaded(album_key):
            print(f"⏭️  Album bereits heruntergeladen, überspringe...")
            return True
        
        # Suche Album auf Spotify
        print(f"🔍 Suche Album auf Spotify...")
        album_url = self._search_album_on_spotify(artist, album)
        
        if not album_url:
            print(f"❌ Album nicht auf Spotify gefunden: {album_key}")
            return False
        
        try:
            # Erstelle Album-Ordner
            album_folder = None
            original_output = None
            
            if self.config['download']['create_album_folders']:
                album_folder = self._create_album_folder(artist, album)
                # Temporär Output-Pfad für dieses Album ändern
                original_output = self.spotdl.downloader.settings['output']
                self.spotdl.downloader.settings['output'] = str(album_folder)
                print(f"📁 Download-Ordner: {album_folder}")
            
            # Lade Album-Metadaten
            print(f"📥 Lade Album-Information...")
            album_metadata, songs = Album.get_metadata(album_url)
            
            if not songs:
                print(f"❌ Keine Songs im Album gefunden")
                return False
            
            print(f"🎵 Gefunden: {len(songs)} Songs")
            print(f"   Album: {album_metadata.get('name', 'Unbekannt')}")
            print(f"   Künstler: {album_metadata.get('artist', {}).get('name', 'Unbekannt')}")
            
            # Lade Songs herunter
            print(f"⬇️  Lade Songs herunter...")
            
            successful = 0
            failed = 0
            
            for i, song in enumerate(songs, 1):
                try:
                    print(f"   [{i}/{len(songs)}] {song.name}", end="")
                    song_result, path = self.spotdl.download(song)
                    
                    if path is not None:
                        print(" ✅")
                        successful += 1
                    else:
                        print(" ❌")
                        failed += 1
                        
                except Exception as e:
                    print(f" ❌ ({e})")
                    failed += 1
            
            # Stelle ursprünglichen Output-Pfad wieder her
            if original_output is not None:
                self.spotdl.downloader.settings['output'] = original_output
            
            if successful > 0:
                print(f"✅ {successful}/{len(songs)} Songs erfolgreich heruntergeladen")
                if failed > 0:
                    print(f"⚠️  {failed} Songs fehlgeschlagen")
                self.tracker.mark_downloaded(album_key)
                return True
            else:
                print(f"❌ Keine Songs konnten heruntergeladen werden")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Download von {album_key}: {e}")
            # Stelle Output-Pfad wieder her auch bei Fehler
            if original_output is not None:
                self.spotdl.downloader.settings['output'] = original_output
            return False
    
    def run(self, json_file: str = "YourLibrary.json") -> None:
        """Hauptmethode zum Ausführen des Downloads."""
        print("🎵 Album Multi-Downloader gestartet")
        print(f"📁 Download-Ordner: {self.config['download']['base_path']}")
        print(f"📊 Bereits heruntergeladen: {self.tracker.get_downloaded_count()} Alben")
        print()
        
        # Lade JSON-Datei
        print(f"📖 Lade Bibliothek aus {json_file}...")
        tracks = self._load_library_json(json_file)
        print(f"🎵 {len(tracks)} Tracks gefunden")
        
        # Gruppiere nach Alben
        albums = self._group_tracks_by_album(tracks)
        print(f"💿 {len(albums)} einzigartige Alben identifiziert")
        print()
        
        # Download-Statistiken
        total_albums = len(albums)
        successful_downloads = 0
        skipped_albums = 0
        failed_downloads = 0
        
        for i, (album_key, album_tracks) in enumerate(albums.items(), 1):
            print(f"[{i}/{total_albums}] ", end="")
            
            if self.config['tracking']['skip_existing'] and self.tracker.is_downloaded(album_key):
                skipped_albums += 1
                print(f"⏭️  Album bereits heruntergeladen: {album_key}")
                continue
            
            success = self._download_album(album_key, album_tracks)
            
            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Kurze Pause zwischen Downloads
            time.sleep(1)
        
        # Finale Statistiken
        print(f"\n{'='*60}")
        print(f"📊 Download-Statistiken:")
        print(f"   ✅ Erfolgreich: {successful_downloads}")
        print(f"   ⏭️  Übersprungen: {skipped_albums}")
        print(f"   ❌ Fehlgeschlagen: {failed_downloads}")
        print(f"   📊 Gesamt: {total_albums}")
        print(f"{'='*60}")

def main():
    """Hauptfunktion."""
    try:
        # Lade oder erstelle Konfiguration
        try:
            config = load_config()
            print("✓ Konfiguration geladen")
        except FileNotFoundError:
            print("❓ Keine Konfiguration gefunden. Starte Setup...")
            config = setup_config()
        
        # Starte Downloader
        downloader = AlbumMultiDownloader(config)
        
        # Prüfe ob JSON-Datei existiert
        json_file = "YourLibrary.json"
        if len(sys.argv) > 1:
            json_file = sys.argv[1]
        
        if not os.path.exists(json_file):
            print(f"❌ JSON-Datei nicht gefunden: {json_file}")
            print("Verwende: python album_multi_downloader.py [json_datei]")
            sys.exit(1)
        
        downloader.run(json_file)
        
    except KeyboardInterrupt:
        print("\n⏹️  Download abgebrochen.")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
