import sys
from pathlib import Path

# Add src folder to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from agents.agent import Agent, AzureOpenAiModelConfig, AgentConfig
from agents.enums import LLM_MODEL, LLM_PROVIDER
from langchain_core.messages import HumanMessage
import yaml
import os
from dotenv import load_dotenv
import random
load_dotenv()

def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)




def main():
    """Main entry point for the Personal Assistant application."""
    print("=" * 50)
    print("Welcome to Personal Assistant")
    print("=" * 50)
    
    # Load configuration from YAML
    try:
        config = load_config()
        llm_config = create_llm_config_from_yaml(config)
        print(f"\n✓ Configuration loaded: {llm_config.model.value} ({llm_config.provider.value})")
    except Exception as e:
        print(f"\n❌ Failed to load configuration: {str(e)}")
        return
    
    agent = Agent(llm_config)
    print("\n✓ Agent initialized successfully!")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nGoodbye! 👋")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Send message to agent
            message = HumanMessage(role="user", content=user_input)
            response = agent.invoke(message)
            
            # Display response
            print(f"\nAssistant: {response.content}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()