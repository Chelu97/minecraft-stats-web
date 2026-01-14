#!/bin/bash
# Levanta servidor local para desarrollo

SCRIPT_DIR="$(dirname "$0")"
SRC_DIR="$SCRIPT_DIR/../src"
DATA_DIR="$SCRIPT_DIR/../data"

# Copia stats.json a src/ para que el HTML lo encuentre
if [ -f "$DATA_DIR/stats.json" ]; then
    cp "$DATA_DIR/stats.json" "$SRC_DIR/stats.json"
    echo "Stats copiados a src/"
else
    echo "AVISO: No hay stats.json en data/. Ejecuta sync-data.sh primero."
fi

echo ""
echo "Servidor local iniciado en: http://localhost:8000"
echo "Presiona Ctrl+C para detener"
echo ""

cd "$SRC_DIR" && python3 -m http.server 8000
