#!/bin/bash
# Restaura la versión anterior del deploy

echo "=== Restaurando versión anterior ==="

echo "1. Restaurando index.html..."
ssh chelu-vps 'cp /var/www/html/index.html.pre-deploy /var/www/html/index.html'

echo "2. Restaurando generate_stats.py..."
ssh chelu-vps 'cp /home/ubuntu/minecraft-server/generate_stats.py.pre-deploy /home/ubuntu/minecraft-server/generate_stats.py'

echo "3. Regenerando estadísticas..."
ssh chelu-vps 'cd /home/ubuntu/minecraft-server && python3 generate_stats.py'

echo "=== Rollback completado ==="
