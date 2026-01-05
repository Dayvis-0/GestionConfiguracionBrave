#!/usr/bin/env python3
"""
Script para gestionar configuración de Brave Browser desde backup
Maneja perfiles múltiples y configuraciones específicas del navegador
"""

import os
import platform
import shutil
import sys
import argparse
import datetime
import json
from pathlib import Path

def detect_os():
    """Detecta el sistema operativo"""
    os_name = platform.system().lower()
    if os_name == "linux":
        return "🐧 Linux"
    elif os_name == "windows":
        return "🪟 Windows"
    elif os_name == "darwin":
        return "🍎 macOS"
    else:
        return f"🔧 {os_name}"

def get_brave_config_path():
    """Obtiene la ruta de configuración de Brave según el SO"""
    os_name = platform.system().lower()
    if os_name == "windows":
        return Path(os.environ.get("LOCALAPPDATA", "")) / "BraveSoftware" / "Brave-Browser" / "User Data"
    elif os_name == "darwin":
        return Path.home() / "Library" / "Application Support" / "BraveSoftware" / "Brave-Browser" / "User Data"
    else:  # Linux
        return Path.home() / ".config" / "BraveSoftware" / "Brave-Browser"

def get_backups_dir():
    """Obtiene la ruta del directorio de backups"""
    current_dir = Path.cwd()
    backups_dir = current_dir / "backup"
    backups_dir.mkdir(exist_ok=True)
    return backups_dir

def get_saved_configs_dir():
    """Obtiene la ruta del directorio de configuraciones guardadas"""
    current_dir = Path.cwd()
    saved_dir = current_dir / "saved_configs"
    saved_dir.mkdir(exist_ok=True)
    return saved_dir

def detect_profiles(brave_path):
    """Detecta los perfiles disponibles en Brave"""
    profiles = []
    
    if not brave_path.exists():
        return profiles
    
    # Buscar carpetas de perfiles
    for item in brave_path.iterdir():
        if item.is_dir() and item.name.startswith(("Profile ", "Default", "Guest Profile")):
            # Intentar obtener el nombre del perfil desde Preferences
            profile_name = item.name
            preferences_file = item / "Preferences"
            if preferences_file.exists():
                try:
                    with open(preferences_file, 'r', encoding='utf-8') as f:
                        prefs = json.load(f)
                        if 'profile' in prefs and 'name' in prefs['profile']:
                            profile_name = prefs['profile']['name']
                except:
                    pass
            
            # Calcular tamaño
            size = 0
            if item.exists():
                try:
                    for f in item.rglob('*'):
                        if f.is_file():
                            size += f.stat().st_size
                except:
                    pass
            
            profiles.append({
                'path': item,
                'folder_name': item.name,
                'display_name': profile_name,
                'size': size
            })
    
    return sorted(profiles, key=lambda x: x['folder_name'])

def find_brave_configurations():
    """Busca configuraciones de Brave en el repositorio actual"""
    current_dir = Path.cwd()
    possible_sources = []
    
    # Buscar carpetas de configuración (Linux, Windows)
    linux_dir = current_dir / "Linux"
    windows_dir = current_dir / "Windows"
    
    # Buscar en Linux/ - buscar carpetas que puedan ser configs de Brave
    if linux_dir.exists():
        for item in linux_dir.iterdir():
            if item.is_dir():
                # Revisar si tiene estructura de configuración de Brave
                # Puede tener Preferences.json o archivos .json dentro
                has_json_files = False
                has_prefs = False
                
                for subitem in item.iterdir():
                    if subitem.is_file():
                        if subitem.name == "Preferences" or subitem.name.endswith(".json"):
                            has_json_files = True
                            if subitem.name == "Preferences":
                                has_prefs = True
                
                # Considerarlo como configuración si tiene archivos json
                if has_json_files:
                    possible_sources.append(item)
    
    # Buscar en Windows/
    if windows_dir.exists():
        for item in windows_dir.iterdir():
            if item.is_dir():
                has_json_files = False
                for subitem in item.iterdir():
                    if subitem.is_file() and subitem.name.endswith(".json"):
                        has_json_files = True
                        break
                
                if has_json_files:
                    possible_sources.append(item)
    
    return sorted(possible_sources)

def list_saved_configurations():
    """Lista las configuraciones guardadas"""
    saved = []
    
    # Buscar en saved_configs/
    saved_dir = get_saved_configs_dir()
    if saved_dir.exists():
        for item in saved_dir.iterdir():
            if item.is_dir() and item.name.startswith("brave_saved_"):
                saved.append(item)
    
    # También buscar en Linux/ (configs guardadas manualmente)
    current_dir = Path.cwd()
    linux_dir = current_dir / "Linux"
    if linux_dir.exists():
        for item in linux_dir.iterdir():
            if item.is_dir():
                # Detectar como config guardada si tiene archivos json o Preferences
                has_config_files = False
                for subitem in item.iterdir():
                    if subitem.is_file() and (subitem.name.endswith(".json") or subitem.name == "Preferences"):
                        has_config_files = True
                        break
                
                if has_config_files:
                    saved.append(item)
    
    # Ordenar por nombre
    saved.sort(key=lambda x: x.name)
    return saved

def list_available_backups():
    """Lista los backups disponibles"""
    backups_dir = get_backups_dir()
    
    if not backups_dir.exists():
        return []
    
    backups = []
    for item in backups_dir.iterdir():
        if item.is_dir() and item.name.startswith("brave_backup_"):
            backups.append(item)
    
    # Ordenar por nombre (que incluye timestamp)
    backups.sort(reverse=True)
    return backups

def get_status_info():
    """Obtiene información del estado actual"""
    brave_config = get_brave_config_path()
    profiles = detect_profiles(brave_config)
    saved_configs = list_saved_configurations()
    backups = list_available_backups()
    brave_configs_repo = find_brave_configurations()
    
    status = {
        'brave_current': brave_config.exists(),
        'profiles_count': len(profiles),
        'backups_count': len(backups),
        'saved_configs_count': len(saved_configs),
        'brave_configs_count': len(brave_configs_repo),
        'brave_path_display': get_brave_config_path_display()
    }
    return status

def get_brave_config_path_display():
    """Obtiene la ruta de config para mostrar según SO"""
    os_name = platform.system().lower()
    if os_name == "windows":
        return "%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser\\User Data"
    elif os_name == "darwin":
        return "~/Library/Application Support/BraveSoftware/Brave-Browser/User Data"
    else:
        return "~/.config/BraveSoftware/Brave-Browser"

def ask_yes_no(message):
    """Pregunta Sí/No y devuelve True para Sí, False para No"""
    while True:
        response = input(f"\n{message} (S/n): ").lower().strip()
        if response == 's' or response == '':
            return True
        elif response == 'n':
            return False
        else:
            print("❌ Por favor respondé Sí o No")

def create_backup():
    """Crea un backup con timestamp"""
    brave_config = get_brave_config_path()
    
    if not brave_config.exists():
        print("❌ No existe configuración actual de Brave para hacer backup")
        return None
    
    # Crear directorio de backups si no existe
    backups_dir = get_backups_dir()
    backups_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"brave_backup_{timestamp}"
    backup_path = backups_dir / backup_name
    
    # Verificar si ya existe
    if backup_path.exists():
        print(f"❌ Ya existe un backup con el nombre: {backup_name}")
        return None
    
    print(f"🔄 Creando backup: {backup_name}")
    
    try:
        # Crear la carpeta de backup
        backup_path.mkdir(exist_ok=True)
        
        # Excluir archivos problemáticos
        exclude_files = {
            'SingletonLock', 'SingletonSocket', 'SingletonCookie',
            '.org.chromium.*', '*.tmp', '*.lock'
        }
        
        # Copiar solo lo necesario, excluyendo archivos temporales y bloqueados
        for item in brave_config.iterdir():
            # Omitir archivos problemáticos
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
                    # Para directorios, usar copytree con ignore
                    def ignore_files(dir, files):
                        return [f for f in files if f.startswith('.') or 'Singleton' in f or f.endswith('.tmp')]
                    
                    shutil.copytree(item, backup_path / item.name, ignore=ignore_files)
            except Exception as e:
                print(f"⚠️ Omitiendo {item.name}: {e}")
                continue
        
        print(f"✅ Backup completado: {backup_name}")
        return backup_path
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return None

def save_all_profiles():
    """Guarda todos los perfiles (Solo configuraciones, sin datos personales)"""
    brave_config = get_brave_config_path()
    profiles = detect_profiles(brave_config)
    
    if not profiles:
        print("❌ No se detectaron perfiles de Brave")
        return False
    
    # Preguntar por backup
    if ask_yes_no("¿Querés hacer backup antes de guardar?"):
        if not create_backup():
            print("⚠️ No se pudo crear el backup, continuando...")
    
    # Preguntar dónde guardar
    print("\n📁 ¿Dónde querés guardar?")
    print("   1. En saved_configs/ (recomendado)")
    print("   2. En Linux/ (repositorio local)")
    print("   3. En una carpeta personalizada")
    print("   4. En backup/ (como backup manual)")
    print("   5. Volver al menú anterior")
    
    try:
        choice = int(input("\n🔢 Elegí opción: "))
        
        if choice == 5:
            return False
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if choice == 1:
            saved_dir = get_saved_configs_dir()
            saved_name = f"brave_all_profiles_config_{timestamp}"
            saved_path = saved_dir / saved_name
        elif choice == 2:
            current_dir = Path.cwd()
            linux_dir = current_dir / "Linux"
            linux_dir.mkdir(exist_ok=True)
            saved_name = f"brave_all_profiles_config_{timestamp}"
            saved_path = linux_dir / saved_name
        elif choice == 3:
            custom_name = input("📝 Nombre de la carpeta: ").strip()
            if not custom_name:
                print("❌ El nombre no puede estar vacío")
                return False
            current_dir = Path.cwd()
            saved_path = current_dir / custom_name
        elif choice == 4:
            backups_dir = get_backups_dir()
            saved_name = f"brave_all_profiles_config_{timestamp}"
            saved_path = backups_dir / saved_name
        else:
            print("❌ Opción inválida")
            return False
        
        # Crear la carpeta de destino
        saved_path.mkdir(exist_ok=True, parents=True)
        
        print(f"🔄 Guardando configuraciones de {len(profiles)} perfiles...")
        
        # 1. Copiar archivos globales primero
        global_files = ['Local State', 'Preferences']
        for f in global_files:
            src = brave_config / f
            if src.exists():
                shutil.copy2(src, saved_path / f)

        # 2. Copiar solo configuración de cada perfil
        config_files_to_keep = ['Preferences', 'Web Data', 'Secure Preferences']
        
        for profile in profiles:
            profile_folder = profile['folder_name']
            dest_profile_path = saved_path / profile_folder
            dest_profile_path.mkdir(exist_ok=True)
            
            print(f"   👤 Procesando: {profile['display_name']} ({profile_folder})")
            
            for config_file in config_files_to_keep:
                src_file = profile['path'] / config_file
                if src_file.exists():
                    shutil.copy2(src_file, dest_profile_path / config_file)
        
        print(f"✅ ¡Hecho! Configuraciones guardadas en: {saved_path.name}")
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        return False

def save_specific_profile():
    """Guarda un perfil específico (Solo configuraciones, sin datos personales)"""
    brave_config = get_brave_config_path()
    profiles = detect_profiles(brave_config)
    
    if not profiles:
        print("❌ No se detectaron perfiles de Brave")
        return False
    
    print("\n👥 ¿Qué perfil querés guardar?")
    for i, profile in enumerate(profiles, 1):
        size_mb = profile['size'] / (1024 * 1024)
        print(f"   {i}. {profile['display_name']} ({profile['folder_name']}) - {size_mb:.1f} MB")
    print(f"   {len(profiles) + 1}. Volver al menú anterior")
    
    try:
        choice = int(input("\n🔢 Elegí perfil: ")) - 1
        if choice == len(profiles):
            return False
        
        if choice < 0 or choice >= len(profiles):
            print("❌ Opción inválida")
            return False
        
        selected_profile = profiles[choice]
        
        # Preguntar por backup
        if ask_yes_no("¿Querés hacer backup antes de guardar?"):
            print("\n💡 Consejo: Para backup 100% seguro, cerrá Brave antes")
            if ask_yes_no("¿Querés cerrar Brave y hacer backup?"):
                print("📂 Por favor, cerrá todas las ventanas de Brave...")
                input("Presioná Enter cuando esté cerrado para continuar...")
            
            if not create_backup():
                print("⚠️ No se pudo crear el backup, continuando...")
        
        # Preguntar dónde guardar
        print("\n📁 ¿Dónde querés guardar?")
        print("   1. En saved_configs/ (recomendado)")
        print("   2. En Linux/ (repositorio local)")
        print("   3. En una carpeta personalizada")
        print("   4. En backup/ (como backup manual)")
        print("   5. Volver al menú anterior")
        
        dest_choice = int(input("\n🔢 Elegí opción: "))
        
        if dest_choice == 5:
            return False
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        profile_name = selected_profile['display_name'].replace(" ", "_")
        
        if dest_choice == 1:
            saved_dir = get_saved_configs_dir()
            saved_name = f"brave_profile_config_{profile_name}_{timestamp}"
            saved_path = saved_dir / saved_name
        elif dest_choice == 2:
            current_dir = Path.cwd()
            linux_dir = current_dir / "Linux"
            linux_dir.mkdir(exist_ok=True)
            saved_name = f"brave_profile_config_{profile_name}_{timestamp}"
            saved_path = linux_dir / saved_name
        elif dest_choice == 3:
            custom_name = input("📝 Nombre de la carpeta: ").strip()
            if not custom_name:
                print("❌ El nombre no puede estar vacío")
                return False
            current_dir = Path.cwd()
            saved_path = current_dir / custom_name
        elif dest_choice == 4:
            backups_dir = get_backups_dir()
            saved_name = f"brave_profile_config_{profile_name}_{timestamp}"
            saved_path = backups_dir / saved_name
        else:
            print("❌ Opción inválida")
            return False
        
        # Crear la configuración guardada
        saved_path.mkdir(exist_ok=True, parents=True)
        
        print(f"🔄 Guardando configuración del perfil: {selected_profile['display_name']}")
        
        # 1. Copiar archivos globales necesarios
        global_files = ['Local State', 'Preferences']
        for f in global_files:
            src = brave_config / f
            if src.exists():
                shutil.copy2(src, saved_path / f)

        # 2. Copiar solo configuración del perfil seleccionado
        config_files_to_keep = ['Preferences', 'Web Data', 'Secure Preferences']
        profile_folder = selected_profile['folder_name']
        dest_profile_path = saved_path / profile_folder
        dest_profile_path.mkdir(exist_ok=True)
        
        for config_file in config_files_to_keep:
            src_file = selected_profile['path'] / config_file
            if src_file.exists():
                shutil.copy2(src_file, dest_profile_path / config_file)
        
        print(f"✅ Perfil guardado (solo config): {saved_path.name}")
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al guardar perfil: {e}")
        return False

def save_global_config_only():
    """Guarda solo la configuración global sin datos de navegación"""
    brave_config = get_brave_config_path()
    
    if not brave_config.exists():
        print("❌ No existe configuración actual de Brave")
        return False
    
    # Preguntar por backup
    if ask_yes_no("¿Querés hacer backup antes de guardar?"):
        if not create_backup():
            print("⚠️ No se pudo crear el backup, continuando...")
    
    # Preguntar dónde guardar
    print("\n📁 ¿Dónde querés guardar?")
    print("   1. En saved_configs/ (recomendado)")
    print("   2. En Linux/ (repositorio local)")
    print("   3. En una carpeta personalizada")
    print("   4. En backup/ (como backup manual)")
    print("   5. Volver al menú anterior")
    
    try:
        choice = int(input("\n🔢 Elegí opción: "))
        
        if choice == 5:
            return False
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if choice == 1:
            saved_dir = get_saved_configs_dir()
            saved_name = f"brave_global_{timestamp}"
            saved_path = saved_dir / saved_name
        elif choice == 2:
            # Guardar en Linux/
            current_dir = Path.cwd()
            linux_dir = current_dir / "Linux"
            linux_dir.mkdir(exist_ok=True)
            saved_name = f"brave_global_{timestamp}"
            saved_path = linux_dir / saved_name
        elif choice == 3:
            custom_name = input("📝 Nombre de la carpeta: ").strip()
            if not custom_name:
                print("❌ El nombre no puede estar vacío")
                return False
            current_dir = Path.cwd()
            saved_path = current_dir / custom_name
        elif choice == 4:
            backups_dir = get_backups_dir()
            saved_name = f"brave_global_{timestamp}"
            saved_path = backups_dir / saved_name
        else:
            print("❌ Opción inválida")
            return False
        
        # Crear la configuración guardada
        saved_path.mkdir(exist_ok=True)
        
        # Copiar solo archivos globales
        global_files = ['Local State', 'Preferences']
        for file_name in global_files:
            src_file = brave_config / file_name
            if src_file.exists():
                shutil.copy2(src_file, saved_path / file_name)
        
        print(f"✅ Configuración global guardada: {saved_path.name}")
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al guardar configuración global: {e}")
        return False

def save_current_configuration():
    """Menú principal para guardar configuración"""
    brave_config = get_brave_config_path()
    profiles = detect_profiles(brave_config)
    
    if not profiles:
        print("❌ No se detectaron perfiles de Brave")
        print("📂 Abrí Brave Browser primero para crear los perfiles")
        return False
    
    print(f"\n📥 GUARDAR CONFIGURACIÓN ACTUAL")
    print("=" * 40)
    print(f"📍 Desde: {get_brave_config_path_display()}")
    print(f"👥 Perfiles detectados: {len(profiles)}")
    
    for i, profile in enumerate(profiles, 1):
        size_mb = profile['size'] / (1024 * 1024)
        print(f"   {i}. {profile['display_name']} ({profile['folder_name']}) - {size_mb:.1f} MB")
    
    print("\n🔄 ¿Qué querés guardar?")
    print("   1. Todos los perfiles")
    print("   2. Perfil específico")
    print("   3. Solo configuración global (sin datos de navegación)")
    print("   4. Volver al menú principal")
    
    try:
        choice = int(input("\n🔢 Elegí opción: "))
        
        if choice == 1:
            return save_all_profiles()
        elif choice == 2:
            return save_specific_profile()
        elif choice == 3:
            return save_global_config_only()
        elif choice == 4:
            return True
        else:
            print("❌ Opción inválida")
            return False
            
    except ValueError:
        print("❌ Entrada inválida")
        return False

def restore_from_saved():
    """Restaurar desde configuración guardada"""
    saved_configs = list_saved_configurations()
    
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
        
        if not ask_yes_no(f"¿Restaurar configuración guardada '{saved_name}'?"):
            print("❌ Operación cancelada")
            return False
        
        # AVISO IMPORTANTE: Cerrar Brave
        print("\n⚠️ ¡IMPORTANTE!")
        print("🌐 Brave Browser debe estar completamente cerrado antes de restaurar")
        print("💡 Cierra todas las ventanas y pestañas de Brave")
        
        if not ask_yes_no("¿Confirmás que Brave está cerrado para continuar?"):
            print("❌ Operación cancelada - cerrá Brave primero")
            return False
        
        # Hacer backup si se desea
        brave_config = get_brave_config_path()
        if brave_config.exists():
            if ask_yes_no("¿Hacer backup de la configuración actual?"):
                if not create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
        
        # Eliminar configuración actual
        if brave_config.exists():
            shutil.rmtree(brave_config)
        
        # Restaurar desde guardada
        shutil.copytree(selected_saved, brave_config)
        print(f"✅ Configuración '{saved_name}' restaurada!")
        
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al restaurar: {e}")
        return False

def restore_from_repo():
    """Restaurar desde configuración del repositorio"""
    brave_configs = find_brave_configurations()
    
    if not brave_configs:
        print("❌ No hay configuraciones disponibles en este repo")
        input("Presioná Enter para continuar...")
        return False
    
    print("\n📦 CONFIGURACIONES DISPONIBLES EN ESTE REPO:")
    print("=" * 50)
    for i, config_dir in enumerate(brave_configs, 1):
        print(f"  {i}. {config_dir.name}")
    
    print(f"  {len(brave_configs) + 1}. Volver")
    print("=" * 50)
    
    try:
        choice = int(input("\n🔢 Elegí configuración: ")) - 1
        if choice == len(brave_configs):
            return False
        
        if choice < 0 or choice >= len(brave_configs):
            print("❌ Opción inválida")
            return False
        
        selected_config = brave_configs[choice]
        
        if not ask_yes_no(f"¿Restaurar '{selected_config.name}' a tu sistema?"):
            print("❌ Operación cancelada")
            return False
        
        # AVISO IMPORTANTE: Cerrar Brave
        print("\n⚠️ ¡IMPORTANTE!")
        print("🌐 Brave Browser debe estar completamente cerrado antes de restaurar")
        print("💡 Cierra todas las ventanas y pestañas de Brave")
        
        if not ask_yes_no("¿Confirmás que Brave está cerrado para continuar?"):
            print("❌ Operación cancelada - cerrá Brave primero")
            return False
        
        # Hacer backup si se desea
        brave_config = get_brave_config_path()
        if brave_config.exists():
            if ask_yes_no("¿Hacer backup de tu configuración actual?"):
                if not create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
        
        # Eliminar configuración actual
        if brave_config.exists():
            shutil.rmtree(brave_config)
        
        # Restaurar desde configuración seleccionada
        shutil.copytree(selected_config, brave_config)
        print(f"✅ '{selected_config.name}' restaurada en tu sistema!")
        
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al restaurar: {e}")
        return False

def restore_from_backup():
    """Restaurar desde backups"""
    backups = list_available_backups()
    
    if not backups:
        print("❌ No hay backups disponibles")
        input("Presioná Enter para continuar...")
        return False
    
    print("\n📦 BACKUPS DISPONIBLES:")
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
        
        if not ask_yes_no(f"¿Restaurar backup '{backup_name}'?"):
            print("❌ Operación cancelada")
            return False
        
        # AVISO IMPORTANTE: Cerrar Brave
        print("\n⚠️ ¡IMPORTANTE!")
        print("🌐 Brave Browser debe estar completamente cerrado antes de restaurar")
        print("💡 Cierra todas las ventanas y pestañas de Brave")
        
        if not ask_yes_no("¿Confirmás que Brave está cerrado para continuar?"):
            print("❌ Operación cancelada - cerrá Brave primero")
            return False
        
        # Hacer backup si se desea
        brave_config = get_brave_config_path()
        if brave_config.exists():
            if ask_yes_no("¿Hacer backup de la configuración actual?"):
                if not create_backup():
                    print("⚠️ No se pudo crear el backup, continuando...")
        
        # Eliminar configuración actual
        if brave_config.exists():
            shutil.rmtree(brave_config)
        
        # Restaurar desde backup
        shutil.copytree(selected_backup, brave_config)
        print(f"✅ Backup '{backup_name}' restaurado!")
        
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al restaurar backup: {e}")
        return False

def show_restore_menu():
    """Menú para restaurar configuración"""
    obs_path_display = get_brave_config_path_display()
    
    while True:
        print(f"\n📤 Selecciona configuración para restaurar a tu sistema:")
        print(f"📂 Se restaurará en: {obs_path_display}")
        print("   1. Configs guardadas en este repo")
        print("   2. Configs disponibles en este repo")
        print("   3. Backups en este repo")
        print("   4. Volver al menú principal")
        
        try:
            choice = int(input("\n🔢 Seleccioná opción (1-4): "))
            
            if choice == 1:
                return restore_from_saved()
                
            elif choice == 2:
                return restore_from_repo()
                
            elif choice == 3:
                return restore_from_backup()
                
            elif choice == 4:
                return True  # Volver al menú principal
                
            else:
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                
        except ValueError:
            print("❌ Entrada inválida")
            input("Presioná Enter para continuar...")

def replace_with_saved():
    """Reemplazar configuración local con configuración guardada"""
    saved_configs = list_saved_configurations()
    
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
        
        brave_configs = find_brave_configurations()
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
            if not create_backup():
                print("⚠️ No se pudo crear el backup, continuando...")
        
        # Eliminar carpeta de configuración
        if target_config.exists():
            shutil.rmtree(target_config)
        
        # Copiar configuración guardada
        shutil.copytree(selected_saved, target_config)
        print(f"✅ Configuración guardada importada como '{target_config.name}'!")
        
        return True
        
    except ValueError:
        print("❌ Entrada inválida")
        return False
    except Exception as e:
        print(f"❌ Error al reemplazar: {e}")
        return False

def replace_with_backup():
    """Reemplazar configuración local con backup"""
    backups = list_available_backups()
    
    if not backups:
        print("❌ No hay backups disponibles")
        input("Presioná Enter para continuar...")
        return False
    
    print("\n📦 BACKUPS DISPONIBLES:")
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
        
        brave_configs = find_brave_configurations()
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
            if not create_backup():
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

def show_replace_menu():
    """Menú para reemplazar configuración local"""
    while True:
        print("\n🔄 Reemplazando configuración de este repo...")
        print("   1. Reemplazar con config guardada")
        print("   2. Reemplazar con backup")
        print("   3. Volver al menú principal")
        
        try:
            choice = int(input("\n🔢 Seleccioná opción (1-3): "))
            
            if choice == 1:
                return replace_with_saved()
                
            elif choice == 2:
                return replace_with_backup()
                
            elif choice == 3:
                return True  # Volver al menú principal
                
            else:
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                
        except ValueError:
            print("❌ Entrada inválida")
            input("Presioná Enter para continuar...")

def show_main_menu():
    """Muestra el menú principal con estado"""
    os_system = detect_os()
    status = get_status_info()
    brave_path = status['brave_path_display']
    
    print(f"\n🦁 BRAVE BROWSER CONFIGURATION MANAGER - {os_system}")
    print("=" * 60)
    print(f"📂 Directorio de perfiles: {brave_path}")
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

def interactive_mode():
    """Modo interactivo con menús"""
    while True:
        show_main_menu()
        
        try:
            main_choice = input("\n🔢 Seleccioná una opción: ").strip()
            
            if main_choice == "1":
                # Guardar configuración actual
                success = save_current_configuration()
                if success:
                    input("\n✅ ¡Listo! Presioná Enter para continuar...")
                else:
                    input("\n❌ Error. Presioná Enter para continuar...")
                    
            elif main_choice == "2":
                # Restaurar configuración
                success = show_restore_menu()
                if success:
                    input("\n✅ Operación completada. Presioná Enter para continuar...")
                else:
                    input("\n❌ Error. Presioná Enter para continuar...")
                    
            elif main_choice == "3":
                # Reemplazar configuración local
                success = show_replace_menu()
                if success:
                    input("\n✅ Operación completada. Presioná Enter para continuar...")
                else:
                    input("\n❌ Error. Presioná Enter para continuar...")
                    
            elif main_choice == "4":
                if ask_yes_no("¿Querés salir?"):
                    print("👋 ¡Hasta luego!")
                    break
                
            else:
                print("❌ Opción inválida")
                input("Presioná Enter para continuar...")
                
        except (KeyboardInterrupt, EOFError):
            if ask_yes_no("\n¿Querés salir?"):
                print("\n👋 ¡Hasta luego!")
                break

def main():
    parser = argparse.ArgumentParser(description="Gestionar configuración de Brave Browser")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interactivo")
    
    args = parser.parse_args()
    
    # Modo interactivo por defecto
    interactive_mode()

if __name__ == "__main__":
    main()