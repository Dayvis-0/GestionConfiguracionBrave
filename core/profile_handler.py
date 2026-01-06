"""
Manejo de perfiles de Brave Browser
"""
import json
import platform
from pathlib import Path
from typing import List, Optional

from models.profile import Profile


class ProfileHandler:
    """Gestiona la detección y manejo de perfiles de Brave"""
    
    @staticmethod
    def get_brave_config_path() -> Path:
        """Obtiene la ruta de configuración de Brave según el SO"""
        os_name = platform.system().lower()
        if os_name == "windows":
            import os
            return Path(os.environ.get("LOCALAPPDATA", "")) / "BraveSoftware" / "Brave-Browser" / "User Data"
        elif os_name == "darwin":
            return Path.home() / "Library" / "Application Support" / "BraveSoftware" / "Brave-Browser" / "User Data"
        else:  # Linux
            return Path.home() / ".config" / "BraveSoftware" / "Brave-Browser"
    
    @staticmethod
    def detect_profiles(brave_path: Path) -> List[Profile]:
        """
        Detecta los perfiles disponibles en Brave
        
        Args:
            brave_path: Path a la configuración de Brave
            
        Returns:
            Lista de perfiles detectados
        """
        profiles = []
        
        if not brave_path.exists():
            return profiles
        
        # Buscar carpetas de perfiles
        for item in brave_path.iterdir():
            if item.is_dir() and item.name.startswith(("Profile ", "Default", "Guest Profile")):
                profile = Profile.from_path(item)
                profiles.append(profile)
        
        # Ordenar por nombre de carpeta
        return sorted(profiles, key=lambda p: p.folder_name)
    
    @staticmethod
    def find_brave_configurations(current_dir: Path) -> List[Path]:
        """
        Busca configuraciones de Brave en el repositorio actual
        
        Args:
            current_dir: Directorio actual donde buscar
            
        Returns:
            Lista de paths con configuraciones encontradas
        """
        possible_sources = []
        
        # Buscar en Linux/ y Windows/
        for os_dir in ["Linux", "Windows"]:
            os_path = current_dir / os_dir
            if os_path.exists():
                for item in os_path.iterdir():
                    if item.is_dir():
                        # Revisar si tiene estructura de configuración
                        has_json_files = False
                        
                        for subitem in item.iterdir():
                            if subitem.is_file():
                                if subitem.name in ["Preferences"] or subitem.name.endswith(".json"):
                                    has_json_files = True
                                    break
                        
                        if has_json_files:
                            possible_sources.append(item)
        
        return sorted(possible_sources)
    
    @staticmethod
    def get_brave_config_path_display() -> str:
        """Obtiene ruta display-friendly de configuración de Brave"""
        return str(ProfileHandler.get_brave_config_path())