"""
Gestión de backups de configuraciones de Brave
"""
import datetime
import platform
import shutil
from pathlib import Path
from typing import List, Optional

from core.profile_handler import ProfileHandler


class BackupManager:
    """Gestiona creación y restauración de backups"""
    
    @staticmethod
    def get_backups_dir() -> Path:
        """Obtiene el directorio de backups"""
        current_dir = Path.cwd()
        backups_dir = current_dir / "backup"
        backups_dir.mkdir(exist_ok=True)
        return backups_dir
    
    @staticmethod
    def get_saved_configs_dir() -> Path:
        """Obtiene el directorio de configuraciones guardadas"""
        current_dir = Path.cwd()
        saved_dir = current_dir / "saved_configs"
        saved_dir.mkdir(exist_ok=True)
        return saved_dir
    
    @staticmethod
    def list_available_backups() -> List[Path]:
        """Lista backups disponibles"""
        backups_dir = BackupManager.get_backups_dir()
        backups = []
        
        if backups_dir.exists():
            for item in backups_dir.iterdir():
                if item.is_dir() and item.name.startswith("brave_backup_"):
                    backups.append(item)
        
        return sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)
    
    @staticmethod
    def list_saved_configurations() -> List[Path]:
        """Lista configuraciones guardadas"""
        saved = []
        
        # Buscar en saved_configs/
        saved_dir = BackupManager.get_saved_configs_dir()
        if saved_dir.exists():
            for item in saved_dir.iterdir():
                if item.is_dir() and item.name.startswith("brave_saved_"):
                    saved.append(item)
        
        # Buscar en Linux/ (configs guardadas manualmente)
        current_dir = Path.cwd()
        linux_dir = current_dir / "Linux"
        if linux_dir.exists():
            for item in linux_dir.iterdir():
                if item.is_dir():
                    # Revisar si tiene archivos JSON
                    has_json = any(f.suffix == '.json' for f in item.iterdir() if f.is_file())
                    if has_json:
                        saved.append(item)
        
        return sorted(saved, key=lambda x: x.stat().st_mtime, reverse=True)
    
    @staticmethod
    def create_backup() -> Optional[Path]:
        """
        Crea un backup completo con timestamp
        
        Returns:
            Path al backup creado o None si hay error
        """
        brave_config = ProfileHandler.get_brave_config_path()
        
        if not brave_config.exists():
            print("❌ No existe configuración actual de Brave para hacer backup")
            return None
        
        backups_dir = BackupManager.get_backups_dir()
        backups_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"brave_backup_{timestamp}"
        backup_path = backups_dir / backup_name
        
        if backup_path.exists():
            print(f"❌ Ya existe un backup con el nombre: {backup_name}")
            return None
        
        print(f"🔄 Creando backup: {backup_name}")
        
        try:
            backup_path.mkdir(exist_ok=True)
            
            # Excluir archivos problemáticos
            exclude_files = {
                'SingletonLock', 'SingletonSocket', 'SingletonCookie',
                '.org.chromium.*', '*.tmp', '*.lock'
            }
            
            # Copiar archivos excluyendo problemáticos
            for item in brave_config.iterdir():
                if (item.name.startswith('.') or 
                    item.name in exclude_files or
                    'Singleton' in item.name or
                    item.name.endswith('.tmp') or
                    item.name.endswith('.lock')):
                    continue
                
                try:
                    if item.is_file():
                        shutil.copy2(item, backup_path / item.name)
                    elif item.is_dir() and not item.name.startswith('.'):
                        def ignore_files(dir, files):
                            return [f for f in files if f.startswith('.') or 'Singleton' in f or f.endswith('.tmp')]
                        
                        shutil.copytree(item, backup_path / item.name, ignore=ignore_files)
                except Exception as e:
                    print(f"⚠️ No se pudo copiar {item.name}: {e}")
                    continue
            
            print(f"✅ Backup creado: {backup_name}")
            return backup_path
            
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return None