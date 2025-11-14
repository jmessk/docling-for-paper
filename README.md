# Docling PDF Converter (Prototype)

Docling を使って PDF を Markdown または HTML に変換するシンプルな Web サーバのプロトタイプです。UI は単一の HTML で、ファイル選択とドラッグ＆ドロップに対応しています。

## 起動方法

uv を使用して依存関係を解決し、開発サーバを起動します。

```bash
# 依存関係は pyproject.toml に定義済み（docling, fastapi, uvicorn, python-multipart）
uv run python main.py
```

サーバが起動したら、ブラウザで以下を開きます。

```text
http://localhost:8000/
```

## 使い方

1. PDF をドラッグ＆ドロップ（またはファイル選択）
2. 出力形式（HTML / Markdown）を選択
3. 変換ボタンをクリック

変換結果は以下のように返却されます。

- HTML を選択: `text/html` として返却され、ブラウザでレンダリングされます
- Markdown を選択: `text/plain` として返却され、ブラウザ上でテキスト表示されます

ブラウザの「戻る」でアップロード画面に戻れます。

## エンドポイント

- `GET /` — 最小のアップロード UI（HTML 1 枚）
- `POST /convert` — フォーム（multipart/form-data）で PDF と `format`（`html` or `markdown`）を受け取り、変換結果を返却

## 注意事項（プロトタイプ）

- 大きな PDF では変換に時間がかかる場合があります。
- 変換はサーバ上で実行されます。アップロードした PDF は一時ファイルとして保存され、処理後に削除します。
- 本番運用では、並列処理・タイムアウト・バリデーション・ログ・永続化（結果のダウンロード用保存）などの強化が必要です。
