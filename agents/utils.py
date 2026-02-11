from enum import Enum
from langchain.chat_models import init_chat_model, BaseChatModel
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from enums import *
from langchain_core.messages import (
    BaseMessage
)
import uuid


class Utils:
    @staticmethod
    def init_azure_openai_model(llm_config: AzureOpenAiModelConfig) -> BaseChatModel:
        from langchain_openai import AzureChatOpenAI
            
        model = AzureChatOpenAI(
            azure_endpoint=llm_config.host,
            azure_deployment=llm_config.model, 
            api_version=llm_config.api_version,
            api_key=llm_config.api_key,
            temperature=llm_config.temperature
        )
        
        return model
    
    
    @staticmethod
    def init_llm_model(llm_config: LlmConfig) -> BaseChatModel:
        if llm_config.provider == LLM_PROVIDER.AZURE_OPENAI:
            model = init_azure_openai_model()
        else:
            
            model = init_chat_model(
                model=llm_config.model,
                model_provider=llm_config.provider,  # optional: "anthropic", "cohere", etc.
                temperature=llm_config.temperature
            )
        
        # TODO: Validate model instance
        
        return model