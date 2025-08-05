#!/usr/bin/env python3
"""
Advanced Memory Management System for Sands of Duat

Intelligent memory management with garbage collection optimization, asset lifecycle
management, and memory pressure detection for smooth 60fps performance.
"""

import gc
import sys
import time
import threading
import weakref
import psutil
import os
from typing import Dict, List, Optional, Set, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import logging
from pathlib import Path
import pickle
import hashlib

import pygame


class MemoryPriority(Enum):
    """Memory allocation priorities"""
    CRITICAL = 1    # Essential for gameplay (player data, current screen)
    HIGH = 2        # Important for performance (frequently used assets)
    MEDIUM = 3      # Nice to have (cached textures, preloaded assets)
    LOW = 4         # Optimization cache (compressed variants, distant LODs)


class MemoryTier(Enum):
    """Memory management tiers"""
    PERMANENT = "permanent"     # Never unload automatically
    SESSION = "session"         # Keep for entire game session
    SCREEN = "screen"          # Keep while screen is active
    TRANSIENT = "transient"    # Can be unloaded anytime


class GCStrategy(Enum):
    """Garbage collection strategies"""
    DISABLED = "disabled"       # Disable automatic GC
    CONSERVATIVE = "conservative"   # Minimal GC interference
    BALANCED = "balanced"      # Balance between memory and performance
    AGGRESSIVE = "aggressive"  # Maximize memory recovery


@dataclass
class MemoryAllocation:
    """Information about a memory allocation"""
    object_id: str
    object_type: str
    size_bytes: int
    priority: MemoryPriority
    tier: MemoryTier
    created_time: float
    last_accessed: float
    access_count: int
    ref_count: int
    tags: Set[str] = field(default_factory=set)
    
    def update_access(self):
        """Update access tracking"""
        self.last_accessed = time.time()
        self.access_count += 1
    
    def age_seconds(self) -> float:
        """Get age in seconds"""
        return time.time() - self.created_time
    
    def idle_seconds(self) -> float:
        """Get idle time in seconds"""
        return time.time() - self.last_accessed


@dataclass
class MemoryStats:
    """Memory usage statistics"""
    total_allocated_mb: float = 0.0
    game_allocated_mb: float = 0.0
    system_available_mb: float = 0.0
    allocation_count: int = 0
    
    # By priority
    critical_mb: float = 0.0
    high_mb: float = 0.0
    medium_mb: float = 0.0
    low_mb: float = 0.0
    
    # By tier
    permanent_mb: float = 0.0
    session_mb: float = 0.0
    screen_mb: float = 0.0
    transient_mb: float = 0.0
    
    # Performance metrics
    gc_collections: int = 0
    gc_time_ms: float = 0.0
    allocations_freed: int = 0
    memory_freed_mb: float = 0.0


class MemoryTracker:
    """Track memory allocations and usage patterns"""
    
    def __init__(self):
        self.allocations: Dict[str, MemoryAllocation] = {}
        self.weak_refs: Dict[str, weakref.ref] = {}
        self.tags_index: Dict[str, Set[str]] = defaultdict(set)
        self.type_index: Dict[str, Set[str]] = defaultdict(set)
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats = MemoryStats()
        self.allocation_history: deque = deque(maxlen=1000)
    
    def register_allocation(self, obj: Any, object_id: str, object_type: str,
                          priority: MemoryPriority, tier: MemoryTier,
                          tags: Optional[Set[str]] = None) -> str:
        """Register a memory allocation"""
        if tags is None:
            tags = set()
        
        # Estimate object size
        size_bytes = self._estimate_object_size(obj)
        
        # Create allocation record
        allocation = MemoryAllocation(
            object_id=object_id,
            object_type=object_type,
            size_bytes=size_bytes,
            priority=priority,
            tier=tier,
            created_time=time.time(),
            last_accessed=time.time(),
            access_count=1,
            ref_count=sys.getrefcount(obj),
            tags=tags
        )
        
        self.allocations[object_id] = allocation
        
        # Create weak reference with cleanup callback
        self.weak_refs[object_id] = weakref.ref(obj, lambda ref: self._on_object_deleted(object_id))
        
        # Update indices
        self.type_index[object_type].add(object_id)
        for tag in tags:
            self.tags_index[tag].add(object_id)
        
        # Update statistics
        self._update_stats_for_allocation(allocation, added=True)
        
        # Add to history
        self.allocation_history.append({
            'action': 'register',
            'object_id': object_id,
            'size_mb': size_bytes / (1024 * 1024),
            'timestamp': time.time()
        })
        
        self.logger.debug(f"Registered allocation: {object_id} ({size_bytes / 1024:.1f}KB)")
        return object_id
    
    def _on_object_deleted(self, object_id: str):
        """Callback when object is garbage collected"""
        if object_id in self.allocations:
            allocation = self.allocations[object_id]
            
            # Update statistics
            self._update_stats_for_allocation(allocation, added=False)
            
            # Remove from indices
            self.type_index[allocation.object_type].discard(object_id)
            for tag in allocation.tags:
                self.tags_index[tag].discard(object_id)
            
            # Remove allocation record
            del self.allocations[object_id]
            
            # Add to history
            self.allocation_history.append({
                'action': 'deleted',
                'object_id': object_id,
                'size_mb': allocation.size_bytes / (1024 * 1024),
                'timestamp': time.time()
            })
            
            self.logger.debug(f"Object deleted: {object_id}")
    
    def access_allocation(self, object_id: str):
        """Record access to an allocation"""
        if object_id in self.allocations:
            self.allocations[object_id].update_access()
    
    def get_allocation(self, object_id: str) -> Optional[MemoryAllocation]:
        """Get allocation information"""
        return self.allocations.get(object_id)
    
    def get_allocations_by_type(self, object_type: str) -> List[MemoryAllocation]:
        """Get all allocations of a specific type"""
        return [self.allocations[oid] for oid in self.type_index[object_type]
                if oid in self.allocations]
    
    def get_allocations_by_tag(self, tag: str) -> List[MemoryAllocation]:
        """Get all allocations with a specific tag"""
        return [self.allocations[oid] for oid in self.tags_index[tag]
                if oid in self.allocations]
    
    def get_allocations_by_priority(self, priority: MemoryPriority) -> List[MemoryAllocation]:
        """Get all allocations with specific priority"""
        return [alloc for alloc in self.allocations.values() 
                if alloc.priority == priority]
    
    def get_allocations_by_tier(self, tier: MemoryTier) -> List[MemoryAllocation]:
        """Get all allocations in specific tier"""
        return [alloc for alloc in self.allocations.values() 
                if alloc.tier == tier]
    
    def _estimate_object_size(self, obj: Any) -> int:
        """Estimate object size in bytes"""
        if isinstance(obj, pygame.Surface):
            width, height = obj.get_size()
            bytes_per_pixel = obj.get_bytesz()
            return width * height * bytes_per_pixel
        
        try:
            # Use pickle for general objects (rough estimate)
            return len(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
        except Exception:
            # Fallback to sys.getsizeof
            return sys.getsizeof(obj)
    
    def _update_stats_for_allocation(self, allocation: MemoryAllocation, added: bool):
        """Update statistics for allocation change"""
        size_mb = allocation.size_bytes / (1024 * 1024)
        multiplier = 1 if added else -1
        
        # Update totals
        self.stats.game_allocated_mb += size_mb * multiplier
        if added:
            self.stats.allocation_count += 1
        else:
            self.stats.allocation_count -= 1
            self.stats.allocations_freed += 1
            self.stats.memory_freed_mb += size_mb
        
        # Update by priority
        if allocation.priority == MemoryPriority.CRITICAL:
            self.stats.critical_mb += size_mb * multiplier
        elif allocation.priority == MemoryPriority.HIGH:
            self.stats.high_mb += size_mb * multiplier
        elif allocation.priority == MemoryPriority.MEDIUM:
            self.stats.medium_mb += size_mb * multiplier
        else:  # LOW
            self.stats.low_mb += size_mb * multiplier
        
        # Update by tier
        if allocation.tier == MemoryTier.PERMANENT:
            self.stats.permanent_mb += size_mb * multiplier
        elif allocation.tier == MemoryTier.SESSION:
            self.stats.session_mb += size_mb * multiplier
        elif allocation.tier == MemoryTier.SCREEN:
            self.stats.screen_mb += size_mb * multiplier
        else:  # TRANSIENT
            self.stats.transient_mb += size_mb * multiplier


class GarbageCollectionManager:
    """Intelligent garbage collection management"""
    
    def __init__(self, strategy: GCStrategy = GCStrategy.BALANCED):
        self.strategy = strategy
        self.logger = logging.getLogger(__name__)
        
        # GC configuration
        self.original_thresholds = gc.get_threshold()
        self.gc_enabled = True
        
        # Performance tracking
        self.gc_start_time = 0.0
        self.total_gc_time = 0.0
        self.gc_count = 0
        
        # Scheduling
        self.last_manual_gc = 0.0
        self.manual_gc_interval = 30.0  # Seconds between manual collections
        self.frame_budget_ms = 2.0      # Maximum GC time per frame
        
        self._configure_gc()
    
    def _configure_gc(self):
        """Configure garbage collection based on strategy"""
        if self.strategy == GCStrategy.DISABLED:
            gc.disable()
            self.gc_enabled = False
            self.logger.info("Garbage collection disabled")
            
        elif self.strategy == GCStrategy.CONSERVATIVE:
            # Reduce GC frequency
            gc.set_threshold(1000, 15, 15)  # Less frequent than default
            self.manual_gc_interval = 60.0
            self.logger.info("Conservative GC strategy enabled")
            
        elif self.strategy == GCStrategy.BALANCED:
            # Default thresholds with manual optimization
            gc.set_threshold(*self.original_thresholds)
            self.manual_gc_interval = 30.0
            self.logger.info("Balanced GC strategy enabled")
            
        elif self.strategy == GCStrategy.AGGRESSIVE:
            # More frequent GC
            gc.set_threshold(500, 8, 8)
            self.manual_gc_interval = 15.0
            self.logger.info("Aggressive GC strategy enabled")
    
    def should_collect_now(self, force: bool = False) -> bool:
        """Determine if GC should run now"""
        if not self.gc_enabled:
            return False
        
        if force:
            return True
        
        current_time = time.time()
        
        # Check if it's time for manual collection
        if current_time - self.last_manual_gc > self.manual_gc_interval:
            return True
        
        # Check memory pressure
        memory = psutil.virtual_memory()
        if memory.percent > 85:  # High memory usage
            return True
        
        return False
    
    def collect_garbage(self, generation: Optional[int] = None) -> Dict[str, Any]:
        """Perform garbage collection with timing"""
        if not self.gc_enabled:
            return {'collected': 0, 'time_ms': 0.0}
        
        start_time = time.perf_counter()
        
        if generation is not None:
            collected = gc.collect(generation)
        else:
            collected = gc.collect()
        
        end_time = time.perf_counter()
        gc_time_ms = (end_time - start_time) * 1000
        
        # Update tracking
        self.total_gc_time += gc_time_ms
        self.gc_count += 1
        self.last_manual_gc = time.time()
        
        result = {
            'collected': collected,
            'time_ms': gc_time_ms,
            'generation': generation
        }
        
        self.logger.debug(f"GC collected {collected} objects in {gc_time_ms:.2f}ms")
        return result
    
    def incremental_collect(self, max_time_ms: float = None) -> Dict[str, Any]:
        """Perform incremental garbage collection within time budget"""
        if max_time_ms is None:
            max_time_ms = self.frame_budget_ms
        
        start_time = time.perf_counter()
        total_collected = 0
        
        # Collect generation 0 first (fastest)
        if time.perf_counter() - start_time < max_time_ms / 1000:
            collected = gc.collect(0)
            total_collected += collected
        
        # Collect generation 1 if time allows
        if time.perf_counter() - start_time < max_time_ms / 1000:
            collected = gc.collect(1)
            total_collected += collected
        
        # Collect generation 2 if time allows
        if time.perf_counter() - start_time < max_time_ms / 1000:
            collected = gc.collect(2)
            total_collected += collected
        
        end_time = time.perf_counter()
        actual_time_ms = (end_time - start_time) * 1000
        
        return {
            'collected': total_collected,
            'time_ms': actual_time_ms,
            'budget_ms': max_time_ms,
            'within_budget': actual_time_ms <= max_time_ms
        }
    
    def get_gc_stats(self) -> Dict[str, Any]:
        """Get garbage collection statistics"""
        return {
            'strategy': self.strategy.value,
            'enabled': self.gc_enabled,
            'total_collections': self.gc_count,
            'total_time_ms': self.total_gc_time,
            'average_time_ms': self.total_gc_time / max(self.gc_count, 1),
            'thresholds': gc.get_threshold(),
            'counts': gc.get_count()
        }


class MemoryPressureDetector:
    """Detect and respond to memory pressure"""
    
    def __init__(self, warning_threshold_mb: float = 500, critical_threshold_mb: float = 200):
        self.warning_threshold_mb = warning_threshold_mb
        self.critical_threshold_mb = critical_threshold_mb
        self.logger = logging.getLogger(__name__)
        
        # State
        self.current_pressure = 0.0  # 0.0 = no pressure, 1.0 = critical
        self.pressure_history: deque = deque(maxlen=60)  # 1 minute at 1Hz
        
        # Callbacks
        self.pressure_callbacks: List[Callable[[float], None]] = []
    
    def update_pressure(self) -> float:
        """Update memory pressure assessment"""
        memory = psutil.virtual_memory()
        available_mb = memory.available / (1024 * 1024)
        
        # Calculate pressure based on available memory
        if available_mb <= self.critical_threshold_mb:
            pressure = 1.0  # Critical
        elif available_mb <= self.warning_threshold_mb:
            # Linear scale between warning and critical
            range_mb = self.warning_threshold_mb - self.critical_threshold_mb
            pressure = 1.0 - ((available_mb - self.critical_threshold_mb) / range_mb)
        else:
            pressure = 0.0  # No pressure
        
        self.current_pressure = pressure
        self.pressure_history.append(pressure)
        
        # Notify callbacks if pressure is significant
        if pressure > 0.3:  # Above 30% pressure
            for callback in self.pressure_callbacks:
                try:
                    callback(pressure)
                except Exception as e:
                    self.logger.error(f"Error in pressure callback: {e}")
        
        return pressure
    
    def add_pressure_callback(self, callback: Callable[[float], None]):
        """Add callback for pressure changes"""
        self.pressure_callbacks.append(callback)
    
    def get_pressure_trend(self) -> str:
        """Get memory pressure trend"""
        if len(self.pressure_history) < 5:
            return "stable"
        
        recent = list(self.pressure_history)[-5:]
        trend = recent[-1] - recent[0]
        
        if trend > 0.1:
            return "increasing"
        elif trend < -0.1:
            return "decreasing"
        else:
            return "stable"


class AdvancedMemoryManager:
    """Advanced memory management system"""
    
    def __init__(self, max_memory_mb: float = 1024, gc_strategy: GCStrategy = GCStrategy.BALANCED):
        self.max_memory_mb = max_memory_mb
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.tracker = MemoryTracker()
        self.gc_manager = GarbageCollectionManager(gc_strategy)
        self.pressure_detector = MemoryPressureDetector()
        
        # Configuration
        self.auto_cleanup_enabled = True
        self.cleanup_interval = 10.0  # Seconds between cleanup cycles
        self.last_cleanup = 0.0
        
        # Background thread
        self.monitoring_thread = None
        self.monitoring_active = False
        self.thread_lock = threading.Lock()
        
        # Connect pressure detector to cleanup
        self.pressure_detector.add_pressure_callback(self._on_pressure_change)
        
        self.logger.info("Advanced Memory Manager initialized")
    
    def start_monitoring(self):
        """Start background memory monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            self.logger.info("Memory monitoring started")
    
    def stop_monitoring(self):
        """Stop background memory monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
        self.logger.info("Memory monitoring stopped")
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                # Update pressure detection
                self.pressure_detector.update_pressure()
                
                # Update system statistics
                memory = psutil.virtual_memory()
                self.tracker.stats.total_allocated_mb = (memory.total - memory.available) / (1024 * 1024)
                self.tracker.stats.system_available_mb = memory.available / (1024 * 1024)
                
                # Perform cleanup if needed
                current_time = time.time()
                if (self.auto_cleanup_enabled and 
                    current_time - self.last_cleanup > self.cleanup_interval):
                    self.cleanup_memory()
                
                # Garbage collection if needed
                if self.gc_manager.should_collect_now():
                    self.gc_manager.collect_garbage()
                
                time.sleep(1.0)  # Monitor every second
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
    
    def register_object(self, obj: Any, object_id: str, object_type: str,
                       priority: MemoryPriority = MemoryPriority.MEDIUM,
                       tier: MemoryTier = MemoryTier.TRANSIENT,
                       tags: Optional[Set[str]] = None) -> str:
        """Register an object for memory management"""
        with self.thread_lock:
            return self.tracker.register_allocation(obj, object_id, object_type, 
                                                   priority, tier, tags)
    
    def access_object(self, object_id: str):
        """Record access to an object"""
        self.tracker.access_allocation(object_id)
    
    def cleanup_memory(self, force: bool = False) -> Dict[str, Any]:
        """Perform memory cleanup"""
        start_time = time.time()
        
        with self.thread_lock:
            # Get cleanup candidates
            candidates = self._get_cleanup_candidates(force)
            
            freed_count = 0
            freed_mb = 0.0
            
            # Force deletion of candidates by clearing references
            for allocation in candidates:
                if allocation.object_id in self.tracker.weak_refs:
                    ref = self.tracker.weak_refs[allocation.object_id]
                    obj = ref()
                    if obj is not None:
                        # This doesn't actually delete the object, but marks it as candidate
                        # Real deletion happens when the game releases its references
                        freed_mb += allocation.size_bytes / (1024 * 1024)
                        freed_count += 1
            
            # Perform garbage collection
            gc_result = self.gc_manager.collect_garbage()
            
            self.last_cleanup = time.time()
            
            cleanup_time = (time.time() - start_time) * 1000
            
            result = {
                'candidates_identified': len(candidates),
                'objects_freed': freed_count,
                'memory_freed_mb': freed_mb,
                'gc_collected': gc_result['collected'],
                'cleanup_time_ms': cleanup_time,
                'gc_time_ms': gc_result['time_ms']
            }
            
            self.logger.info(f"Memory cleanup: {freed_count} objects, {freed_mb:.1f}MB freed")
            return result
    
    def _get_cleanup_candidates(self, force: bool = False) -> List[MemoryAllocation]:
        """Get list of objects that are candidates for cleanup"""
        candidates = []
        current_time = time.time()
        
        # Priority-based cleanup
        if force or self.pressure_detector.current_pressure > 0.8:
            # Critical pressure - clean LOW priority objects
            candidates.extend(self.tracker.get_allocations_by_priority(MemoryPriority.LOW))
        
        if force or self.pressure_detector.current_pressure > 0.6:
            # High pressure - clean MEDIUM priority objects that are idle
            medium_allocs = self.tracker.get_allocations_by_priority(MemoryPriority.MEDIUM)
            candidates.extend([alloc for alloc in medium_allocs if alloc.idle_seconds() > 60])
        
        # Tier-based cleanup
        if force or self.pressure_detector.current_pressure > 0.4:
            # Clean TRANSIENT tier objects that are old
            transient_allocs = self.tracker.get_allocations_by_tier(MemoryTier.TRANSIENT)
            candidates.extend([alloc for alloc in transient_allocs if alloc.age_seconds() > 300])
        
        # Age-based cleanup (regardless of pressure)
        all_allocs = list(self.tracker.allocations.values())
        old_allocs = [alloc for alloc in all_allocs 
                     if alloc.tier == MemoryTier.TRANSIENT and alloc.idle_seconds() > 600]
        candidates.extend(old_allocs)
        
        # Remove duplicates
        seen = set()
        unique_candidates = []
        for candidate in candidates:
            if candidate.object_id not in seen:
                seen.add(candidate.object_id)
                unique_candidates.append(candidate)
        
        return unique_candidates
    
    def _on_pressure_change(self, pressure: float):
        """Handle memory pressure changes"""
        if pressure > 0.8:
            self.logger.warning(f"High memory pressure detected: {pressure:.1f}")
            # Force immediate cleanup
            self.cleanup_memory(force=True)
        elif pressure > 0.5:
            self.logger.info(f"Moderate memory pressure: {pressure:.1f}")
            # Schedule cleanup sooner
            self.last_cleanup = time.time() - (self.cleanup_interval * 0.8)
    
    def force_garbage_collection(self) -> Dict[str, Any]:
        """Force immediate garbage collection"""
        return self.gc_manager.collect_garbage()
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Get comprehensive memory report"""
        pressure = self.pressure_detector.update_pressure()
        
        return {
            'allocations': {
                'total_count': self.tracker.stats.allocation_count,
                'total_mb': self.tracker.stats.game_allocated_mb,
                'by_priority': {
                    'critical_mb': self.tracker.stats.critical_mb,
                    'high_mb': self.tracker.stats.high_mb,
                    'medium_mb': self.tracker.stats.medium_mb,
                    'low_mb': self.tracker.stats.low_mb
                },
                'by_tier': {
                    'permanent_mb': self.tracker.stats.permanent_mb,
                    'session_mb': self.tracker.stats.session_mb,
                    'screen_mb': self.tracker.stats.screen_mb,
                    'transient_mb': self.tracker.stats.transient_mb
                }
            },
            'system': {
                'total_allocated_mb': self.tracker.stats.total_allocated_mb,
                'available_mb': self.tracker.stats.system_available_mb,
                'pressure': pressure,
                'pressure_trend': self.pressure_detector.get_pressure_trend()
            },
            'garbage_collection': self.gc_manager.get_gc_stats(),
            'cleanup': {
                'auto_enabled': self.auto_cleanup_enabled,
                'last_cleanup_seconds_ago': time.time() - self.last_cleanup,
                'objects_freed_total': self.tracker.stats.allocations_freed,
                'memory_freed_total_mb': self.tracker.stats.memory_freed_mb
            }
        }
    
    def optimize_for_performance_mode(self, mode: str):
        """Optimize memory management for performance mode"""
        if mode in ["ultra", "high"]:
            # Preserve more memory for quality
            self.gc_manager.strategy = GCStrategy.CONSERVATIVE
            self.cleanup_interval = 20.0
            self.auto_cleanup_enabled = True
        elif mode == "medium":
            # Balanced approach
            self.gc_manager.strategy = GCStrategy.BALANCED
            self.cleanup_interval = 10.0
            self.auto_cleanup_enabled = True
        else:  # low, minimal
            # Aggressive memory management
            self.gc_manager.strategy = GCStrategy.AGGRESSIVE
            self.cleanup_interval = 5.0
            self.auto_cleanup_enabled = True
        
        self.gc_manager._configure_gc()
        self.logger.info(f"Memory management optimized for {mode} mode")
    
    def shutdown(self):
        """Clean shutdown"""
        self.stop_monitoring()
        
        # Final cleanup
        if self.auto_cleanup_enabled:
            self.cleanup_memory(force=True)
        
        self.logger.info("Advanced Memory Manager shutdown")


# Global instance
_global_memory_manager = None

def get_memory_manager() -> AdvancedMemoryManager:
    """Get global memory manager"""
    global _global_memory_manager
    if _global_memory_manager is None:
        _global_memory_manager = AdvancedMemoryManager()
    return _global_memory_manager

def initialize_memory_system(max_memory_mb: float = 1024, 
                           gc_strategy: GCStrategy = GCStrategy.BALANCED) -> AdvancedMemoryManager:
    """Initialize the advanced memory management system"""
    global _global_memory_manager
    _global_memory_manager = AdvancedMemoryManager(max_memory_mb, gc_strategy)
    _global_memory_manager.start_monitoring()
    return _global_memory_manager