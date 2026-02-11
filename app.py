from agents.agent import Agent, AzureOpenAiModelConfig, LlmConfig
from agents.enums import LLM_MODEL, LLM_PROVIDER
from langchain_core.messages import HumanMessage
import yaml
import os


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_llm_config_from_yaml(config: dict) -> LlmConfig:
    """Create LlmConfig from YAML configuration."""
    llm_cfg = config['model']
    provider=LLM_PROVIDER[llm_cfg['provider']]
    if provider == LLM_PROVIDER.AZURE_OPENAI: 
        return AzureOpenAiModelConfig(host=llm_cfg['host'],
            model=LLM_MODEL[llm_cfg['model']],
            temperature=llm_cfg['temperature'],
            provider=provider,
            api_key=llm_cfg['apiKey'] if llm_cfg['apiKey'] is not None else '',
            api_version=llm_cfg['apiVersion'] if llm_cfg['apiVersion'] is not None else ''
        )
    return LlmConfig(
        host=llm_cfg['host'],
        model=LLM_MODEL[llm_cfg['model']],
        temperature=llm_cfg['temperature'],
        provider=provider
    )


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