import argparse
import subprocess

from config_loader import ConfigLoader
from write_tfvars import TfVarWritter

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config_filename", type=str, help="the filename for the config file")
parser.add_argument("-v", "--variable_definition_filename", type=str, help="filename for variable definition")
parser.add_argument("-e", "--env", type=str, help="environment to setup")
parser.add_argument("-d", "--dry_run", type=str, help="if false run the deploy")
parsed_args = parser.parse_args()

## Load the Config and Definitions
config_loader = ConfigLoader(parsed_args.config_filename, parsed_args.variable_definition_filename)
config_loader.load_files()

# Validate that the config vars match the definition
is_valid, validation_errors = config_loader.validate_config()
if not is_valid:
    exit(f"Found the following validation errors {validation_errors.join(' ')}")

# Start running the different setup scripts based off of 
# the inputted config files
if config_loader.get_cloud_provider() == "azure":
    subprocess.call("deploys/bin/azure/key-vault-setup")
    subprocess.call("ssh-keygen -t rsa -b 4096 -f $HOME/.ssh/bastion", shell=True)

if config_loader.get_email_sender == "SES" and config_loader.get_cloud_provider() == "azure":
    subprocess.call("deploys/bin/ses-to-keyvault")

# Form the path to the correct directory. This feels a lil tenuous. 
terraform_directory = f"../deploys/{parsed_args.env}_{config_loader.get_cloud_provider()}"

# Write the passthrough vars to a temporary file
tf_var_writter = TfVarWritter(terraform_directory)
variables_to_write = config_loader.get_terraform_variables()
tf_var_writter.write_variables(variables_to_write)

if parsed_args.dry_run.lower() != "false":
    subprocess.call("terraform plan", shell=True, cwd=terraform_directory)
else:
    subprocess.call("terraform deploy", shell=True, cwd=terraform_directory)
