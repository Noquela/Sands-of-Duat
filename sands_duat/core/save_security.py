"""
Save Security and Validation System for Sands of Duat

Comprehensive security measures for protecting player save data including
validation, encryption, tampering detection, and recovery mechanisms.
"""

import os
import json
import hmac
import hashlib
import secrets
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecurityLevel(Enum):
    """Security levels for save data."""
    BASIC = "basic"        # Basic checksums only
    STANDARD = "standard"  # Checksums + validation
    HIGH = "high"         # Checksums + validation + encryption
    PARANOID = "paranoid" # All security measures + additional checks


class ValidationError(Exception):
    """Raised when save data validation fails."""
    pass


class SecurityViolation(Exception):
    """Raised when security checks detect tampering."""
    pass


@dataclass
class SecurityMetadata:
    """Security metadata for save files."""
    security_level: SecurityLevel
    checksum_sha256: str
    hmac_signature: str
    validation_timestamp: str
    encryption_enabled: bool = False
    salt: Optional[str] = None
    key_derivation_rounds: int = 100000
    validation_rules_version: str = "1.0"
    
    # Tamper detection
    file_size: int = 0
    creation_timestamp: str = ""
    modification_count: int = 0
    
    # Backup references for recovery
    last_valid_backup: Optional[str] = None
    recovery_checkpoints: List[str] = field(default_factory=list)


class SaveValidator:
    """
    Validates save data structure and content for integrity.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_rules = self._initialize_validation_rules()
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules for save data."""
        return {
            "player_profile": {
                "required_fields": ["name", "level", "xp", "total_wins", "total_losses"],
                "field_types": {
                    "name": str,
                    "level": int,
                    "xp": int,
                    "total_wins": int,
                    "total_losses": int,
                    "playtime_hours": (int, float)
                },
                "field_ranges": {
                    "level": (1, 100),
                    "xp": (0, 10000000),
                    "total_wins": (0, 100000),
                    "total_losses": (0, 100000),
                    "playtime_hours": (0, 10000)
                }
            },
            "card_collection": {
                "required_fields": ["owned_cards"],
                "field_types": {
                    "owned_cards": dict
                },
                "constraints": {
                    "max_card_count": 1000,  # Maximum cards of single type
                    "max_unique_cards": 500  # Maximum unique card types
                }
            },
            "progression": {
                "required_fields": ["chambers_completed", "achievements"],
                "field_types": {
                    "chambers_completed": (list, set),
                    "achievements": (list, set),
                    "battles_won": int,
                    "battles_lost": int
                },
                "field_ranges": {
                    "battles_won": (0, 1000000),
                    "battles_lost": (0, 1000000)
                }
            }
        }
    
    def validate_save_data(self, save_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate save data structure and content.
        
        Args:
            save_data: Save data to validate
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            # Check top-level structure
            required_sections = ["player_profile", "card_collection", "progression"]
            for section in required_sections:
                if section not in save_data:
                    errors.append(f"Missing required section: {section}")
                    continue
                
                # Validate section
                section_errors = self._validate_section(section, save_data[section])
                errors.extend(section_errors)
            
            # Cross-section validation
            cross_errors = self._validate_cross_section_consistency(save_data)
            errors.extend(cross_errors)
            
            # Detect suspicious patterns
            suspicious_errors = self._detect_suspicious_patterns(save_data)
            errors.extend(suspicious_errors)
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _validate_section(self, section_name: str, section_data: Dict[str, Any]) -> List[str]:
        """Validate a specific section of save data."""
        errors = []
        
        if section_name not in self.validation_rules:
            return errors
        
        rules = self.validation_rules[section_name]
        
        # Check required fields
        for field in rules.get("required_fields", []):
            if field not in section_data:
                errors.append(f"{section_name}: Missing required field '{field}'")
        
        # Check field types
        for field, expected_type in rules.get("field_types", {}).items():
            if field in section_data:
                value = section_data[field]
                if isinstance(expected_type, tuple):
                    if not isinstance(value, expected_type):
                        errors.append(f"{section_name}.{field}: Expected {expected_type}, got {type(value)}")
                else:
                    if not isinstance(value, expected_type):
                        errors.append(f"{section_name}.{field}: Expected {expected_type.__name__}, got {type(value).__name__}")
        
        # Check field ranges
        for field, (min_val, max_val) in rules.get("field_ranges", {}).items():
            if field in section_data:
                value = section_data[field]
                if isinstance(value, (int, float)):
                    if value < min_val or value > max_val:
                        errors.append(f"{section_name}.{field}: Value {value} outside valid range [{min_val}, {max_val}]")
        
        # Check constraints
        constraints = rules.get("constraints", {})
        if section_name == "card_collection":
            owned_cards = section_data.get("owned_cards", {})
            
            # Check max card count per type
            max_card_count = constraints.get("max_card_count", 1000)
            for card_id, count in owned_cards.items():
                if count > max_card_count:
                    errors.append(f"card_collection: Card '{card_id}' count {count} exceeds maximum {max_card_count}")
            
            # Check max unique cards
            max_unique = constraints.get("max_unique_cards", 500)
            if len(owned_cards) > max_unique:
                errors.append(f"card_collection: Unique card count {len(owned_cards)} exceeds maximum {max_unique}")
        
        return errors
    
    def _validate_cross_section_consistency(self, save_data: Dict[str, Any]) -> List[str]:
        """Validate consistency between different sections."""
        errors = []
        
        try:
            profile = save_data.get("player_profile", {})
            progression = save_data.get("progression", {})
            
            # Win/loss consistency
            profile_wins = profile.get("total_wins", 0)
            profile_losses = profile.get("total_losses", 0)
            progression_wins = progression.get("battles_won", 0)
            progression_losses = progression.get("battles_lost", 0)
            
            if profile_wins != progression_wins:
                errors.append(f"Inconsistent win counts: profile={profile_wins}, progression={progression_wins}")
            
            if profile_losses != progression_losses:
                errors.append(f"Inconsistent loss counts: profile={profile_losses}, progression={progression_losses}")
            
            # Level vs XP consistency
            level = profile.get("level", 1)
            xp = profile.get("xp", 0)
            
            # Basic level/XP relationship check (1000 XP per level as rough estimate)
            expected_min_xp = max(0, (level - 1) * 800)  # Allow some flexibility
            expected_max_xp = level * 1200
            
            if xp < expected_min_xp or xp > expected_max_xp:
                errors.append(f"Suspicious level/XP relationship: level={level}, xp={xp}")
            
        except Exception as e:
            errors.append(f"Cross-section validation error: {str(e)}")
        
        return errors
    
    def _detect_suspicious_patterns(self, save_data: Dict[str, Any]) -> List[str]:
        """Detect patterns that might indicate tampering."""
        errors = []
        
        try:
            profile = save_data.get("player_profile", {})
            
            # Detect impossible statistics
            wins = profile.get("total_wins", 0)
            losses = profile.get("total_losses", 0)
            playtime = profile.get("playtime_hours", 0)
            
            # Check for impossible win rates with low playtime
            total_battles = wins + losses
            if total_battles > 0 and playtime > 0:
                battles_per_hour = total_battles / playtime
                if battles_per_hour > 100:  # More than 100 battles per hour is suspicious
                    errors.append(f"Suspicious battle rate: {battles_per_hour:.1f} battles/hour")
            
            # Check for perfect win rates with high battle counts
            if total_battles > 50 and losses == 0:
                errors.append(f"Suspicious perfect win rate with {total_battles} battles")
            
            # Check for round numbers that might indicate manual editing
            suspicious_round_numbers = [xp for xp in [profile.get("xp", 0)] if xp > 1000 and xp % 1000 == 0]
            if suspicious_round_numbers:
                errors.append(f"Suspicious round XP values: {suspicious_round_numbers}")
            
        except Exception as e:
            errors.append(f"Suspicious pattern detection error: {str(e)}")
        
        return errors


class SaveEncryption:
    """
    Handles encryption and decryption of save data.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_key_from_password(self, password: str, salt: bytes) -> bytes:
        """Generate encryption key from password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_data(self, data: str, password: str) -> Tuple[str, str]:
        """
        Encrypt save data.
        
        Args:
            data: Data to encrypt
            password: Encryption password
        
        Returns:
            (encrypted_data, salt)
        """
        try:
            # Generate salt
            salt = secrets.token_bytes(16)
            
            # Generate key
            key = self.generate_key_from_password(password, salt)
            
            # Encrypt data
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data.encode())
            
            return base64.b64encode(encrypted_data).decode(), base64.b64encode(salt).decode()
            
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str, password: str, salt: str) -> str:
        """
        Decrypt save data.
        
        Args:
            encrypted_data: Encrypted data
            password: Decryption password
            salt: Salt used for encryption
        
        Returns:
            Decrypted data
        """
        try:
            # Decode salt and encrypted data
            salt_bytes = base64.b64decode(salt.encode())
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            
            # Generate key
            key = self.generate_key_from_password(password, salt_bytes)
            
            # Decrypt data
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_bytes)
            
            return decrypted_data.decode()
            
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            raise


class SaveSecurityManager:
    """
    Comprehensive save security management system.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        self.logger = logging.getLogger(__name__)
        self.security_level = security_level
        self.validator = SaveValidator()
        self.encryption = SaveEncryption()
        
        # Security keys (in production, these would be properly managed)
        self.hmac_key = self._generate_or_load_hmac_key()
        
        self.logger.info(f"Save security manager initialized with {security_level.value} security")
    
    def _generate_or_load_hmac_key(self) -> bytes:
        """Generate or load HMAC key for signature verification."""
        key_file = Path("keys") / "hmac.key"
        
        if key_file.exists():
            try:
                with open(key_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                self.logger.warning(f"Failed to load HMAC key: {e}")
        
        # Generate new key
        key = secrets.token_bytes(32)
        
        # Save key (in production, use proper key management)
        try:
            key_file.parent.mkdir(exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
        except Exception as e:
            self.logger.warning(f"Failed to save HMAC key: {e}")
        
        return key
    
    def secure_save_data(self, save_data: Dict[str, Any], password: Optional[str] = None) -> Dict[str, Any]:
        """
        Apply security measures to save data.
        
        Args:
            save_data: Save data to secure
            password: Optional password for encryption
        
        Returns:
            Secured save data with security metadata
        """
        try:
            # Validate save data first
            is_valid, errors = self.validator.validate_save_data(save_data)
            if not is_valid:
                self.logger.error(f"Save data validation failed: {errors}")
                if self.security_level in [SecurityLevel.HIGH, SecurityLevel.PARANOID]:
                    raise ValidationError(f"Save data validation failed: {errors}")
            
            # Serialize data
            serialized_data = json.dumps(save_data, sort_keys=True, default=str)
            
            # Create security metadata
            security_metadata = SecurityMetadata(
                security_level=self.security_level,
                checksum_sha256="",
                hmac_signature="",
                validation_timestamp=datetime.now().isoformat(),
                file_size=len(serialized_data),
                creation_timestamp=datetime.now().isoformat()
            )
            
            # Calculate checksum
            security_metadata.checksum_sha256 = hashlib.sha256(serialized_data.encode()).hexdigest()
            
            # Calculate HMAC signature
            security_metadata.hmac_signature = hmac.new(
                self.hmac_key,
                serialized_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Apply encryption if required
            final_data = serialized_data
            if self.security_level in [SecurityLevel.HIGH, SecurityLevel.PARANOID] and password:
                encrypted_data, salt = self.encryption.encrypt_data(serialized_data, password)
                security_metadata.encryption_enabled = True
                security_metadata.salt = salt
                final_data = encrypted_data
            
            # Package secured save
            secured_save = {
                "security_metadata": security_metadata.__dict__,
                "save_data": final_data if not security_metadata.encryption_enabled else {"encrypted": final_data}
            }
            
            self.logger.info(f"Save data secured with {self.security_level.value} security")
            return secured_save
            
        except Exception as e:
            self.logger.error(f"Failed to secure save data: {e}")
            raise
    
    def verify_and_load_save_data(self, secured_save: Dict[str, Any], password: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify security and load save data.
        
        Args:
            secured_save: Secured save data
            password: Optional password for decryption
        
        Returns:
            Verified and loaded save data
        """
        try:
            # Extract security metadata
            metadata_dict = secured_save.get("security_metadata", {})
            security_metadata = SecurityMetadata(**metadata_dict)
            
            # Extract data
            save_data_container = secured_save.get("save_data", {})
            
            # Handle decryption if needed
            if security_metadata.encryption_enabled:
                if not password:
                    raise SecurityViolation("Password required for encrypted save data")
                
                encrypted_data = save_data_container.get("encrypted", "")
                if not encrypted_data or not security_metadata.salt:
                    raise SecurityViolation("Invalid encrypted save data")
                
                serialized_data = self.encryption.decrypt_data(
                    encrypted_data, password, security_metadata.salt
                )
            else:
                serialized_data = json.dumps(save_data_container, sort_keys=True, default=str)
            
            # Verify checksum
            calculated_checksum = hashlib.sha256(serialized_data.encode()).hexdigest()
            if calculated_checksum != security_metadata.checksum_sha256:
                raise SecurityViolation("Checksum verification failed - data may be corrupted or tampered")
            
            # Verify HMAC signature
            calculated_hmac = hmac.new(
                self.hmac_key,
                serialized_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if calculated_hmac != security_metadata.hmac_signature:
                if self.security_level in [SecurityLevel.HIGH, SecurityLevel.PARANOID]:
                    raise SecurityViolation("HMAC verification failed - data integrity compromised")
                else:
                    self.logger.warning("HMAC verification failed, but continuing due to security level")
            
            # Load save data
            if security_metadata.encryption_enabled:
                save_data = json.loads(serialized_data)
            else:
                save_data = save_data_container
            
            # Validate loaded data
            if self.security_level in [SecurityLevel.STANDARD, SecurityLevel.HIGH, SecurityLevel.PARANOID]:
                is_valid, errors = self.validator.validate_save_data(save_data)
                if not is_valid:
                    if self.security_level in [SecurityLevel.HIGH, SecurityLevel.PARANOID]:
                        raise ValidationError(f"Loaded save data validation failed: {errors}")
                    else:
                        self.logger.warning(f"Save data validation warnings: {errors}")
            
            self.logger.info("Save data verified and loaded successfully")
            return save_data
            
        except Exception as e:
            self.logger.error(f"Failed to verify and load save data: {e}")
            raise
    
    def create_recovery_checkpoint(self, save_data: Dict[str, Any]) -> str:
        """
        Create a recovery checkpoint for the save data.
        
        Args:
            save_data: Save data to checkpoint
        
        Returns:
            Checkpoint ID
        """
        try:
            checkpoint_id = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create checkpoint directory
            checkpoint_dir = Path("recovery") / checkpoint_id
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            
            # Save secured data
            secured_data = self.secure_save_data(save_data)
            checkpoint_file = checkpoint_dir / "save.json"
            
            with open(checkpoint_file, 'w') as f:
                json.dump(secured_data, f, indent=2)
            
            self.logger.info(f"Recovery checkpoint created: {checkpoint_id}")
            return checkpoint_id
            
        except Exception as e:
            self.logger.error(f"Failed to create recovery checkpoint: {e}")
            raise
    
    def restore_from_checkpoint(self, checkpoint_id: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Restore save data from a recovery checkpoint.
        
        Args:
            checkpoint_id: Checkpoint to restore from
            password: Optional password for decryption
        
        Returns:
            Restored save data
        """
        try:
            checkpoint_file = Path("recovery") / checkpoint_id / "save.json"
            
            if not checkpoint_file.exists():
                raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
            
            with open(checkpoint_file, 'r') as f:
                secured_data = json.load(f)
            
            restored_data = self.verify_and_load_save_data(secured_data, password)
            
            self.logger.info(f"Save data restored from checkpoint: {checkpoint_id}")
            return restored_data
            
        except Exception as e:
            self.logger.error(f"Failed to restore from checkpoint: {e}")
            raise


# Global security manager instance
_security_manager: Optional[SaveSecurityManager] = None


def get_security_manager() -> SaveSecurityManager:
    """Get the global security manager instance."""
    global _security_manager
    if _security_manager is None:
        _security_manager = SaveSecurityManager()
    return _security_manager


def init_security_manager(security_level: SecurityLevel = SecurityLevel.STANDARD) -> SaveSecurityManager:
    """Initialize the global security manager."""
    global _security_manager
    _security_manager = SaveSecurityManager(security_level)
    return _security_manager