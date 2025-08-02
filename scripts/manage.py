#!/usr/bin/env python3
"""
Sands of Duat Development Management Script

Unified CLI for common development tasks including testing, linting,
art generation, and content validation.

Usage:
    python scripts/manage.py test          # Run full test suite
    python scripts/manage.py lint          # Format and lint code
    python scripts/manage.py typecheck     # MyPy validation
    python scripts/manage.py validate      # Content validation
    python scripts/manage.py generate_art  # Batch art generation
    python scripts/manage.py dev_setup     # First-time environment setup
"""

import sys
import subprocess
import argparse
import logging
from pathlib import Path
import shutil
import os

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class TaskRunner:
    """Handles execution of development tasks."""
    
    def __init__(self):
        self.project_root = project_root
        self.venv_python = self._get_venv_python()
    
    def _get_venv_python(self):
        """Get the correct Python executable for the virtual environment."""
        if os.name == 'nt':  # Windows
            return sys.executable
        else:  # Unix-like
            return sys.executable
    
    def _run_command(self, cmd, check=True, cwd=None):
        """Run a shell command with proper error handling."""
        if cwd is None:
            cwd = self.project_root
        
        logger.info(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=check, cwd=cwd, 
                                  capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e}")
            if e.stderr:
                print(e.stderr)
            if check:
                sys.exit(1)
            return e
    
    def test(self, args):
        """Run test suite."""
        logger.info("Running test suite...")
        
        # Run different test categories
        test_commands = [
            # Unit tests with coverage
            [self.venv_python, "-m", "pytest", "tests/unit/", "-v", 
             "--cov=sands_duat", "--cov-report=term-missing"],
            
            # Integration tests
            [self.venv_python, "-m", "pytest", "tests/integration/", "-v"],
            
            # Performance tests (if --performance flag)
            *([
                [self.venv_python, "-m", "pytest", "tests/performance/", "-v", "--benchmark-only"]
            ] if args.performance else [])
        ]
        
        for cmd in test_commands:
            self._run_command(cmd)
        
        logger.info("✅ All tests passed!")
    
    def lint(self, args):
        """Format and lint code."""
        logger.info("Formatting and linting code...")
        
        # Black formatting
        self._run_command([self.venv_python, "-m", "black", "sands_duat/", "tests/", "scripts/"])
        
        # Import sorting
        self._run_command([self.venv_python, "-m", "isort", "sands_duat/", "tests/", "scripts/"])
        
        # Flake8 linting
        self._run_command([self.venv_python, "-m", "flake8", "sands_duat/", 
                          "--max-line-length=88", "--extend-ignore=E203,W503"])
        
        logger.info("✅ Code formatting and linting complete!")
    
    def typecheck(self, args):
        """Run MyPy type checking."""
        logger.info("Running type checking...")
        
        self._run_command([self.venv_python, "-m", "mypy", "sands_duat/", 
                          "--ignore-missing-imports", "--strict-optional"])
        
        logger.info("✅ Type checking complete!")
    
    def validate(self, args):
        """Validate YAML content and schemas."""
        logger.info("Validating content...")
        
        # Import and run content validation
        try:
            from sands_duat.content.validator import ContentValidator
            from sands_duat.content.cross_reference_validator import CrossReferenceValidator
            
            # Validate individual YAML files
            validator = ContentValidator()
            content_dir = self.project_root / "sands_duat" / "content"
            
            for yaml_file in content_dir.rglob("*.yaml"):
                logger.info(f"Validating {yaml_file.relative_to(content_dir)}")
                validator.validate_file(yaml_file)
            
            # Cross-reference validation
            cross_validator = CrossReferenceValidator(content_dir)
            cross_validator.validate_all()
            
            logger.info("✅ Content validation complete!")
            
        except ImportError as e:
            logger.error(f"Content validation modules not available: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Content validation failed: {e}")
            sys.exit(1)
    
    def generate_art(self, args):
        """Generate art assets using AI pipeline."""
        logger.info("Starting art generation...")
        
        try:
            # Check if models are available
            models_dir = self.project_root / "models"
            if not models_dir.exists():
                logger.info("Models directory not found. Running model setup...")
                self._run_command([self.venv_python, "tools/model_downloader.py", "--setup"])
            
            # Generate art from YAML prompts
            art_cmd = [
                self.venv_python, "tools/gen_art.py",
                "--content", "sands_duat/content/cards/",
                "--output", "sands_duat/assets/art_raw/",
                "--batch-size", "2",
                "--offload-to-cpu"
            ]
            
            if args.fast:
                art_cmd.extend(["--fast-mode"])
            
            self._run_command(art_cmd)
            
            # Upscale generated images
            if not args.skip_upscale:
                logger.info("Upscaling generated images...")
                self._run_command([
                    self.venv_python, "tools/upscale.py",
                    "sands_duat/assets/art_raw",
                    "sands_duat/assets/art_clean",
                    "--model", "real-esrgan",
                    "--fit-and-pad", "400x650"
                ])
            
            logger.info("✅ Art generation complete!")
            
        except Exception as e:
            logger.error(f"Art generation failed: {e}")
            sys.exit(1)
    
    def dev_setup(self, args):
        """Set up development environment."""
        logger.info("Setting up development environment...")
        
        # Create necessary directories
        dirs_to_create = [
            "sands_duat/assets/art_raw",
            "sands_duat/assets/art_clean",
            "sands_duat/assets/audio",
            "sands_duat/assets/fonts",
            "models",
            "logs",
            "temp"
        ]
        
        for dir_path in dirs_to_create:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")
        
        # Install development dependencies
        logger.info("Installing development dependencies...")
        self._run_command([self.venv_python, "-m", "pip", "install", "-r", "config/requirements-dev.txt"])
        
        # Set up pre-commit hooks (if available)
        try:
            self._run_command([self.venv_python, "-m", "pre_commit", "install"], check=False)
        except FileNotFoundError:
            logger.info("Pre-commit not available, skipping hook setup")
        
        # Create sample config file
        config_file = self.project_root / "config" / "config.ini"
        if not config_file.exists():
            self._create_sample_config(config_file)
        
        logger.info("✅ Development environment setup complete!")
    
    def _create_sample_config(self, config_file):
        """Create a sample configuration file."""
        config_content = """[paths]
models_dir = models/
content_dir = sands_duat/content/
assets_dir = sands_duat/assets/
temp_dir = temp/

[models]
playground_v25_hash = sha256:f42ad2a86c6f19aa2c11b2a6e62b93f8c77b21e8
stable_cascade_hash = sha256:71c4925c1c4723ced0b6ad0abc85b5d76176a3c2
kandinsky_3_hash = sha256:4f4bdeb0bb89e4d9e8f1c3ebbde0e84dcbf0d857
realesrgan_version = v0.6.0

[development]
debug_mode = true
hot_reload = true
log_level = INFO

[display]
default_width = 3440
default_height = 1440
target_fps = 60
"""
        config_file.write_text(config_content)
        logger.info(f"Created sample config: {config_file}")
    
    def benchmark(self, args):
        """Run performance benchmarks."""
        logger.info("Running performance benchmarks...")
        
        self._run_command([
            self.venv_python, "-m", "pytest", "tests/performance/",
            "--benchmark-only", "--benchmark-json=benchmark_results.json"
        ])
        
        logger.info("✅ Benchmarks complete! Results saved to benchmark_results.json")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Sands of Duat Development Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run test suite')
    test_parser.add_argument('--performance', action='store_true', 
                           help='Include performance tests')
    
    # Lint command
    lint_parser = subparsers.add_parser('lint', help='Format and lint code')
    
    # Type check command
    typecheck_parser = subparsers.add_parser('typecheck', help='Run MyPy type checking')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate YAML content')
    
    # Generate art command
    art_parser = subparsers.add_parser('generate_art', help='Generate art assets')
    art_parser.add_argument('--fast', action='store_true', help='Use fast generation mode')
    art_parser.add_argument('--skip-upscale', action='store_true', help='Skip upscaling step')
    
    # Dev setup command
    setup_parser = subparsers.add_parser('dev_setup', help='Set up development environment')
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Run performance benchmarks')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    runner = TaskRunner()
    
    # Dispatch to appropriate method
    method = getattr(runner, args.command, None)
    if method:
        method(args)
    else:
        logger.error(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()