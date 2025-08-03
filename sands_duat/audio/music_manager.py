"""
Music Manager for Sands of Duat

Manages background music, atmospheric tracks, and adaptive audio
for different game states and contexts.
"""

import pygame
import threading
import time
import logging
from typing import Dict, Optional, List, Callable
from enum import Enum
from pathlib import Path


class MusicState(Enum):
    """Music playback states."""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    FADING_IN = "fading_in"
    FADING_OUT = "fading_out"
    CROSSFADING = "crossfading"


class MusicTrack:
    """Represents a music track with metadata."""
    
    def __init__(self, name: str, file_path: str, loop: bool = True, 
                 intro_length: float = 0.0, mood: str = "neutral"):
        self.name = name
        self.file_path = file_path
        self.loop = loop
        self.intro_length = intro_length
        self.mood = mood
        self.loaded = False


class MusicManager:
    """
    Advanced music management system with adaptive features.
    
    Provides seamless music transitions, dynamic mood matching,
    and contextual audio experiences.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Music library
        self.tracks: Dict[str, MusicTrack] = {}
        self.playlists: Dict[str, List[str]] = {}
        
        # Playback state
        self.current_track: Optional[MusicTrack] = None
        self.current_state = MusicState.STOPPED
        self.current_volume = 0.7
        self.target_volume = 0.7
        self.is_muted = False
        
        # Adaptive features
        self.mood_transition_enabled = True
        self.current_mood = "neutral"
        self.mood_weights: Dict[str, float] = {}
        
        # Threading for smooth transitions
        self.fade_thread: Optional[threading.Thread] = None
        self.fade_active = False
        
        # Initialize default tracks
        self._setup_default_tracks()
        self._setup_playlists()
        
        self.logger.info("Music Manager initialized")
    
    def _setup_default_tracks(self) -> None:
        """Set up default music tracks."""
        # Define themed tracks for the Egyptian setting
        default_tracks = [
            MusicTrack("main_menu", "music/desert_winds.ogg", True, 0.0, "peaceful"),
            MusicTrack("combat_intro", "music/battle_preparation.ogg", False, 5.0, "tense"),
            MusicTrack("combat_main", "music/battle_drums.ogg", True, 0.0, "intense"),
            MusicTrack("victory", "music/triumph_fanfare.ogg", False, 0.0, "triumphant"),
            MusicTrack("defeat", "music/lament.ogg", False, 0.0, "somber"),
            MusicTrack("exploration", "music/ancient_mysteries.ogg", True, 2.0, "mysterious"),
            MusicTrack("temple", "music/sacred_chambers.ogg", True, 0.0, "reverent"),
            MusicTrack("boss_battle", "music/pharaoh_wrath.ogg", True, 3.0, "epic"),
            MusicTrack("ending", "music/eternal_rest.ogg", False, 0.0, "peaceful")
        ]
        
        for track in default_tracks:
            self.tracks[track.name] = track
        
        self.logger.debug(f"Set up {len(self.tracks)} default music tracks")
    
    def _setup_playlists(self) -> None:
        """Set up contextual playlists."""
        self.playlists = {
            "menu": ["main_menu"],
            "combat": ["combat_intro", "combat_main"],
            "exploration": ["exploration", "temple"],
            "boss_fights": ["boss_battle"],
            "endings": ["victory", "defeat", "ending"],
            "peaceful": ["main_menu", "temple", "ending"],
            "intense": ["combat_main", "boss_battle"],
            "atmospheric": ["exploration", "temple"]
        }
    
    def add_track(self, track: MusicTrack) -> None:
        """Add a track to the music library."""
        self.tracks[track.name] = track
        self.logger.debug(f"Added music track: {track.name}")
    
    def play_track(self, track_name: str, fade_in_ms: int = 1000, 
                   volume: Optional[float] = None) -> bool:
        """
        Play a specific music track.
        
        Args:
            track_name: Name of the track to play
            fade_in_ms: Fade in duration in milliseconds
            volume: Volume override (0.0 to 1.0)
            
        Returns:
            True if track started successfully
        """
        if track_name not in self.tracks:
            self.logger.warning(f"Music track not found: {track_name}")
            return False
        
        track = self.tracks[track_name]
        
        # Stop current track if playing
        if self.current_state != MusicState.STOPPED:
            self.stop_track(fade_out_ms=500)
            time.sleep(0.5)  # Wait for fade out
        
        try:
            # Load and play track
            track_path = Path(__file__).parent.parent / "assets" / "audio" / track.file_path
            
            if track_path.exists():
                pygame.mixer.music.load(str(track_path))
                loops = -1 if track.loop else 0
                
                # Set volume
                play_volume = volume if volume is not None else self.current_volume
                if not self.is_muted:
                    pygame.mixer.music.set_volume(0.0)  # Start silent for fade in
                    pygame.mixer.music.play(loops)
                    self._fade_to_volume(play_volume, fade_in_ms)
                else:
                    pygame.mixer.music.set_volume(0.0)
                    pygame.mixer.music.play(loops)
                
                self.current_track = track
                self.current_state = MusicState.FADING_IN if fade_in_ms > 0 else MusicState.PLAYING
                self.current_mood = track.mood
                
                self.logger.info(f"Started music track: {track_name}")
                return True
            else:
                self.logger.warning(f"Music file not found: {track_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to play music track {track_name}: {e}")
            return False
    
    def stop_track(self, fade_out_ms: int = 1000) -> None:
        """Stop the current music track."""
        if self.current_state == MusicState.STOPPED:
            return
        
        if fade_out_ms > 0:
            self.current_state = MusicState.FADING_OUT
            self._fade_to_volume(0.0, fade_out_ms, lambda: self._complete_stop())
        else:
            self._complete_stop()
    
    def _complete_stop(self) -> None:
        """Complete the music stop process."""
        pygame.mixer.music.stop()
        self.current_track = None
        self.current_state = MusicState.STOPPED
        self.logger.debug("Music stopped")
    
    def pause_track(self) -> None:
        """Pause the current music track."""
        if self.current_state == MusicState.PLAYING:
            pygame.mixer.music.pause()
            self.current_state = MusicState.PAUSED
            self.logger.debug("Music paused")
    
    def resume_track(self) -> None:
        """Resume the paused music track."""
        if self.current_state == MusicState.PAUSED:
            pygame.mixer.music.unpause()
            self.current_state = MusicState.PLAYING
            self.logger.debug("Music resumed")
    
    def crossfade_to_track(self, track_name: str, crossfade_ms: int = 2000) -> bool:
        """
        Crossfade from current track to a new track.
        
        Args:
            track_name: Name of the track to crossfade to
            crossfade_ms: Crossfade duration in milliseconds
            
        Returns:
            True if crossfade started successfully
        """
        if track_name not in self.tracks:
            self.logger.warning(f"Music track not found for crossfade: {track_name}")
            return False
        
        if self.current_state == MusicState.STOPPED:
            # No current track, just play the new one
            return self.play_track(track_name, crossfade_ms // 2)
        
        # Start crossfade process
        self.current_state = MusicState.CROSSFADING
        old_volume = self.current_volume
        
        # Fade out current track
        fade_out_thread = threading.Thread(
            target=self._fade_to_volume,
            args=(0.0, crossfade_ms // 2, lambda: self._start_crossfade_new_track(track_name, old_volume, crossfade_ms // 2))
        )
        fade_out_thread.daemon = True
        fade_out_thread.start()
        
        return True
    
    def _start_crossfade_new_track(self, track_name: str, target_volume: float, fade_in_ms: int) -> None:
        """Start the new track in a crossfade."""
        self.play_track(track_name, fade_in_ms, target_volume)
    
    def set_volume(self, volume: float, fade_ms: int = 0) -> None:
        """
        Set music volume.
        
        Args:
            volume: Target volume (0.0 to 1.0)
            fade_ms: Fade duration in milliseconds
        """
        target_volume = max(0.0, min(1.0, volume))
        self.target_volume = target_volume
        
        if not self.is_muted:
            if fade_ms > 0:
                self._fade_to_volume(target_volume, fade_ms)
            else:
                self.current_volume = target_volume
                pygame.mixer.music.set_volume(self.current_volume)
    
    def mute(self) -> None:
        """Mute the music."""
        self.is_muted = True
        pygame.mixer.music.set_volume(0.0)
        self.logger.debug("Music muted")
    
    def unmute(self) -> None:
        """Unmute the music."""
        self.is_muted = False
        pygame.mixer.music.set_volume(self.current_volume)
        self.logger.debug("Music unmuted")
    
    def _fade_to_volume(self, target_volume: float, fade_ms: int, callback: Optional[Callable] = None) -> None:
        """
        Fade music to a target volume.
        
        Args:
            target_volume: Target volume (0.0 to 1.0)
            fade_ms: Fade duration in milliseconds
            callback: Function to call when fade completes
        """
        if self.fade_active:
            return  # Already fading
        
        def fade_worker():
            self.fade_active = True
            start_volume = self.current_volume
            start_time = time.time()
            fade_duration = fade_ms / 1000.0
            
            try:
                while time.time() - start_time < fade_duration and self.fade_active:
                    elapsed = time.time() - start_time
                    progress = elapsed / fade_duration
                    
                    # Smooth interpolation
                    current_vol = start_volume + (target_volume - start_volume) * progress
                    self.current_volume = current_vol
                    
                    if not self.is_muted:
                        pygame.mixer.music.set_volume(current_vol)
                    
                    time.sleep(0.01)  # 10ms update rate
                
                # Ensure final volume is set
                self.current_volume = target_volume
                if not self.is_muted:
                    pygame.mixer.music.set_volume(target_volume)
                
                if callback:
                    callback()
                    
            except Exception as e:
                self.logger.error(f"Error during volume fade: {e}")
            finally:
                self.fade_active = False
        
        self.fade_thread = threading.Thread(target=fade_worker)
        self.fade_thread.daemon = True
        self.fade_thread.start()
    
    def play_playlist(self, playlist_name: str, shuffle: bool = False) -> bool:
        """
        Play a playlist.
        
        Args:
            playlist_name: Name of the playlist
            shuffle: Whether to shuffle the playlist
            
        Returns:
            True if playlist started successfully
        """
        if playlist_name not in self.playlists:
            self.logger.warning(f"Playlist not found: {playlist_name}")
            return False
        
        tracks = self.playlists[playlist_name].copy()
        if shuffle:
            import random
            random.shuffle(tracks)
        
        if tracks:
            return self.play_track(tracks[0])
        
        return False
    
    def set_mood_adaptive_mode(self, enabled: bool) -> None:
        """Enable or disable adaptive mood-based music selection."""
        self.mood_transition_enabled = enabled
        self.logger.info(f"Mood adaptive mode: {'enabled' if enabled else 'disabled'}")
    
    def update_mood_weights(self, mood_weights: Dict[str, float]) -> None:
        """Update mood weights for adaptive music selection."""
        self.mood_weights = mood_weights.copy()
        
        if self.mood_transition_enabled:
            self._evaluate_mood_transition()
    
    def _evaluate_mood_transition(self) -> None:
        """Evaluate if a mood-based music transition should occur."""
        if not self.mood_weights or not self.current_track:
            return
        
        # Find the strongest mood
        dominant_mood = max(self.mood_weights.items(), key=lambda x: x[1])
        mood_name, mood_strength = dominant_mood
        
        # If mood has changed significantly, consider transition
        if (mood_name != self.current_mood and 
            mood_strength > 0.7 and 
            self.current_state == MusicState.PLAYING):
            
            # Find a track that matches the new mood
            suitable_tracks = [name for name, track in self.tracks.items() 
                             if track.mood == mood_name]
            
            if suitable_tracks and suitable_tracks[0] != self.current_track.name:
                self.logger.info(f"Adaptive mood transition: {self.current_mood} -> {mood_name}")
                self.crossfade_to_track(suitable_tracks[0], 3000)
    
    def get_music_info(self) -> Dict[str, any]:
        """Get current music system information."""
        return {
            "current_track": self.current_track.name if self.current_track else None,
            "current_state": self.current_state.value,
            "current_volume": self.current_volume,
            "current_mood": self.current_mood,
            "is_muted": self.is_muted,
            "tracks_loaded": len(self.tracks),
            "playlists_available": len(self.playlists),
            "mood_adaptive_enabled": self.mood_transition_enabled
        }
    
    def cleanup(self) -> None:
        """Clean up music manager resources."""
        self.fade_active = False
        if self.fade_thread and self.fade_thread.is_alive():
            self.fade_thread.join(timeout=1.0)
        
        pygame.mixer.music.stop()
        self.logger.info("Music Manager cleaned up")