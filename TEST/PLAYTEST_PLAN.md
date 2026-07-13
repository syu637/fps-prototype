# Playtest plan (簡易)

目的:
- 武器バランス確認（TtK、1v1勝率、命中率）

手順:
1. 1v1 固定マップ、武器ごとに対戦（AR v AR, AR v SMG, SMG v SG 等）
2. 各セッションはウォームアップ3分＋10ラウンド、本番は合計30セッション以上
3. 収集項目: timestamp, sessionId, playerId, weapon, event(fire/hit/kill), position(x,y,z), targetId, damage
4. アンケート: 1分で答えられる感想（当てやすさ、爽快感、不満点）

ログフォーマット（CSV 例）:
- timestamp,sessionId,playerId,weapon,event,hitX,hitY,hitZ,targetId,damage

KPI:
- 平均TtK（近・中・遠）
- 武器別1v1勝率 (weapon win rate)
- 命中率（ヒット率）＝ hits / fires（距離別）
- 弾切れ発生率
- リロード中にキルされた回数

プレイテスト手順（実行）
- 固定ルールでマッチを作成、各ラウンドでログをサーバーに記録してCSV保存
- 終了後、CSV を `scripts/analysis/playtest_analysis.py` にかける（自動で集計される）

判断基準（仮）
- 各武器の1v1勝率が 45–55% に収束しているか
- 近距離TtKが 1.8–2.5s 程度であるか（目安）
