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

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .tool-card {
        background: #f9fafb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #6366f1;
    }
    .stButton > button {
        background-color: #6366f1;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #4f46e5;
    }
</style>
""", unsafe_allow_html=True)

TOOLS = {
    "📝 ブログ記事作成": "blog",
    "📧 メール返信文作成": "email",
    "📋 文章要約": "summarize",
    "🔍 文章校正・改善": "proofread",
    "📱 SNS投稿文作成": "social",
    "🔄 文体変換": "tone",
}

with st.sidebar:
    st.markdown("## ✍️ AI ライティングツール")
    st.markdown("---")
    st.markdown("**ツールを選んでください**")
    selected_label = st.radio(
        "ツール選択",
        list(TOOLS.keys()),
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#9ca3af'>Powered by Gemini 2.0 Flash</small>",
        unsafe_allow_html=True,
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
        ["丁寧・敬語", "フォーマル・ビジネス", "カジュアル・友達口調", "やわらかく親しみやすい", "力強く説得力のある", "シンプル・わかりやすい"],
    )

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
