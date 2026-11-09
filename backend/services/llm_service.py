from langchain_ollama import OllamaLLM


class LLMService:

    _llm = None

    @classmethod
    def get_llm(cls):

        if cls._llm is None:

            print("Loading LLM...")

            cls._llm = OllamaLLM(
                model="qwen2.5:7b"
            )

        return cls._llm