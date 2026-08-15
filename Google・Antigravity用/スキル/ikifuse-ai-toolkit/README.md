# ikifuse AI Toolkit — Google Antigravity版

AIとの共同作業で、証拠、許可された行動範囲、外部へ出してよい情報を分けて確認するための、Google Antigravity向けAgent Skillsです。

このディレクトリは配布・編集用パッケージです。直下の`.agents/skills/`は、Antigravityのworkspace-local配置をそのまま再現しています。

> [!IMPORTANT]
> このリポジトリを`ikifuse-custom-toolset`をworkspace rootとして開く場合、この入れ子の`.agents/skills/`は自動探索されません。Antigravityが実際に読むインストール先は、リポジトリルートの`.agents/skills/`です。現在は3 Skillをそこにも配置しています。

## 3つのSkill

| Skill | 責務 |
| --- | --- |
| `evidence-audit` | 結論に必要な証拠を調べ、事実・推論・矛盾・未確認事項を分ける |
| `action-check` | ユーザーが許可した操作・対象・停止点を維持し、開始前と作業後の変更範囲を照合する |
| `secret-privacy-guard` | 外部へ出る直前の情報を検査し、秘密・個人・ローカル専用情報の公開可否を分類する |

責務は統合しません。たとえばpushでは、`action-check`が操作許可と対象範囲を扱い、`secret-privacy-guard`が送信内容を扱います。秘密候補が実データか公開済みダミーかなど、追加の事実確認が必要な場合だけ`evidence-audit`を使います。

## 公式仕様との対応

2026年8月15日に、Googleの現行公式ドキュメントを確認しました。

- workspace-local Skill: `<workspace-root>/.agents/skills/<skill-folder>/`
- global Skill: `~/.gemini/config/skills/<skill-folder>/`
- `.agent/skills`は後方互換であり、現在の既定は`.agents/skills`
- 各Skillで必須なのは`SKILL.md`
- YAML frontmatterでは`description`が必須。`name`は省略可能だが、ディレクトリ名へ既定される
- `scripts/`、`examples/`、`resources/`を任意で同梱できる
- Skillは会話開始時にnameとdescriptionが発見され、関連時に`SKILL.md`全文が読み込まれる

参照した公式資料:

- [Google Antigravity Docs — Agent Skills](https://antigravity.google/docs/skills)
- [Google Antigravity Docs — CLI Reference](https://antigravity.google/docs/cli/reference)
- [Google Antigravity Docs — Plugins](https://antigravity.google/docs/ide/plugins)

`name`は現行仕様では省略可能ですが、識別を明確にし、Google Codelabの例とも互換になるよう3 Skillすべてへ明記しています。

Antigravityには複数Skillを束ねるplugin形式もありますが、この版はSkill以外のrule、MCP、hookを必要としません。3つの責務を独立Skillとして保つため、plugin manifestは採用していません。

## ディレクトリ構成

```text
ikifuse-ai-toolkit/
├── .agents/
│   └── skills/
│       ├── evidence-audit/
│       │   └── SKILL.md
│       ├── action-check/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── test_action_check_contract.py
│       └── secret-privacy-guard/
│           ├── SKILL.md
│           └── scripts/
│               ├── scan_sensitive.py
│               └── test_scan_sensitive.py
├── tests/
│   └── test_toolkit_contract.py
└── README.md
```

## 配置・導入方法

### workspace-local

対象workspaceのルートに、配布パッケージの`.agents/skills/`配下にある3フォルダを配置します。

```text
<workspace-root>/.agents/skills/evidence-audit/
<workspace-root>/.agents/skills/action-check/
<workspace-root>/.agents/skills/secret-privacy-guard/
```

このリポジトリでは、次のように役割を分けています。

```text
Google・Antigravity用/スキル/ikifuse-ai-toolkit/.agents/skills/  # 保管・配布・編集用
.agents/skills/                                                  # ikifuse-custom-toolset workspaceのインストール先
```

配布パッケージ自体を独立したworkspace rootとしてAntigravityに開く場合に限り、パッケージ内の`.agents/skills/`が直接探索対象になります。親リポジトリをworkspace rootとして開く場合は、必ず親リポジトリ直下へ配置してください。

### global

3つのSkillフォルダを次へ配置します。

```text
~/.gemini/config/skills/evidence-audit/
~/.gemini/config/skills/action-check/
~/.gemini/config/skills/secret-privacy-guard/
```

globalへの実コピーは、このリポジトリの正本とインストール済みコピーが分かれる操作です。更新時はこのAntigravity版を編集し、明示的に再配置してください。

配置後、Antigravity CLIでは`/skills`で読み込まれたSkillを確認できます。

## 呼び出し方

Antigravityはdescriptionから関連Skillを自動選択します。確実に使わせたい場合は、Skill名をそのまま指定します。

Skillごとの`/skill-name`はslash commandではありません。`/secret-privacy-guard`のように入力して`No matching results`となっても、それだけではSkill未検出とは判定できません。読み込み確認には公式の`/skills`を使い、実際の依頼では次のように自然文でSkill名を指定してください。

```text
evidence-audit を使って実質調査し、事実・推論・矛盾・未確認事項を分けてください。
```

```text
action-check を使って、開始前の変更を保護し、許可した範囲だけ修正してください。
```

```text
secret-privacy-guard を使って、push対象に秘密情報や個人情報が含まれないか確認してください。
```

## Secret scanner

`scan_sensitive.py`はCodex版の読み取り専用スキャナーを基礎に、Antigravityのローカル設定パスも検査候補へ加えたものです。Python標準ライブラリだけを使い、`--staged`ではローカルのGit indexを読み取ります。

```bash
python3 .agents/skills/secret-privacy-guard/scripts/scan_sensitive.py --help
python3 .agents/skills/secret-privacy-guard/scripts/scan_sensitive.py --staged
python3 .agents/skills/secret-privacy-guard/scripts/scan_sensitive.py path/to/file
```

安全境界:

- 読み取り専用であり、ファイルを書き換えない
- 外部通信を行わない
- 検出した秘密値そのものを出力しない
- 検出時も削除、マスク、unstage、commit、pushを行わない
- `SAFE`は読み取れた範囲だけの判定であり、秘密情報が絶対に存在しないという証明ではない
- バイナリ、UTF-8以外、上限超過、読み取り不能は`UNKNOWN`として残す
- Antigravityのpermissionやsandboxを迂回せず、その確認に従う

判定は`SAFE`、`SENSITIVE`、`REVIEW_REQUIRED`、`UNKNOWN`です。

## テスト方法

パッケージルートで実行します。

```bash
python3 -m unittest discover -s tests -v
python3 .agents/skills/action-check/scripts/test_action_check_contract.py
python3 -m unittest discover -s .agents/skills/secret-privacy-guard/scripts -p 'test_*.py' -v
```

テストは一時ディレクトリと合成データだけを使います。実データや重要ファイルを削除する破壊試験は行いません。契約テストはSkill本文に必須ルールが残っていることを確認するもので、新規Antigravityセッションでのモデル挙動試験を完全には代替しません。

## Codex版との関係

安全思想・責務分離の正本は次です。

```text
OpenAI・Codex用/プラグイン/ikifuse-ai-toolkit/
```

Antigravity版は、その3 SkillをGoogle Antigravityの現行Agent Skill仕様へ移植した独立版です。今回は大規模な共通ライブラリ化やリポジトリ再編を行っていません。

再利用したもの:

- Evidence Auditの証拠レーン、5分類、4結論状態、削除安全性調査
- Action Checkの4内部ガード、scope分類、軽量編集と破壊操作の境界
- Secret & Privacy Guardの公開直前検査、4判定、安全停止
- 読み取り専用scannerの検出ロジックと合成データテスト

Antigravity向けに変更したもの:

- `.agents/skills/<skill-folder>/SKILL.md`配置
- Antigravityの自動発見に合うfrontmatter description
- Codex固有の呼び出し表記を使わず、Skill名を明示する呼び出し例
- Antigravityのpermission・sandboxを迂回しない実行説明
- scannerのローカル設定候補へ`.agent`、`.agents`、`.gemini`を追加
- テストをどの作業ディレクトリからでも実行できるimport方式へ変更

移植していないCodex固有要素:

- `.codex-plugin/plugin.json`
- `agents/openai.yaml`
- Codexのキャッシュ構造
- `$skill-name`形式の呼び出し例
- Codexのpluginインストール処理

## 更新方針

安全契約を変更する場合は、先にCodex版の正本で変更意図を確定し、この独立版へ意図的に反映します。自動同期はありません。Antigravity公式仕様は変わり得るため、配置やfrontmatterを変更する前に公式資料を再確認してください。
