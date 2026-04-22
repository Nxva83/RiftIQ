"""
NeuralIQ — Analyse des données (module 1)
=========================================
À lancer après riot_pipeline.py.
Génère des insights à partir des JSON sauvegardés.

Usage:
    python analyze.py --name "TonPseudo" --tag "EUW"
"""

import json
import os
import argparse
import math
from collections import Counter, defaultdict


def load_data(name: str, tag: str) -> tuple[list, list]:
    base = "data"
    with open(f"{base}/matches_{name}_{tag}.json", encoding="utf-8") as f:
        matches = json.load(f)
    try:
        with open(f"{base}/events_{name}_{tag}.json", encoding="utf-8") as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []
    return matches, events


def winrate_by_agent(matches: list) -> dict:
    stats = defaultdict(lambda: {"wins": 0, "total": 0, "kda_sum": 0.0})
    for m in matches:
        a = m["agent"]
        stats[a]["total"] += 1
        stats[a]["kda_sum"] += m["kda"]
        if m["won"]:
            stats[a]["wins"] += 1

    result = {}
    for agent, s in stats.items():
        result[agent] = {
            "winrate": round(s["wins"] / s["total"] * 100, 1),
            "avg_kda": round(s["kda_sum"] / s["total"], 2),
            "games": s["total"],
        }
    return dict(sorted(result.items(), key=lambda x: x[1]["games"], reverse=True))


def winrate_by_map(matches: list) -> dict:
    stats = defaultdict(lambda: {"wins": 0, "total": 0})
    for m in matches:
        mp = m["map_name"] or "Unknown"
        stats[mp]["total"] += 1
        if m["won"]:
            stats[mp]["wins"] += 1
    return {
        mp: {
            "winrate": round(s["wins"] / s["total"] * 100, 1),
            "games": s["total"],
        }
        for mp, s in sorted(stats.items(), key=lambda x: x[1]["total"], reverse=True)
    }


def performance_trend(matches: list, window: int = 5) -> list[dict]:
    """Calcule la moyenne glissante de KDA et winrate sur les N derniers matchs."""
    trend = []
    for i in range(len(matches)):
        chunk = matches[max(0, i - window + 1): i + 1]
        wins = sum(1 for m in chunk if m["won"])
        avg_kda = sum(m["kda"] for m in chunk) / len(chunk)
        trend.append({
            "match_index": i + 1,
            "date": matches[i]["game_start"][:10],
            "rolling_winrate": round(wins / len(chunk) * 100, 1),
            "rolling_kda": round(avg_kda, 2),
            "headshot_pct": matches[i]["headshot_pct"],
        })
    return trend


def death_timing_analysis(events: list) -> dict:
    """
    Analyse quand les morts surviennent dans le round.
    Permet de détecter si le joueur joue trop agressivement en début de round,
    ou s'il se fait éliminer systématiquement en clutch.
    """
    deaths = [e for e in events if e.get("event_type") == "death"]
    if not deaths:
        return {}

    # Buckets : early (0-15s), mid (15-45s), late (45s+)
    buckets = {"early_0_15s": 0, "mid_15_45s": 0, "late_45s_plus": 0}
    for d in deaths:
        t = d.get("timestamp_ms", 0) / 1000
        if t < 15:
            buckets["early_0_15s"] += 1
        elif t < 45:
            buckets["mid_15_45s"] += 1
        else:
            buckets["late_45s_plus"] += 1

    total = sum(buckets.values())
    pcts = {k: round(v / total * 100, 1) for k, v in buckets.items()}

    # Conseil automatique
    advice = ""
    if pcts["early_0_15s"] > 40:
        advice = "⚠️  Tu meurs beaucoup en début de round (rush / prise de position agressive trop tôt)."
    elif pcts["late_45s_plus"] > 40:
        advice = "⚠️  Tu te retrouves souvent en situation de clutch — travaille la gestion d'équipe."
    else:
        advice = "✅  Ta gestion du timing de round est équilibrée."

    return {
        "death_timing_pct": pcts,
        "total_deaths_analyzed": total,
        "advice": advice,
    }


def economy_analysis(matches: list) -> dict:
    """
    Analyse les décisions économiques.
    Compare les performances selon le niveau d'investissement.
    """
    low_eco  = [m for m in matches if m.get("economy_score", 0) < 2000]
    mid_eco  = [m for m in matches if 2000 <= m.get("economy_score", 0) < 4000]
    full_buy = [m for m in matches if m.get("economy_score", 0) >= 4000]

    def stats(ms):
        if not ms:
            return None
        return {
            "games": len(ms),
            "winrate": round(sum(1 for m in ms if m["won"]) / len(ms) * 100, 1),
            "avg_kda": round(sum(m["kda"] for m in ms) / len(ms), 2),
        }

    return {
        "eco_round":  stats(low_eco),
        "half_buy":   stats(mid_eco),
        "full_buy":   stats(full_buy),
    }


def generate_report(name: str, tag: str, matches: list, events: list) -> str:
    """Génère un rapport texte lisible — base du futur module LLM."""
    total  = len(matches)
    wins   = sum(1 for m in matches if m["won"])
    wr     = round(wins / total * 100) if total else 0
    avg_kda = round(sum(m["kda"] for m in matches) / total, 2) if total else 0
    avg_hs  = round(sum(m["headshot_pct"] for m in matches) / total, 1) if total else 0

    agents  = winrate_by_agent(matches)
    maps    = winrate_by_map(matches)
    timing  = death_timing_analysis(events)
    eco     = economy_analysis(matches)

    lines = [
        f"╔══════════════════════════════════════════════╗",
        f"  📊 Rapport NeuralIQ — {name}#{tag}",
        f"╚══════════════════════════════════════════════╝",
        f"",
        f"  Sur {total} matchs analysés :",
        f"  • Winrate  : {wr}%",
        f"  • KDA moy. : {avg_kda}",
        f"  • HS%  moy : {avg_hs}%",
        f"",
        f"──── 🎮 Par agent ────────────────────────────────",
    ]
    for agent, s in list(agents.items())[:5]:
        bar = "█" * int(s["winrate"] / 10)
        lines.append(
            f"  {agent[:20]:20} {s['winrate']:5}% WR  KDA {s['avg_kda']}  ({s['games']} parties)"
        )

    lines += [
        f"",
        f"──── 🗺️  Par map ─────────────────────────────────",
    ]
    for mp, s in maps.items():
        lines.append(f"  {mp[:20]:20} {s['winrate']:5}% WR  ({s['games']} parties)")

    if timing:
        lines += [
            f"",
            f"──── ⏱️  Timing des morts ──────────────────────",
            f"  Early (0-15s)   : {timing['death_timing_pct'].get('early_0_15s', 0)}%",
            f"  Mid   (15-45s)  : {timing['death_timing_pct'].get('mid_15_45s', 0)}%",
            f"  Late  (45s+)    : {timing['death_timing_pct'].get('late_45s_plus', 0)}%",
            f"  → {timing.get('advice', '')}",
        ]

    if eco:
        lines += [
            f"",
            f"──── 💰 Économie ─────────────────────────────",
        ]
        for tier, s in eco.items():
            if s:
                lines.append(
                    f"  {tier:12} : {s['winrate']}% WR  KDA {s['avg_kda']}  ({s['games']} parties)"
                )

    # Axe d'amélioration principal
    lines += ["", "──── 🎯 Axe prioritaire ──────────────────────"]
    if avg_hs < 20:
        lines.append("  → Travaille ta visée : un HS% < 20% est un handicap sérieux.")
        lines.append("    Conseil : Fais 15 min de deathmatch en visant uniquement la tête avant chaque session.")
    elif avg_kda < 1.0:
        lines.append("  → Ton KDA < 1.0 signifie que tu meurs plus que tu ne tues.")
        lines.append("    Conseil : Joue plus prudemment, prends des duels 1v1 favorables seulement.")
    else:
        worst_map = min(maps.items(), key=lambda x: x[1]["winrate"])[0]
        lines.append(f"  → Ta map la plus faible : {worst_map}.")
        lines.append(f"    Conseil : Regarde 3 replays sur cette map et identifie tes erreurs de positionnement.")

    lines.append("")
    return "\n".join(lines)


# ─── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeuralIQ — Analyse des données")
    parser.add_argument("--name", required=True, help="Riot ID")
    parser.add_argument("--tag",  required=True, help="Tag (ex: EUW)")
    args = parser.parse_args()

    print(f"\nChargement des données pour {args.name}#{args.tag}...")
    matches, events = load_data(args.name, args.tag)
    print(f"  {len(matches)} matchs chargés, {len(events)} évènements")

    report = generate_report(args.name, args.tag, matches, events)
    print("\n" + report)

    # Sauvegarde du rapport
    out_path = f"data/report_{args.name}_{args.tag}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n💾 Rapport sauvegardé : {out_path}")
