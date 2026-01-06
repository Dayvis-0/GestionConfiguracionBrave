# 🦁 Brave Browser Configuration Manager

Gestiona, respalda y restaura configuraciones de Brave Browser de forma sencilla y multiplataforma.

## 📋 Descripción

Esta herramienta te permite gestionar las configuraciones de Brave Browser de forma segura, incluyendo:
- Múltiples perfiles de usuario (solo configuración)
- Configuraciones globales y locales (sin datos personales)
- Backups automáticos y manuales (solo preferencias)
- Gestión segura sin comprometer tu privacidad

## 🚀 Características

- 🌐 **Multiplataforma**: Linux, Windows y macOS
- 👥 **Gestión de perfiles**: Detección automática de múltiples perfiles
- 🔒 **Máxima privacidad**: Solo guarda configuración pura, cero datos personales
- 📄 **JSONs compactos**: Extrae solo settings esenciales como `BraveDayvis.json`
- 💾 **Backups inteligentes**: Excluye archivos temporales y datos sensibles
- 📁 **Múltiples destinos**: Guarda en diferentes carpetas según necesites
- 🔄 **Restauración segura**: Verifica cierre de Brave antes de restaurar
- 📊 **Estado en tiempo real**: Información actualizada del sistema

## 📁 Estructura del Proyecto

```
BraveConfigManager/
├── 🦁 brave_config_manager.py    # Script principal
├── 📁 backup/                     # Backups automáticos
├── 📁 saved_configs/              # Configuraciones guardadas manualmente
├── 📁 Linux/                      # Configuraciones para Linux
│   └── 📁 Dayvis/                 # Configuración de Dayvis
│       └── 📄 BraveDayvis.json    # Configuración específica
├── 📁 Windows/                    # Configuraciones para Windows (si aplica)
├── 📄 README.md                   # Esta documentación
├── 📄 LICENSE                     # Licencia del proyecto
└── 📁 Linux/                      # Documentación por configuración
    └── 📄 Dayvis.md                # Documentación específica de Dayvis
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.6+
- Brave Browser instalado

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd BraveConfigManager

# Hacer ejecutable el script
chmod +x brave_config_manager.py

# Ejecutar
python3 brave_config_manager.py
# o
./brave_config_manager.py
```

## 🎯 Uso

### Menú Principal
```
🦁 BRAVE BROWSER CONFIGURATION MANAGER - 🐧 Linux
============================================================
📂 Directorio de perfiles: ~/.config/BraveSoftware/Brave-Browser
👥 Perfiles detectados: 4
📄 Configuraciones disponibles: 1
💾 Backups en este repo: 2
📁 Configs guardadas en este repo: ✅
🔧 Configuración en tu sistema: ✅
------------------------------------------------------------
  1. 📥 Guardar config de tu sistema
  2. 📤 Restaurar config a tu sistema
  3. 🔄 Reemplazar config de este repo
  4. 🚪 Salir
------------------------------------------------------------
```

### Opciones Disponibles

#### 1. 📥 Guardar Configuración
- **Todos los perfiles**: Guarda configuración pura de todos los perfiles (JSONs limpios)
- **Perfil específico**: Guarda configuración pura del perfil seleccionado (JSON limpio)
- **Solo configuración global**: Guarda solo preferencias globales sin datos de navegación
- **🎯 Solo settings clave**: Extrae configuración esencial (brave_settings, keyboard_shortcuts) como JSON compacto

#### 2. 📤 Restaurar Configuración
- **Configs guardadas**: Restaurar desde configuraciones guardadas
- **Configs del repo**: Restaurar desde configuraciones en Linux/
- **Backups**: Restaurar desde backups automáticos

#### 3. 🔄 Reemplazar Configuración del Repo
- **Con config guardada**: Importar configuración guardada al repo
- **Con backup**: Importar backup al repo

## 🔧 Configuración

### Rutas por Sistema Operativo
- **Linux**: `~/.config/BraveSoftware/Brave-Browser/`
- **Windows**: `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data`
- **macOS**: `~/Library/Application Support/BraveSoftware/Brave-Browser/User Data`

### Archivos Incluidos en Configuraciones

✅ **Incluidos (Solo configuración pura)**:
- **brave_settings**: Temas, privacidad, shields, descargas, idioma
- **keyboard_shortcuts**: Atajos de teclado personalizados
- **Extensions**: Lista y configuración de extensiones instaladas
- **Global preferences**: Configuración global del navegador

❌ **Excluidos (Todos los datos personales)**:
- Historial de navegación, cookies, contraseñas
- Marcadores, descargas, sesiones
- Caché, archivos temporales, datos de sitios
- Datos de extensiones, wallets, bases de datos locales

✅ **Formato de salida**:
- Archivos JSON limpios y compactos
- Similares a `BraveDayvis.json` (ejemplo incluido)
- Seguros para compartir y versionar

❌ **Excluidos automáticamente**:
- Archivos temporales (*.tmp, *.lock)
- Archivos de bloqueo (SingletonLock, SingletonSocket, SingletonCookie)
- Archivos del sistema

## 🚨 Notas Importantes

### Seguridad y Privacidad
- **Configuraciones**: Solo guardan preferencias del navegador, sin datos personales
- **Privacidad**: No se incluye historial, contraseñas, cookies ni marcadores
- **Restauración**: REQUIERE Brave completamente cerrado
- **Confirmación**: Siempre confirma operaciones destructivas

### Mejores Prácticas
1. **Hacer backup** antes de cualquier restauración
2. **Cerrar Brave** completamente antes de restaurar
3. **Privacidad primero**: Todos los JSONs generados son seguros para compartir
4. **Version control**: Los JSONs compactos son perfectos para Git
5. **Configuración portátil**: Lleva tus settings entre dispositivos fácilmente

## 📄 Cambios (Changelog)

### v2.0.0 - **Configuración Pura**
- **🎯 JSONs compactos**: Todas las opciones ahora guardan configuración pura en formato JSON
- **⚡ Extracción inteligente**: Nueva función `extract_settings_only()` extrae solo datos esenciales
- **📁 Formato unificado**: Todos los perfiles guardados como JSONs limpios (tipo `BraveDayvis.json`)
- **🔒 Máxima privacidad**: Cero datos personales, solo configuración portátil
- **🔄 Opción 4 renovada**: "Solo settings clave" extrae brave_settings y keyboard_shortcuts

### v1.1.0
- **🔒 Mejora de privacidad**: Ahora solo guarda configuraciones sin datos personales
- **👥 Perfiles limpios**: Opción 1 y 2 ahora excluyen historial, contraseñas y cookies
- **📁 Nomenclatura clara**: Nombres de archivos indican "config" vs "saved"
- **🛡️ Seguridad reforzada**: Todas las opciones de guardado son seguras para compartir

### v1.0.0
- Gestión completa de perfiles de Brave
- Detección automática de configuraciones
- Backups inteligentes con exclusión de archivos bloqueados
- Soporte multiplataforma
- Menú interactivo intuitivo
- Documentación completa

---

**🦁 Hecho con ❤️ para usuarios de Brave Browser**