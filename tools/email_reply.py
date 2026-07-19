from .gemini_client import generate


def write_email_reply(
    original_email: str,
    reply_intent: str,
    tone: str,
    sender_name: str,
) -> str:
    sender_str = f"\n- 差出人名: {sender_name}" if sender_name.strip() else ""

    prompt = f"""あなたはビジネスメールの専門家です。以下の受信メールに対する返信文を作成してください。

## 受信メール
{original_email}

## 返信の条件
- 返信の意図・内容: {reply_intent}
- 文体・トーン: {tone}{sender_str}

## 出力形式
件名と本文を含む完全なメール文を出力してください。
- 件名: Re: [適切な件名]
- 宛名
- 本文
- 署名（[お名前]と記載）

メール文のみを出力し、余計な説明は不要です。"""

    return generate(prompt)
