# OpenAI・Codex用

Codexで使うプラグイン、単体スキル、専用設定を管理します。

## 構成

```text
OpenAI・Codex用/
├── プラグイン/
├── 単体スキル/
└── Codex専用の設定/
```

一つのプラグインにつき、一つの独立したフォルダを`プラグイン`へ追加します。

## Codex用プラグインの技術用ファイル

### `.agents/plugins/marketplace.json`

リポジトリのルートにある、Codexへこのリポジトリに含まれるプラグインの名前、保存場所、利用可能状態などを伝えるマーケットプレイス定義です。

このファイルへ登録されていることと、Codexへ実際にインストール済みであることは別です。

### `.codex-plugin/plugin.json`

各Codex用プラグインの中に置く、そのプラグイン自身の定義ファイルです。

Evidence Firstでは、次の場所にあります。

```text
OpenAI・Codex用/プラグイン/evidence-first/.codex-plugin/plugin.json
```

Codex用プラグインを追加した場合は、必要に応じてルートの`.agents/plugins/marketplace.json`へ登録します。具体的な導入・更新・取り外し方法は、各プラグインのREADMEで確認します。
