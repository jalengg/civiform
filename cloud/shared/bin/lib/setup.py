import argparse
import subprocess

from config_validator import ConfigLoader
from write_tfvars import TfVarWritter

parser = argparse.ArgumentParser()

parser.addArgument("-c", "--config_filename", type=string, help="the filename for the config file")
parser.addArgument("-v", "--variable_definition_filename", type=string, help="filename for variable definition")
parser.addArgument("-e", "--env", type=string, help="environment to setup")


## Load the Config and Definitions
config_loader = ConfigLoader(parser.config_filename, parser.variable_definition_filename)
config_loader.load_files()

# Validate that the config vars match the definition
is_valid, validation_errors = config_loader.validate_config()
if not is_valid:
    exit(f'Found the following validation errors {validation_errors.join(' ')}')

# Start running the different setup scripts based off of 
# the inputted config files
if config_loader.get_cloud_provider() == "azure":
    subprocess.call("deploys/bin/azure/key-vault-setup")

if config_loader.get_email_sender == "SES" and config_loader.get_cloud_provider() == "azure":
    subprocess.call("deploys/bin/ses-to-keyvault")

# Form the path to the correct directory. This feels a lil tenuous. 
deploy_directory = f'deploys/{parser.env)}_{config_loader.get_cloud_provider()}'

# Write the passthrough vars to a temporary file
tf_var_writter = TfVarWritter(deploy_directory)
variables_to_write = validator.get_terraform_variables()
tf_var_writter.write_variables(variables_to_write)

# Call the terraform apply to do the initial deploy
call f
subprocess.call("terraform apply")