from enum import Enum
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from message import Message
import uuid

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
    
    
class Agent:
    def __init__(self, llm_model: LLM_MODEL):
        self.agent_id = uuid.uuid4()
        memory = MemorySaver()
        self.model = init_chat_model(llm_model)
        # self.search = TavilySearch(max_results=2)
        self.tools = []
        self.agent_executor = create_react_agent(self.model, self.tools, checkpointer=memory)
    
    def invoke(self, message: Message) -> Message:
        config = {"configurable": {"thread_id": self.agent_id}}

        input_message = {
            "role": message.owner,
            "content":  message.value,
        }
        
        agent_stream = self.agent_executor.stream( {"messages": [input_message]}, config, stream_mode="values")
        
        return agent_stream["messages"][-1]