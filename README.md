# Crypto AI Agent

A FastAPI-based AI agent that provides **real-time cryptocurrency prices** and **answers general crypto-related questions** using **Together AI's LLaMA 3.1 8B model**. It also supports **language translation** while keeping system responses in English.

---

## Setup Instructions
1. **Clone the Repository**  
   - Download or clone the GitHub repository to your local machine.

2. **Set Up Environment Variables**  
   - Copy the provided `.env.example` file to `.env`, then add your actual API keys and host configurations.

3. **Run with Docker Compose**  
   - In the root directory, run:
     ```
     docker-compose up -d --build
     ```
   - This starts FastAPI, Redis, and Qdrant containers.

4. **Test the API**  
   - Health Check:  
     ```
     GET http://localhost:8000/
     ```
   - Chat Endpoint:  
     ```
     POST http://localhost:8000/api/chat
     Body: { "user_message": "What is the price of Bitcoin?" }
     ```

---

## Prompt Engineering Approach
- **System Prompt** instructs the AI agent to:
  - Use `fetch_price(coin)` for crypto price requests.
  - Use `translate(text, language)` when a translation is requested.
  - Answer crypto-related questions directly.
  - Refuse off-topic queries.
  - Maintain context and always return JSON for tool calls.

- **Conversation Flow**:
  - The AI checks if a user query is about crypto prices, translation, or general crypto knowledge.
  - Off-topic queries result in a polite refusal.

---

## Example Conversations

1. **Price Query**  
   **User**: "What's the price of Bitcoin?"  
   **Assistant**:  
   ```json
   {
     "action": "fetch_price",
     "coin": "bitcoin"
   }
   ```
## General Crypto Knowledge
**User:** "What is Ethereum?"  
**Assistant:**  
Ethereum is a decentralized blockchain platform that enables smart contracts and decentralized applications, powered by Ether (ETH).

---

## Translation
  **User:** "Translate 'What is Bitcoin?' to Spanish."  
  **Assistant:**  
  ```json
  {
    "action": "translate",
    "text": "What is Bitcoin?",
    "language": "Spanish"
  }
  ```

## Off-Topic Query
**User:** "Who won the football match?"  
**Assistant:**  
"I'm designed to answer cryptocurrency-related questions only."

---

## Assumptions and Limitations

### Assumptions
- Users mostly ask crypto-related queries (prices, definitions, or translations).
- Translation is a simple placeholder (can be extended with a real translation API).
- The model reliably returns JSON for tool calls when asked for price or translation.

### Limitations
- **No Non-Crypto Topics:** Off-topic questions are politely declined.
- **Dependent on External APIs:** If the crypto API is down or rate-limited, price fetching may fail.
- **Contextual Memory is basic:** Long-running conversations may require more advanced memory strategies.
