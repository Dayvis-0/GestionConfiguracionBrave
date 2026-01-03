# 📖 Configuración de Dayvis - Brave Browser

Documentación específica de la configuración personal de Brave Browser para Dayvis.

## 🌟 Overview

Esta configuración está optimizada para el uso diario y profesional de Brave Browser, incluyendo extensiones esenciales, bookmarks organizados y preferencias de privacidad personalizadas.

## 📁 Archivos de Configuración

### 📄 BraveDayvis.json
```json
{
  "name": "Dayvis Configuration",
  "version": "1.0.0",
  "description": "Configuración personal de Brave para Dayvis Atao Mallqui",
  "created": "2025-01-02",
  "last_updated": "2025-01-03"
}
```

## 🔧 Características Principales

### 🛡️ Privacidad y Seguridad
- **Shields de Brave**: Configuración optimizada
- **Bloqueo de rastreadores**: Nivel estándar
- **Modo privado**: Configuración personalizada
- **VPN/Tor**: Integrado según necesidades

### 🧩 Extensiones Instaladas
- **uBlock Origin**: Bloqueador de anuncios
- **LastPass**: Gestor de contraseñas
- **Grammarly**: Corrección ortográfica
- **HTTPS Everywhere**: Conexión segura
- **React Developer Tools**: Desarrollo web
- **Vue.js devtools**: Desarrollo frontend

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
- **Directorio**: ~/Descargas/Brave
- **Preguntar siempre**: Activado
- **Abrir archivos PDF**: En navegador

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