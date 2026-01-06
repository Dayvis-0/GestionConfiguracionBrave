"""
Utilidades del sistema
"""
import os
import platform
from pathlib import Path
from typing import Tuple


class SystemUtils:
    """Utilidades generales del sistema"""
    
    @staticmethod
    def detect_os() -> str:
        """Detecta el sistema operativo y retorna emoji + nombre"""
        os_name = platform.system().lower()
        if os_name == "linux":
            return "🐧 Linux"
        elif os_name == "windows":
            return "🪟 Windows"
        elif os_name == "darwin":
            return "🍎 macOS"
        else:
            return f"🔧 {os_name}"
    
    @staticmethod
    def clear_screen():
        """Limpia la pantalla según el sistema operativo"""
        os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    
    @staticmethod
    def ask_yes_no(question: str) -> bool:
        """
        Pregunta usuario Sí/No
        
        Args:
            question: Pregunta a hacer
            
        Returns:
            True si respuesta es sí, False si no
        """
        while True:
            response = input(f"{question} (S/n): ").strip().lower()
            if response in ['', 's', 'si', 'sí', 'y', 'yes']:
                return True
            elif response in ['n', 'no', 'nop']:
                return False
            else:
                print("❌ Por favor respondé Sí o No")
    
    @staticmethod
    def get_status_info() -> dict:
        """
        Obtiene información del estado actual del sistema
        
        Returns:
            Diccionario con información del estado
        """
        from core.profile_handler import ProfileHandler
        from storage.backup_manager import BackupManager
        
        brave_path = ProfileHandler.get_brave_config_path()
        profiles = ProfileHandler.detect_profiles(brave_path)
        backups = BackupManager.list_available_backups()
        saved = BackupManager.list_saved_configurations()
        brave_configs = ProfileHandler.find_brave_configurations(Path.cwd())
        
        # Combinar configs sin duplicar
        all_configs = set(brave_configs + saved)
        
        return {
            'brave_path_display': str(brave_path),
            'profiles_count': len(profiles),
            'brave_configs_count': len(all_configs),  # Total sin duplicados
            'backups_count': len(backups),
            'saved_configs_count': len(saved),
            'brave_current': brave_path.exists()
        }