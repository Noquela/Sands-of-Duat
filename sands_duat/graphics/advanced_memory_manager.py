"""
Advanced Memory Management System for Sands of Duat

Sophisticated memory management system designed for premium visual quality
while maintaining stable performance on RTX 5070 and lower-end hardware.

Features:
- Smart garbage collection scheduling
- Memory pool management for visual effects
- Asset lifecycle management
- Texture memory optimization
- GPU memory tracking and optimization
- Memory pressure detection and response
- Leak detection and prevention
"""

import pygame
import gc
import threading
import time
import weakref
import psutil
from typing import Dict, List, Set, Optional, Any, Callable, Tuple, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, OrderedDict
import logging
from concurrent.futures import ThreadPoolExecutor
import sys

from ..core.performance_profiler import profile_operation

T = TypeVar('T')


class MemoryType(Enum):
    """Types of memory being managed."""
    TEXTURE = "texture"
    SURFACE = "surface" 
    PARTICLE = "particle"
    AUDIO = "audio"
    FONT = "font"
    CACHED_DATA = "cached_data"
    TEMPORARY = "temporary"


class MemoryPriority(Enum):
    """Memory priority levels for retention."""
    CRITICAL = 1      # Never evict (core game assets)
    HIGH = 2          # Evict only under severe pressure
    MEDIUM = 3        # Standard eviction candidate
    LOW = 4           # First to be evicted
    TEMPORARY = 5     # Evict immediately when needed


@dataclass
class MemoryAllocation:
    """Tracks a memory allocation."""
    allocation_id: str
    memory_type: MemoryType
    size_bytes: int
    priority: MemoryPriority
    allocated_time: float
    last_access_time: float
    access_count: int
    obj_ref: weakref.ReferenceType
    metadata: Dict[str, Any]


class ObjectPool(Generic[T]):
    """Generic object pool for memory-efficient object reuse."""
    
    def __init__(self, factory: Callable[[], T], max_size: int = 100):
        self.factory = factory
        self.max_size = max_size
        self.available: List[T] = []
        self.in_use: Set[int] = set()
        self.total_created = 0
        self.total_reused = 0
        self._lock = threading.Lock()
    
    def acquire(self) -> T:
        """Get an object from the pool."""
        with self._lock:
            if self.available:
                obj = self.available.pop()
                self.in_use.add(id(obj))
                self.total_reused += 1
                return obj
            else:
                obj = self.factory()
                self.in_use.add(id(obj))
                self.total_created += 1
                return obj
    
    def release(self, obj: T):
        """Return an object to the pool."""
        with self._lock:
            obj_id = id(obj)
            if obj_id in self.in_use:
                self.in_use.remove(obj_id)
                
                if len(self.available) < self.max_size:
                    # Reset object state if it has a reset method
                    if hasattr(obj, 'reset'):
                        obj.reset()
                    self.available.append(obj)
                # If pool is full, let object be garbage collected
    
    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        with self._lock:
            return {
                "available": len(self.available),
                "in_use": len(self.in_use),
                "total_created": self.total_created,
                "total_reused": self.total_reused,
                "pool_utilization": len(self.in_use) / max(1, len(self.in_use) + len(self.available))
            }


class TextureMemoryManager:
    """Manages texture memory usage and optimization."""
    
    def __init__(self, max_texture_memory_mb: int = 256):
        self.max_texture_memory = max_texture_memory_mb * 1024 * 1024
        self.current_texture_memory = 0
        self.texture_registry: Dict[int, Dict[str, Any]] = {}
        self.compressed_textures: Dict[int, pygame.Surface] = {}
        self.texture_access_order = OrderedDict()
        
    def register_texture(self, surface: pygame.Surface, compressed: bool = False, 
                        priority: MemoryPriority = MemoryPriority.MEDIUM):
        """Register a texture surface for memory tracking."""
        surface_id = id(surface)
        width, height = surface.get_size()
        
        # Calculate memory usage (assume 32-bit RGBA)
        memory_size = width * height * 4
        if compressed:
            memory_size = int(memory_size * 0.5)  # Estimate 50% compression
        
        self.texture_registry[surface_id] = {
            "size": (width, height),
            "memory_bytes": memory_size,
            "compressed": compressed,
            "priority": priority,
            "access_count": 0,
            "created_time": time.time()
        }
        
        self.current_texture_memory += memory_size
        self.texture_access_order[surface_id] = time.time()
        
        # Check if we need to free some memory
        if self.current_texture_memory > self.max_texture_memory:
            self._evict_textures()
    
    def access_texture(self, surface: pygame.Surface):
        """Mark texture as accessed."""
        surface_id = id(surface)
        if surface_id in self.texture_registry:
            self.texture_registry[surface_id]["access_count"] += 1
            self.texture_access_order[surface_id] = time.time()
            self.texture_access_order.move_to_end(surface_id)
    
    def _evict_textures(self):
        """Evict least recently used textures to free memory."""
        target_memory = self.max_texture_memory * 0.8  # Free to 80% capacity
        evicted_count = 0
        
        # Sort by priority and access time
        sorted_textures = sorted(
            self.texture_access_order.items(),
            key=lambda x: (
                self.texture_registry.get(x[0], {}).get("priority", MemoryPriority.MEDIUM).value,
                x[1]  # access time
            )
        )
        
        for surface_id, _ in sorted_textures:
            if self.current_texture_memory <= target_memory:
                break
            
            if surface_id in self.texture_registry:
                texture_info = self.texture_registry[surface_id]
                if texture_info["priority"] != MemoryPriority.CRITICAL:
                    self.current_texture_memory -= texture_info["memory_bytes"]
                    del self.texture_registry[surface_id]
                    del self.texture_access_order[surface_id]
                    evicted_count += 1
        
        if evicted_count > 0:
            logging.getLogger(__name__).info(f"Evicted {evicted_count} textures to free memory")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get texture memory statistics."""
        return {
            "current_memory_mb": self.current_texture_memory / (1024 * 1024),
            "max_memory_mb": self.max_texture_memory / (1024 * 1024),
            "utilization_percent": (self.current_texture_memory / self.max_texture_memory) * 100,
            "texture_count": len(self.texture_registry),
            "compressed_textures": len(self.compressed_textures)
        }


class MemoryPressureDetector:
    """Detects and responds to memory pressure."""
    
    def __init__(self, warning_threshold: float = 0.8, critical_threshold: float = 0.9):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.callbacks: Dict[str, List[Callable]] = {
            "warning": [],
            "critical": [],
            "recovered": []
        }
        self.current_pressure = 0.0
        self.last_check_time = 0.0
        self.check_interval = 1.0  # Check every second
        
    def update(self):
        """Update memory pressure monitoring."""
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return
        
        self.last_check_time = current_time
        
        # Get system memory info
        memory_info = psutil.virtual_memory()
        previous_pressure = self.current_pressure
        self.current_pressure = memory_info.percent / 100.0
        
        # Trigger callbacks based on pressure changes
        if previous_pressure < self.warning_threshold and self.current_pressure >= self.warning_threshold:
            self._trigger_callbacks("warning")
        elif previous_pressure < self.critical_threshold and self.current_pressure >= self.critical_threshold:
            self._trigger_callbacks("critical")
        elif previous_pressure >= self.warning_threshold and self.current_pressure < self.warning_threshold:
            self._trigger_callbacks("recovered")
    
    def _trigger_callbacks(self, event_type: str):
        """Trigger registered callbacks for memory pressure events."""
        for callback in self.callbacks[event_type]:
            try:
                callback(self.current_pressure)
            except Exception as e:
                logging.getLogger(__name__).error(f"Error in memory pressure callback: {e}")
    
    def register_callback(self, event_type: str, callback: Callable[[float], None]):
        """Register callback for memory pressure events."""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def get_pressure_level(self) -> str:
        """Get current pressure level as string."""
        if self.current_pressure >= self.critical_threshold:
            return "critical"
        elif self.current_pressure >= self.warning_threshold:
            return "warning"
        else:
            return "normal"


class GarbageCollectionOptimizer:
    """Optimizes garbage collection timing and performance."""
    
    def __init__(self):
        self.gc_enabled = True
        self.gc_threshold_adjustments = [700, 10, 10]  # Default Python GC thresholds
        self.last_gc_time = 0.0
        self.gc_interval = 5.0  # Run full GC every 5 seconds max
        self.frame_budget_ms = 2.0  # Max 2ms per frame for GC
        
        # Statistics
        self.gc_stats = {
            "collections_performed": 0,
            "objects_collected": 0,
            "time_spent_ms": 0.0
        }
        
        # Apply optimized GC settings
        self._optimize_gc_settings()
    
    def _optimize_gc_settings(self):
        """Apply optimized garbage collection settings."""
        if self.gc_enabled:
            # Adjust GC thresholds for gaming performance
            # Increase gen 0 threshold to reduce frequent collections
            gc.set_threshold(*self.gc_threshold_adjustments)
            
            # Disable automatic GC for generation 2 (we'll handle it manually)
            gc.disable()
    
    def should_run_gc(self, frame_time_budget_ms: float = None) -> bool:
        """Determine if garbage collection should run now."""
        if not self.gc_enabled:
            return False
        
        current_time = time.time()
        time_since_last_gc = current_time - self.last_gc_time
        
        # Check if enough time has passed
        if time_since_last_gc < self.gc_interval:
            return False
        
        # Check frame time budget
        budget = frame_time_budget_ms or self.frame_budget_ms
        if budget < 1.0:  # Not enough budget
            return False
        
        return True
    
    def run_incremental_gc(self, time_budget_ms: float = 2.0) -> Dict[str, Any]:
        """Run incremental garbage collection within time budget."""
        if not self.should_run_gc(time_budget_ms):
            return {"ran": False, "reason": "not_needed"}
        
        start_time = time.perf_counter()
        
        try:
            # Run generation 0 collection (fastest)
            collected_gen0 = gc.collect(0)
            
            # Check if we have time for generation 1
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            if elapsed_ms < time_budget_ms * 0.5:
                collected_gen1 = gc.collect(1)
            else:
                collected_gen1 = 0
            
            # Only run generation 2 if we have plenty of time
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            if elapsed_ms < time_budget_ms * 0.3:
                collected_gen2 = gc.collect(2)
            else:
                collected_gen2 = 0
            
            total_collected = collected_gen0 + collected_gen1 + collected_gen2
            final_time = (time.perf_counter() - start_time) * 1000
            
            # Update statistics
            self.gc_stats["collections_performed"] += 1
            self.gc_stats["objects_collected"] += total_collected
            self.gc_stats["time_spent_ms"] += final_time
            self.last_gc_time = time.time()
            
            return {
                "ran": True,
                "objects_collected": total_collected,
                "time_ms": final_time,
                "gen0": collected_gen0,
                "gen1": collected_gen1,
                "gen2": collected_gen2
            }
        
        except Exception as e:
            logging.getLogger(__name__).error(f"Error during garbage collection: {e}")
            return {"ran": False, "error": str(e)}
    
    def get_gc_stats(self) -> Dict[str, Any]:
        """Get garbage collection statistics."""
        return {
            **self.gc_stats,
            "gc_enabled": self.gc_enabled,
            "gc_thresholds": gc.get_threshold(),
            "gc_counts": gc.get_count(),
            "average_time_ms": (self.gc_stats["time_spent_ms"] / 
                              max(1, self.gc_stats["collections_performed"]))
        }


class AdvancedMemoryManager:
    """Main advanced memory management system."""
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.allocations: Dict[str, MemoryAllocation] = {}
        self.object_pools: Dict[type, ObjectPool] = {}
        
        # Sub-managers
        self.texture_manager = TextureMemoryManager(max_memory_mb // 2)  # Half for textures
        self.pressure_detector = MemoryPressureDetector()
        self.gc_optimizer = GarbageCollectionOptimizer()
        
        # Memory tracking
        self.total_allocated_bytes = 0
        self.allocation_counter = 0
        self.weak_refs: Dict[str, weakref.ReferenceType] = {}
        
        # Threading
        self.memory_lock = threading.RLock()
        self.cleanup_executor = ThreadPoolExecutor(max_workers=1)
        
        # Statistics
        self.stats = {
            "allocations_tracked": 0,
            "memory_freed_bytes": 0,
            "pools_created": 0,
            "gc_optimizations": 0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Register memory pressure callbacks
        self._setup_pressure_callbacks()
        
        # Start background cleanup
        self._start_background_cleanup()
    
    def _setup_pressure_callbacks(self):
        """Setup memory pressure response callbacks."""
        self.pressure_detector.register_callback("warning", self._handle_memory_warning)
        self.pressure_detector.register_callback("critical", self._handle_memory_critical)
    
    def _handle_memory_warning(self, pressure: float):
        """Handle memory warning pressure."""
        self.logger.warning(f"Memory pressure warning: {pressure:.1%}")
        
        # Trigger aggressive cleanup
        self._cleanup_low_priority_allocations()
        
        # Run garbage collection
        self.gc_optimizer.run_incremental_gc(5.0)
    
    def _handle_memory_critical(self, pressure: float):
        """Handle critical memory pressure."""
        self.logger.error(f"Critical memory pressure: {pressure:.1%}")
        
        # Emergency cleanup
        self._emergency_memory_cleanup()
        
        # Force full garbage collection
        gc.collect()
    
    def _start_background_cleanup(self):
        """Start background cleanup thread."""
        def cleanup_loop():
            while True:
                try:
                    time.sleep(10)  # Run every 10 seconds
                    self._background_cleanup()
                except Exception as e:
                    self.logger.error(f"Error in background cleanup: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
    
    def _background_cleanup(self):
        """Background cleanup of stale allocations."""
        with self.memory_lock:
            current_time = time.time()
            stale_allocations = []
            
            for alloc_id, allocation in self.allocations.items():
                # Check if object still exists
                if allocation.obj_ref() is None:
                    stale_allocations.append(alloc_id)
                # Check for old temporary allocations
                elif (allocation.priority == MemoryPriority.TEMPORARY and
                      current_time - allocation.last_access_time > 60):  # 1 minute
                    stale_allocations.append(alloc_id)
            
            # Remove stale allocations
            for alloc_id in stale_allocations:
                self._free_allocation(alloc_id)
        
        # Update memory pressure
        self.pressure_detector.update()
    
    def allocate_tracked(self, obj: Any, memory_type: MemoryType, size_bytes: int,
                        priority: MemoryPriority = MemoryPriority.MEDIUM,
                        metadata: Dict[str, Any] = None) -> str:
        """Track a memory allocation."""
        with self.memory_lock:
            self.allocation_counter += 1
            allocation_id = f"{memory_type.value}_{self.allocation_counter}"
            
            current_time = time.time()
            
            allocation = MemoryAllocation(
                allocation_id=allocation_id,
                memory_type=memory_type,
                size_bytes=size_bytes,
                priority=priority,
                allocated_time=current_time,
                last_access_time=current_time,
                access_count=1,
                obj_ref=weakref.ref(obj, lambda ref: self._free_allocation(allocation_id)),
                metadata=metadata or {}
            )
            
            self.allocations[allocation_id] = allocation
            self.total_allocated_bytes += size_bytes
            self.stats["allocations_tracked"] += 1
            
            # Special handling for textures
            if memory_type == MemoryType.TEXTURE and isinstance(obj, pygame.Surface):
                self.texture_manager.register_texture(obj, 
                    compressed=metadata.get("compressed", False) if metadata else False,
                    priority=priority)
            
            return allocation_id
    
    def access_allocation(self, allocation_id: str):
        """Mark allocation as accessed."""
        with self.memory_lock:
            if allocation_id in self.allocations:
                allocation = self.allocations[allocation_id]
                allocation.last_access_time = time.time()
                allocation.access_count += 1
                
                # Update texture access if applicable
                obj = allocation.obj_ref()
                if obj and allocation.memory_type == MemoryType.TEXTURE:
                    self.texture_manager.access_texture(obj)
    
    def _free_allocation(self, allocation_id: str):
        """Free a tracked allocation."""
        with self.memory_lock:
            if allocation_id in self.allocations:
                allocation = self.allocations[allocation_id]
                self.total_allocated_bytes -= allocation.size_bytes
                self.stats["memory_freed_bytes"] += allocation.size_bytes
                del self.allocations[allocation_id]
    
    def get_object_pool(self, obj_type: type, factory: Callable = None, max_size: int = 100) -> ObjectPool:
        """Get or create object pool for specified type."""
        if obj_type not in self.object_pools:
            if factory is None:
                factory = obj_type
            
            self.object_pools[obj_type] = ObjectPool(factory, max_size)
            self.stats["pools_created"] += 1
        
        return self.object_pools[obj_type]
    
    def _cleanup_low_priority_allocations(self):
        """Cleanup low priority allocations to free memory."""
        with self.memory_lock:
            to_remove = []
            
            for alloc_id, allocation in self.allocations.items():
                if allocation.priority in [MemoryPriority.LOW, MemoryPriority.TEMPORARY]:
                    to_remove.append(alloc_id)
            
            for alloc_id in to_remove:
                self._free_allocation(alloc_id)
            
            if to_remove:
                self.logger.info(f"Cleaned up {len(to_remove)} low priority allocations")
    
    def _emergency_memory_cleanup(self):
        """Emergency memory cleanup for critical pressure."""
        with self.memory_lock:
            # Clear all temporary and low priority allocations
            to_remove = []
            
            for alloc_id, allocation in self.allocations.items():
                if allocation.priority in [MemoryPriority.LOW, MemoryPriority.TEMPORARY, MemoryPriority.MEDIUM]:
                    # Keep only recently accessed medium priority items
                    if (allocation.priority == MemoryPriority.MEDIUM and
                        time.time() - allocation.last_access_time < 30):
                        continue
                    to_remove.append(alloc_id)
            
            for alloc_id in to_remove:
                self._free_allocation(alloc_id)
            
            # Clear object pools
            for pool in self.object_pools.values():
                pool.available.clear()
            
            self.logger.warning(f"Emergency cleanup freed {len(to_remove)} allocations")
    
    def update(self, frame_time_budget_ms: float = 2.0):
        """Update memory manager - call once per frame."""
        with profile_operation("memory_manager_update"):
            # Update memory pressure detection
            self.pressure_detector.update()
            
            # Run incremental garbage collection if needed
            gc_result = self.gc_optimizer.run_incremental_gc(frame_time_budget_ms)
            if gc_result.get("ran"):
                self.stats["gc_optimizations"] += 1
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Get comprehensive memory usage report."""
        with self.memory_lock:
            # Calculate memory by type
            memory_by_type = defaultdict(int)
            allocations_by_priority = defaultdict(int)
            
            for allocation in self.allocations.values():
                memory_by_type[allocation.memory_type.value] += allocation.size_bytes
                allocations_by_priority[allocation.priority.value] += 1
            
            # Get system memory info
            system_memory = psutil.virtual_memory()
            process_memory = psutil.Process().memory_info()
            
            return {
                "system_memory": {
                    "total_gb": system_memory.total / (1024**3),
                    "available_gb": system_memory.available / (1024**3),
                    "used_percent": system_memory.percent,
                    "pressure_level": self.pressure_detector.get_pressure_level()
                },
                "process_memory": {
                    "rss_mb": process_memory.rss / (1024**2),
                    "vms_mb": process_memory.vms / (1024**2)
                },
                "tracked_memory": {
                    "total_mb": self.total_allocated_bytes / (1024**2),
                    "allocation_count": len(self.allocations),
                    "by_type_mb": {k: v / (1024**2) for k, v in memory_by_type.items()},
                    "by_priority": dict(allocations_by_priority)
                },
                "texture_memory": self.texture_manager.get_memory_stats(),
                "object_pools": {
                    obj_type.__name__: pool.get_stats() 
                    for obj_type, pool in self.object_pools.items()
                },
                "garbage_collection": self.gc_optimizer.get_gc_stats(),
                "statistics": self.stats.copy()
            }
    
    def optimize_for_screen(self, screen_name: str):
        """Apply screen-specific memory optimizations."""
        if screen_name == "menu":
            # Menu can free combat-specific assets
            self._cleanup_allocations_by_metadata("screen", "combat")
        elif screen_name in ["combat", "dynamic_combat"]:
            # Combat should free menu-specific assets
            self._cleanup_allocations_by_metadata("screen", "menu")
    
    def _cleanup_allocations_by_metadata(self, key: str, value: str):
        """Cleanup allocations with specific metadata."""
        with self.memory_lock:
            to_remove = []
            
            for alloc_id, allocation in self.allocations.items():
                if allocation.metadata.get(key) == value:
                    to_remove.append(alloc_id)
            
            for alloc_id in to_remove:
                self._free_allocation(alloc_id)


# Global memory manager
_global_memory_manager = None

def get_memory_manager(max_memory_mb: int = 512) -> AdvancedMemoryManager:
    """Get global memory manager."""
    global _global_memory_manager
    if _global_memory_manager is None:
        _global_memory_manager = AdvancedMemoryManager(max_memory_mb)
    return _global_memory_manager

def track_allocation(obj: Any, memory_type: MemoryType, size_bytes: int,
                    priority: MemoryPriority = MemoryPriority.MEDIUM,
                    metadata: Dict[str, Any] = None) -> str:
    """Track a memory allocation globally."""
    manager = get_memory_manager()
    return manager.allocate_tracked(obj, memory_type, size_bytes, priority, metadata)

def get_object_pool(obj_type: type, factory: Callable = None, max_size: int = 100) -> ObjectPool:
    """Get object pool for specified type."""
    manager = get_memory_manager()
    return manager.get_object_pool(obj_type, factory, max_size)

def update_memory_management(frame_time_budget_ms: float = 2.0):
    """Update memory management system - call once per frame."""
    manager = get_memory_manager()
    manager.update(frame_time_budget_ms)