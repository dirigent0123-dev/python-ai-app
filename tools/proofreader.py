from .gemini_client import generate


def proofread_text(text: str, focus: list[str]) -> str:
    focus_str = "、".join(focus) if focus else "全般的な改善"

    prompt = f"""あなたはプロの校正者・編集者です。以下の文章を校正・改善してください。

## 校正の重点項目
{focus_str}

## 対象テキスト
{text}

## 出力形式
以下の形式で出力してください：

### 改善後の文章
[校正・改善した文章全文]

### 修正ポイント
[変更した箇所と理由を箇条書きで3〜7点]"""

    return generate(prompt)
