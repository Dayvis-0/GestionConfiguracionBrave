"""
Motor de extracción de configuraciones de Brave
"""
import json
import datetime
from pathlib import Path
from typing import Optional

from models.profile import Configuration


class ExtractionEngine:
    """Motor principal para extraer configuraciones de Brave"""
    
    @staticmethod
    def extract_settings(profile_path: Path) -> Optional[Configuration]:
        """
        Extrae configuración pura de un perfil
        
        Args:
            profile_path: Path al perfil de Brave
            
        Returns:
            Configuration con los datos extraídos o None si hay error
        """
        try:
            # Buscar archivo de configuración
            prefs_file = profile_path / "Preferences"
            json_files = list(profile_path.glob("*.json"))
            
            if not prefs_file.exists() and not json_files:
                return None
            
            # Leer configuración
            if prefs_file.exists():
                config_data = ExtractionEngine._extract_from_preferences(prefs_file)
            else:
                config_data = ExtractionEngine._extract_from_json(json_files[0])
            
            return config_data
            
        except Exception as e:
            print(f"❌ Error al extraer configuración: {e}")
            return None
    
    @staticmethod
    def _extract_from_preferences(prefs_file: Path) -> Configuration:
        """Extrae desde archivo Preferences estándar"""
        with open(prefs_file, 'r', encoding='utf-8') as f:
            prefs = json.load(f)
        
        config = Configuration.create_empty()
        
        # Extraer configuraciones de Brave
        if 'brave' in prefs:
            config.brave_settings = prefs['brave']
        
        # Extraer atajos de teclado
        if 'shortcuts' in prefs:
            config.keyboard_shortcuts = prefs['shortcuts']
        elif 'keyboard_shortcuts' in prefs:
            config.keyboard_shortcuts = prefs['keyboard_shortcuts']
        
        # Extraer nombre del perfil
        if 'profile' in prefs and 'name' in prefs['profile']:
            config.profile_name = prefs['profile']['name']
        
        return config
    
    @staticmethod
    def _extract_from_json(json_file: Path) -> Configuration:
        """Extrae desde JSON existente (ya está en formato correcto)"""
        with open(json_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        config = Configuration.from_dict(existing_data)
        
        # Actualizar timestamp
        if config.extraction_metadata:
            config.extraction_metadata['extracted_at'] = datetime.datetime.now().isoformat()
        
        return config
    
    @staticmethod
    def save_configuration(config: Configuration, output_path: Path) -> bool:
        """
        Guarda configuración como JSON
        
        Args:
            config: Configuración a guardar
            output_path: Path donde guardar
            
        Returns:
            True si éxito, False si error
        """
        try:
            config_dict = config.to_dict()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
            return False