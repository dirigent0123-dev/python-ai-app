import json
from datetime import date, datetime
from pathlib import Path
import streamlit as st
from tools.blog_writer import write_blog
from tools.email_reply import write_email_reply
from tools.summarizer import summarize_text
from tools.proofreader import proofread_text
from tools.social_post import create_social_post
from tools.tone_converter import convert_tone

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── テーマ定義 ──────────────────────────────────────────────
THEME_CONFIG = {
    "carp": {
        "label": "⚾ カープ",
        "sidebar_icon": "⚾",
        "sidebar_title": "AI ライティングツール",
        "sidebar_sub": "広島東洋カープ応援中！",
        "css": """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');
        html, body, .stApp, p, label, .stMarkdown, .stTextArea textarea,
        .stTextInput input, .stSelectbox, .stButton button, .stRadio,
        .stCheckbox, .element-container {
            font-family: 'Noto Sans JP', sans-serif !important;
        }
        .stApp { background-color: #fafafa; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #C8102E 0%, #8B0000 100%) !important;
        }
        [data-testid="stSidebar"] * { color: #ffffff !important; }
        [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.3) !important; }
        .main-title {
            font-size: 2rem; font-weight: 900; color: #C8102E;
            margin-bottom: 0.25rem;
            border-left: 6px solid #C8102E; padding-left: 0.6rem;
        }
        .sub-title {
            font-size: 0.95rem; color: #6b7280;
            margin-bottom: 1.5rem; padding-left: 0.8rem;
        }
        .stButton > button {
            background-color: #C8102E !important; color: white !important;
            border: none !important; border-radius: 6px !important;
            font-weight: 700 !important;
        }
        .stButton > button:hover { background-color: #8B0000 !important; }
        .stTextArea textarea, .stTextInput input {
            border: 1.5px solid #e8b4b8 !important; border-radius: 8px !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #C8102E !important;
            box-shadow: 0 0 0 2px rgba(200,16,46,0.15) !important;
        }
        hr { border-color: #f5c6cb !important; }
        [data-testid="stDownloadButton"] button {
            border: 2px solid #C8102E !important; color: #C8102E !important;
            background: white !important; font-weight: 700 !important;
            border-radius: 6px !important;
        }
        [data-testid="stDownloadButton"] button:hover { background: #fff0f0 !important; }
        </style>
        """,
    },
    "koupen": {
        "label": "🐧 コウペンちゃん",
        "sidebar_icon": "🐧",
        "sidebar_title": "AI ライティングツール",
        "sidebar_sub": "えらい！すごい！できてる！🍀",
        "css": """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700&display=swap');
        html, body, .stApp, p, label, .stMarkdown, .stTextArea textarea,
        .stTextInput input, .stSelectbox, .stButton button, .stRadio,
        .stCheckbox, .element-container {
            font-family: 'M PLUS Rounded 1c', sans-serif !important;
        }
        .stApp {
            background: linear-gradient(160deg, #fff0f8 0%, #e8f6ff 50%, #f0fff6 100%) !important;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ff8fab 0%, #a8d8ea 100%) !important;
        }
        [data-testid="stSidebar"] * { color: #3d2040 !important; }
        [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.5) !important; }
        .main-title {
            font-size: 2rem; font-weight: 700; color: #d45f82;
            margin-bottom: 0.25rem;
            border-left: 6px solid #ffb3c6; padding-left: 0.6rem;
        }
        .sub-title {
            font-size: 0.95rem; color: #888;
            margin-bottom: 1.5rem; padding-left: 0.8rem;
        }
        .stButton > button {
            background: linear-gradient(135deg, #ff8fab, #ffb3c6) !important;
            color: white !important; border: none !important;
            border-radius: 25px !important; font-weight: 700 !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #ff6b8a, #ff8fab) !important;
        }
        .stTextArea textarea, .stTextInput input {
            border: 2px solid #ffb3c6 !important;
            border-radius: 14px !important; background: #fff8fb !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #ff8fab !important;
            box-shadow: 0 0 0 2px rgba(255,143,171,0.2) !important;
        }
        hr { border-color: #ffd6e4 !important; }
        [data-testid="stDownloadButton"] button {
            border: 2px solid #ff8fab !important; color: #d45f82 !important;
            background: white !important; font-weight: 700 !important;
            border-radius: 20px !important;
        }
        </style>
        """,
    },
    "orchestra": {
        "label": "🎻 オーケストラ",
        "sidebar_icon": "🎻",
        "sidebar_title": "AI ライティングツール",
        "sidebar_sub": "♩ Powered by Gemini 2.0 Flash",
        "css": """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');
        html, body, .stApp, p, label, .stMarkdown, .stTextArea textarea,
        .stTextInput input, .stSelectbox, .stButton button, .stRadio,
        .stCheckbox, .element-container {
            font-family: 'Noto Serif JP', serif !important;
        }
        .stApp { background-color: #FAFAF5; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E1E2E 0%, #0D0D1A 100%) !important;
        }
        [data-testid="stSidebar"] * { color: #E8DCC8 !important; }
        [data-testid="stSidebar"] hr { border-color: rgba(201,168,76,0.4) !important; }
        .main-title {
            font-size: 2rem; font-weight: 700; color: #1E1E2E;
            margin-bottom: 0.25rem;
            border-left: 6px solid #C9A84C; padding-left: 0.6rem;
        }
        .sub-title {
            font-size: 0.95rem; color: #7a7060;
            margin-bottom: 1.5rem; padding-left: 0.8rem;
        }
        .stButton > button {
            background-color: #1E1E2E !important; color: #C9A84C !important;
            border: 1.5px solid #C9A84C !important;
            border-radius: 4px !important; font-weight: 700 !important;
        }
        .stButton > button:hover {
            background-color: #C9A84C !important; color: #1E1E2E !important;
        }
        .stTextArea textarea, .stTextInput input {
            border: 1.5px solid #C9A84C !important; border-radius: 4px !important;
            background: #FDFCF7 !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #a8893a !important;
            box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
        }
        hr { border-color: #e8d9a0 !important; }
        [data-testid="stDownloadButton"] button {
            border: 1.5px solid #1E1E2E !important; color: #1E1E2E !important;
            background: #FAFAF5 !important; font-weight: 700 !important;
            border-radius: 4px !important;
        }
        [data-testid="stDownloadButton"] button:hover { background: #f0ede0 !important; }
        </style>
        """,
    },
}

# ── テーマ初期化 ──────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "carp"

theme = st.session_state.theme
cfg = THEME_CONFIG[theme]

# テーマCSS適用
st.markdown(cfg["css"], unsafe_allow_html=True)

TOOLS = {
    "📝 ブログ記事作成": "blog",
    "📧 メール返信文作成": "email",
    "📋 文章要約": "summarize",
    "🔍 文章校正・改善": "proofread",
    "📱 SNS投稿文作成": "social",
    "🔄 文体変換": "tone",
    "📅 スケジュール管理": "calendar",
}

SCHEDULE_FILE = Path(__file__).parent / "schedule.json"

def load_schedule():
    return json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))

def save_schedule(events):
    SCHEDULE_FILE.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")

# ── サイドバー ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:0.5rem 0 0.2rem;'>
        <div style='font-size:2.2rem;'>{cfg["sidebar_icon"]}</div>
        <div style='font-size:1.1rem; font-weight:900; letter-spacing:1px;'>{cfg["sidebar_title"]}</div>
        <div style='font-size:0.75rem; opacity:0.8; margin-top:2px;'>{cfg["sidebar_sub"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # テーマ切り替え
    st.markdown("<div style='font-size:0.8rem; opacity:0.8; margin-bottom:4px;'>テーマ</div>", unsafe_allow_html=True)
    theme_keys = ["carp", "koupen", "orchestra"]
    theme_labels = {"carp": "⚾ カープ", "koupen": "🐧 コウペン", "orchestra": "🎻 オーケストラ"}
    selected_theme = st.radio(
        "テーマ選択",
        theme_keys,
        format_func=lambda x: theme_labels[x],
        index=theme_keys.index(st.session_state.theme),
        label_visibility="collapsed",
    )
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.markdown("---")
    st.markdown("**ツールを選んでください**")
    selected_label = st.radio(
        "ツール選択",
        list(TOOLS.keys()),
        label_visibility="collapsed",
    )

tool = TOOLS[selected_label]

st.markdown(f'<div class="main-title">{selected_label}</div>', unsafe_allow_html=True)


def show_result(result: str, copy_label: str = "結果"):
    st.markdown("---")
    st.subheader("生成結果")
    if tool == "blog":
        st.markdown(result)
    else:
        st.text_area(copy_label, value=result, height=350, key="output_area")
    st.download_button(
        label="テキストをダウンロード",
        data=result,
        file_name="output.txt",
        mime="text/plain",
    )


# ── ブログ記事作成 ──────────────────────────────────────────────
if tool == "blog":
    st.markdown('<div class="sub-title">テーマや条件を入力してブログ記事を生成します</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("記事のテーマ *", placeholder="例: 在宅ワークの生産性を上げる5つの方法")
        keywords = st.text_input("含めたいキーワード（任意）", placeholder="例: ポモドーロ、集中力、環境づくり")
        target_audience = st.text_input("ターゲット読者", placeholder="例: 在宅ワーク初心者の20〜30代会社員")
    with col2:
        tone = st.selectbox("文体・トーン", ["親しみやすい", "専門的", "エネルギッシュ", "落ち着いた", "ユーモラス"])
        length = st.selectbox("文字数", ["短め（500字）", "普通（1000字）", "長め（2000字）"])

    if st.button("記事を生成する", use_container_width=True):
        if not topic.strip():
            st.warning("テーマを入力してください。")
        else:
            with st.spinner("記事を生成中..."):
                try:
                    result = write_blog(topic, target_audience, tone, length, keywords)
                    show_result(result, "ブログ記事")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ── メール返信文作成 ──────────────────────────────────────────────
elif tool == "email":
    st.markdown('<div class="sub-title">受信したメールと返信の意図を入力すると、返信文を生成します</div>', unsafe_allow_html=True)

    original_email = st.text_area("受信メール本文 *", height=180, placeholder="返信したいメールの本文をここに貼り付けてください")
    reply_intent = st.text_area("返信の意図・内容 *", height=100, placeholder="例: 来週水曜日の会議を承諾する。資料は事前に共有してほしいと伝える。")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("文体・トーン", ["丁寧・ビジネス", "フレンドリー", "簡潔", "かしこまった"])
    with col2:
        sender_name = st.text_input("自分の名前（任意）", placeholder="例: 山田 太郎")

    if st.button("返信文を生成する", use_container_width=True):
        if not original_email.strip() or not reply_intent.strip():
            st.warning("受信メールと返信の意図を入力してください。")
        else:
            with st.spinner("返信文を生成中..."):
                try:
                    result = write_email_reply(original_email, reply_intent, tone, sender_name)
                    show_result(result, "メール返信文")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ── 文章要約 ──────────────────────────────────────────────
elif tool == "summarize":
    st.markdown('<div class="sub-title">テキストを貼り付けると、指定したスタイルで要約します</div>', unsafe_allow_html=True)

    text = st.text_area("要約したいテキスト *", height=250, placeholder="要約したい文章をここに貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("要約スタイル", ["要点まとめ", "一文要約", "段落要約", "キーワード抽出"])
    with col2:
        length = st.selectbox("要約の長さ", ["短め", "普通", "詳しめ"])

    if st.button("要約する", use_container_width=True):
        if not text.strip():
            st.warning("テキストを入力してください。")
        else:
            with st.spinner("要約中..."):
                try:
                    result = summarize_text(text, style, length)
                    show_result(result, "要約結果")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ── 文章校正・改善 ──────────────────────────────────────────────
elif tool == "proofread":
    st.markdown('<div class="sub-title">文章の誤字・表現・読みやすさを改善します</div>', unsafe_allow_html=True)

    text = st.text_area("校正したいテキスト *", height=220, placeholder="校正・改善したい文章をここに貼り付けてください")

    st.markdown("**重点的に確認する項目**")
    col1, col2, col3 = st.columns(3)
    with col1:
        c1 = st.checkbox("誤字・脱字", value=True)
        c2 = st.checkbox("文法・句読点")
    with col2:
        c3 = st.checkbox("表現の自然さ", value=True)
        c4 = st.checkbox("文章の流れ・構成")
    with col3:
        c5 = st.checkbox("語彙の適切さ")
        c6 = st.checkbox("読みやすさ・わかりやすさ", value=True)

    focus = [
        label for checked, label in [
            (c1, "誤字・脱字"), (c2, "文法・句読点"), (c3, "表現の自然さ"),
            (c4, "文章の流れ・構成"), (c5, "語彙の適切さ"), (c6, "読みやすさ・わかりやすさ"),
        ] if checked
    ]

    if st.button("校正する", use_container_width=True):
        if not text.strip():
            st.warning("テキストを入力してください。")
        elif not focus:
            st.warning("確認する項目を1つ以上選択してください。")
        else:
            with st.spinner("校正中..."):
                try:
                    result = proofread_text(text, focus)
                    show_result(result, "校正結果")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ── SNS投稿文作成 ──────────────────────────────────────────────
elif tool == "social":
    st.markdown('<div class="sub-title">SNSプラットフォームに合わせた投稿文を生成します</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_area("投稿のテーマ・伝えたいこと *", height=120, placeholder="例: 新しいカフェを見つけた。ラテアートが素敵で、落ち着いた空間だった")
    with col2:
        platform = st.selectbox("プラットフォーム", ["X (Twitter)", "Instagram", "LinkedIn", "Facebook", "Threads"])
        tone = st.selectbox("トーン", ["自然体", "テンション高め", "落ち着いた", "プロフェッショナル", "ユーモラス"])
        include_hashtags = st.checkbox("ハッシュタグを追加", value=True)

    if st.button("投稿文を生成する", use_container_width=True):
        if not topic.strip():
            st.warning("テーマを入力してください。")
        else:
            with st.spinner("投稿文を生成中..."):
                try:
                    result = create_social_post(platform, topic, tone, include_hashtags)
                    show_result(result, "投稿文")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ── 文体変換 ──────────────────────────────────────────────
elif tool == "tone":
    st.markdown('<div class="sub-title">文章の意味を保ちながら、指定した文体に変換します</div>', unsafe_allow_html=True)

    text = st.text_area("変換したいテキスト *", height=200, placeholder="文体を変換したい文章をここに貼り付けてください")

    target_tone = st.selectbox(
        "変換先の文体",
        ["丁寧・敬語", "フォーマル・ビジネス", "カジュアル・友達口調", "やわらかく親しみやすい", "力強く説得力のある", "シンプル・わかりやすい", "コウペンちゃん風"],
    )

    if target_tone == "コウペンちゃん風":
        st.markdown("""
        <div style="text-align:center; font-size:2rem; letter-spacing:4px; margin:0.5rem 0;">
            🍀🐧🍀🐧🍀🐧🍀
        </div>
        <div style="text-align:center; background:linear-gradient(135deg,#ffb3c6,#a8d8ea);
            border-radius:18px; padding:0.9rem 1rem; margin-bottom:1rem;">
            <span style="font-size:1.05rem; color:white; font-weight:700;">
                なんでもコウペンちゃん風に変換するよ〜！えらい！🐧🍀
            </span>
        </div>
        """, unsafe_allow_html=True)

    if st.button("文体を変換する", use_container_width=True):
        if not text.strip():
            st.warning("テキストを入力してください。")
        else:
            with st.spinner("変換中..."):
                try:
                    result = convert_tone(text, target_tone)
                    show_result(result, "変換結果")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ── スケジュール管理 ──────────────────────────────────────────────
elif tool == "calendar":
    st.markdown('<div class="sub-title">予定を登録・確認できます。データはローカルに保存されます。</div>', unsafe_allow_html=True)

    events = load_schedule()

    st.subheader("＋ 予定を追加する")
    col1, col2 = st.columns(2)
    with col1:
        new_title = st.text_input("タイトル *", placeholder="例: チームミーティング")
        new_date = st.date_input("日付 *", value=date.today())
    with col2:
        new_time = st.text_input("時間（任意）", placeholder="例: 14:00")
        new_note = st.text_input("メモ（任意）", placeholder="例: Zoom URLを確認する")

    if st.button("予定を保存する", use_container_width=True):
        if not new_title.strip():
            st.warning("タイトルを入力してください。")
        else:
            events.append({
                "id": datetime.now().isoformat(),
                "title": new_title.strip(),
                "date": new_date.isoformat(),
                "time": new_time.strip(),
                "note": new_note.strip(),
            })
            events.sort(key=lambda e: e["date"])
            save_schedule(events)
            st.success("予定を保存しました。")
            st.rerun()

    st.markdown("---")
    st.subheader("予定一覧")

    if not events:
        st.info("予定はまだありません。")
    else:
        today_str = date.today().isoformat()
        upcoming = [e for e in events if e["date"] >= today_str]
        past = [e for e in events if e["date"] < today_str]

        def render_events(event_list):
            for e in event_list:
                col_info, col_del = st.columns([5, 1])
                with col_info:
                    time_str = f" {e['time']}" if e["time"] else ""
                    note_str = f"　{e['note']}" if e["note"] else ""
                    st.markdown(f"**{e['date']}{time_str}　{e['title']}**{note_str}")
                with col_del:
                    if st.button("削除", key=f"del_{e['id']}"):
                        events.remove(e)
                        save_schedule(events)
                        st.rerun()

        if upcoming:
            st.markdown("**今日以降の予定**")
            render_events(upcoming)
        if past:
            with st.expander("過去の予定"):
                render_events(past)
