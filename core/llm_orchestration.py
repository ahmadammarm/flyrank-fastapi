import google.generativeai as genai
import os

api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
genai.configure(api_key=api_key)

def generate_rag_response(query: str, context_chunks: list[str], chat_history: list[dict]) -> str:
    context_text = "\n\n".join(context_chunks)
    
    system_prompt = f"""You are a helpful Civic and Tenant Rights AI Assistant.
    Answer the user's question based strictly on the following context.
    If the context does not contain the answer, say "I don't have enough information to answer that."
    
    Context:
    {context_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
        
        # Convert custom history format to Gemini format if needed, but for simplicity we just pass the prompt
        # In a real scenario, we pass history properly
        history = [{"role": msg["role"], "parts": [msg["content"]]} for msg in chat_history]
        
        chat = model.start_chat(history=history)
        response = chat.send_message(query)
        return response.text
    except Exception as e:
        return f"AI Response Simulated (Missing/Invalid API Key). Found context: {context_text[:100]}..."
