import os
import asyncio
from generic_rag.config import ProviderConfig
from generic_rag.core.schemas import LLMRequest, ChatMessage
from generic_rag.llm.providers.ollama import OllamaProvider
from generic_rag.llm.dispatcher import DefaultLLMDispatcher

async def main():
    print("=== Ollama Chat Example ===")
    base_url = os.getenv("GENERIC_RAG_BASE_URL", "http://localhost:11434")
    model = os.getenv("GENERIC_RAG_MODEL", "llama3")
    
    print(f"Using base_url: {base_url}")
    print(f"Using model: {model}")
    print("Make sure you have Ollama running locally and the model is pulled ('ollama run llama3').\n")

    config = ProviderConfig(
        name="ollama-local",
        base_url=base_url,
        default_model=model,
        max_retries=2
    )
    provider = OllamaProvider(config)
    
    dispatcher = DefaultLLMDispatcher()
    dispatcher.register_provider(provider)

    request = LLMRequest(
        provider="ollama-local",
        model=model,
        messages=[
            ChatMessage(role="system", content="You are a helpful and concise assistant."),
            ChatMessage(role="user", content="Explain the concept of Retrieval-Augmented Generation in one short paragraph.")
        ],
        temperature=0.7,
        max_tokens=200
    )

    try:
        response = await dispatcher.dispatch(request)
        print("Response:")
        print(response.text)
        print(f"\nTokens used: {response.usage.total_tokens}")
    except Exception as e:
        print(f"Error during request: {e}")

if __name__ == "__main__":
    asyncio.run(main())
