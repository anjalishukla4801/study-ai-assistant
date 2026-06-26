from groq import Groq
from rag.prompts import SYSTEM_PROMPT

class GroqLLM:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Groq API Key is missing. Check your settings/environment variables.")
        try:
            self.client = Groq(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Groq client: {str(e)}")

    def generate_answer(self, query: str, retrieved_chunks: list, chat_history: list) -> str:
        """
        Generates a RAG-based answer using the retrieved chunks and chat history.
        Automatically appends verified source citations if information is found.
        """
        if not retrieved_chunks:
            return "I couldn't find this information in the uploaded documents."

        # 1. Format retrieved chunks as system context
        context_lines = []
        sources = []
        for item in retrieved_chunks:
            meta = item["metadata"]
            text = item["text"]
            
            source_detail = {
                "filename": meta.get("filename", "unknown"),
                "page_number": meta.get("page_number", "?")
            }
            if source_detail not in sources:
                sources.append(source_detail)
                
            context_lines.append(
                f"[Source: {source_detail['filename']}, Page {source_detail['page_number']}]\n"
                f"Content: {text}\n"
                f"---"
            )
            
        context_str = "\n".join(context_lines)

        # 2. Build Groq chat completion messages
        messages = [
            {
                "role": "system", 
                "content": f"{SYSTEM_PROMPT}\n\nRetrieved Context:\n{context_str}\n\nAlways cite the filename and Page in your response."
            }
        ]
        
        # Add limited chat history
        messages.extend(chat_history)
        
        # Add current user query
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.3,
                max_tokens=600
            )
            
            answer = completion.choices[0].message.content.strip()
            
            # Normalize fallback check
            fallback_msg = "I couldn't find this information in the uploaded documents."
            if fallback_msg.lower() in answer.lower():
                return fallback_msg
                
            # If LLM didn't format source citations explicitly, append the correct Python metadata
            if "Source:" not in answer and "source:" not in answer.lower():
                citation_lines = ["", "Source:"]
                for src in sources:
                    citation_lines.append(f"{src['filename']}")
                    citation_lines.append(f"Page {src['page_number']}")
                answer += "\n" + "\n".join(citation_lines)
                
            return answer
        except Exception as e:
            raise RuntimeError(f"Groq API completion call failed: {str(e)}")
