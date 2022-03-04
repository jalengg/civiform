import os
import json

class ConfigLoader(): 
    def __init__(self, config_filename, variable_definition_filename):
        self.config_filename = config_filename
        self.variable_definition_filename = variable_definition_filename
    
    def load_files(self):
        with open(config_filename, 'r') as config_file:
            self.configs = json.loads(config_file.read())

        with open(variable_definition_filename, 'r') as definitions_file:
            self.variable_definitions = json.loads(definitions_file.read())

    def validate_config(self):
        is_valid = True
        validation_errors = []

        for name, definition in self.variable_definitions.items():
            is_required = isinstance(variable_definition.get("required", None), bool)
            config_value = self.configs.get(name, None)
            
            if (is_required and not config_value): 
                is_valid = False
                validation_errors.push(f'{name} is required, but not provided')
            
            is_enum = variable_definition.get("type") == "enum"
            if config_value and is_enum and (config_value not in variable_definition.get("values")):
                is_valid = False
                validation_errors.push(f'{config_value} not supported enum for {name}')
                
        return is_valid, validation_errors
        
    def get_cloud_provider(self):
        return self.variable_definitions.get("CIVIFORM_CLOUD_PROVIDER")
    
    def get_email_sender(self):
        return self.variable_definitions.get("EMAIL_SENDER")

    def get_config_variables(self):
        return self.variable_definitions
    
    def get_terraform_variables(self):
        tf_variables = filter(lambda x: x.type == "tfvar", self.variable_definitions)
        return filter(lambda x: x in tf_variables, self.config)
