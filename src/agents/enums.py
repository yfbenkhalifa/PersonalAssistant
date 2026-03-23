from enum import Enum


class LLM_MODEL(Enum):
    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    ANTHROPIC_CLAUDE_2 = "claude-2"
    ANTHROPIC_CLAUDE_3 = "claude-3"
    COHERE_COMMAND = "cohere-command"
    MISTRAL_1 = "mistral-1"
    LLAMA_2 = "llama-2"
    MPT_30B = "mpt-30b"
    GEMMA34B = "google/gemma-3-4b"
    
class LLM_PROVIDER(Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    AZURE_OPENAI = "azure_openai"
    LMSTUDIO = "lmstudio"
