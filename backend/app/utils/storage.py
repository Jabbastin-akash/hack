import json
import os
from typing import Any, Dict
from pathlib import Path
from datetime import datetime


class JSONStorage:
    """
    Simple JSON file storage utility for prototype data persistence.
    Handles reading and writing JSON files with error handling.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize JSON storage with data directory.
        
        Args:
            data_dir: Path to data directory. Defaults to app/data/
        """
        if data_dir is None:
            # Get the app/data directory
            app_dir = Path(__file__).parent.parent
            data_dir = app_dir / "data"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def read(self, filename: str, default: Any = None) -> Any:
        """
        Read data from JSON file.
        
        Args:
            filename: Name of the JSON file
            default: Default value if file doesn't exist
            
        Returns:
            Parsed JSON data or default value
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            return default if default is not None else {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return default if default is not None else {}
    
    def write(self, filename: str, data: Any) -> bool:
        """
        Write data to JSON file.
        
        Args:
            filename: Name of the JSON file
            data: Data to write (must be JSON-serializable)
            
        Returns:
            True if successful, False otherwise
        """
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            return False
    
    def append_log(self, filename: str, entry: Dict) -> bool:
        """
        Append an entry to a JSON array log file.
        
        Args:
            filename: Name of the JSON file
            entry: Dictionary entry to append
            
        Returns:
            True if successful, False otherwise
        """
        logs = self.read(filename, default=[])
        
        if not isinstance(logs, list):
            logs = []
        
        # Add timestamp if not present
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.utcnow().isoformat()
        
        logs.append(entry)
        return self.write(filename, logs)
    
    def get_latest_logs(self, filename: str, limit: int = 10) -> list:
        """
        Get the latest N log entries.
        
        Args:
            filename: Name of the JSON file
            limit: Maximum number of entries to return
            
        Returns:
            List of recent log entries
        """
        logs = self.read(filename, default=[])
        
        if not isinstance(logs, list):
            return []
        
        return logs[-limit:]


# Global storage instance
_storage: JSONStorage = None


def get_storage() -> JSONStorage:
    """
    Get the global JSON storage instance.
    
    Returns:
        JSONStorage instance
    """
    global _storage
    if _storage is None:
        _storage = JSONStorage()
    return _storage
