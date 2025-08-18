from abc import abstractmethod
from enum import Enum
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

from document_chunking.document_chunker import DocumentChunker

class DocumentChunkResult:
    output: str
    messages: List[str]


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
                "4. Consider the document type and structure\n"
                "5. Aim for chunks that are neither too small (losing context) nor too large (overwhelming)\n\n"
                "Document Type Specific Guidelines:\n"
                "- CHAT: Preserve conversational flow, group related exchanges, maintain speaker context\n"
                "- GENERIC_DOCUMENT: Follow document structure (headings, sections, paragraphs), maintain logical flow\n\n"
                "IMPORTANT: You must return a valid JSON array where each entry specifies the chunk_id and the content of the chunk."
                "DOT NOT INCLUDE ANY ADDITIONAL TEXT OR EXPLANATION OF THE THOUGHT PROCESS Only return the JSON array, no additional text or explanation.",
            ),
            ("user", "Document Type: {content_type}\n\nContent to chunk:\n{input}"),
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
        agent = (
            {
                "input": lambda x: x["input"],
                "content_type": lambda x: x["content_type"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            } | self.prompt | self.llm | OpenAIToolsAgentOutputParser()
        )
        agent_executor = AgentExecutor(agent=agent, verbose=True, tools=[])
        result = list(agent_executor.stream(
            {"input": content, "content_type": DocumentContentType.GENERIC_DOCUMENT.value}))[0]
        
        return result['output']


