from enum import Enum
from langchain.chat_models import init_chat_model, BaseChatModel
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_core.messages import (
    BaseMessage
)
import uuid

from agents.enums import LLM_MODEL, LLM_PROVIDER

class LlmConfig:
    def __init__(self, host: str, model: LLM_MODEL, temperature: float, provider: LLM_PROVIDER):
        self.host = host
        self.model = model
        self.temperature = temperature
        self.provider = provider
    
    @property
    def temperature(self) -> float:
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float):
        if not 0.0 <= value <= 1.0:
            raise ValueError("Temperature must be between 0 and 1")
        self._temperature = value
    
class AzureOpenAiModelConfig(LlmConfig):
    def __init__(self, host, model, temperature, provider, api_version: str, api_key: str):
        super().__init__(host, model, temperature, provider)
        self.provider = LLM_PROVIDER.AZURE_OPENAI
        self.api_version = api_version
        self.api_key = api_key
        
    
class Agent:
    def __init__(self,llm_config: LlmConfig):
        self.agent_id = uuid.uuid4()
        memory = MemorySaver()
        self.model = self.init_llm_model(llm_config)
        self.tools = []
        self.agent = create_agent(self.model, self.tools, checkpointer=memory)
        self.history = []
    
    def invoke(self, message: BaseMessage) -> BaseMessage:
        config = {"configurable": {"thread_id": self.agent_id}}
        self.history.append(message)
        result = self.agent.invoke({"messages": self.history}, config=config)
        self.history = result['messages']
        response = self.history[-1]
        return response
    
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
            from langchain_openai import AzureChatOpenAI
            
            model = AzureChatOpenAI(
                azure_endpoint=llm_config.host,
                azure_deployment=llm_config.model, 
                api_version=llm_config.api_version,
                api_key=llm_config.api_key,
                temperature=llm_config.temperature
            )
        
        else:
            
            model = init_chat_model(
                model=llm_config.model,
                model_provider=llm_config.provider,  # optional: "anthropic", "cohere", etc.
                temperature=llm_config.temperature
            )
        
        # TODO: Validate model instance
        
        return model
    
    