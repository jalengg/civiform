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

    def _validate_config(self, variable_definitions, configs): 
        is_valid = True
        validation_errors = []

        for name, definition in variable_definitions.items():
            is_required = definition.get("required", False)
            config_value = configs.get(name, None)

            if (is_required and config_value is None): 
                is_valid = False
                validation_errors.append(f'{name} is required, but not provided')
            
            is_enum = definition.get("type") == "enum"

            if config_value is not None and is_enum: 
                if config_value not in definition.get("values"):
                    is_valid = False
                    validation_errors.append(f'{config_value} not supported enum for {name}')
                
        return is_valid, validation_errors

    def validate_config(self):
        return self.__validate_config(self.variable_definitions, self.configs)

    def get_cloud_provider(self):
        return self.configs.get("CIVIFORM_CLOUD_PROVIDER")
    
    def get_email_sender(self):
        return self.configs.get("EMAIL_SENDER")

    def get_config_variables(self):
        return self.configs

    def _get_terraform_variables(self, variable_definitions, configs): 
        tf_variables = list(filter(lambda x: variable_definitions.get(x).get("tfvar", False), self.variable_definitions))
        tf_config_vars = {}
        for key, value in configs.items():
            if key in tf_variables: 
                tf_config_vars[key] = value
        return tf_config_vars

    def get_terraform_variables(self):
        return self.__get_terraform_variables(self.variable_definitions, self.configs)
