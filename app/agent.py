from app.services.together_ai import query_together_ai
from app.services.tools import fetch_crypto_price, translate
from app.services.cache import find_similar_query, cache_response


class CryptoAgent:
    def __init__(self):
        self.conversation_history = []

    def process_message(self, user_message: str) -> str:
        """
        1. Check if a similar query exists in cache.
        2. If found, return cached response.
        3. Otherwise, query LLaMA and cache the response.
        """
        cached_response = find_similar_query(user_message)
        if cached_response:
            print("returning from cache")
            return cached_response

        ai_response = query_together_ai(user_message)
        action = ai_response.get("action")

        if action == "fetch_price":
            coin = ai_response.get("coin", "bitcoin")
            result = fetch_crypto_price(coin)
        elif action == "translate":
            text = ai_response.get("text", "")
            language = ai_response.get("language", "english")
            result = translate(text, language)
        else:
            result = ai_response.get(
                "answer", "I can only provide cryptocurrency information."
            )

        cache_response(user_message, result)

        self.conversation_history.append(("user", user_message))
        self.conversation_history.append(("assistant", result))

        return result
