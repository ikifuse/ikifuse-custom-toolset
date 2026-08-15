# 取り込み元と履歴

- 取り込み元: https://github.com/ikifuse/evidence-first
- 取り込み日: 2026-08-14
- 取り込み時点のブランチ: main
- 取り込み時点の最新コミット: 3614b5bc074237c3a6cfeeae080398ade8279b44
- 元リポジトリの公開範囲: Private
- ライセンス: 元リポジトリ内では確認できず

## 元リポジトリで確認したコミット

1. 913bf6dd8e295000775f30514dd970d145f3a89d — Add evidence-first plugin manifest
2. 5205fd3dddf18d7a95768814a08d235e7c3c484e — Add evidence audit skill
3. 77d63efbc62142f4006237b9b910e6eb3f82c3b9 — Add evidence audit agent metadata
4. 3614b5bc074237c3a6cfeeae080398ade8279b44 — Add Japanese README and usage guide

## 管理方針

元の evidence-first リポジトリは削除せず、取り込み前の履歴と復旧元として残します。
このフォルダの内容を変更した場合は、このファイルへ変更理由と元との差分を追記します。
外部へ共有する前に、元リポジトリにライセンスが設定されているかを改めて確認します。

## ikifuse AI Toolkitへの拡張

- 変更理由: ikifuse-custom-toolset Issue #1で整理した認識差と、obsidian-ig-migration開発時に蓄積した行動範囲の問題へ対応するため
- プラグイン名: `evidence-first` から `ikifuse-ai-toolkit` へ変更
- バージョン: `0.1.1` から `0.2.0` へ変更
- 維持したもの: `evidence-audit` の調査・証拠分類・削除安全性の手順
- 追加したもの: `action-check` の相談／実装境界、変更範囲、重要な曖昧さ、完成済み範囲、任意改善、作成物報告の手順
- 設計根拠: https://github.com/ikifuse/ikifuse-custom-toolset/issues/1

## Secret & Privacy Guardの追加

- 変更理由: GitHubや外部サービスへ、秘密情報・個人情報・ローカル専用情報が意図せず流出することを防ぐため
- バージョン: `0.2.0` から `0.3.0` へ変更
- 追加したもの: `secret-privacy-guard` の外部公開前検査、4段階判定、検出後の停止報告、明示許可なしの修正禁止
- 補助機能: 検出値を表示・変更しない読み取り専用スキャナーと、合成データによる指定8ケース＋絶対パス補助ケースのテスト
- 責務分離: 証拠は`evidence-audit`、操作許可は`action-check`、外部公開情報は`secret-privacy-guard`が担当
