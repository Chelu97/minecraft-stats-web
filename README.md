# Minecraft Stats Web Dashboard

Dashboard web para visualizar estadísticas de jugadores del servidor de Minecraft.

## Estructura

```
├── src/
│   ├── index.html          # Dashboard principal
│   └── generate_stats.py   # Script que genera stats.json
├── data/
│   └── stats.json          # Datos de prueba (descargados del servidor)
├── scripts/
│   ├── deploy.sh           # Desplegar cambios al servidor
│   ├── sync-data.sh        # Descargar stats.json actualizado
│   ├── serve-local.sh      # Servidor local para desarrollo
│   └── rollback.sh         # Restaurar versión anterior
└── config/
    └── (configuraciones de referencia)
```

## Uso

### Desarrollo local

```bash
# 1. Descargar datos actualizados del servidor
./scripts/sync-data.sh

# 2. Iniciar servidor local
./scripts/serve-local.sh

# 3. Abrir en navegador: http://localhost:8000
```

### Desplegar cambios

```bash
# Sube los cambios al servidor (hace backup automático)
./scripts/deploy.sh
```

### Rollback

```bash
# Si algo sale mal, restaura la versión anterior
./scripts/rollback.sh
```

## Servidor

- **URL**: http://79.72.62.61/
- **SSH**: `ssh chelu-vps`
- **Stats se regeneran**: cada 5 minutos via cron

## Archivos en el servidor

- `/var/www/html/index.html` - Dashboard
- `/var/www/html/stats.json` - Datos (generado automáticamente)
- `/home/ubuntu/minecraft-server/generate_stats.py` - Script generador
