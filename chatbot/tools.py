import json
from langchain_core.tools import tool

from langchain_core.messages import ToolMessage
from langgraph.graph import END
from chatbot.state_graph import State

from server import startup


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    

def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


@tool("Return length of user query")
def query_lenght(query: str) -> int:
    """Return length of user query"""
    return len(query)

@tool("Search in the indexed documents database")
def search_indexed_documents(query: str) -> str:
    """Search for documents, whatsapp conversations or personal information stored in in the indexed database"""
    es_client = startup.elasticsearch_client
    try:
        response = es_client.client.search(
            index="whatsapp_chats",
            body={
                "query": {
                    "match": {
                        "content": query
                    }
                }
            }
        )
        result = []
        for hit in response.get("hits", {}).hits:
            result.append(hit["_source"])
        return result
    except Exception as e:
        print(f"Error searching indexed documents: {e}")
        return None