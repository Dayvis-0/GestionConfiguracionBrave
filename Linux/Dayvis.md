# 📖 Configuración de Dayvis - Brave Browser

Documentación específica de la configuración personal de Brave Browser para Dayvis.

## 🌟 Overview

Esta configuración está optimizada para el uso diario y profesional de Brave Browser, incluyendo extensiones esenciales, bookmarks organizados y preferencias de privacidad personalizadas.

## 📁 Archivos de Configuración

### 📄 BraveDayvis.json

Archivo JSON con la configuración completa y personalizada de Brave Browser.

**⚠️ DATOS IMPORTANTES:**

#### ✅ **Qué contiene este archivo:**

- **Configuración principal de Brave**: tema, shields, privacidad, sincronización
- **Atajos de teclado personalizados**: navegación, pestañas, búsqueda, DevTools
- **Lista de extensiones instaladas**: Vimium, PDF Viewer, Tienda Brave
- **Preferencias de privacidad**: todo configurado para borrado automático al salir
- **Configuración de descargas**: directorio `/home/dayvis/Descargas/Dayvis`
- **Idioma y configuración regional**: español (es-419, es)

#### ❌ **Qué NO contiene (y por qué es seguro):**

- **Contraseñas**: configuradas para borrarse al salir (`"passwords_on_exit": true`)
- **Historial de navegación**: se elimina automáticamente (`"browsing_history_on_exit": true`)
- **Cookies**: desactivadas para persistencia (`"cookies": false`)
- **Datos de formularios**: se limpian al cerrar (`"form_data_on_exit": true`)
- **Historial de descargas**: se borra automáticamente (`"download_history_on_exit": true`)
- **Configuraciones específicas de extensiones**: como tus atajos personalizados de Vimium

#### ⌨️ **ATAJOS DE TECLADO PERSONALIZADOS (CONFIGURADOS POR VOS):**

**🔥 Navegación y Pestañas:**

```json
"Control+KeyN", "Alt+KeyN"           // Nueva ventana
"Control+Shift+KeyN"                  // Nueva ventana incógnito
"Control+KeyT", "Alt+KeyT"           // Nueva pestaña
"Control+KeyW", "Alt+KeyX"           // Cerrar pestaña actual
"Control+Tab", "Alt+KeyS"            // Siguiente pestaña
"Control+Shift+Tab", "Alt+KeyA"      // Anterior pestaña
"Alt+Digit1" al "Alt+Digit9"         // Ir a pestaña 1-9
"Alt+KeyD"                           // Foco en barra de direcciones
```

**🌍 Navegación Web:**

```json
"Alt+ArrowLeft", "Alt+KeyQ"           // Atrás
"Alt+ArrowRight", "Alt+KeyW"          // Adelante
"F5", "Alt+KeyR"                     // Recargar página
"Control+F5", "Shift+F5"             // Recargar forzado
"Alt+KeyL"                           // Foco en contenido principal
"Alt+KeyU"                           // Ver código fuente
```

**🛠️ Herramientas de Desarrollo (DEVTOOLS):**

```json
"Control+Shift+KeyI", "Alt+Shift+KeyD"  // DevTools completa
"Control+Shift+KeyC"                     // Inspeccionar elemento
"Control+Shift+KeyM"                     // Modo responsive design
"F12"                                    // Abrir/cerrar DevTools
"Shift+Escape"                           // Abrir task manager
```

**🔍 Zoom y Visualización:**

```json
"Control+Equal", "Control+Shift+Equal"   // Zoom in (agrandar)
"Control+Digit0", "Control+Numpad0"      // Zoom reset (100%)
"Control+Minus", "Control+Shift+Minus"   // Zoom out (achicar)
"F11", "Alt+KeyC"                        // Pantalla completa
```

**🎯 Búsqueda y Utilidades:**

```json
"Control+KeyF", "Alt+KeyB"               // Buscar en página
"Control+KeyG", "F3"                     // Siguiente resultado búsqueda
"Control+Shift+KeyG", "Shift+F3"         // Anterior resultado búsqueda
"Escape"                                  // Salir de búsqueda
"Control+KeyE", "Control+KeyK"           // Foco en barra de búsqueda
```

**📁 Gestión de Archivos y Ventanas:**

```json
"Control+KeyO"                          // Abrir archivo local
"Control+Shift+KeyS"                    // Guardar página como
"Control+KeyH", "Alt+Shift+KeyH"         // Historial
"Control+Shift+Delete"                  // Limpiar datos navegación
"Control+Shift+KeyW", "Alt+F4", "Alt+Shift+KeyW"  // Cerrar ventana
```

**⚡ Favoritos y Accesos Rápidos:**

```json
"Alt+KeyM"                              // Agregar marcador
"Alt+Shift+KeyM"                        // Administrador marcadores
"Alt+Shift+KeyB"                        // Barra de marcadores
"Control+Shift+KeyB"                    // Alternar barra de favoritos
```

**📋 Portapapeles y Compartir:**

```json
"Alt+Shift+KeyP"                        // Imprimir página
"Alt+KeyY"                              // Ver código fuente elemento
"Alt+KeyJ"                              // Descargas
"Alt+Shift+KeyS"                        // Compartir página
```

---

## 🔧 Características Principales

### 🛡️ Privacidad y Seguridad

- **Shields de Brave**: Configuración optimizada
- **Bloqueo de rastreadores**: Nivel estándar
- **Modo privado**: Configuración personalizada
- **VPN/Tor**: Integrado según necesidades

### 🧩 Extensiones Instaladas (detectadas en BraveDayvis.json)

- **Vimium v2.3.1**: Navegación por teclado estilo Vim
- **Tienda virtual de Brave**: Webstore oficial de Brave
- **Chrome PDF Viewer**: Visor de PDF integrado
- **Brave Extension**: Extension nativa de Brave (v1.0.0)

### 🔖 Marcadores Organizados

```
📁 Desarrollo
├── 📁 Documentación
├── 📁 GitHub
├── 📁 Stack Overflow
└── 📁 Tutoriales

📁 Trabajo
├── 📁 Proyectos
├── 📁 Herramientas
└── 📁 Recursos

📁 Personal
├── 📁 Redes Sociales
├── 📁 Noticias
└── 📁 Entretenimiento
```

### ⚙️ Preferencias de Navegación

#### 🎨 Interfaz

- **Tema**: Modo oscuro/brave-theme
- **Fuente**: Default Sans-serif
- **Tamaño de fuente**: 16px
- **Página de inicio**: Brave New Tab

#### 🔍 Búsqueda

- **Motor de búsqueda**: Brave Search (privado)
- **Sugerencias**: Activadas
- **Historial de búsqueda**: Desactivado en modo privado

#### 📥 Descargas

- **Directorio**: `/home/dayvis/Descargas/Dayvis` (confirmado en JSON)
- **Preguntar siempre**: Desactivado (`"prompt_for_download": false`)
- **Abrir archivos PDF**: En navegador (via Chrome PDF Viewer)

### 🌐 Configuraciones Web

#### 🍪 Cookies

- **Cookies de terceros**: Bloqueadas
- **Cookies persistentes**: Solo sitios permitidos
- **Cookies de sesión**: Permitidas

#### 🔔 Notificaciones

- **Notificaciones de escritorio**: Solo sitios permitidos
- **Sonido de notificaciones**: Activado
- **Silenciar sitios no permitidos**: Sí

## 🔄 Restauración de esta Configuración

### Usando el Script Principal

1. Ejecutar `./brave_config_manager.py`
2. Seleccionar opción `2. 📤 Restaurar config a tu sistema`
3. Elegir `2. Configs disponibles en este repo`
4. Seleccionar `Dayvis`
5. Seguir instrucciones (cerrar Brave primero)

### Restauración Manual

```bash
# Cerrar completamente Brave
pkill brave

# Copiar configuración
cp -r Linux/Dayvis/* ~/.config/BraveSoftware/Brave-Browser/

# Ajustar permisos
chmod -R 755 ~/.config/BraveSoftware/Brave-Browser/
```

## 📊 Estadísticas de Uso

### 📈 Tamaño de Configuración

- **Perfil Principal**: ~200 MB
- **Extensiones**: ~50 MB
- **Marcadores**: ~5 MB
- **Historial**: ~100 MB
- **Total**: ~355 MB

### 🧹 Archivos Excluidos en Backups

- `SingletonLock`, `SingletonSocket`, `SingletonCookie`
- Archivos temporales `*.tmp`, `*.lock`
- Caché del navegador

## 🛠️ Personalización Adicional

### 🎨 Temas Personalizados

- **Brave Theme**: Predeterminado
- **Dark Reader**: Para sitios sin modo oscuro
- **Custom CSS**: Pequeñas personalizaciones

### 🔧 Development Tools

- **Console**: Siempre abierta al desarrollar
- **Network**: Monitor de red activado
- **Performance**: Métricas de rendimiento
- **Application**: Almacenamiento local visible

## 📱 Sincronización (Opcional)

Si deseas sincronizar esta configuración entre dispositivos:

1. Crear cuenta Brave Sync
2. Exportar esta configuración como base
3. Sincronizar extensiones y marcadores manualmente
4. Mantener las preferencias de privacidad personales

## 🚨 Notas de Seguridad

### 🔐 Datos Sensibles

- **Contraseñas**: Usar LastPass (no guardar en navegador)
- **Tarjetas de crédito**: Desactivar autocompletar
- **Formularios**: Limpiar datos sensibles regularmente

### 🧹 Limpieza Regular

```bash
# Limpiar caché y datos temporales
rm -rf ~/.config/BraveSoftware/Brave-Browser/Default/Cache/
rm -rf ~/.config/BraveSoftware/Brave-Browser/Default/Code\ Cache/
```

## 🔄 Actualizaciones

### 📦 Actualizar Configuración

1. Hacer backup de configuración actual
2. Actualizar archivos en `Linux/Dayvis/`
3. Aplicar cambios usando el script
4. Verificar funcionalidad

### 🐛 Solución de Problemas

- **Brave no inicia**: Verificar permisos y archivos corruptos
- **Configuración perdida**: Restaurar desde backup
- **Extensiones no funcionan**: Reinstalar desde Brave Store

## 📞 Soporte

Si tienes problemas con esta configuración:

1. Revisa el [README.md](../README.md) principal
2. Verifica que Brave esté completamente cerrado antes de restaurar
3. Asegúrate de tener espacio suficiente en disco
4. Crea un nuevo backup antes de hacer cambios

---

**👤 Creado por**: Dayvis Atao Mallqui  
**📅 Última actualización**: 03/01/2026  
**🦁 Compatible con**: Brave Browser 1.60+
