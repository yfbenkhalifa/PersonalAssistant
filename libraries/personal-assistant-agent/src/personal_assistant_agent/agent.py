from __future__ import annotations

import os
import random
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

import yaml
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage

from personal_assistant_agent.enums import LLM_MODEL, LLM_PROVIDER


def _coerce_model_name(model: str | LLM_MODEL) -> str:
    return model.value if isinstance(model, LLM_MODEL) else model


@dataclass(slots=True)
class AgentConfig:
    nickname: str
    host: str | None
    model: str | LLM_MODEL
    temperature: float
    provider: LLM_PROVIDER

    def __post_init__(self) -> None:
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError("Temperature must be between 0 and 1")


@dataclass(slots=True)
class AzureOpenAIModelConfig(AgentConfig):
    api_version: str = ""
    api_key: str | None = None
    provider: LLM_PROVIDER = field(default=LLM_PROVIDER.AZURE_OPENAI, init=False)


class Agent:
    def __init__(self, llm_config: AgentConfig, system_prompt: str | None = None):
        self.agent_id = str(uuid.uuid4())
        self.nickname = llm_config.nickname
        self.system_prompt = system_prompt
        self.model = self.init_llm_model(llm_config)
        self.tools: list[Callable[..., Any]] = []
        self.history: list[BaseMessage] = []

    def invoke(self, message: BaseMessage) -> BaseMessage:
        self.history.append(message)
        messages: list[BaseMessage] = []
        if self.system_prompt:
            messages.append(SystemMessage(content=self.system_prompt))
        messages.extend(self.history)

        response = self.model.invoke(messages)
        self.history.append(response)
        return response

    def add_tool(self, tool: Callable[..., Any]) -> None:
        self.tools.append(tool)

    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt = prompt

    @staticmethod
    def init_azure_openai_model(llm_config: AzureOpenAIModelConfig) -> BaseChatModel:
        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI(
            azure_endpoint=llm_config.host,
            azure_deployment=_coerce_model_name(llm_config.model),
            api_version=llm_config.api_version,
            api_key=llm_config.api_key,
            temperature=llm_config.temperature,
        )

    @staticmethod
    def init_llm_model(llm_config: AgentConfig) -> BaseChatModel:
        if llm_config.provider == LLM_PROVIDER.AZURE_OPENAI:
            if not isinstance(llm_config, AzureOpenAIModelConfig):
                raise TypeError("Azure OpenAI configuration requires AzureOpenAIModelConfig")
            return Agent.init_azure_openai_model(llm_config)

        model_name = _coerce_model_name(llm_config.model)
        provider = str(llm_config.provider.value)
        extra_kwargs: dict[str, Any] = {"temperature": llm_config.temperature}

        if llm_config.host:
            extra_kwargs["base_url"] = llm_config.host
            if llm_config.provider == LLM_PROVIDER.LMSTUDIO:
                extra_kwargs["api_key"] = os.getenv("LMSTUDIO_API_KEY", "lm-studio")

        return init_chat_model(
            model=model_name,
            model_provider=provider,
            **extra_kwargs,
        )


def load_config(config_path: str) -> dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def create_llm_config_from_yaml(config: Mapping[str, Any]) -> AgentConfig:
    llm_cfg = config["model"]
    provider = LLM_PROVIDER(llm_cfg["provider"].lower())
    nickname = llm_cfg.get("nickname") or f"random_animal_{random.randint(1, 100)}"
    model_name = llm_cfg["model"]

    try:
        model: str | LLM_MODEL = LLM_MODEL(model_name)
    except ValueError:
        model = model_name

    if provider == LLM_PROVIDER.AZURE_OPENAI:
        return AzureOpenAIModelConfig(
            nickname=nickname,
            host=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model=model,
            temperature=llm_cfg["temperature"],
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=llm_cfg.get("apiVersion") or "",
        )

    return AgentConfig(
        nickname=nickname,
        host=llm_cfg.get("host"),
        model=model,
        temperature=llm_cfg["temperature"],
        provider=provider,
    )




