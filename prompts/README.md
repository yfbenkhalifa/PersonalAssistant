# ChatWiZPt Prompt Management System

This directory contains the organized prompt configuration system for ChatWiZPt's LLM orchestration.

## 📁 Structure

```
prompts/
├── executive_roles.yaml      # Executive role definitions and prompts
├── prompt_config.json        # Templates, strategies, and configurations
├── requirements.txt          # Dependencies for prompt system
└── README.md                # This file
```

## 🎯 Key Features

### 1. **Executive Roles (YAML)**
- **Business Head**: Strategic planning, revenue management, stakeholder relations
- **Development Head**: Technical architecture, performance optimization, team leadership  
- **Marketing Head**: Brand strategy, customer acquisition, digital marketing
- **Technical Head**: System design, innovation, product development

### 2. **Flexible Templates (JSON)**
- **System Message Templates**: Customizable prompt structures
- **Context Templates**: Domain-specific context injection
- **Response Formats**: Structured output formatting

### 3. **Orchestration Strategies**
- **Sequential**: Execute executives in priority order
- **Parallel**: Run all executives simultaneously
- **Conditional**: Smart routing based on query content

## 🚀 Usage

### Basic Setup
```python
from prompt_manager import PromptManager
from chatbot.orchestrator import create_executive_orchestrator

# Initialize prompt manager
pm = PromptManager("prompts")

# Create orchestrator with executive team
orchestrator = create_executive_orchestrator(your_llm_model)

# Get executive prompt
business_prompt = pm.get_executive_prompt("business_head")
```

### Smart Orchestration
```python
from chatbot.orchestrator import smart_orchestrate

# Auto-route and execute
result = await smart_orchestrate(
    orchestrator, 
    "How can we improve our technical architecture?"
)
```

### Role-Specific LLMs
```python
from chatbot.orchestrator import create_business_head_llm

# Create specialized business-focused LLM
business_llm = create_business_head_llm(model)
result = await business_llm.orchestrate("What's our revenue strategy?")
```

## ⚙️ Configuration

### Executive Roles (executive_roles.yaml)
Each role contains:
- **Title & Context**: Role description and organizational position
- **Responsibilities**: Key areas of expertise and authority
- **Approach**: Decision-making style and methodology
- **Guidelines**: Response structure and tone requirements
- **Routing Keywords**: Words that trigger role selection
- **Agent Config**: Temperature, priority, and behavior settings

### Prompt Templates (prompt_config.json)
Configurable templates for:
- **System Messages**: Role-specific prompt construction
- **Context Injection**: Domain expertise integration
- **Response Formatting**: Output structure control
- **Strategy Selection**: Orchestration pattern definitions

## 🔧 Customization

### Adding New Roles
1. **Update executive_roles.yaml**:
```yaml
new_role:
  title: "New Role Title"
  role_context: "Role description..."
  responsibilities: ["Responsibility 1", "Responsibility 2"]
  # ... other fields
```

2. **Update PromptManager** (if needed):
```python
# Add role mapping in register_executive_llm
role_mapping = {
    "new_role": LLMRole.SPECIALIST,
    # ... existing mappings
}
```

### Custom Templates
Add new templates to `prompt_config.json`:
```json
"custom_template": {
  "template": "You are {title}. {custom_field}...",
  "required_fields": ["title", "custom_field"]
}
```

### Routing Rules
Modify routing keywords in `executive_roles.yaml`:
```yaml
routing_keywords:
  - "custom keyword"
  - "domain specific term"
```

## 📊 Benefits

### ✅ **Improved Organization**
- Centralized prompt management
- Clear role separation
- Version-controlled configurations

### ✅ **Enhanced Flexibility** 
- Easy prompt modifications without code changes
- Template-based customization
- Dynamic role routing

### ✅ **Better Maintainability**
- Structured configuration files
- Consistent prompt formatting
- Reusable components

### ✅ **Scalability**
- Add new roles without orchestrator changes
- Configurable strategies and templates
- Modular prompt system

## 🔍 Examples

See `orchestrator_demo.py` for comprehensive usage examples including:
- Basic orchestration setup
- Smart auto-routing
- Specialized role usage
- Configuration management

## 📋 Migration Notes

This system replaces the previous `ExecutivePrompts` class with:
- YAML-based role definitions
- JSON-based configuration templates
- Programmatic prompt management via `PromptManager`

Old prompt access:
```python
# OLD
prompt = ExecutivePrompts.get_business_head_prompt()
```

New prompt access:
```python
# NEW  
pm = PromptManager()
prompt = pm.get_executive_prompt("business_head")
```

## 🛠️ Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Core dependencies:
- `pyyaml` - YAML configuration parsing
- `langchain-core` - LLM orchestration framework
- `langchain` - Extended LLM capabilities