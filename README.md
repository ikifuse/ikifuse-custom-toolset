# ikifuse Custom Toolset

AI協働開発で繰り返し使うプラグイン、スキル、ルーティン、テンプレート、判断基準をまとめる個人用ツールセットです。

困り事ごとに小さく追加し、必要なものだけをプロジェクトへ導入できる状態を目指します。

> [!IMPORTANT]
> このリポジトリは個人用の非公開リポジトリです。外部から導入したものは、元の作者・URL・取り込んだ版を記録します。

## 目次

- [目的](#目的)
- [現在入っているもの](#現在入っているもの)
- [全体構成](#全体構成)
- [運用ルール](#運用ルール)
- [新しいプロジェクトへの導入](#新しいプロジェクトへの導入)

## 目的

- 困り事ごとに小さな道具を追加する
- 不要なものを個別に無効化・削除できるようにする
- 一つの変更が他の道具へ影響しにくい構成にする
- GitHubで全体と由来を一覧できるようにする
- 新しいプロジェクトでも同じ道具を再利用する
- 役に立ったものだけを将来ほかの人へ渡せるようにする

## 現在入っているもの

| 種類 | 名前 | 目的 | 元の履歴 |
| --- | --- | --- | --- |
| Codexプラグイン | [evidence-first](plugins/evidence-first/) | 「確認」を必要な証拠範囲まで調査する | [ikifuse/evidence-first](https://github.com/ikifuse/evidence-first) |

## 全体構成

```text
ikifuse-custom-toolset/
├── README.md
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── evidence-first/
├── standalone-skills/
├── routines/
├── templates/
├── shared/
├── platforms/
│   ├── codex/
│   └── antigravity/
└── external/
```

空の分類フォルダは先に増やさず、実際に入れるものが決まった時点で追加します。

- `plugins/`: Codexで個別に導入・無効化できるプラグイン
- `standalone-skills/`: プラグイン化しない単体スキル
- `routines/`: 複数の作業で共通利用する手順
- `templates/`: 再利用する雛形
- `shared/`: 複数環境で共通の判断基準や事例
- `platforms/codex/`: OpenAI・Codexだけで使う設定
- `platforms/antigravity/`: Google・Antigravityだけで使う設定
- `external/`: 外部から導入したものの記録や未変更の保管場所

## 運用ルール

1. 新しい道具の名前は、作成前に候補と意味を確認して決める
2. 一つの困り事につき、できるだけ一つの独立した単位にする
3. 外部由来のものには、元URL・版・変更内容を残す
4. 既存の正本を削除する前に、新しい場所から動作確認する
5. 生成キャッシュや個人認証情報は保存しない
6. READMEの一覧を、追加・削除と同時に更新する

## 新しいプロジェクトへの導入

Codex用プラグインは、リポジトリ内の `.agents/plugins/marketplace.json` を入口として個別に導入できる構成にします。

現在の `evidence-first` は既存環境を壊さないため、元のリポジトリと現在のローカル登録を残したまま、このツールセット側での導入確認を進めます。
