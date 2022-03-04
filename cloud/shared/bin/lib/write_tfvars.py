import os

class TfVarWritter():
    def __init__(self, directory):
        self.filepath = f'{config_loader.get_cloud_provider()}/test.auto.tfvars'
    
    # a json of key = vals to turn itno a tfvars
    def write_variables(self, config_vars):
        with open(self.filepath, 'a') as file:
            for name, definition in config_vars.items():
                file.write(f'{name}={definition}')