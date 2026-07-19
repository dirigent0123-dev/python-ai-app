from .gemini_client import generate


def convert_tone(text: str, target_tone: str) -> str:
    tone_descriptions = {
        "丁寧・敬語": "丁寧語・敬語を使った礼儀正しい文体",
        "フォーマル・ビジネス": "ビジネスシーンに適したフォーマルな文体",
        "カジュアル・友達口調": "友人に話しかけるような親しみやすいカジュアルな文体",
        "やわらかく親しみやすい": "温かみがあり読みやすい、やさしい文体",
        "力強く説得力のある": "自信に満ちた、読者を動かす力強い文体",
        "シンプル・わかりやすい": "専門用語を避けた、誰でも理解できるシンプルな文体",
    }

    description = tone_descriptions.get(target_tone, target_tone)

    prompt = f"""あなたは文体変換の専門家です。以下の文章を指定した文体に変換してください。

## 変換先の文体
{description}

## 元の文章
{text}

## 出力形式
変換後の文章のみを出力してください。前置きや説明は不要です。
元の意味・内容は保ちながら、文体のみを変換してください。"""

    return generate(prompt)
