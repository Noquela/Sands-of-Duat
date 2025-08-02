"""
Enhanced Hot Reload Manager

Monitors content files for changes and automatically reloads them
during development for rapid iteration without restarting the game.

Features:
- Intelligent change detection with debouncing
- Partial reloading of specific files
- Validation integration with real-time error reporting
- Performance optimization for large content libraries
- Cross-reference validation on reload
"""

import asyncio
import logging
import time
import hashlib
from pathlib import Path
from typing import Callable, Dict, Optional, Set, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
from dataclasses import dataclass
from threading import Lock, Timer

from .loader import ContentLoader, ContentType
from .validator import ContentValidator, ValidationReport
from .cross_reference_validator import CrossReferenceValidator


@dataclass
class FileChangeEvent:
    """Represents a file change event with metadata."""
    file_path: Path
    event_type: str  # 'modified', 'created', 'deleted'
    timestamp: float
    file_hash: Optional[str] = None


class ContentFileHandler(FileSystemEventHandler):
    """Enhanced file system event handler with debouncing and change detection."""
    
    def __init__(self, reload_callback: Callable[[FileChangeEvent], None], debounce_delay: float = 0.5):
        self.reload_callback = reload_callback
        self.logger = logging.getLogger(__name__)
        self.debounce_delay = debounce_delay
        self.pending_changes: Dict[str, Timer] = {}
        self.file_hashes: Dict[str, str] = {}
        self.lock = Lock()
    
    def on_modified(self, event):
        self._handle_event(event, 'modified')
    
    def on_created(self, event):
        self._handle_event(event, 'created')
    
    def on_deleted(self, event):
        self._handle_event(event, 'deleted')
    
    def _handle_event(self, event, event_type: str):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix not in ['.yaml', '.yml']:
            return
        
        # Calculate file hash for change detection
        file_hash = None
        if event_type != 'deleted' and file_path.exists():
            try:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                # Check if file actually changed
                if file_path.as_posix() in self.file_hashes:
                    if self.file_hashes[file_path.as_posix()] == file_hash:
                        return  # No actual change
                
                self.file_hashes[file_path.as_posix()] = file_hash
            except Exception as e:
                self.logger.warning(f"Could not calculate hash for {file_path}: {e}")
        
        change_event = FileChangeEvent(
            file_path=file_path,
            event_type=event_type,
            timestamp=time.time(),
            file_hash=file_hash
        )
        
        self._debounce_change(change_event)
    
    def _debounce_change(self, change_event: FileChangeEvent):
        """Debounce file changes to avoid multiple rapid reloads."""
        file_key = change_event.file_path.as_posix()
        
        with self.lock:
            # Cancel existing timer for this file
            if file_key in self.pending_changes:
                self.pending_changes[file_key].cancel()
            
            # Set new timer
            timer = Timer(self.debounce_delay, self._execute_reload, args=[change_event])
            self.pending_changes[file_key] = timer
            timer.start()
    
    def _execute_reload(self, change_event: FileChangeEvent):
        """Execute the actual reload after debounce delay."""
        file_key = change_event.file_path.as_posix()
        
        with self.lock:
            if file_key in self.pending_changes:
                del self.pending_changes[file_key]
        
        self.logger.info(f"Content file {change_event.event_type}: {change_event.file_path}")
        self.reload_callback(change_event)


class HotReloadManager:
    """
    Enhanced hot reload manager with validation and optimization.
    
    Monitors content directories for changes and automatically
    reloads modified files with validation and cross-reference checking.
    """
    
    def __init__(self, content_loader: ContentLoader, enable_validation: bool = True):
        self.content_loader = content_loader
        self.observer = Observer()
        self.is_watching = False
        self.reload_callbacks: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)
        
        # Validation components
        self.enable_validation = enable_validation
        self.validator = ContentValidator(enable_performance_tracking=True) if enable_validation else None
        self.cross_validator = CrossReferenceValidator(enable_performance_tracking=True) if enable_validation else None
        
        # Performance tracking
        self.reload_count = 0
        self.total_reload_time = 0.0
        self.last_validation_report: Optional[ValidationReport] = None
        
        # File tracking
        self.watched_files: Set[Path] = set()
        self.file_modification_times: Dict[str, float] = {}
    
    def start_watching(self, debounce_delay: float = 0.5) -> None:
        """Start watching content directories for changes."""
        if self.is_watching:
            return
        
        handler = ContentFileHandler(self._on_file_changed, debounce_delay)
        
        # Watch all content subdirectories
        for content_type in ContentType:
            directory = self.content_loader.content_root / content_type.value
            if directory.exists():
                self.observer.schedule(handler, str(directory), recursive=True)
                self._scan_directory_for_files(directory)
                self.logger.info(f"Watching directory: {directory}")
        
        self.observer.start()
        self.is_watching = True
        self.logger.info(f"Hot reload monitoring started (validation: {self.enable_validation})")
        
        # Initial validation if enabled
        if self.enable_validation:
            self._perform_full_validation()
    
    def _scan_directory_for_files(self, directory: Path) -> None:
        """Scan directory and track all YAML files."""
        for file_path in directory.rglob('*.yaml'):
            self.watched_files.add(file_path)
            try:
                self.file_modification_times[file_path.as_posix()] = file_path.stat().st_mtime
            except OSError:
                pass
        
        for file_path in directory.rglob('*.yml'):
            self.watched_files.add(file_path)
            try:
                self.file_modification_times[file_path.as_posix()] = file_path.stat().st_mtime
            except OSError:
                pass
    
    def stop_watching(self) -> None:
        """Stop watching for file changes."""
        if not self.is_watching:
            return
        
        self.observer.stop()
        self.observer.join()
        self.is_watching = False
        self.logger.info("Hot reload monitoring stopped")
    
    def register_reload_callback(self, callback_name: str, callback: Callable) -> None:
        """Register a callback to be called when content is reloaded."""
        self.reload_callbacks[callback_name] = callback
        self.logger.debug(f"Registered reload callback: {callback_name}")
    
    def unregister_reload_callback(self, callback_name: str) -> None:
        """Unregister a reload callback."""
        if callback_name in self.reload_callbacks:
            del self.reload_callbacks[callback_name]
            self.logger.debug(f"Unregistered reload callback: {callback_name}")
    
    def _on_file_changed(self, change_event: FileChangeEvent) -> None:
        """Handle when a content file is changed."""
        start_time = time.time()
        file_path = change_event.file_path
        
        try:
            # Determine content type from file path
            content_type = self._get_content_type_from_path(file_path)
            if not content_type:
                self.logger.warning(f"Could not determine content type for {file_path}")
                return
            
            # Handle different event types
            if change_event.event_type == 'deleted':
                self._handle_file_deletion(file_path, content_type)
            else:
                self._handle_file_modification(file_path, content_type, change_event)
            
            # Update tracking
            self.reload_count += 1
            reload_time = time.time() - start_time
            self.total_reload_time += reload_time
            
            # Performance validation if enabled
            if self.enable_validation:
                self._perform_incremental_validation(content_type, file_path)
            
            # Call registered callbacks
            for callback_name, callback in self.reload_callbacks.items():
                try:
                    callback(content_type, file_path, change_event)
                except Exception as e:
                    self.logger.error(f"Error in reload callback '{callback_name}': {e}")
            
            self.logger.info(f"Reloaded {content_type.value} from {file_path.name} in {reload_time:.3f}s")
        
        except Exception as e:
            self.logger.error(f"Error processing file change {file_path}: {e}")
    
    def _handle_file_modification(self, file_path: Path, content_type: ContentType, change_event: FileChangeEvent) -> None:
        """Handle file modification or creation."""
        # Update modification time tracking
        if file_path.exists():
            self.file_modification_times[file_path.as_posix()] = file_path.stat().st_mtime
            self.watched_files.add(file_path)
        
        # Reload the specific content type
        self.content_loader.load_content_directory(content_type)
    
    def _handle_file_deletion(self, file_path: Path, content_type: ContentType) -> None:
        """Handle file deletion."""
        # Remove from tracking
        self.watched_files.discard(file_path)
        file_key = file_path.as_posix()
        if file_key in self.file_modification_times:
            del self.file_modification_times[file_key]
        
        # Reload the content type to reflect deletion
        self.content_loader.load_content_directory(content_type)
        self.logger.info(f"File deleted: {file_path}")
    
    def _perform_full_validation(self) -> None:
        """Perform full validation of all content."""
        if not self.validator or not self.cross_validator:
            return
        
        try:
            # Load all content
            all_content = {
                'cards': {},
                'enemies': {},
                'events': {},
                'decks': {}
            }
            
            for content_type in ContentType:
                content = self.content_loader.get_content(content_type, reload=True)
                if content_type == ContentType.CARDS:
                    all_content['cards'] = content
                elif content_type == ContentType.ENEMIES:
                    all_content['enemies'] = content
                elif content_type == ContentType.EVENTS:
                    all_content['events'] = content
                elif content_type == ContentType.DECKS:
                    all_content['decks'] = content
            
            # Populate cross-reference database
            self.cross_validator.populate_database(
                all_content['cards'], all_content['enemies'],
                all_content['events'], all_content['decks']
            )
            
            # Validate cross-references
            self.last_validation_report = self.cross_validator.validate_all_cross_references()
            
            # Log validation results
            if self.last_validation_report.is_valid:
                self.logger.info("✅ Full validation passed")
            else:
                self.logger.warning(f"⚠️ Validation found {len(self.last_validation_report.errors)} errors and {len(self.last_validation_report.warnings)} warnings")
                
                # Log first few errors
                for error in self.last_validation_report.errors[:3]:
                    self.logger.error(f"  - {error.message}")
                
                if len(self.last_validation_report.errors) > 3:
                    self.logger.error(f"  ... and {len(self.last_validation_report.errors) - 3} more errors")
        
        except Exception as e:
            self.logger.error(f"Error during full validation: {e}")
    
    def _perform_incremental_validation(self, content_type: ContentType, file_path: Path) -> None:
        """Perform incremental validation of changed content."""
        if not self.validator:
            return
        
        try:
            report = self.validator.validate_content_file(file_path, content_type)
            
            if report.is_valid:
                self.logger.debug(f"✅ {file_path.name} validation passed")
            else:
                self.logger.warning(f"⚠️ {file_path.name} validation found issues")
                for error in report.errors:
                    self.logger.error(f"  - {error.message}")
                for warning in report.warnings:
                    self.logger.warning(f"  - {warning.message}")
        
        except Exception as e:
            self.logger.error(f"Error during incremental validation of {file_path}: {e}")
    
    def _get_content_type_from_path(self, file_path: Path) -> Optional[ContentType]:
        """Determine content type from file path."""
        for content_type in ContentType:
            content_dir = self.content_loader.content_root / content_type.value
            try:
                file_path.relative_to(content_dir)
                return content_type
            except ValueError:
                continue
        return None
    
    def get_reload_statistics(self) -> Dict[str, Any]:
        """Get statistics about reload operations."""
        avg_reload_time = self.total_reload_time / max(self.reload_count, 1)
        
        stats = {
            'total_reloads': self.reload_count,
            'total_reload_time': self.total_reload_time,
            'average_reload_time': avg_reload_time,
            'watched_files_count': len(self.watched_files),
            'is_watching': self.is_watching,
            'validation_enabled': self.enable_validation
        }
        
        if self.last_validation_report:
            stats['last_validation'] = {
                'is_valid': self.last_validation_report.is_valid,
                'errors': len(self.last_validation_report.errors),
                'warnings': len(self.last_validation_report.warnings),
                'total_issues': self.last_validation_report.total_issues
            }
        
        return stats
    
    def force_reload_all(self) -> None:
        """Force reload of all content regardless of file changes."""
        self.logger.info("Force reloading all content...")
        start_time = time.time()
        
        for content_type in ContentType:
            self.content_loader.load_content_directory(content_type)
        
        if self.enable_validation:
            self._perform_full_validation()
        
        reload_time = time.time() - start_time
        self.logger.info(f"Force reload completed in {reload_time:.3f}s")
    
    def get_validation_report(self) -> Optional[ValidationReport]:
        """Get the last validation report."""
        return self.last_validation_report
    
    def enable_validation_mode(self) -> None:
        """Enable validation during hot reload."""
        if not self.enable_validation:
            self.enable_validation = True
            self.validator = ContentValidator(enable_performance_tracking=True)
            self.cross_validator = CrossReferenceValidator(enable_performance_tracking=True)
            self.logger.info("Validation mode enabled")
            
            if self.is_watching:
                self._perform_full_validation()
    
    def disable_validation_mode(self) -> None:
        """Disable validation during hot reload for better performance."""
        if self.enable_validation:
            self.enable_validation = False
            self.validator = None
            self.cross_validator = None
            self.last_validation_report = None
            self.logger.info("Validation mode disabled")
    
    def get_watched_files(self) -> Set[Path]:
        """Get set of all watched files."""
        return self.watched_files.copy()
    
    def is_file_being_watched(self, file_path: Path) -> bool:
        """Check if a specific file is being watched."""
        return file_path in self.watched_files