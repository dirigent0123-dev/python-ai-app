from .gemini_client import generate


def create_social_post(
    platform: str,
    topic: str,
    tone: str,
    include_hashtags: bool,
) -> str:
    platform_rules = {
        "X (Twitter)": "140字以内（日本語）で簡潔に。インパクトのある書き出しで。",
        "Instagram": "改行を活用した読みやすい文章で。感情に訴える表現を使って。",
        "LinkedIn": "プロフェッショナルなトーンで。学びや価値提供を意識して。",
        "Facebook": "親しみやすく詳しめに書いて。エンゲージメントを促す問いかけを含めて。",
        "Threads": "会話的なトーンで自然な文体で。",
    }

    rule = platform_rules.get(platform, "プラットフォームに合った文章で。")
    hashtag_instruction = "最後に関連するハッシュタグを3〜5個追加してください。" if include_hashtags else "ハッシュタグは不要です。"

    prompt = f"""あなたはSNSマーケティングの専門家です。以下の条件で{platform}の投稿文を作成してください。

## 条件
- プラットフォーム: {platform}
- テーマ・内容: {topic}
- 文体・トーン: {tone}
- プラットフォームルール: {rule}
- ハッシュタグ: {hashtag_instruction}

投稿文のみを出力してください。前置きや説明は不要です。"""

    return generate(prompt)
