from .gemini_client import generate


def summarize_text(
    text: str,
    style: str,
    length: str,
) -> str:
    style_map = {
        "要点まとめ": "重要なポイントを箇条書きでまとめてください。",
        "一文要約": "全体を1〜2文で簡潔に要約してください。",
        "段落要約": "各段落・セクションごとに要約してください。",
        "キーワード抽出": "重要なキーワードと概念を抽出・説明してください。",
    }
    length_map = {"短め": "できるだけ短く", "普通": "適切な長さで", "詳しめ": "詳しく"}

    style_instruction = style_map.get(style, style_map["要点まとめ"])
    length_instruction = length_map.get(length, "適切な長さで")

    prompt = f"""あなたは優秀な文章要約の専門家です。以下の文章を{length_instruction}{style_instruction}

## 対象テキスト
{text}

要約結果のみを出力してください。前置きや説明は不要です。"""

    return generate(prompt)
