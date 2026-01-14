#!/usr/bin/env python3
import json
import os
import re
import subprocess
from datetime import datetime, timezone, timedelta

STATS_DIR = "/home/ubuntu/minecraft-server/world/stats"
USERCACHE_FILE = "/home/ubuntu/minecraft-server/usercache.json"
OUTPUT_FILE = "/var/www/html/stats.json"

def load_usercache():
    try:
        with open(USERCACHE_FILE, "r") as f:
            cache = json.load(f)
            return {entry["uuid"]: entry["name"] for entry in cache}
    except:
        return {}

def get_online_players():
    try:
        result = subprocess.run(
            ["mcrcon", "-H", "localhost", "-P", "25575", "-p", "mc2025admin", "list"],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip()
        output = re.sub(r"\x1b\[[0-9;]*m", "", output)
        output = re.sub(r"\[0m", "", output)
        
        if "players online:" in output:
            parts = output.split("players online:")
            if len(parts) > 1:
                players_str = parts[1].strip()
                if players_str:
                    return [p.strip() for p in players_str.split(",") if p.strip()]
        return []
    except:
        return []

def get_top_5(stat_dict):
    """Retorna top 5 items ordenados por valor"""
    sorted_items = sorted(stat_dict.items(), key=lambda x: -x[1])[:5]
    return [{"name": k.replace("minecraft:", ""), "value": v} for k, v in sorted_items]

def get_death_causes(killed_by_dict):
    """Retorna todas las causas de muerte ordenadas"""
    sorted_items = sorted(killed_by_dict.items(), key=lambda x: -x[1])
    return [{"name": k.replace("minecraft:", ""), "value": v} for k, v in sorted_items]

def process_player_stats(filepath, uuid, name_map):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except:
        return None
    
    stats = data.get("stats", {})
    custom = stats.get("minecraft:custom", {})
    mined = stats.get("minecraft:mined", {})
    killed = stats.get("minecraft:killed", {})
    killed_by = stats.get("minecraft:killed_by", {})
    crafted = stats.get("minecraft:crafted", {})
    broken = stats.get("minecraft:broken", {})
    
    play_time_ticks = custom.get("minecraft:play_time", 0)
    play_time_hours = round(play_time_ticks / 72000, 1)
    
    if play_time_hours < 0.1:
        return None
    
    deaths = custom.get("minecraft:deaths", 0)
    mob_kills = sum(killed.values())
    kd_ratio = round(mob_kills / max(1, deaths), 1)
    
    # Distancias (convertir de cm a km)
    walk_km = round(custom.get("minecraft:walk_one_cm", 0) / 100000, 1)
    sprint_km = round(custom.get("minecraft:sprint_one_cm", 0) / 100000, 1)
    swim_km = round(custom.get("minecraft:swim_one_cm", 0) / 100000, 1)
    fly_km = round(custom.get("minecraft:fly_one_cm", 0) / 100000, 1)
    horse_km = round(custom.get("minecraft:horse_one_cm", 0) / 100000, 1)
    boat_km = round(custom.get("minecraft:boat_one_cm", 0) / 100000, 1)
    total_distance = round(walk_km + sprint_km + swim_km + fly_km + horse_km + boat_km, 1)
    
    # Tiempo desde ultima muerte (convertir ticks a horas)
    time_since_death_ticks = custom.get("minecraft:time_since_death", 0)
    time_since_death_hours = round(time_since_death_ticks / 72000, 1)
    
    return {
        "uuid": uuid,
        "name": name_map.get(uuid, uuid[:8]),
        "play_time_hours": play_time_hours,
        "deaths": deaths,
        "mob_kills": mob_kills,
        "blocks_mined": sum(mined.values()),
        "items_crafted": sum(crafted.values()),
        "distance_km": total_distance,
        "kd_ratio": kd_ratio,
        # Datos extendidos - General
        "leave_game": custom.get("minecraft:leave_game", 0),
        "sleep_in_bed": custom.get("minecraft:sleep_in_bed", 0),
        "jump": custom.get("minecraft:jump", 0),
        "animals_bred": custom.get("minecraft:animals_bred", 0),
        "open_chest": custom.get("minecraft:open_chest", 0),
        # Datos extendidos - Combate
        "damage_dealt": custom.get("minecraft:damage_dealt", 0),
        "damage_taken": custom.get("minecraft:damage_taken", 0),
        "damage_blocked": custom.get("minecraft:damage_blocked_by_shield", 0),
        "player_kills": custom.get("minecraft:player_kills", 0),
        # Datos extendidos - Viajes
        "walk_km": walk_km,
        "sprint_km": sprint_km,
        "swim_km": swim_km,
        "fly_km": fly_km,
        "horse_km": horse_km,
        "boat_km": boat_km,
        # Datos extendidos - Mineria
        "tools_broken": sum(broken.values()),
        "villager_trades": custom.get("minecraft:traded_with_villager", 0),
        # Datos extendidos - Muertes
        "time_since_death_hours": time_since_death_hours,
        # Top 5 listas
        "top_mobs_killed": get_top_5(killed),
        "top_blocks_mined": get_top_5(mined),
        "death_causes": get_death_causes(killed_by)
    }

def main():
    name_map = load_usercache()
    players = []
    
    for filename in os.listdir(STATS_DIR):
        if filename.endswith(".json"):
            uuid = filename.replace(".json", "")
            filepath = os.path.join(STATS_DIR, filename)
            player_stats = process_player_stats(filepath, uuid, name_map)
            if player_stats:
                players.append(player_stats)
    
    players.sort(key=lambda x: -x["play_time_hours"])
    
    records = {}
    if players:
        most_hours = max(players, key=lambda x: x["play_time_hours"])
        most_blocks = max(players, key=lambda x: x["blocks_mined"])
        most_mobs = max(players, key=lambda x: x["mob_kills"])
        most_deaths = max(players, key=lambda x: x["deaths"])
        best_kd = max(players, key=lambda x: x["kd_ratio"])
        most_distance = max(players, key=lambda x: x["distance_km"])
        
        records = {
            "most_hours": {"name": most_hours["name"], "value": str(most_hours["play_time_hours"]) + "h"},
            "most_blocks": {"name": most_blocks["name"], "value": "{:,}".format(most_blocks["blocks_mined"])},
            "most_mobs": {"name": most_mobs["name"], "value": "{:,}".format(most_mobs["mob_kills"])},
            "most_deaths": {"name": most_deaths["name"], "value": str(most_deaths["deaths"])},
            "best_kd": {"name": best_kd["name"], "value": str(best_kd["kd_ratio"])},
            "most_distance": {"name": most_distance["name"], "value": str(most_distance["distance_km"]) + " km"}
        }
    
    online_players = get_online_players()
    
    output = {
        "updated": datetime.now(timezone(timedelta(hours=1))).strftime("%d/%m/%Y %H:%M:%S"),
        "total_players": len(players),
        "online_players": online_players,
        "online_count": len(online_players),
        "players": players,
        "records": records
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("Stats generated:", len(players), "players,", len(online_players), "online")

if __name__ == "__main__":
    main()
