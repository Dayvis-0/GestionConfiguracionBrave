#!/usr/bin/env python3
"""
Brave Configuration Manager - CLI Modular
Sistema escalable para gestionar configuraciones de Brave Browser
"""

import argparse
from pathlib import Path

# Importaciones modulares
from core.profile_handler import ProfileHandler
from ui.menus import MenuManager
from utils.system_utils import SystemUtils


class BraveConfigManager:
    """Orquestador principal del sistema"""
    
    def __init__(self):
        self.profile_handler = ProfileHandler()
        self.menu_manager = MenuManager()
        self.system_utils = SystemUtils()
    
    def run_interactive(self):
        """Ejecuta el modo interactivo"""
        while True:
            # Obtener estado actual
            status = self.system_utils.get_status_info()
            
            # Mostrar menú principal
            self.menu_manager.show_main_menu(status)
            
            try:
                main_choice = input("\n🔢 Seleccioná una opción: ").strip()
                
                if main_choice == "1":
                    # Guardar configuración actual
                    profiles = ProfileHandler.detect_profiles(ProfileHandler.get_brave_config_path())
                    success = self.menu_manager.show_save_menu(profiles)
                    self._handle_operation_result(success, "guardar configuración")
                    
                elif main_choice == "2":
                    # Restaurar configuración
                    success = self.menu_manager.show_restore_menu()
                    self._handle_operation_result(success, "restaurar configuración")
                    
                elif main_choice == "3":
                    # Reemplazar configuración local
                    success = self.menu_manager.show_replace_menu()
                    self._handle_operation_result(success, "reemplazar configuración")
                    
                elif main_choice == "4":
                    if SystemUtils.ask_yes_no("¿Querés salir?"):
                        print("👋 ¡Hasta luego!")
                        break
                    
                else:
                    print("❌ Opción inválida")
                    input("Presioná Enter para continuar...")
                    
            except (KeyboardInterrupt, EOFError):
                if SystemUtils.ask_yes_no("\n¿Querés salir?"):
                    print("\n👋 ¡Hasta luego!")
                    break
    
    def _handle_operation_result(self, success: bool, operation: str):
        """Maneja el resultado de una operación"""
        if success:
            input(f"\n✅ {operation} completada. Presioná Enter para continuar...")
        else:
            input(f"\n❌ Error en {operation}. Presioná Enter para continuar...")
        
        # Limpiar pantalla para siguiente operación
        self.system_utils.clear_screen()
    
    def show_help(self):
        """Muestra ayuda del sistema"""
        print("""
🦁 Brave Configuration Manager - Ayuda

🎯 Comandos disponibles:
  --interactive, -i    Modo interactivo (default)
  --help, -h          Muestra esta ayuda

📁 Estructura modular:
  core/                Lógica de negocio principal
  ui/                  Menús e interfaz
  storage/             Gestión de archivos y backups
  utils/               Utilidades del sistema
  models/              Clases de datos

🔧 Características:
  • Extracción pura de configuración (JSON limpios)
  • Gestión múltiple de perfiles
  • Backups automáticos y manuales
  • Multiplataforma (Linux, Windows, macOS)
  • Privacidad garantizada (solo configuración, sin datos)

💡 Uso recomendado:
  python3 main.py --interactive

        """)


def main():
    """Punto de entrada principal"""
    parser = argparse.ArgumentParser(
        description="Gestionar configuración de Brave Browser",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--interactive", "-i", 
        action="store_true", 
        help="Modo interactivo (default)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="🦁 Brave Config Manager v2.0.0 - Modular Edition"
    )
    
    args = parser.parse_args()
    
    # Crear instancia del gestor
    manager = BraveConfigManager()
    
    # Ejecutar modo interactivo por defecto
    manager.run_interactive()


if __name__ == "__main__":
    main()