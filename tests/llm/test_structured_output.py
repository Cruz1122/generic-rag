import pytest
from generic_rag.core.schemas import LLMRequest, ChatMessage
from generic_rag.llm.providers.openai_compatible import OpenAICompatibleProvider
from generic_rag.llm.providers.ollama import OllamaProvider
from generic_rag.llm.providers.gemini import GeminiProvider
from generic_rag.config import ProviderConfig

def test_openai_structured_output_payload():
    config = ProviderConfig(name="test", default_model="test-model")
    provider = OpenAICompatibleProvider(config)
    
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    req = LLMRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
        response_format="json_object",
        json_schema=schema
    )
    
    payload = provider._prepare_payload(req)
    assert payload["response_format"]["type"] == "json_schema"
    assert payload["response_format"]["json_schema"]["schema"] == schema

def test_ollama_structured_output_payload():
    config = ProviderConfig(name="test", default_model="test-model")
    provider = OllamaProvider(config)
    
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    req = LLMRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
        response_format="json_object",
        json_schema=schema
    )
    
    payload = provider._prepare_payload(req)
    assert payload["format"] == schema

def test_gemini_structured_output_payload():
    config = ProviderConfig(name="test", default_model="test-model", api_key="test")
    provider = GeminiProvider(config)
    
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    req = LLMRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
        response_format="json_object",
        json_schema=schema
    )
    
    payload = provider._prepare_payload(req)
    assert payload["generationConfig"]["responseMimeType"] == "application/json"
    assert payload["generationConfig"]["responseSchema"] == schema
