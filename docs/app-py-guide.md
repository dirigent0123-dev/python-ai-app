# Streamlit × Gemini で作る「AI ライティングツール」— `app.py` の仕組みを解説

Python と Streamlit だけで、6 種類の AI ライティング機能を 1 画面にまとめたアプリです。この記事では、その中心となる `app.py` がどう動いているかを、コードの流れに沿って整理します。

---

## このアプリは何をしているか

サイドバーでツールを選び、フォームに入力してボタンを押すと、Gemini API が文章を生成して画面に表示する——というシンプルな構成です。

| ツール | できること |
|---|---|
| ブログ記事作成 | テーマ・読者・文体から記事を生成 |
| メール返信文作成 | 受信メールと意図から返信文を生成 |
| 文章要約 | テキストを指定スタイルで要約 |
| 文章校正・改善 | 誤字・表現・読みやすさを改善 |
| SNS 投稿文作成 | プラットフォームに合わせた投稿文を生成 |
| 文体変換 | 意味を保ったまま文体を変換 |

**UI は `app.py`、AI ロジックは `tools/` フォルダ** に分かれています。役割分担がはっきりしているのが、このコードの設計の肝です。

---

## 全体アーキテクチャ

```
app.py（UI・画面切り替え）
    ↓ 関数呼び出し
tools/blog_writer.py など（プロンプト組み立て）
    ↓
tools/gemini_client.py（API 通信）
    ↓
Gemini API
```

ルーティングライブラリは使っていません。サイドバーの選択結果を文字列 `tool` に変換し、`if / elif` で画面を切り替えるだけです。小規模な個人ツールには、この素直な書き方が向いています。

---

## `app.py` を上から読む

### 1. インポートとページ設定

```python
import streamlit as st
from tools.blog_writer import write_blog
# ... 他のツールも同様

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

Streamlit 本体と、各ツールの関数だけをインポートしています。AI や API の詳細は `app.py` には書きません。

`set_page_config` は **必ず最初の Streamlit コマンド** として呼ぶ必要があります。タブ名・アイコン・レイアウトをここで決めています。

---

### 2. CSS で見た目を整える

```python
st.markdown("""<style>...</style>""", unsafe_allow_html=True)
```

Streamlit 標準 UI に CSS を上書きして、タイトル・ボタン・カードの色を統一しています。`unsafe_allow_html=True` を付けると HTML/CSS がそのまま描画されます。

---

### 3. ツール一覧の辞書 — ナビゲーションの核心

```python
TOOLS = {
    "📝 ブログ記事作成": "blog",
    "📧 メール返信文作成": "email",
    # ...
}
```

**表示ラベル（日本語＋絵文字）→ 内部キー（英語）** の対応表です。

サイドバーの `st.radio` でラベルを選び、`tool = TOOLS[selected_label]` で内部キーを取り出します。この 1 行が、以降の `if tool == "blog":` 分岐の起点になります。

新しいツールを足すときは：

1. `TOOLS` に 1 行追加
2. `tools/` に関数を作る
3. `elif tool == "新キー":` ブロックを追加

この 3 ステップで完結します。

---

### 4. サイドバー — ツール選択 UI

```python
with st.sidebar:
    selected_label = st.radio("ツール選択", list(TOOLS.keys()), ...)
tool = TOOLS[selected_label]
```

`with st.sidebar:` の中に書いたウィジェットは、すべて左サイドバーに配置されます。メインエリアはツールごとのフォーム専用に使えます。

---

### 5. `show_result()` — 結果表示の共通化

```python
def show_result(result: str, copy_label: str = "結果"):
    st.subheader("生成結果")
    if tool == "blog":
        st.markdown(result)          # Markdown としてレンダリング
    else:
        st.text_area(...)            # プレーンテキスト
    st.download_button(...)
```

6 ツールすべて同じ「結果表示 → ダウンロード」の流れなので、関数にまとめています。

- **ブログだけ** `st.markdown()` — AI が Markdown で返すため
- **それ以外** `st.text_area()` — コピーしやすいプレーンテキスト表示

---

### 6. 各ツールの UI ブロック — 同じパターンの繰り返し

6 つの `if / elif` ブロックは、ほぼ同じ型を踏襲しています。

```python
if tool == "blog":
    # ① 説明文
    # ② 入力フォーム（text_input, selectbox など）
    # ③ 生成ボタン
    if st.button("記事を生成する"):
        if not topic.strip():          # バリデーション
            st.warning("...")
        else:
            with st.spinner("生成中..."):
                try:
                    result = write_blog(...)
                    show_result(result)
                except ValueError as e:   # API キー未設定など
                    st.error(str(e))
                except Exception as e:    # その他のエラー
                    st.error(f"エラーが発生しました: {e}")
```

| ステップ | 役割 |
|---|---|
| 入力フォーム | ユーザーからパラメータを集める |
| バリデーション | 必須項目の空チェック |
| `st.spinner` | 生成中のローディング表示 |
| `try / except` | API キー不足と一般エラーを分けて表示 |
| `show_result()` | 結果の表示とダウンロード |

UI の見た目はツールごとに違いますが、**処理の骨格は共通** です。1 つ理解すれば、他も同じ考え方で読めます。

---

## ツール側（`tools/`）は何をしているか

`app.py` は UI 専用です。実際の AI 処理は `tools/` にあります。

例：`tools/blog_writer.py`

```python
def write_blog(topic, target_audience, tone, length, keywords) -> str:
    prompt = f"""あなたはプロのブログライターです。
    テーマ: {topic}
    ターゲット読者: {target_audience}
    ...
    """
    return generate(prompt)  # gemini_client.py を呼ぶ
```

各ツールは **プロンプトを組み立てて `generate()` に渡すだけ** です。API の詳細は `tools/gemini_client.py` に集約されています。

```python
def generate(prompt: str) -> str:
    model = get_model()  # 初回だけ初期化（シングルトン）
    response = model.generate_content(prompt)
    return response.text
```

429（レート制限）が出たときは、API が示す待機時間後に最大 3 回まで自動リトライします。

---

## データの流れ（1 リクエストの全体像）

```
ユーザーがフォーム入力
    ↓
「生成する」ボタンをクリック
    ↓
app.py が write_blog() などを呼ぶ
    ↓
tools/ が日本語プロンプトを組み立て
    ↓
gemini_client.py が Gemini API に送信
    ↓
生成テキスト（str）が返る
    ↓
show_result() で画面表示 + ダウンロードボタン
```

セッション状態・DB・認証はありません。**完全にステートレス** な設計です。ページをリロードすれば入力は消えますが、コードはシンプルに保てます。

---

## この設計から学べること

### 1. 関心の分離

| ファイル | 責務 |
|---|---|
| `app.py` | 画面・入力・表示 |
| `tools/*.py` | プロンプト設計 |
| `gemini_client.py` | API 通信 |

### 2. 辞書 + `if/elif` によるルーティング

フレームワークなしで複数画面を切り替える、最小構成のパターンです。

### 3. 共通関数での DRY

`show_result()` や各ツールの `try/except` パターンで、同じコードの繰り返しを避けています。

### 4. プロンプトをコードに埋め込む

出力形式の指示（Markdown 形式で、など）もプロンプト内に書いています。後処理ではなく、AI への指示で形式をコントロールするアプローチです。

---

## まとめ

`app.py` は **「辞書でツールを管理 → サイドバーで選択 → `if/elif` で画面切り替え → ツール関数を呼んで結果を表示」** という流れのファイルです。

複雑に見えても、パターンは 1 つだけ繰り返されています。新しい AI ツールを足したいときも、この型に沿って 3 ステップ追加すれば動きます。
