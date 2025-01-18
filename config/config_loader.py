import yaml


def load_config(config_path="config/config.yaml"):
    """
    Load the configuration file.

    Args:
        config_path (str):
            The path to the configuration file.

    Returns:
        dict:
            The loaded configuration as a dictionary.
    """
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config
