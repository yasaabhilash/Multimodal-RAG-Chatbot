from langchain_ollama import OllamaLLM


class AnswerService:

    def __init__(self):

        self.llm = OllamaLLM(
            model="qwen2.5:7b"
        )

    def generate_answer(
        self,
        question,
        context,
        history=None
    ):

        if history is None:
            history = []

        conversation_history = ""

        for msg in history:

            conversation_history += (
                f"{msg['sender']}: {msg['text']}\n"
            )

        prompt = f"""
You are an enterprise RAG assistant.

Rules:

1. Answer ONLY using the supplied context.

2. Never invent information.

3. If the answer is not found in the context, reply EXACTLY:

I could not find that information in the documents.

4. Use conversation history only for understanding follow-up questions.

5. Never mention filenames, document names or page numbers in your answer.

6. If multiple documents contain relevant information,
combine them into one complete answer.

Context:
{context}

Conversation History:
{conversation_history}

Current Question:
{question}

Answer:
"""

        print("\nCalling Qwen...")

        answer = self.llm.invoke(prompt)

        print("LLM Finished.")

        return answer.strip()