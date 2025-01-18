Module tests.test_generator
===========================

Functions
---------

`temp_output_dir(tmpdir)`
:   Fixture to create a temporary output directory for testing.

`test_generate_repository(temp_output_dir)`
:   Test the generate_repository function to ensure it generates the Terraform file.
    
    Test Cases:
    1. Verify that the Terraform file is created in the output directory.
    2. Verify that the content of the generated Terraform file includes the repository resource.

`test_generate_team(temp_output_dir)`
:   Test the generate_team function to ensure it generates the Terraform file correctly.
    
    Test Cases:
    1. Verify that the Terraform file is created in the output directory.
    2. Verify that the content of the generated Terraform file includes the team resource.