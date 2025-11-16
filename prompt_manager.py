import yaml
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class PromptManager:
    """Manages prompts from YAML/JSON configuration files."""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self._executive_roles = None
        self._prompt_config = None
        
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        file_path = self.prompts_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON configuration file."""
        file_path = self.prompts_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @property
    def executive_roles(self) -> Dict[str, Any]:
        """Get executive roles configuration."""
        if self._executive_roles is None:
            self._executive_roles = self._load_yaml("executive_roles.yaml")
        return self._executive_roles
    
    @property
    def prompt_config(self) -> Dict[str, Any]:
        """Get prompt configuration."""
        if self._prompt_config is None:
            self._prompt_config = self._load_json("prompt_config.json")
        return self._prompt_config
    
    def get_executive_prompt(self, role: str) -> str:
        """Get system prompt for a specific executive role."""
        roles = self.executive_roles.get("executive_roles", {})
        if role not in roles:
            raise ValueError(f"Unknown executive role: {role}")
        
        role_data = roles[role]
        
        # Get the appropriate template based on role type
        templates = self.prompt_config.get("prompt_templates", {})
        if role == "technical_head":
            template = templates.get("technical_system_message", {}).get("template", "")
        elif role == "marketing_head":
            template = templates.get("marketing_system_message", {}).get("template", "")
        else:
            template = templates.get("system_message", {}).get("template", "")
        
        # Format the template with role data
        return self._format_prompt(template, role_data)
    
    def _format_prompt(self, template: str, role_data: Dict[str, Any]) -> str:
        """Format a prompt template with role data."""
        try:
            # Prepare formatting data
            format_data = {
                "title": role_data.get("title", ""),
                "role_context": role_data.get("role_context", ""),
                "responsibilities": self._format_list(role_data.get("responsibilities", [])),
                "approach": self._format_list(role_data.get("approach", [])),
                "response_guidelines": self._format_list(role_data.get("response_guidelines", [])),
                "tone": role_data.get("tone", "professional"),
                "technical_expertise": self._format_list(role_data.get("technical_expertise", [])),
                "marketing_expertise": self._format_list(role_data.get("marketing_expertise", [])),
                "target_markets": self._format_list(role_data.get("target_markets", []))
            }
            
            return template.format(**format_data)
        except KeyError as e:
            raise ValueError(f"Missing required field in role data: {e}")
    
    def _format_list(self, items: List[str]) -> str:
        """Format a list of items as bullet points."""
        if not items:
            return ""
        return "\n".join(f"• {item}" for item in items)
    
    def get_routing_keywords(self, role: str) -> List[str]:
        """Get routing keywords for a specific role."""
        roles = self.executive_roles.get("executive_roles", {})
        if role not in roles:
            return []
        return roles[role].get("routing_keywords", [])
    
    def get_role_priority(self, role: str) -> int:
        """Get priority level for a specific role."""
        roles = self.executive_roles.get("executive_roles", {})
        if role not in roles:
            return 1
        return roles[role].get("agent_config", {}).get("priority", 1)
    
    def get_role_temperature(self, role: str) -> float:
        """Get temperature setting for a specific role."""
        roles = self.executive_roles.get("executive_roles", {})
        if role not in roles:
            return 0.7
        return roles[role].get("agent_config", {}).get("temperature", 0.7)
    
    def determine_best_executive(self, query: str) -> str:
        """Determine the most appropriate executive for a query."""
        query_lower = query.lower()
        best_role = "business_head"  # Default
        max_matches = 0
        
        for role_name, role_data in self.executive_roles.get("executive_roles", {}).items():
            keywords = role_data.get("routing_keywords", [])
            matches = sum(1 for keyword in keywords if keyword.lower() in query_lower)
            
            if matches > max_matches:
                max_matches = matches
                best_role = role_name
        
        return best_role
    
    def get_orchestration_strategy(self, strategy_name: str) -> Dict[str, Any]:
        """Get orchestration strategy configuration."""
        strategies = self.prompt_config.get("orchestration_strategies", {})
        return strategies.get(strategy_name, {})
    
    def get_context_template(self, context_type: str) -> Dict[str, str]:
        """Get context template for specific domain."""
        contexts = self.prompt_config.get("context_templates", {})
        return contexts.get(context_type, {})
    
    def get_response_format(self, format_name: str) -> Dict[str, Any]:
        """Get response format configuration."""
        formats = self.prompt_config.get("response_formats", {})
        return formats.get(format_name, {})
    
    def list_available_roles(self) -> List[str]:
        """Get list of all available executive roles."""
        return list(self.executive_roles.get("executive_roles", {}).keys())
    
    def list_available_strategies(self) -> List[str]:
        """Get list of all available orchestration strategies."""
        return list(self.prompt_config.get("orchestration_strategies", {}).keys())
    
    def reload_configs(self):
        """Reload all configuration files."""
        self._executive_roles = None
        self._prompt_config = None


# Factory function for easy instantiation
def create_prompt_manager(prompts_dir: str = "prompts") -> PromptManager:
    """Create a PromptManager instance."""
    return PromptManager(prompts_dir)


# Example usage
if __name__ == "__main__":
    # Example usage
    pm = create_prompt_manager()
    
    print("Available roles:", pm.list_available_roles())
    print("Available strategies:", pm.list_available_strategies())
    
    # Get a prompt for business head
    business_prompt = pm.get_executive_prompt("business_head")
    print(f"\nBusiness Head Prompt:\n{business_prompt}")
    
    # Determine best executive for a query
    query = "How can we improve our API performance and reduce latency?"
    best_exec = pm.determine_best_executive(query)
    print(f"\nBest executive for query '{query}': {best_exec}")