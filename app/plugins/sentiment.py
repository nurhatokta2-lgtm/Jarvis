from app.plugins.base import Plugin


class SentimentPlugin(Plugin):
    name = "sentiment"

    async def run(self, user_input: str) -> dict:
        positive_words = {"great", "awesome", "love", "excellent", "happy", "good"}
        negative_words = {"bad", "hate", "awful", "terrible", "sad", "angry"}
        tokens = {token.strip('.,!?').lower() for token in user_input.split()}
        score = len(tokens & positive_words) - len(tokens & negative_words)
        mood = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        return {"score": score, "mood": mood}
