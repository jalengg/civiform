import os

class TfVarWritter():
    def __init__(self, filepath):
        self.filepath = filepath
    
    # a json of key = vals to turn itno a tfvars
    def write_variables(self, config_vars):
        with open(self.filepath, 'w') as file:
            print(config_vars)
            for name, definition in config_vars.items():
                file.write(f'{name}="{definition}"\n')