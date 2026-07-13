# Playtest plan (簡易)

目的:
- 武器バランス確認（TtK、1v1勝率、命中率）

手順:
1. 1v1 固定マップ、武器ごとに対戦（AR v AR, AR v SMG, SMG v SG 等）
2. 各セッションはウォームアップ3分＋10ラウンド、本番は合計30セッション以上
3. 収集項目: timestamp, playerId, weapon, event(fire/hit/kill), position, targetId
4. アンケート: 1分で答えられる感想（当てやすさ、爽快感、不満点）

ログフォーマット（CSV 例）:
- timestamp,sessionId,playerId,weapon,event,hitX,hitY,hitZ,targetId,damage

KPI:
- 平均TtK（近・中・遠）
- 武器別1v1勝率
- 命中率（距離別）
- 弾切れ発生率
- リロード中にキルされた回数
