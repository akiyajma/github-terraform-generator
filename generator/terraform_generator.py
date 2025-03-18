import logging
import os

logger = logging.getLogger(__name__)


class TerraformGenerator:
    def __init__(self, template_dir, output_dir):
        self.template_dir = template_dir
        self.output_dir = output_dir

    def generate_repository(self, repository):
        # Logic to generate Terraform file for a repository
        tf_file_path = os.path.join(
            self.output_dir, f"{repository['repository_name']}_repository.tf")
        with open(tf_file_path, 'w') as tf_file:
            tf_file.write(f"""
resource "github_repository" "{repository['repository_name']}" {{
  name        = "{repository['repository_name']}"
  description = "{repository['description']}"
  visibility  = "{repository['visibility']}"
  gitignore_template = "{repository['gitignore_template'] if repository['gitignore_template'] != 'None' else ''}"
}}
""")
        logger.info(f"Generated Terraform file for repository: {tf_file_path}")

    def generate_team(self, team):
        # Logic to generate Terraform file for a team
        tf_file_path = os.path.join(
            self.output_dir, f"{team['team_name']}_team.tf")
        with open(tf_file_path, 'w') as tf_file:
            tf_file.write(f"""
resource "github_team" "{team['team_name']}" {{
  name        = "{team['team_name']}"
  description = "{team['description']}"
  privacy     = "{team['privacy']}"
}}
""")
        logger.info(f"Generated Terraform file for team: {tf_file_path}")
        logger.debug(f"Generating team: {team['team_name']}")
