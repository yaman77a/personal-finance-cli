import json
import os
from typing import Dict, Any, Optional

class SettingsManager:
    """
    Class for managing application settings stored in a local JSON file
    """
    
    def __init__(self, filename: str = "settings.json"):
        self.filename = filename
        self.settings = {}
        self.default_settings = {
            "monthly_limit": 0
        }
        self._initialize_settings()
    
    def _initialize_settings(self):
        """
        Initialize settings by loading from file or creating with defaults
        """
        if os.path.exists(self.filename):
            self.load_settings()
        else:
            self._create_default_settings()
    
    def _create_default_settings(self):
        """
        Create settings file with default values
        """
        self.settings = self.default_settings.copy()
        self.save_settings()
    
    def load_settings(self) -> bool:
        """
        Load settings from JSON file
        Returns True if successful, False otherwise
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
                
                # Merge with defaults to ensure all required keys exist
                self.settings = self.default_settings.copy()
                self.settings.update(loaded_settings)
                
                return True
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Settings loading error: {e}")
            print("Creating new settings file with defaults...")
            self._create_default_settings()
            return False
        except Exception as e:
            print(f"Unexpected error loading settings: {e}")
            self._create_default_settings()
            return False
    
    def save_settings(self) -> bool:
        """
        Save current settings to JSON file
        Returns True if successful, False otherwise
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Settings saving error: {e}")
            return False
    
    def get_monthly_limit(self) -> float:
        """
        Return the current monthly spending limit
        """
        return self.settings.get("monthly_limit", 0)
    
    def set_monthly_limit(self, limit: float) -> bool:
        """
        Update the monthly spending limit and save to file
        
        Args:
            limit (float): The new monthly limit value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate input
            if not isinstance(limit, (int, float)):
                raise ValueError("Limit must be a number")
            
            if limit < 0:
                raise ValueError("Limit cannot be negative")
            
            # Update setting
            self.settings["monthly_limit"] = float(limit)
            
            # Save to file
            return self.save_settings()
            
        except ValueError as e:
            print(f"Invalid limit value: {e}")
            return False
        except Exception as e:
            print(f"Error setting monthly limit: {e}")
            return False
    
    def get_setting(self, key: str, default_value: Any = None) -> Any:
        """
        Get a specific setting value
        
        Args:
            key (str): The setting key
            default_value: Value to return if key doesn't exist
            
        Returns:
            The setting value or default_value
        """
        return self.settings.get(key, default_value)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """
        Set a specific setting value and save to file
        
        Args:
            key (str): The setting key
            value: The value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.settings[key] = value
            return self.save_settings()
        except Exception as e:
            print(f"Error setting {key}: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Return a copy of all current settings
        """
        return self.settings.copy()
    
    def reset_to_defaults(self) -> bool:
        """
        Reset all settings to default values and save
        """
        try:
            self.settings = self.default_settings.copy()
            return self.save_settings()
        except Exception as e:
            print(f"Error resetting settings: {e}")
            return False
    
    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """
        Update multiple settings at once
        
        Args:
            new_settings (dict): Dictionary of settings to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.settings.update(new_settings)
            return self.save_settings()
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
    
    def delete_setting(self, key: str) -> bool:
        """
        Delete a specific setting (except protected defaults)
        
        Args:
            key (str): The setting key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if key in self.default_settings:
                print(f"Cannot delete protected setting: {key}")
                return False
            
            if key in self.settings:
                del self.settings[key]
                return self.save_settings()
            
            return True  # Key doesn't exist, consider successful
            
        except Exception as e:
            print(f"Error deleting setting {key}: {e}")
            return False
    
    def __str__(self) -> str:
        """
        String representation of current settings
        """
        return f"Settings: {json.dumps(self.settings, indent=2)}"
    
    def __repr__(self) -> str:
        """
        Developer representation of SettingsManager
        """
        return f"SettingsManager(filename='{self.filename}', settings={self.settings})"