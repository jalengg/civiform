import os
import json

class ConfigLoader(): 
    def __init__(self, config_filename, variable_definition_filename):
        self.config_filename = config_filename
        self.variable_definition_filename = variable_definition_filename
    
    def load_files(self):
        with open(self.config_filename, 'r') as config_file:
            self.configs = json.loads(config_file.read())
        with open(self.variable_definition_filename, 'r') as definitions_file:
            self.variable_definitions = json.loads(definitions_file.read())

    def validate_config(self):
        is_valid = True
        validation_errors = []

        for name, definition in self.variable_definitions.items():
            is_required = isinstance(self.variable_definitions.get("required", None), bool)
            config_value = self.configs.get(name, None)
            
            if (is_required and not config_value): 
                is_valid = False
                validation_errors.push(f'{name} is required, but not provided')
            
            is_enum = self.variable_definitions.get("type") == "enum"
            if config_value and is_enum and (config_value not in self.variable_definitions.get("values")):
                is_valid = False
                validation_errors.push(f'{config_value} not supported enum for {name}')
                
        return is_valid, validation_errors

    def get_cloud_provider(self):
        return self.configs.get("CIVIFORM_CLOUD_PROVIDER")
    
    def get_email_sender(self):
        return self.configs.get("EMAIL_SENDER")

    def get_config_variables(self):
        return self.configs
    
    def get_terraform_variables(self):
        tf_variables = list(filter(lambda x: self.variable_definitions.get(x).get("type") == "tfvar", self.variable_definitions))
        tf_config_vars = {}
        for key, value in self.configs.items():
            print(key, list(tf_variables))
            if key in tf_variables: 
                tf_config_vars[key] = value
        return tf_config_vars
