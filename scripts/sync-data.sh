#!/bin/bash
# Descarga stats.json actualizado del servidor

SCRIPT_DIR="$(dirname "$0")"
scp chelu-vps:/var/www/html/stats.json "$SCRIPT_DIR/../data/stats.json"
echo "Stats actualizados: $(date)"
echo "Archivo: $SCRIPT_DIR/../data/stats.json"
