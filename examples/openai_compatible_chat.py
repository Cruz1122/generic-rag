import os
import asyncio
from pydantic import SecretStr
from generic_rag.config import ProviderConfig
from generic_rag.core.schemas import LLMRequest, ChatMessage
from generic_rag.llm.providers.openai_compatible import OpenAICompatibleProvider
from generic_rag.llm.dispatcher import DefaultLLMDispatcher

async def main():
    print("=== OpenAI-Compatible Chat Example ===")
    
    # Can be OpenAI, Groq, LM Studio, vLLM, etc.
    base_url = os.getenv("GENERIC_RAG_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("GENERIC_RAG_MODEL", "gpt-3.5-turbo")
    api_key = os.getenv("GENERIC_RAG_API_KEY")
    
    print(f"Using base_url: {base_url}")
    print(f"Using model: {model}")
    
    if not api_key and "openai.com" in base_url:
        print("Warning: GENERIC_RAG_API_KEY is not set. OpenAI API calls will likely fail.")
        
    config = ProviderConfig(
        name="openai-compatible",
        base_url=base_url,
        default_model=model,
        api_key=SecretStr(api_key) if api_key else None,
        max_retries=2
    )
    provider = OpenAICompatibleProvider(config)
    
    dispatcher = DefaultLLMDispatcher()
    dispatcher.register_provider(provider)

    # Example using Structured Output via JSON Schema
    extraction_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "age"],
        "additionalProperties": False
    }

    request = LLMRequest(
        provider="openai-compatible",
        model=model,
        messages=[
            ChatMessage(role="system", content="You are a helpful data extraction assistant. Always output JSON."),
            ChatMessage(
                role="user",
                content=(
                    "Given the following text, extract for every mentioned person their name and age. "
                    "If the age is not explicitly given, infer it if possible, otherwise set it as null. "
                    "The text may include multiple people with varying data formats and extraneous information.\n\n"
                    "Text:\n"
                    " - John Doe is 30 years old and lives in Boston.\n"
                    " - Jane Smith, aged 27, is a software engineer at Acme Corp.\n"
                    " - Mike was born in 1990 and Anne just started college this year (she is 19)."
                )
            )
       
        ],
        json_schema=extraction_schema,
        response_format="json_object",
        temperature=0.0
    )

    try:
        response = await dispatcher.dispatch(request)
        print("Response (JSON expected):")
        print(response.text)
        print(f"\nTokens used: {response.usage.total_tokens}")
    except Exception as e:
        print(f"Error during request: {e}")

if __name__ == "__main__":
    asyncio.run(main())
