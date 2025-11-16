"""
Example usage of the updated LLM orchestrator with YAML/JSON prompt management.
This demonstrates how to use the new PromptManager system for better organization.
"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.orchestrator import (
    LLMOrchestrator,
    OrchestrationType,
    create_executive_orchestrator,
    create_business_head_llm,
    smart_orchestrate
)
from prompt_manager import PromptManager


# Mock LLM for demonstration
class MockChatModel:
    """Mock chat model for testing purposes"""
    
    def __init__(self, name: str = "MockGPT"):
        self.name = name
    
    async def ainvoke(self, messages):
        """Mock async invoke that returns a simple response"""
        # Extract the last human message
        human_msg = None
        for msg in reversed(messages):
            if hasattr(msg, 'content') and 'human' in str(type(msg)).lower():
                human_msg = msg.content
                break
        
        # Simple mock response based on query content
        if human_msg:
            if "business" in human_msg.lower() or "strategy" in human_msg.lower():
                response = f"[BUSINESS PERSPECTIVE] Strategic analysis of: {human_msg[:100]}..."
            elif "technical" in human_msg.lower() or "development" in human_msg.lower():
                response = f"[TECHNICAL PERSPECTIVE] Technical solution for: {human_msg[:100]}..."
            elif "marketing" in human_msg.lower() or "customer" in human_msg.lower():
                response = f"[MARKETING PERSPECTIVE] Customer-focused approach to: {human_msg[:100]}..."
            else:
                response = f"[GENERAL RESPONSE] Analysis of: {human_msg[:100]}..."
        else:
            response = "Mock response generated"
        
        # Return an object that mimics AIMessage
        class MockResponse:
            def __init__(self, content):
                self.content = content
        
        return MockResponse(response)


async def demo_prompt_manager():
    """Demonstrate PromptManager capabilities"""
    print("🎯 PromptManager Demo")
    print("=" * 50)
    
    pm = PromptManager()
    
    # Show available roles
    print(f"Available Executive Roles: {pm.list_available_roles()}")
    print(f"Available Strategies: {pm.list_available_strategies()}")
    print()
    
    # Demonstrate prompt generation
    business_prompt = pm.get_executive_prompt("business_head")
    print("📋 Business Head Prompt Preview:")
    print(business_prompt[:200] + "...")
    print()
    
    # Demonstrate routing
    test_queries = [
        "How can we improve our revenue model?",
        "What technical architecture should we use for scaling?",
        "How do we market to enterprise customers?",
        "What's our competitive positioning strategy?"
    ]
    
    print("🎯 Automatic Role Routing:")
    for query in test_queries:
        best_role = pm.determine_best_executive(query)
        keywords = pm.get_routing_keywords(best_role)
        print(f"Query: {query}")
        print(f"  → Best Role: {best_role}")
        print(f"  → Keywords: {keywords[:3]}...")  # Show first 3 keywords
        print()


async def demo_basic_orchestration():
    """Demonstrate basic orchestration with YAML prompts"""
    print("🤖 Basic Orchestration Demo")
    print("=" * 50)
    
    # Create mock model
    model = MockChatModel("DemoGPT")
    
    # Create orchestrator with executive team
    orchestrator = create_executive_orchestrator(model)
    
    # Show status
    status = orchestrator.get_status()
    print(f"Orchestrator Status:")
    print(f"  Total LLMs: {status['total_llms']}")
    print(f"  Available Roles: {status['available_roles']}")
    print()
    
    # Test sequential strategy
    query = "How can we improve our AI document search platform to increase customer satisfaction and revenue?"
    
    print(f"Query: {query}")
    print(f"Strategy: Sequential")
    print()
    
    result = await orchestrator.orchestrate(query, OrchestrationType.SEQUENTIAL)
    
    print(f"✅ Execution successful: {result.success}")
    print(f"⏱️ Total time: {result.total_time:.2f}s")
    print(f"🔄 Execution path: {' → '.join(result.execution_path)}")
    print(f"📝 Final response: {result.final_response[:200]}...")
    print()


async def demo_smart_orchestration():
    """Demonstrate smart orchestration with auto-routing"""
    print("🧠 Smart Orchestration Demo")
    print("=" * 50)
    
    model = MockChatModel("SmartGPT")
    orchestrator = create_executive_orchestrator(model)
    
    test_scenarios = [
        {
            "query": "What technical stack should we use for our API?",
            "expected_strategy": "Should route to Development Head"
        },
        {
            "query": "How do we increase market share in the enterprise segment?", 
            "expected_strategy": "Should route to Business/Marketing"
        },
        {
            "query": "Compare different approaches to customer acquisition",
            "expected_strategy": "Should use parallel for multiple perspectives"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"Scenario {i}: {scenario['expected_strategy']}")
        print(f"Query: {scenario['query']}")
        
        result = await smart_orchestrate(orchestrator, scenario['query'])
        
        print(f"  Strategy used: {result.execution_path}")
        print(f"  Success: {result.success}")
        print(f"  Response preview: {result.final_response[:100]}...")
        print()


async def demo_specialized_llms():
    """Demonstrate creating specialized single-role LLMs"""
    print("🎯 Specialized LLM Demo")
    print("=" * 50)
    
    model = MockChatModel("SpecializedGPT")
    
    # Create specialized orchestrators
    business_orch = create_business_head_llm(model)
    
    query = "What's our strategy for entering the healthcare market?"
    
    print(f"Query: {query}")
    print("Using Business Head only...")
    
    result = await business_orch.orchestrate(query)
    
    print(f"Business Head Response: {result.final_response}")
    print()


async def demo_configuration_management():
    """Demonstrate configuration and template management"""
    print("⚙️ Configuration Management Demo")
    print("=" * 50)
    
    pm = PromptManager()
    
    # Show orchestration strategies
    strategies = pm.prompt_config.get("orchestration_strategies", {})
    print("Available Orchestration Strategies:")
    for name, config in strategies.items():
        print(f"  📋 {name.title()}: {config.get('description', 'No description')}")
        print(f"     Best for: {config.get('best_for', 'General use')}")
    print()
    
    # Show context templates
    contexts = pm.prompt_config.get("context_templates", {})
    print("Available Context Templates:")
    for context_type, template in contexts.items():
        print(f"  🏷️ {context_type.title()}:")
        for key, value in list(template.items())[:2]:  # Show first 2 items
            print(f"     • {key}: {value}")
    print()
    
    # Show response formats
    formats = pm.prompt_config.get("response_formats", {})
    print("Available Response Formats:")
    for format_name, format_config in formats.items():
        structure = format_config.get("structure", [])
        max_length = format_config.get("max_length", "No limit")
        print(f"  📊 {format_name.title()}: {structure} (max: {max_length} chars)")
    print()


async def main():
    """Run all demonstrations"""
    print("🚀 ChatWiZPt Orchestrator Demo")
    print("=" * 60)
    print()
    
    demos = [
        demo_prompt_manager,
        demo_configuration_management,
        demo_basic_orchestration,
        demo_smart_orchestration,
        demo_specialized_llms
    ]
    
    for i, demo in enumerate(demos, 1):
        try:
            await demo()
            if i < len(demos):
                print("\n" + "─" * 60 + "\n")
        except Exception as e:
            print(f"❌ Demo {demo.__name__} failed: {e}")
            print()
    
    print("✅ All demos completed!")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())