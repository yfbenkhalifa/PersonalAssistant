from abc import abstractmethod
from typing import List, Optional, Type
from pydantic import Field, BaseModel
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI

class DocumentChunker:
    @abstractmethod
    def chunk_document(self, content: str) -> List[str]:
        """
        Splits the document content into smaller chunks for processing.
        
        Args:
            content (str): The full content of the document.
            
        Returns:
            List[str]: A list of content chunks.
        """
        pass


class AgenticDocumentChunker(DocumentChunker):
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an intelligent document chunking agent. Your purpose is to analyze document content and split it into meaningful, coherent chunks that preserve semantic relationships and context.\n\n"
                "When chunking documents, follow these principles:\n"
                "1. Maintain semantic coherence - keep related ideas together\n"
                "2. Respect natural boundaries like paragraphs, sections, and logical breaks\n"
                "3. Ensure each chunk is self-contained and meaningful\n"
                "4. Consider the document type and structure (e.g., academic papers, reports, stories)\n"
                "5. Aim for chunks that are neither too small (losing context) nor too large (overwhelming)\n\n"
                "Use the available tools to process and chunk the document content effectively. Return a json of well-structured chunks that maintain the document's logical flow and meaning.",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )   
    
    def __init__(self, host: str, port: int, api_key: Optional[str] = None):
        """
        Initializes the AgenticDocumentChunker with a language model.
        
        Args:
            llm (ChatOpenAI): The language model to use for processing.
        """
        self.llm : ChatOpenAI = ChatOpenAI(
            base_url=f"{host}:{port}/v1",
            temperature=0,
            api_key=api_key
        )
    
    def chunk_document(self, content: str) -> List[str]:
        """
        Splits the document content into smaller chunks for processing.
        
        Args:
            content (str): The full content of the document.
            
        Returns:
            List[str]: A list of content chunks.
        """
        # Here you would implement the logic to chunk the document
        # For simplicity, we return a list with the original content
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            } | self.prompt | self.llm | OpenAIToolsAgentOutputParser()
        )
        agent_executor = AgentExecutor(agent=agent, verbose=True, tools=[])
        list(agent_executor.stream(
            {"input": "what is the length of characters in the word eudca"}))
        
        return ["Chunk 1: " + content[:len(content)//2], "Chunk 2: " + content[len(content)//2:]]


