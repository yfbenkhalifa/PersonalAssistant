from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage


class AgentPrompts:
    """Central configuration for agent prompts and instructions"""

    SYSTEM_INSTRUCTIONS = """If you are not able 
    to provide the requested information, search the content in the document database using the provided search_indexed_documents tool.
    """
    @classmethod
    def get_chat_template(cls):
        """Get the chat prompt template with system instructions"""
        return ChatPromptTemplate.from_messages(
            [
                ("system", cls.SYSTEM_INSTRUCTIONS),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    @classmethod
    def get_system_message(cls):
        """Get the system message for direct use"""
        return SystemMessage(content=cls.SYSTEM_INSTRUCTIONS)
