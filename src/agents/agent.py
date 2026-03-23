import os
import random
from enum import Enum
from typing import Callable
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import (
    BaseMessage
)
import uuid
from agents.enums import LLM_MODEL, LLM_PROVIDER
import logging
logger = logging.getLogger(__name__)

class AgentConfig:
    def __init__(self, nickname: str, host: str, model: LLM_MODEL, temperature: float, provider: LLM_PROVIDER):
        self.nickname = nickname
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
    
class AzureOpenAiModelConfig(AgentConfig):
    def __init__(self,nickname: str, host, model, temperature, provider, api_version: str, api_key: str):
        super().__init__(nickname, host, model, temperature, provider)
        self.provider = LLM_PROVIDER.AZURE_OPENAI
        self.api_version = api_version
        self.api_key = api_key
        
    
class Agent:
    def __init__(self,llm_config: AgentConfig, system_prompt: str = None):
        self.agent_id = uuid.uuid4()
        memory = MemorySaver()
        self.nickname = llm_config.nickname
        self.model = self.init_llm_model(llm_config)
        self.tools = []
        logger.info("Initializing Agent with model: %s, provider: %s", llm_config.model.value, llm_config.provider.value)
        self.agent = create_agent(self.model, self.tools, checkpointer=memory)
        if self.agent is None:
            logger.error("Failed to initialize agent")
            return
        if system_prompt:
            self.set_system_prompt(system_prompt)
        self.history = []
    
    def invoke(self, message: BaseMessage) -> BaseMessage:
        config = {"configurable": {"thread_id": self.agent_id}}
        self.history.append(message)
        result = self.agent.invoke({"messages": self.history}, config=config)
        self.history = result['messages']
        response = self.history[-1]
        return response
    
    @classmethod
    def add_tool(self, tool: Callable) -> None:
        pass

    @classmethod
    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt = prompt
    
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
    def init_llm_model(llm_config: AgentConfig) -> BaseChatModel:
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
                model_provider=llm_config.provider.value,  # optional: "anthropic", "cohere", etc.
                temperature=llm_config.temperature,

            )
        
        return model
    

def create_llm_config_from_yaml(config: dict) -> AgentConfig:
    """Create LlmConfig from YAML configuration."""
    llm_cfg = config['model']
    provider=LLM_PROVIDER[llm_cfg['provider']]
    nickname = llm_cfg['nickname'] if 'nickname' in llm_cfg else f"random_animal_{random.randint(1, 100)}"
    if provider == LLM_PROVIDER.AZURE_OPENAI:
        return AzureOpenAiModelConfig(
            nickname=nickname,
            host=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model=LLM_MODEL[llm_cfg['model']],
            temperature=llm_cfg['temperature'],
            provider=provider,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=llm_cfg['apiVersion'] if llm_cfg['apiVersion'] is not None else ''
        )
    return AgentConfig(
        nickname=nickname,
        host=llm_cfg['host'],
        model=llm_cfg['model'],
        temperature=llm_cfg['temperature'],
        provider=provider
    )
