"""
SANDS OF DUAT - HADES-QUALITY ASSET MANAGEMENT SYSTEM
=====================================================

Professional asset management and versioning for AI-generated Egyptian artwork.
Maintains organization, quality standards, and seamless game integration.
"""

import json
import shutil
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class AssetMetadata:
    """Metadata for generated assets."""
    asset_id: str
    name: str
    category: str  # card_art, background, ui_element, etc.
    subcategory: str  # god, artifact, spell, etc.
    
    # Generation info
    generation_date: str
    ai_model: str
    prompt_used: str
    negative_prompt: str
    generation_params: Dict[str, Any]
    
    # Quality metrics
    validation_score: float
    hades_quality_passed: bool
    validation_issues: List[str]
    
    # File info
    file_path: str
    file_size: int
    resolution: Tuple[int, int]
    file_hash: str
    
    # Game integration
    card_name: Optional[str] = None
    rarity: Optional[str] = None
    integrated_in_game: bool = False

class HadesQualityAssetManager:
    """
    Professional asset management system for Hades-quality Egyptian artwork.
    """
    
    def __init__(self, asset_root: str = "assets"):
        self.asset_root = Path(asset_root)
        self.generated_dir = self.asset_root / "generated_art"
        self.approved_dir = self.asset_root / "approved_hades_quality"
        self.metadata_file = self.asset_root / "asset_metadata.json"
        
        # Create directory structure
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        
        # Category directories
        self.category_dirs = {
            'card_art': self.approved_dir / 'cards',
            'backgrounds': self.approved_dir / 'backgrounds', 
            'ui_elements': self.approved_dir / 'ui',
            'characters': self.approved_dir / 'characters',
            'environments': self.approved_dir / 'environments'
        }
        
        for cat_dir in self.category_dirs.values():
            cat_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing metadata
        self.assets_metadata: Dict[str, AssetMetadata] = {}
        self._load_metadata()
        
        logger.info("Hades-Quality Asset Manager initialized")
        logger.info(f"Asset root: {self.asset_root}")
        logger.info(f"Tracking {len(self.assets_metadata)} assets")
    
    def register_generated_asset(self, asset_path: str, generation_data: Dict[str, Any],
                                validation_result: Any) -> str:
        """Register a newly generated asset."""
        
        asset_file = Path(asset_path)
        if not asset_file.exists():
            raise FileNotFoundError(f"Asset file not found: {asset_path}")
        
        # Generate unique asset ID
        asset_id = self._generate_asset_id(asset_file.name)
        
        # Calculate file hash for integrity
        file_hash = self._calculate_file_hash(asset_path)
        
        # Get image resolution
        try:
            from PIL import Image
            with Image.open(asset_path) as img:
                resolution = img.size
        except Exception:
            resolution = (0, 0)
        
        # Create metadata
        metadata = AssetMetadata(
            asset_id=asset_id,
            name=asset_file.stem,
            category=generation_data.get('category', 'unknown'),
            subcategory=generation_data.get('subcategory', 'unknown'),
            generation_date=datetime.now().isoformat(),
            ai_model=generation_data.get('model', 'unknown'),
            prompt_used=generation_data.get('prompt', ''),
            negative_prompt=generation_data.get('negative_prompt', ''),
            generation_params=generation_data.get('params', {}),
            validation_score=validation_result.overall_score if validation_result else 0.0,
            hades_quality_passed=validation_result.passed if validation_result else False,
            validation_issues=validation_result.issues if validation_result else [],
            file_path=str(asset_file),
            file_size=asset_file.stat().st_size,
            resolution=resolution,
            file_hash=file_hash,
            card_name=generation_data.get('card_name'),
            rarity=generation_data.get('rarity')
        )
        
        # Store metadata
        self.assets_metadata[asset_id] = metadata
        self._save_metadata()
        
        logger.info(f"Registered asset: {asset_id} - {metadata.name}")
        
        return asset_id
    
    def approve_asset_for_game(self, asset_id: str) -> bool:
        """Approve an asset for game use (moves to approved directory)."""
        
        if asset_id not in self.assets_metadata:
            logger.error(f"Asset not found: {asset_id}")
            return False
        
        metadata = self.assets_metadata[asset_id]
        
        # Check if asset passes Hades quality standards
        if not metadata.hades_quality_passed:
            logger.warning(f"Asset {asset_id} does not meet Hades quality standards")
            logger.warning(f"Quality score: {metadata.validation_score:.2f}")
            return False
        
        # Move to approved directory
        current_path = Path(metadata.file_path)
        if not current_path.exists():
            logger.error(f"Asset file not found: {metadata.file_path}")
            return False
        
        # Determine target directory based on category
        target_dir = self.category_dirs.get(metadata.category, self.approved_dir)
        
        # Create filename with asset info
        file_extension = current_path.suffix
        approved_filename = f"{metadata.name}_{metadata.rarity}_{asset_id}{file_extension}"
        approved_path = target_dir / approved_filename
        
        # Copy file to approved directory
        shutil.copy2(current_path, approved_path)
        
        # Update metadata
        metadata.file_path = str(approved_path)
        metadata.integrated_in_game = True
        self._save_metadata()
        
        logger.info(f"✅ Approved asset for game: {asset_id} -> {approved_path}")
        
        return True
    
    def batch_approve_hades_quality_assets(self) -> List[str]:
        """Approve all assets that meet Hades quality standards."""
        
        approved_ids = []
        
        for asset_id, metadata in self.assets_metadata.items():
            if metadata.hades_quality_passed and not metadata.integrated_in_game:
                if self.approve_asset_for_game(asset_id):
                    approved_ids.append(asset_id)
        
        logger.info(f"Batch approved {len(approved_ids)} Hades-quality assets")
        
        return approved_ids
    
    def get_assets_by_category(self, category: str) -> List[AssetMetadata]:
        """Get all assets in a specific category."""
        return [metadata for metadata in self.assets_metadata.values() 
                if metadata.category == category]
    
    def get_hades_quality_assets(self) -> List[AssetMetadata]:
        """Get all assets that meet Hades quality standards."""
        return [metadata for metadata in self.assets_metadata.values()
                if metadata.hades_quality_passed]
    
    def get_card_assets(self) -> Dict[str, AssetMetadata]:
        """Get all card assets organized by card name."""
        card_assets = {}
        
        for metadata in self.assets_metadata.values():
            if metadata.category == 'card_art' and metadata.card_name:
                card_assets[metadata.card_name] = metadata
        
        return card_assets
    
    def generate_asset_report(self) -> Dict[str, Any]:
        """Generate comprehensive asset management report."""
        
        total_assets = len(self.assets_metadata)
        hades_quality = sum(1 for m in self.assets_metadata.values() if m.hades_quality_passed)
        integrated = sum(1 for m in self.assets_metadata.values() if m.integrated_in_game)
        
        # Category breakdown
        category_stats = {}
        for category in ['card_art', 'backgrounds', 'ui_elements', 'characters', 'environments']:
            category_assets = self.get_assets_by_category(category)
            category_hades = sum(1 for m in category_assets if m.hades_quality_passed)
            category_stats[category] = {
                'total': len(category_assets),
                'hades_quality': category_hades,
                'integration_rate': f"{category_hades/len(category_assets)*100:.1f}%" if category_assets else "0%"
            }
        
        # Quality metrics
        all_scores = [m.validation_score for m in self.assets_metadata.values() if m.validation_score > 0]
        avg_quality = sum(all_scores) / len(all_scores) if all_scores else 0.0
        
        report = {
            'summary': {
                'total_assets': total_assets,
                'hades_quality_assets': hades_quality,
                'integrated_assets': integrated,
                'hades_quality_rate': f"{hades_quality/total_assets*100:.1f}%" if total_assets else "0%",
                'integration_rate': f"{integrated/total_assets*100:.1f}%" if total_assets else "0%",
                'average_quality_score': f"{avg_quality:.2f}"
            },
            'category_breakdown': category_stats,
            'quality_distribution': self._get_quality_distribution(),
            'recent_assets': self._get_recent_assets(limit=10)
        }
        
        return report
    
    def _get_quality_distribution(self) -> Dict[str, int]:
        """Get distribution of assets by quality level."""
        distribution = {
            'Legendary (0.9-1.0)': 0,
            'Excellent (0.8-0.9)': 0,
            'Good (0.7-0.8)': 0,
            'Fair (0.6-0.7)': 0,
            'Poor (<0.6)': 0
        }
        
        for metadata in self.assets_metadata.values():
            score = metadata.validation_score
            if score >= 0.9:
                distribution['Legendary (0.9-1.0)'] += 1
            elif score >= 0.8:
                distribution['Excellent (0.8-0.9)'] += 1
            elif score >= 0.7:
                distribution['Good (0.7-0.8)'] += 1
            elif score >= 0.6:
                distribution['Fair (0.6-0.7)'] += 1
            else:
                distribution['Poor (<0.6)'] += 1
        
        return distribution
    
    def _get_recent_assets(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recently generated assets."""
        sorted_assets = sorted(self.assets_metadata.values(), 
                              key=lambda x: x.generation_date, reverse=True)
        
        return [
            {
                'name': asset.name,
                'category': asset.category,
                'quality_score': asset.validation_score,
                'hades_quality': asset.hades_quality_passed,
                'date': asset.generation_date
            }
            for asset in sorted_assets[:limit]
        ]
    
    def cleanup_low_quality_assets(self, min_score: float = 0.5) -> int:
        """Remove assets below quality threshold."""
        
        to_remove = []
        
        for asset_id, metadata in self.assets_metadata.items():
            if metadata.validation_score < min_score and not metadata.integrated_in_game:
                to_remove.append(asset_id)
                
                # Remove file
                asset_file = Path(metadata.file_path)
                if asset_file.exists():
                    asset_file.unlink()
                    logger.info(f"Removed low-quality asset: {asset_file.name}")
        
        # Remove from metadata
        for asset_id in to_remove:
            del self.assets_metadata[asset_id]
        
        self._save_metadata()
        
        logger.info(f"Cleaned up {len(to_remove)} low-quality assets")
        
        return len(to_remove)
    
    def _generate_asset_id(self, filename: str) -> str:
        """Generate unique asset ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_part = hashlib.md5(filename.encode()).hexdigest()[:8]
        return f"asset_{timestamp}_{hash_part}"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file for integrity checking."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _load_metadata(self):
        """Load asset metadata from file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                
                for asset_id, asset_data in data.items():
                    self.assets_metadata[asset_id] = AssetMetadata(**asset_data)
                
                logger.info(f"Loaded metadata for {len(self.assets_metadata)} assets")
                
            except Exception as e:
                logger.error(f"Failed to load asset metadata: {e}")
    
    def _save_metadata(self):
        """Save asset metadata to file."""
        try:
            # Convert to serializable format
            data = {
                asset_id: asdict(metadata) 
                for asset_id, metadata in self.assets_metadata.items()
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to save asset metadata: {e}")

# Global asset manager instance
_asset_manager: Optional[HadesQualityAssetManager] = None

def get_asset_manager() -> HadesQualityAssetManager:
    """Get the global asset manager instance."""
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = HadesQualityAssetManager()
    return _asset_manager