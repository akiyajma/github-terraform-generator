Module tests.test_config_loader
===============================

Functions
---------

`mock_config_file(tmpdir)`
:   Create a mock configuration file for testing

`test_load_config(mock_config_file)`
:   Test the load_config function.
    
    Test Cases:
    1. Verify that the 'template_dir' is correctly loaded from the config file.
    2. Verify that the 'output_dir' is correctly loaded from the config file.
    3. Verify that 'default_repository' is present in the loaded config.
    4. Verify that 'default_team' is present in the loaded config.