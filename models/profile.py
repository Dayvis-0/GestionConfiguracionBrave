"""
Modelos de datos para Brave Configuration Manager
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class Profile:
    """Representa un perfil de Brave"""
    path: Path
    folder_name: str
    display_name: str
    size: int = 0
    
    @classmethod
    def from_path(cls, path: Path) -> 'Profile':
        """Crea un Profile desde un path"""
        folder_name = path.name
        display_name = folder_name
        
        # Intentar obtener nombre real desde Preferences
        prefs_file = path / "Preferences"
        if prefs_file.exists():
            try:
                import json
                with open(prefs_file, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    if 'profile' in prefs and 'name' in prefs['profile']:
                        display_name = prefs['profile']['name']
            except:
                pass
        
        # Calcular tamaño
        size = 0
        if path.exists():
            try:
                for f in path.rglob('*'):
                    if f.is_file():
                        size += f.stat().st_size
            except:
                pass
        
        return cls(path=path, folder_name=folder_name, display_name=display_name, size=size)
    
    @property
    def size_mb(self) -> float:
        """Tamaño en MB"""
        return self.size / (1024 * 1024)


@dataclass
class Configuration:
    """Representa una configuración extraída"""
    brave_settings: Dict[str, Any]
    keyboard_shortcuts: Dict[str, Any]
    profile_name: Optional[str] = None
    extraction_metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def create_empty(cls) -> 'Configuration':
        """Crea una configuración vacía con metadatos"""
        return cls(
            brave_settings={},
            keyboard_shortcuts={},
            extraction_metadata={
                "extracted_at": datetime.now().isoformat(),
                "extraction_version": "pure_v1.0",
                "brave_version": "unknown",
                "sections_extracted": ["brave_settings", "keyboard_shortcuts"]
            }
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para JSON"""
        result = {
            "brave_settings": self.brave_settings,
            "keyboard_shortcuts": self.keyboard_shortcuts
        }
        
        if self.profile_name:
            result["profile_name"] = self.profile_name
        
        if self.extraction_metadata:
            result["extraction_metadata"] = self.extraction_metadata
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Configuration':
        """Crea desde diccionario"""
        return cls(
            brave_settings=data.get("brave_settings", {}),
            keyboard_shortcuts=data.get("keyboard_shortcuts", {}),
            profile_name=data.get("profile_name"),
            extraction_metadata=data.get("extraction_metadata")
        )


@dataclass
class Backup:
    """Representa un backup de configuración"""
    path: Path
    name: str
    timestamp: datetime
    
    @classmethod
    def from_path(cls, path: Path) -> 'Backup':
        """Crea un Backup desde un path"""
        name = path.name
        
        # Extraer timestamp del nombre
        timestamp = datetime.now()
        if "backup_" in name:
            try:
                timestamp_str = name.split("backup_")[1].replace("brave_backup_", "")
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            except:
                pass
        
        return cls(path=path, name=name, timestamp=timestamp)