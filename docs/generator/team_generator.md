Module generator.team_generator
===============================

Functions
---------

`generate_team(team: models.team.Team, template_dir: str, output_dir: str)`
:   Generate a Terraform file for a GitHub team.
    
    Args:
        team (Team): The team object containing team attributes.
        template_dir (str): The directory containing the Jinja2 templates.
        output_dir (str): The directory where the generated Terraform file will be saved.