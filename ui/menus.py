"""
Menús de la interfaz de usuario
"""
import datetime
import shutil
from pathlib import Path
from typing import Optional

from core.profile_handler import ProfileHandler
from core.extraction_engine import ExtractionEngine
from storage.backup_manager import BackupManager
from utils.system_utils import SystemUtils
ask_yes_no = SystemUtils.ask_yes_no


class MenuManager:
    """Gestiona todos los menús interactivos"""
    
    @staticmethod
    def show_main_menu(status: dict):
        """Muestra el menú principal"""
        os_system = SystemUtils.detect_os()
        
        print(f"\n🦁 BRAVE BROWSER CONFIGURATION MANAGER - {os_system}")
        print("=" * 60)
        print(f"📂 Directorio de perfiles: {status['brave_path_display']}")
        print(f"👥 Perfiles detectados: {status['profiles_count']}")
        print(f"📄 Configuraciones disponibles: {status['brave_configs_count']}")
        print(f"💾 Backups en este repo: {status['backups_count']}")
        print(f"📁 Configs guardadas en este repo: {'✅' if status['saved_configs_count'] > 0 else '❌'}")
        print(f"🔧 Configuración en tu sistema: {'✅' if status['brave_current'] else '❌'}")
        print("-" * 60)
        print("  1. 📥 Guardar config de tu sistema")
        print("  2. 📤 Restaurar config a tu sistema")
        print("  3. 🔄 Reemplazar config de este repo")
        print("  4. 🚪 Salir")
        print("-" * 60)
    
    @staticmethod
    def show_save_menu(profiles: list) -> bool:
        """Menú para guardar configuración"""
        print(f"\n📥 GUARDAR CONFIGURACIÓN ACTUAL")
        print("=" * 40)
        print(f"📍 Desde: {ProfileHandler.get_brave_config_path_display()}")
        print(f"👥 Perfiles detectados: {len(profiles)}")
        
        for i, profile in enumerate(profiles, 1):
            print(f"   {i}. {profile.display_name} ({profile.folder_name}) - {profile.size_mb:.1f} MB")
        
        print("\n🔄 ¿Qué querés guardar?")
        print("   1. Todos los perfiles")
        print("   2. Perfil específico")
        print("   3. Solo configuración global (sin datos de navegación)")
        print("   4. 🎯 Solo settings clave (sin datos, como JSON)")
        print("   5. Volver al menú principal")
        
        try:
            choice = int(input("\n🔢 Elegir opción: "))
            
            if choice == 1:
                return MenuManager._save_all_profiles(profiles)
            elif choice == 2:
                return MenuManager._save_specific_profile(profiles)
            elif choice == 3:
                return MenuManager._save_global_config_only()
            elif choice == 4:
                return MenuManager._save_settings_only(profiles)
            elif choice == 5:
                return True  # Volver al menú principal
            else:
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                return False
                    
        except ValueError:
            print("❌ Entrada inválida")
            input("Presioná Enter para continuar...")
            return False
    
    @staticmethod
    def _save_all_profiles(profiles: list) -> bool:
        """Guarda configuración de todos los perfiles"""
        # Preguntar por backup
        if ask_yes_no("¿Querés hacer backup antes de guardar?"):
            if not BackupManager.create_backup():
                print("⚠️ No se pudo crear el backup, continuando...")
        
        # Elegir destino
        saved_path = MenuManager._choose_save_destination("brave_all_profiles_config")
        if not saved_path:
            return False
        
        print(f"🔄 Guardando configuraciones de {len(profiles)} perfiles...")
        
        success_count = 0
        for profile in profiles:
            print(f"   👤 Procesando: {profile.display_name} ({profile.folder_name})")
            
            config = ExtractionEngine.extract_settings(profile.path)
            if config:
                json_filename = f"{profile.folder_name}.json"
                json_path = saved_path / json_filename
                
                if ExtractionEngine.save_configuration(config, json_path):
                    print(f"      ✅ Configuración extraída: {json_filename}")
                    success_count += 1
                else:
                    print(f"      ❌ Error al guardar: {json_filename}")
            else:
                print(f"      ❌ Error al extraer: {profile.display_name}")
        
        if success_count > 0:
            print(f"✅ ¡Hecho! {success_count}/{len(profiles)} perfiles guardados en: {saved_path.name}")
            return True
        else:
            print("❌ No se pudo guardar ningún perfil")
            return False
    
    @staticmethod
    def _save_specific_profile(profiles: list) -> bool:
        """Guarda un perfil específico"""
        print("\n👤 Perfiles disponibles:")
        for i, profile in enumerate(profiles, 1):
            print(f"   {i}. {profile.display_name} ({profile.folder_name})")
        
        try:
            choice = int(input("\n🔢 Elegí perfil: ")) - 1
            if choice < 0 or choice >= len(profiles):
                print("❌ Opción inválida")
                return False
            
            selected_profile = profiles[choice]
            
            # Preguntar por backup
            if ask_yes_no("¿Querés hacer backup antes de guardar?"):
                if not BackupManager.create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
            
            # Elegir destino
            saved_path = MenuManager._choose_save_destination(f"brave_profile_config_{selected_profile.folder_name}")
            if not saved_path:
                return False
            
            print(f"🔄 Guardando configuración del perfil: {selected_profile.display_name}")
            
            config = ExtractionEngine.extract_settings(selected_profile.path)
            if config:
                json_filename = f"{selected_profile.folder_name}.json"
                json_path = saved_path / json_filename
                
                if ExtractionEngine.save_configuration(config, json_path):
                    print(f"✅ Perfil guardado: {json_filename}")
                    return True
                else:
                    print(f"❌ Error al guardar perfil")
                    return False
            else:
                print(f"❌ Error al extraer configuración del perfil")
                return False
                
        except ValueError:
            print("❌ Entrada inválida")
            return False
    
    @staticmethod
    def _save_global_config_only() -> bool:
        """Guarda solo configuración global"""
        brave_config = ProfileHandler.get_brave_config_path()
        
        if not brave_config.exists():
            print("❌ No existe configuración actual de Brave")
            return False
        
        if ask_yes_no("¿Querés hacer backup antes de guardar?"):
            if not BackupManager.create_backup():
                print("⚠️ No se pudo crear el backup, continuando...")
        
        saved_path = MenuManager._choose_save_destination("brave_global")
        if not saved_path:
            return False
        
        # Copiar archivos globales
        global_files = ['Local State', 'Preferences']
        for file_name in global_files:
            src_file = brave_config / file_name
            if src_file.exists():
                shutil.copy2(src_file, saved_path / file_name)
        
        print(f"✅ Configuración global guardada: {saved_path.name}")
        return True
    
    @staticmethod
    def _save_settings_only(profiles: list) -> bool:
        """Guarda solo settings clave como JSON"""
        print(f"\n📥 GUARDAR SOLO CONFIGURACIÓN (SIN DATOS)")
        print("=" * 40)
        print("🎯 Esto guardará solo:")
        print("   • Configuración de Brave (tema, privacidad, etc.)")
        print("   • Atajos de teclado personalizados")
        print("   • Extensiones instaladas")
        print("   ❌ NO guardará: historial, cookies, cachés, datos de sitios")
        print()
        
        # Mostrar perfiles
        for i, profile in enumerate(profiles, 1):
            print(f"   {i}. {profile.display_name} ({profile.folder_name})")
        
        print(f"   {len(profiles) + 1}. Todos los perfiles")
        print(f"   {len(profiles) + 2}. Volver al menú anterior")
        
        try:
            choice = int(input(f"\n🔢 Elegí perfil (1-{len(profiles) + 2}): "))
            
            if choice == len(profiles) + 2:
                return False
            
            saved_path = MenuManager._choose_save_destination("brave_settings")
            if not saved_path:
                return False
            
            # Procesar perfiles seleccionados
            profiles_to_process = []
            if choice == len(profiles) + 1:
                profiles_to_process = profiles
            else:
                profiles_to_process = [profiles[choice - 1]]
            
            success_count = 0
            for profile in profiles_to_process:
                print(f"\n📄 Extrayendo configuración de: {profile.display_name}")
                
                config = ExtractionEngine.extract_settings(profile.path)
                if config:
                    output_file = saved_path / f"{profile.folder_name}.json"
                    if ExtractionEngine.save_configuration(config, output_file):
                        print(f"✅ Guardado: {output_file.name}")
                        success_count += 1
                    else:
                        print(f"❌ Error al guardar: {profile.display_name}")
                else:
                    print(f"❌ Error al extraer: {profile.display_name}")
            
            if success_count > 0:
                print(f"\n✅ Configuración guardada en: {saved_path}")
                print(f"📊 Perfiles procesados: {success_count}/{len(profiles_to_process)}")
                return True
            else:
                print("\n❌ No se pudo extraer ninguna configuración")
                return False
                
        except ValueError:
            print("❌ Entrada inválida")
            return False
    
    @staticmethod
    def _choose_save_destination(base_name: str) -> Optional[Path]:
        """Elige destino para guardar configuración"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\n📁 ¿Dónde querés guardar?")
        print("   1. En saved_configs/ (recomendado)")
        print("   2. En Linux/ (repositorio local)")
        print("   3. En una carpeta personalizada")
        print("   4. En backup/ (como backup manual)")
        print("   5. Volver al menú anterior")
        
        try:
            choice = int(input("\n🔢 Elegí opción: "))
            
            if choice == 5:
                return None
            
            if choice == 1:
                saved_dir = BackupManager.get_saved_configs_dir()
                saved_name = f"{base_name}_{timestamp}"
                saved_path = saved_dir / saved_name
            elif choice == 2:
                current_dir = Path.cwd()
                linux_dir = current_dir / "Linux"
                linux_dir.mkdir(exist_ok=True)
                saved_name = f"{base_name}_{timestamp}"
                saved_path = linux_dir / saved_name
            elif choice == 3:
                custom_name = input("📝 Nombre de la carpeta: ").strip()
                if not custom_name:
                    print("❌ El nombre no puede estar vacío")
                    return None
                current_dir = Path.cwd()
                saved_path = current_dir / custom_name
            elif choice == 4:
                backups_dir = BackupManager.get_backups_dir()
                saved_name = f"{base_name}_{timestamp}"
                saved_path = backups_dir / saved_name
            else:
                print("❌ Opción inválida")
                return None
            
            saved_path.mkdir(exist_ok=True, parents=True)
            return saved_path
            
        except ValueError:
            print("❌ Entrada inválida")
            return None
    
    @staticmethod
    def show_restore_menu() -> bool:
        """Menú para restaurar configuración al sistema"""
        print("\n📤 RESTAURAR CONFIGURACIÓN")
        print("=" * 40)
        print("   1. Restaurar desde configuración guardada")
        print("   2. Restaurar desde backup")
        print("   3. Volver al menú principal")
        
        try:
            choice = int(input("\n🔢 Seleccioná opción (1-3): "))
            
            if choice == 1:
                return MenuManager._restore_from_saved()
            elif choice == 2:
                return MenuManager._restore_from_backup()
            elif choice == 3:
                return True  # Volver al menú principal
            else:
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                return False
                
        except ValueError:
            print("❌ Entrada inválida")
            input("Presioná Enter para continuar...")
            return False
    
    @staticmethod
    def _restore_from_saved() -> bool:
        """Restaura configuración desde configuraciones guardadas"""
        saved_configs = BackupManager.list_saved_configurations()
        
        if not saved_configs:
            print("❌ No hay configuraciones guardadas")
            input("Presioná Enter para continuar...")
            return False
        
        print("\n📦 CONFIGURACIONES GUARDADAS:")
        print("=" * 50)
        for i, saved in enumerate(saved_configs, 1):
            saved_name = saved.name.replace("brave_saved_", "")
            if len(saved_name) >= 14 and saved_name[8] == "_":
                try:
                    dt = datetime.datetime.strptime(saved_name, "%Y%m%d_%H%M%S")
                    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
                    print(f"  {i}. {formatted_time}")
                except:
                    print(f"  {i}. {saved_name}")
            else:
                print(f"  {i}. {saved_name}")
        
        print(f"  {len(saved_configs) + 1}. Volver")
        print("=" * 50)
        
        try:
            choice = int(input("\n🔢 Elegí configuración: ")) - 1
            if choice == len(saved_configs):
                return False
            
            if choice < 0 or choice >= len(saved_configs):
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                return False
            
            selected_saved = saved_configs[choice]
            saved_name = selected_saved.name.replace("brave_saved_", "")
            
            # Verificar que Brave esté cerrado
            if not ask_yes_no("¿Cerraste completamente Brave Browser?"):
                print("❌ Cerrá Brave y volvé a intentarlo")
                input("Presioná Enter para continuar...")
                return False
            
            # Obtener perfiles del sistema actual
            brave_config = ProfileHandler.get_brave_config_path()
            current_profiles = ProfileHandler.detect_profiles(brave_config)
            
            if not current_profiles:
                print("❌ No se encontraron perfiles en el sistema")
                input("Presioná Enter para continuar...")
                return False
            
            print(f"\n👤 Perfiles disponibles en tu sistema:")
            for i, profile in enumerate(current_profiles, 1):
                print(f"   {i}. {profile.display_name} ({profile.folder_name})")
            print(f"   {len(current_profiles) + 1}. Aplicar a toda la configuración (reemplazar todo)")
            print(f"   {len(current_profiles) + 2}. Volver")
            
            try:
                profile_choice = int(input(f"\n🔢 ¿A qué perfil querés aplicar la configuración '{saved_name}'? (1-{len(current_profiles) + 2}): "))
                
                if profile_choice == len(current_profiles) + 2:
                    return False
                elif profile_choice == len(current_profiles) + 1:
                    # Reemplazar toda la configuración (comportamiento anterior)
                    # Reemplazar toda la configuración (comportamiento anterior)
                    # Hacer backup antes de restaurar
                    if ask_yes_no("¿Querés hacer backup antes de restaurar?"):
                        if not BackupManager.create_backup():
                            print("⚠️ No se pudo crear el backup, continuando...")
                    
                    brave_config = ProfileHandler.get_brave_config_path()
                    print(f"\n📤 Restaurando configuración '{saved_name}' (global)...")
                    print(f"📍 Hacia: {brave_config}")
                    
                    # Eliminar configuración actual
                    if brave_config.exists():
                        shutil.rmtree(brave_config)
                    
                    # Copiar configuración guardada
                    shutil.copytree(selected_saved, brave_config)
                    
                    print(f"✅ Configuración global restaurada exitosamente!")
                    print("🔄 Podés abrir Brave Browser ahora")
                    
                    return True
                elif profile_choice < 1 or profile_choice > len(current_profiles):
                    print("❌ Opción inválida")
                    input("Presioná Enter para continuar...")
                    return False
                else:
                    # Aplicar a perfil específico
                    target_profile = current_profiles[profile_choice - 1]
                    
                    # Hacer backup antes de restaurar
                    if ask_yes_no("¿Querés hacer backup antes de restaurar el perfil?"):
                        if not BackupManager.create_backup():
                            print("⚠️ No se pudo crear el backup, continuando...")
                    
                    print(f"\n📤 Aplicando configuración '{saved_name}' al perfil específico...")
                    print(f"👤 Perfil destino: {target_profile.display_name} ({target_profile.folder_name})")
                    
                    try:
                        # Buscar JSON de configuración en la carpeta guardada
                        config_json = None
                        for item in selected_saved.iterdir():
                            if item.is_file() and item.suffix == '.json':
                                config_json = item
                                break
                        
                        if not config_json:
                            print("❌ No se encontró configuración JSON para restaurar")
                            return False
                        
                        # Leer configuración desde JSON
                        import json
                        with open(config_json, 'r', encoding='utf-8') as f:
                            config_data = json.load(f)
                        
                        # Leer Preferences actual del perfil
                        prefs_file = target_profile.path / "Preferences"
                        current_prefs = {}
                        if prefs_file.exists():
                            with open(prefs_file, 'r', encoding='utf-8') as f:
                                current_prefs = json.load(f)
                        
                        # Actualizar solo la sección brave
                        if 'brave_settings' in config_data:
                            current_prefs['brave'] = config_data['brave_settings']
                        if 'keyboard_shortcuts' in config_data:
                            current_prefs['shortcuts'] = config_data['keyboard_shortcuts']
                        
                        # Guardar configuración actualizada
                        with open(prefs_file, 'w', encoding='utf-8') as f:
                            json.dump(current_prefs, f, indent=2)
                        
                        print(f"✅ Configuración aplicada al perfil '{target_profile.display_name}'!")
                        print("🔄 Podés abrir Brave Browser ahora")
                        return True
                        
                    except Exception as e:
                        print(f"❌ Error al aplicar configuración al perfil: {e}")
                        return False
                    
            except ValueError:
                print("❌ Entrada inválida")
                input("Presioná Enter para continuar...")
                return False
            
            print(f"✅ Configuración restaurada exitosamente!")
            print("🔄 Podés abrir Brave Browser ahora")
            
            return True
            
        except ValueError:
            print("❌ Entrada inválida")
            input("Presioná Enter para continuar...")
            return False
        except Exception as e:
            print(f"❌ Error al restaurar: {e}")
            input("Presioná Enter para continuar...")
            return False
    
    @staticmethod
    def _restore_from_backup() -> bool:
        """Restaura configuración desde backup"""
        backups = BackupManager.list_available_backups()
        
        if not backups:
            print("❌ No hay backups disponibles")
            input("Presioná Enter para continuar...")
            return False
        
        print("\n💾 BACKUPS DISPONIBLES:")
        print("=" * 50)
        for i, backup in enumerate(backups, 1):
            backup_name = backup.name.replace("brave_backup_", "")
            if len(backup_name) >= 14 and backup_name[8] == "_":
                try:
                    dt = datetime.datetime.strptime(backup_name, "%Y%m%d_%H%M%S")
                    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
                    print(f"  {i}. {formatted_time}")
                except:
                    print(f"  {i}. {backup_name}")
            else:
                print(f"  {i}. {backup_name}")
        
        print(f"  {len(backups) + 1}. Volver")
        print("=" * 50)
        
        try:
            choice = int(input("\n🔢 Elegí backup: ")) - 1
            if choice == len(backups):
                return False
            
            if choice < 0 or choice >= len(backups):
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                return False
            
            selected_backup = backups[choice]
            backup_name = selected_backup.name.replace("brave_backup_", "")
            
            # Verificar que Brave esté cerrado
            if not ask_yes_no("¿Cerraste completamente Brave Browser?"):
                print("❌ Cerrá Brave y volvé a intentarlo")
                input("Presioná Enter para continuar...")
                return False
            
            # Hacer backup antes de restaurar
            if ask_yes_no("¿Querés hacer backup antes de restaurar?"):
                if not BackupManager.create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
            
            brave_config = ProfileHandler.get_brave_config_path()
            
            print(f"\n📤 Restaurando backup '{backup_name}'...")
            print(f"📍 Hacia: {brave_config}")
            
            # Eliminar configuración actual
            if brave_config.exists():
                shutil.rmtree(brave_config)
            
            # Copiar backup
            shutil.copytree(selected_backup, brave_config)
            
            print(f"✅ Backup restaurado exitosamente!")
            print("🔄 Podés abrir Brave Browser ahora")
            
            return True
            
        except ValueError:
            print("❌ Entrada inválida")
            input("Presioná Enter para continuar...")
            return False
        except Exception as e:
            print(f"❌ Error al restaurar backup: {e}")
            input("Presioná Enter para continuar...")
            return False
    
    @staticmethod
    def show_replace_menu() -> bool:
        """Menú para reemplazar configuración local"""
        while True:
            print("\n🔄 Reemplazando configuración de este repo...")
            print("   1. Reemplazar con config guardada")
            print("   2. Reemplazar con backup")
            print("   3. Volver al menú principal")
            
            try:
                choice = int(input("\n🔢 Seleccioná opción (1-3): "))
                
                if choice == 1:
                    return MenuManager._replace_with_saved()
                elif choice == 2:
                    return MenuManager._replace_with_backup()
                elif choice == 3:
                    return True  # Volver al menú principal
                else:
                    print("❌ Opción inválida")
                    input("Presioná Enter para continuar...")
                    
            except ValueError:
                print("❌ Entrada inválida")
                input("Presioná Enter para continuar...")
    
    @staticmethod
    def _replace_with_saved() -> bool:
        """Reemplazar configuración local con configuración guardada"""
        saved_configs = BackupManager.list_saved_configurations()
        
        if not saved_configs:
            print("❌ No hay configuraciones guardadas")
            input("Presioná Enter para continuar...")
            return False
        
        print("\n📦 CONFIGURACIONES GUARDADAS:")
        print("=" * 50)
        for i, saved in enumerate(saved_configs, 1):
            saved_name = saved.name.replace("brave_saved_", "")
            if len(saved_name) >= 14 and saved_name[8] == "_":
                try:
                    dt = datetime.datetime.strptime(saved_name, "%Y%m%d_%H%M%S")
                    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
                    print(f"  {i}. {formatted_time}")
                except:
                    print(f"  {i}. {saved_name}")
            else:
                print(f"  {i}. {saved_name}")
        
        print(f"  {len(saved_configs) + 1}. Volver")
        print("=" * 50)
        
        try:
            choice = int(input("\n🔢 Elegí configuración: ")) - 1
            if choice == len(saved_configs):
                return False
            
            if choice < 0 or choice >= len(saved_configs):
                print("❌ Opción inválida")
                return False
            
            selected_saved = saved_configs[choice]
            saved_name = selected_saved.name.replace("brave_saved_", "")
            
            brave_configs = ProfileHandler.find_brave_configurations(Path.cwd())
            if not brave_configs:
                print("❌ No hay configuraciones en esta carpeta para reemplazar")
                input("Presioná Enter para continuar...")
                return False
            
            print("\n📁 Seleccioná qué configuración reemplazar:")
            for i, config_dir in enumerate(brave_configs, 1):
                print(f"  {i}. {config_dir.name}")
            
            config_choice = int(input("\n🔢 Elegí configuración a reemplazar: ")) - 1
            if config_choice < 0 or config_choice >= len(brave_configs):
                print("❌ Opción inválida")
                return False
            
            target_config = brave_configs[config_choice]
            
            print(f"\n🔄 Reemplazando '{target_config.name}' con configuración guardada '{saved_name}'...")
            if not ask_yes_no("¿Esto reemplazará la carpeta seleccionada. Continuar?"):
                print("❌ Operación cancelada")
                return False
            
            # Hacer backup si se desea
            if ask_yes_no("¿Hacer backup antes de reemplazar?"):
                if not BackupManager.create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
            
            # Eliminar carpeta de configuración
            if target_config.exists():
                shutil.rmtree(target_config)
            
            # Copiar configuración guardada
            shutil.copytree(selected_saved, target_config)
            print(f"✅ Configuración '{target_config.name}' reemplazada con configuración guardada '{saved_name}'!")
            
            return True
            
        except ValueError:
            print("❌ Entrada inválida")
            return False
        except Exception as e:
            print(f"❌ Error al reemplazar: {e}")
            return False
    
    @staticmethod
    def _replace_with_backup() -> bool:
        """Reemplazar configuración local con backup"""
        backups = BackupManager.list_available_backups()
        
        if not backups:
            print("❌ No hay backups disponibles")
            input("Presioná Enter para continuar...")
            return False
        
        print("\n💾 BACKUPS DISPONIBLES:")
        print("=" * 50)
        for i, backup in enumerate(backups, 1):
            backup_name = backup.name.replace("brave_backup_", "")
            if len(backup_name) >= 14 and backup_name[8] == "_":
                try:
                    dt = datetime.datetime.strptime(backup_name, "%Y%m%d_%H%M%S")
                    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
                    print(f"  {i}. {formatted_time}")
                except:
                    print(f"  {i}. {backup_name}")
            else:
                print(f"  {i}. {backup_name}")
        
        print(f"  {len(backups) + 1}. Volver")
        print("=" * 50)
        
        try:
            choice = int(input("\n🔢 Elegí backup: ")) - 1
            if choice == len(backups):
                return False
            
            if choice < 0 or choice >= len(backups):
                print("❌ Opción inválida")
                return False
            
            selected_backup = backups[choice]
            backup_name = selected_backup.name.replace("brave_backup_", "")
            
            brave_configs = ProfileHandler.find_brave_configurations(Path.cwd())
            if not brave_configs:
                print("❌ No hay configuraciones en esta carpeta para reemplazar")
                input("Presioná Enter para continuar...")
                return False
            
            print("\n📁 Seleccioná qué configuración reemplazar:")
            for i, config_dir in enumerate(brave_configs, 1):
                print(f"  {i}. {config_dir.name}")
            
            config_choice = int(input("\n🔢 Elegí configuración a reemplazar: ")) - 1
            if config_choice < 0 or config_choice >= len(brave_configs):
                print("❌ Opción inválida")
                return False
            
            target_config = brave_configs[config_choice]
            
            print(f"\n🔄 Reemplazando '{target_config.name}' con backup '{backup_name}'...")
            if not ask_yes_no("¿Esto reemplazará la carpeta seleccionada. Continuar?"):
                print("❌ Operación cancelada")
                return False
            
            # Hacer backup si se desea
            if ask_yes_no("¿Hacer backup antes de reemplazar?"):
                if not BackupManager.create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
            
            # Eliminar carpeta de configuración
            if target_config.exists():
                shutil.rmtree(target_config)
            
            # Copiar backup a la configuración
            shutil.copytree(selected_backup, target_config)
            print(f"✅ Configuración '{target_config.name}' reemplazada con backup '{backup_name}'!")
            
            return True
            
        except ValueError:
            print("❌ Entrada inválida")
            return False
        except Exception as e:
            print(f"❌ Error al reemplazar: {e}")
            return False