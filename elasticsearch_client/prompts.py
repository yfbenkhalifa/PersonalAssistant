class PromptTemplate:
    """
    A class to manage prompt templates for document processing and search.
    
    Attributes:
        template (str): The prompt template string.
        variables (list): List of variable names in the template.
    """
    
    def __init__(self, template: str):
        self.template = template
        self.variables = self.extract_variables()
    
    def extract_variables(self):
        """Extract variable names from the template."""
        import re
        return re.findall(r'\{(\w+)\}', self.template)