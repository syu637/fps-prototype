# 3Dアセット作成チェックリスト

以下は武器モデル等を作るときのチェックリスト（1武器あたり）。プロトタイプでは外形とアタッチメントだけでOK。

- [ ] Low-poly メッシュ作成（tris < 3k）
- [ ] UV 展開（保存）
- [ ] 基本テクスチャ（512）作成（色）
- [ ] Muzzle/Handle/ShellEject Attachment の目印を作る（Blender上に Empty か Locator）
- [ ] FBX エクスポート（スケール適用）
- [ ] Roblox にインポート → MeshPart 化
- [ ] Attachment を Roblox 上で正確に配置 & 命名
- [ ] 衝突メッシュ（簡易）を作成・適用
- [ ] テスト（ゲーム内で持たせて見た目・当たりを確認）
- [ ] バージョン保存（例: weapon_ar_v001_20260713.fbx）

命名規約の例:
- assets/models/weapons/weapon_ar_v001.fbx
- attachment_Muzzle, attachment_Handle, attachment_Mag

備考:
- Pivot（原点）は Handle に合わせること
- FBX エクスポート前にスケールを適用（Blender: Ctrl-A）
