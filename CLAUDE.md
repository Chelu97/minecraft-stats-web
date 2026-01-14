# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Development
./scripts/sync-data.sh      # Download fresh stats.json from server
./scripts/serve-local.sh    # Start local server at http://localhost:8000 (run in background)
./scripts/deploy.sh         # Deploy to production (auto-backup before deploy)
./scripts/rollback.sh       # Revert to previous version if deploy fails
```

**Important**: When running `serve-local.sh`, launch it in background (`run_in_background: true`) so you don't block waiting for user verification.

## Architecture

### Data Flow
```
Minecraft Server (world/stats/*.json)
        ↓
generate_stats.py (runs every 5 min via cron on server)
        ↓
stats.json (served at /var/www/html/)
        ↓
index.html (fetches and displays data)
```

### Key Files

- **src/index.html**: Single-page dashboard with vanilla HTML/CSS/JS. Contains player ranking table, player profile modal with 5 tabs (General, Combate, Viajes, Minería, Muertes), and server records section.

- **src/generate_stats.py**: Python script that runs on the server. Reads Minecraft's native stats JSON files, connects via RCON to get online players, and outputs aggregated stats.json.

### Server Details
- **Production URL**: http://79.72.62.61/
- **SSH alias**: `chelu-vps`
- **Web root**: `/var/www/html/`
- **Script location on server**: `/home/ubuntu/minecraft-server/generate_stats.py`

### Style Theme
Gaming aesthetic with neon green (#00ff88) accents on dark background (#0d0d0d to #1a1a2e gradient). Custom scrollbar styling included.
