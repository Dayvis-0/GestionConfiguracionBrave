    @staticmethod
    def _restore_global_config(selected_saved: Path, saved_name: str) -> bool:
        """Restaura configuración global (comportamiento anterior)"""
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
    
    @staticmethod
    def _restore_to_specific_profile(selected_saved: Path, saved_name: str, target_profile) -> bool:
        """Restaura configuración a un perfil específico"""
        # Hacer backup antes de restaurar
        if ask_yes_no("¿Querés hacer backup antes de restaurar el perfil?"):
            if not BackupManager.create_backup():
                print("⚠️ No se pudo crear el backup, continuando...")
        
        print(f"\n📤 Restaurando configuración '{saved_name}' al perfil específico...")
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
            with open(config_json, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Convertir a objeto Configuration
            from models.profile import Configuration
            config = Configuration.from_dict(config_data)
            
            # Guardar en el perfil destino
            prefs_file = target_profile.path / "Preferences"
            success = ExtractionEngine.save_configuration(config, prefs_file)
            
            if success:
                print(f"✅ Configuración restaurada al perfil '{target_profile.display_name}'!")
                print("🔄 Podés abrir Brave Browser ahora")
                return True
            else:
                print(f"❌ Error al guardar configuración en el perfil")
                return False
                
        except Exception as e:
            print(f"❌ Error al restaurar al perfil específico: {e}")
            return False