#!/bin/bash
set -e

echo "=== Desplegando web de Minecraft ==="

# Backup remoto antes de desplegar
echo "1. Creando backup en servidor..."
ssh chelu-vps 'cp /var/www/html/index.html /var/www/html/index.html.pre-deploy'
ssh chelu-vps 'cp /home/ubuntu/minecraft-server/generate_stats.py /home/ubuntu/minecraft-server/generate_stats.py.pre-deploy'

# Subir archivos
echo "2. Subiendo index.html..."
scp "$(dirname "$0")/../src/index.html" chelu-vps:/var/www/html/index.html

echo "3. Subiendo generate_stats.py..."
scp "$(dirname "$0")/../src/generate_stats.py" chelu-vps:/home/ubuntu/minecraft-server/generate_stats.py

# Regenerar stats con nuevo script
echo "4. Regenerando estadísticas..."
ssh chelu-vps 'cd /home/ubuntu/minecraft-server && python3 generate_stats.py'

echo "=== Despliegue completado ==="
echo "Verificar en: http://79.72.62.61/"
