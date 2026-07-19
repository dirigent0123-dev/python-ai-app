from .gemini_client import generate


def write_blog(
    topic: str,
    target_audience: str,
    tone: str,
    length: str,
    keywords: str,
) -> str:
    length_map = {"短め（500字）": "500字程度", "普通（1000字）": "1000字程度", "長め（2000字）": "2000字程度"}
    length_str = length_map.get(length, "1000字程度")

    keywords_str = f"\n- キーワード: {keywords}" if keywords.strip() else ""

    prompt = f"""あなたはプロのブログライターです。以下の条件に従ってブログ記事を執筆してください。

## 条件
- テーマ: {topic}
- ターゲット読者: {target_audience}
- 文体・トーン: {tone}
- 文字数: {length_str}{keywords_str}

## 出力形式
Markdown形式で出力してください。以下の構成を含めてください：
- キャッチーなタイトル（# で始める）
- リード文（読者を引き込む導入）
- 本文（## で章立て、具体例や根拠を含める）
- まとめ

記事本文のみを出力し、余計な説明は不要です。"""

    return generate(prompt)
