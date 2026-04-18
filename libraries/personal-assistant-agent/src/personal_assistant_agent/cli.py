"""Interactive CLI entry point for the Personal Assistant agent."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from personal_assistant_agent.agent import (
    Agent,
    create_llm_config_from_yaml,
    load_config,
)


def _resolve_default_config() -> Path:
    env_value = os.getenv("PERSONAL_ASSISTANT_AGENT_CONFIG")
    if env_value:
        return Path(env_value)
    # config.yaml sits at the package root (two levels up from this file).
    return Path(__file__).resolve().parents[2] / "config.yaml"


def main() -> None:
    """Run an interactive REPL against the configured LLM."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="Personal Assistant Agent CLI")
    parser.add_argument(
        "--config",
        type=Path,
        default=_resolve_default_config(),
        help="Path to the agent configuration YAML file.",
    )
    args = parser.parse_args()

    print("=" * 50)
    print("Welcome to Personal Assistant")
    print("=" * 50)

    try:
        config = load_config(str(args.config))
        llm_config = create_llm_config_from_yaml(config)
        print(
            f"\n✓ Configuration loaded: {getattr(llm_config.model, 'value', llm_config.model)} "
            f"({llm_config.provider.value})"
        )
    except Exception as exc:
        print(f"\n❌ Failed to load configuration: {exc}")
        return

    agent = Agent(llm_config)
    print("\n✓ Agent initialized successfully!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit", "bye"}:
                print("\nGoodbye! 👋")
                break
            if not user_input:
                continue

            response = agent.invoke(HumanMessage(content=user_input))
            print(f"\nAssistant: {response.content}\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as exc:
            print(f"\n❌ Error: {exc}\n")


if __name__ == "__main__":
    main()

