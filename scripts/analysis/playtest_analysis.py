#!/usr/bin/env python3
"""
playtest_analysis.py
入力: playtest CSV (columns: timestamp,sessionId,playerId,weapon,event,hitX,hitY,hitZ,targetId,damage)
出力: weaponごとの平均TtK, 命中率, 勝率の簡易集計（CSV/ターミナル表示）
使い方:
  pip install pandas
  python scripts/analysis/playtest_analysis.py path/to/log.csv
注意: ログの event は "fire", "hit", "kill" を想定
"""

import sys
import pandas as pd
from datetime import datetime

def load_csv(path):
    return pd.read_csv(path, parse_dates=['timestamp'])

def compute_hit_rate(df):
    fires = df[df['event']=='fire'].groupby('weapon').size().rename('fires')
    hits = df[df['event']=='hit'].groupby('weapon').size().rename('hits')
    stats = pd.concat([fires, hits], axis=1).fillna(0)
    stats['hit_rate'] = stats['hits'] / stats['fires'].replace(0, pd.NA)
    return stats.reset_index()

def compute_ttk(df):
    # For each kill event, estimate TtK as (kill_time - first_fire_time_of_killer_in_same_session)
    kills = df[df['event']=='kill'].copy()
    results = []
    for _, k in kills.iterrows():
        session = k['sessionId']
        killer = k['playerId']
        weapon = k['weapon']
        kill_time = k['timestamp']
        fires = df[(df['sessionId']==session) & (df['playerId']==killer) & (df['event']=='fire') & (df['timestamp']<=kill_time)]
        if fires.empty:
            continue
        first_fire_time = fires['timestamp'].min()
        ttk = (kill_time - first_fire_time).total_seconds()
        results.append({'weapon': weapon, 'ttk': ttk})
    if not results:
        return pd.DataFrame(columns=['weapon','avg_ttk'])
    res_df = pd.DataFrame(results)
    return res_df.groupby('weapon')['ttk'].mean().rename('avg_ttk').reset_index()

def compute_win_rate(df):
    # Need per-session winners: assume kill event for final kill contains targetId==None or use last kill per session per player
    # Simple heuristic: count number of kills per player per session; winner = max kills
    kills = df[df['event']=='kill']
    kills_per = kills.groupby(['sessionId','playerId','weapon']).size().reset_index(name='kills')
    # winner per session by player (max kills)
    winners = kills_per.sort_values(['sessionId','kills'], ascending=[True,False]).drop_duplicates('sessionId')
    # winner weapon: weapon used for that player's kills (this heuristic assigns the weapon of the first kill row for that player)
    win_counts = winners['weapon'].value_counts().rename('wins').reset_index().rename(columns={'index':'weapon'})
    sessions = df['sessionId'].nunique()
    if sessions == 0:
        return pd.DataFrame(columns=['weapon','win_rate'])
    win_counts['win_rate'] = win_counts['wins'] / sessions
    return win_counts[['weapon','win_rate']]

def main(path):
    df = load_csv(path)
    hit = compute_hit_rate(df)
    ttk = compute_ttk(df)
    win = compute_win_rate(df)
    print("=== Hit rates ===")
    print(hit.to_string(index=False))
    print("\n=== Avg TtK (s) ===")
    print(ttk.to_string(index=False))
    print("\n=== Win rates ===")
    print(win.to_string(index=False))
    # also save summary
    summary = hit.merge(ttk, on='weapon', how='outer').merge(win, on='weapon', how='outer')
    summary.to_csv('playtest_summary.csv', index=False)
    print("\nSummary saved to playtest_summary.csv")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python playtest_analysis.py path/to/log.csv")
        sys.exit(1)
    main(sys.argv[1])
