# 🦁 Brave Browser Configuration Manager v2.0.0

Sistema modular y escalable para gestionar configuraciones de Brave Browser con máxima privacidad y portabilidad.

## 📋 Descripción

Esta herramienta modular te permite gestionar las configuraciones de Brave Browser de forma segura y precisa:
- **Arquitectura limpia**: Sistema modular con separación de responsabilidades
- **JSONs compactos**: Extrae solo configuración esencial (como `BraveDayvis.json`)
- **Restauración selectiva**: Aplica configuración a perfiles específicos o globalmente
- **Cero datos personales**: Solo settings, themes, atajos y extensiones
- **Multiplataforma**: Linux, Windows y macOS

## 🚀 Características Principales

### 🏗️ **Arquitectura Modular v2.0.0**
- **Core separado**: Lógica de negocio independiente
- **UI desacoplada**: Menús reutilizables
- **Storage abstracto**: Gestión de archivos flexible
- **Models tipados**: Clases de datos robustas
- **Utils reutilizables**: Helper functions compartidas

### 🎯 **Funcionalidades Avanzadas**
- **🔒 Máxima privacidad**: Solo configuración pura, sin datos personales
- **📄 JSONs compactos**: Formato limpio y portátil
- **👤 Restauración selectiva**: Aplica a perfil específico o global
- **💾 Backups inteligentes**: Excluye archivos temporales
- **🔄 CLI limpio**: Interfaz con limpieza automática
- **📊 Estado en tiempo real**: Información actualizada del sistema

## 📁 Estructura Modular

```
brave-config-manager/
├── 🦁 main.py                    # Orquestador principal (150 líneas)
├── 📁 core/                      # Lógica de negocio
│   ├── 🧠 extraction_engine.py   # Motor de extracción JSON
│   └── 👤 profile_handler.py     # Manejo de perfiles
├── 📁 ui/                        # Interfaz usuario
│   └── 📋 menus.py               # Todos los menús interactivos
├── 📁 storage/                   # Almacenamiento
│   └── 💾 backup_manager.py      # Gestión de backups
├── 📁 utils/                     # Utilidades
│   └── ⚙️ system_utils.py        # OS y helpers
├── 📁 models/                    # Datos
│   └── 📊 profile.py             # Clases Profile, Configuration
├── 📁 backup/                    # Backups automáticos
├── 📁 saved_configs/             # Configuraciones guardadas
└── 📁 Linux/                     # Datos de configuración (opcional)
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.7+
- Brave Browser instalado

### Instalación Rápida
```bash
# Clonar el repositorio
git clone <repository-url>
cd brave-config-manager

# Ejecutar sistema modular
python3 main.py --interactive
```

### Archivos Necesarios (14 archivos)
```
main.py                    # Punto de entrada
core/                      # Lógica principal
ui/menus.py               # Menús interactivos
utils/system_utils.py     # Utilidades del sistema
models/profile.py          # Clases de datos
storage/backup_manager.py # Gestión de backups
*/__init__.py             # Python packages (5 archivos)
```

**Nota**: `Linux/` y `__pycache__/` son opcionales para el funcionamiento.

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

#### 2. 📤 Restaurar Configuración (NUEVO)
- **🆕 Restauración selectiva**: Elige a qué perfil aplicar la configuración
- **Restauración global**: Reemplaza toda la configuración (comportamiento anterior)
- **Desde backup**: Restaura desde backups automáticos

**Flujo de restauración mejorado:**
```
📤 RESTAURAR CONFIGURACIÓN
📦 CONFIGURACIONES GUARDADAS:
   1. Dayvis
   2. Volver

👤 ¿A dónde querés aplicar la configuración 'Dayvis'?
   1. Al perfil: Personal (Default)
   2. Al perfil: Trabajo (Profile 1)
   3. Al perfil: Gaming (Profile 2)
   4. A toda la configuración (reemplazar todo)
```

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
6. **🆕 Modularidad**: Cada módulo se puede testear y mantener independientemente
7. **🆕 Selectividad**: Aplica configuración solo donde la necesitas

## 📄 Cambios (Changelog)

### v2.0.0 - **Arquitectura Modular Escalable**
- **🏗️ Refactorización completa**: Sistema monolítico → arquitectura modular
- **📦 14 archivos modulares**: Core, UI, Storage, Utils, Models separados
- **🎯 Restauración selectiva**: Aplica configuración a perfil específico
- **🧠 Motor de extracción**: `ExtractionEngine` para JSONs compactos
- **📋 Menús desacoplados**: `MenuManager` con UI limpia
- **⚡ CLI mejorado**: Limpieza automática entre operaciones
- **🔧 Tipado fuerte**: Clases `Profile` y `Configuration`
- **📊 Mantenibilidad 10x**: 1,126 líneas → 150 líneas en main

### v1.1.0 - **Configuración Pura**
- **🎯 JSONs compactos**: Todas las opciones ahora guardan configuración pura en formato JSON
- **⚡ Extracción inteligente**: Nueva función `extract_settings_only()` extrae solo datos esenciales
- **📁 Formato unificado**: Todos los perfiles guardados como JSONs limpios (tipo `BraveDayvis.json`)
- **🔒 Máxima privacidad**: Cero datos personales, solo configuración portátil
- **🔄 Opción 4 renovada**: "Solo settings clave" extrae brave_settings y keyboard_shortcuts

### v1.0.0
- Gestión completa de perfiles de Brave
- Detección automática de configuraciones
- Backups inteligentes con exclusión de archivos bloqueados
- Soporte multiplataforma
- Menú interactivo intuitivo
- Documentación completa

---

**🦁 Brave Config Manager v2.0.0 - Modular Edition**  
*Arquitectura escalable para gestión profesional de configuraciones*