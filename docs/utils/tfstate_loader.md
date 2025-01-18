Module utils.tfstate_loader
===========================

Functions
---------

`extract_resources(tfstate)`
:   Extract resources from the Terraform state file.
    
    Args:
        tfstate (dict): The Terraform state.
    
    Returns:
        dict: A dictionary containing lists of repositories and teams.

`load_tfstate(tfstate_file)`
:   Load the Terraform state file.
    
    Args:
        tfstate_file (str): The file path of the Terraform state file.
    
    Returns:
        dict: The loaded Terraform state.

`save_existing_state(state, output_file)`
:   Save the existing state of resources to a file.
    
    Args:
        state (dict): The state of the resources to be saved.
        output_file (str): The file path where the state will be saved.