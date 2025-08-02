"""
Centralized Logging Service

Enhanced logging system with structured output, file rotation,
and performance-aware log levels.

Features:
- Structured logging with JSON output option
- File rotation and retention
- Performance-aware filtering
- Context-aware loggers
- Integration with telemetry system
"""

import logging
import logging.handlers
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import sys


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add any extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'lineno', 'funcName', 'created',
                          'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'getMessage', 'exc_info',
                          'exc_text', 'stack_info']:
                log_data[key] = value
        
        return json.dumps(log_data)


class PerformanceFilter(logging.Filter):
    """Filter to reduce log noise during performance-critical sections."""
    
    def __init__(self):
        super().__init__()
        self.performance_mode = False
        self.allowed_levels = {logging.WARNING, logging.ERROR, logging.CRITICAL}
    
    def filter(self, record):
        if self.performance_mode:
            return record.levelno in self.allowed_levels
        return True
    
    def enable_performance_mode(self):
        """Enable performance mode (only warnings and errors)."""
        self.performance_mode = True
    
    def disable_performance_mode(self):
        """Disable performance mode (all log levels)."""
        self.performance_mode = False


def setup_logging(
    log_level: str = "INFO",
    log_dir: Path = Path("logs"),
    structured: bool = False,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Set up centralized logging system.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        structured: Whether to use JSON structured logging
        max_file_size: Maximum size of each log file in bytes
        backup_count: Number of backup files to keep
    
    Returns:
        Root logger instance
    """
    
    # Create log directory
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    if structured:
        console_formatter = StructuredFormatter()
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "sands_duat.log",
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.DEBUG)
    
    if structured:
        file_formatter = StructuredFormatter()
    else:
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )
    
    file_handler.setFormatter(file_formatter)
    
    # Add performance filter
    performance_filter = PerformanceFilter()
    file_handler.addFilter(performance_filter)
    
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)
    
    # Performance log handler
    perf_handler = logging.handlers.RotatingFileHandler(
        log_dir / "performance.log",
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    perf_handler.setLevel(logging.DEBUG)
    perf_handler.addFilter(lambda record: 'performance' in record.name.lower())
    perf_handler.setFormatter(file_formatter)
    root_logger.addHandler(perf_handler)
    
    # Store filter reference for global access
    root_logger._performance_filter = performance_filter
    
    root_logger.info(f"Logging system initialized - Level: {log_level}, Dir: {log_dir}")
    
    return root_logger


def get_logger(name: str, context: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """
    Get a logger with optional context.
    
    Args:
        name: Logger name (usually __name__)
        context: Optional context data to include in log messages
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    if context:
        # Create a custom adapter that adds context
        class ContextAdapter(logging.LoggerAdapter):
            def process(self, msg, kwargs):
                return f"[{', '.join(f'{k}={v}' for k, v in self.extra.items())}] {msg}", kwargs
        
        return ContextAdapter(logger, context)
    
    return logger


def enable_performance_mode():
    """Enable performance logging mode (reduced verbosity)."""
    root_logger = logging.getLogger()
    if hasattr(root_logger, '_performance_filter'):
        root_logger._performance_filter.enable_performance_mode()
        logging.info("Performance logging mode enabled")


def disable_performance_mode():
    """Disable performance logging mode (full verbosity)."""
    root_logger = logging.getLogger()
    if hasattr(root_logger, '_performance_filter'):
        root_logger._performance_filter.disable_performance_mode()
        logging.info("Performance logging mode disabled")


def log_performance_metric(metric_name: str, value: float, unit: str = "", **kwargs):
    """
    Log a performance metric.
    
    Args:
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement
        **kwargs: Additional context
    """
    perf_logger = logging.getLogger("performance")
    extra_data = {
        'metric_name': metric_name,
        'value': value,
        'unit': unit,
        **kwargs
    }
    
    perf_logger.info(f"{metric_name}: {value}{unit}", extra=extra_data)