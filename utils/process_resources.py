import os

from loguru import logger

from generator.terraform_generator import TerraformGenerator


def process_repositories(generator, output_dir, repos_to_add, repos_to_update, repos_to_delete):
    """
    Handle the lifecycle of repositories: addition, update, and deletion.

    This function generates Terraform files for new or updated repositories and removes
    Terraform files for deleted repositories. The generated files are based on the provided
    repository data, including attributes like `repository_name`, `visibility`, `description`,
    and `gitignore_template`.

    If `gitignore_template` is set to "None", the attribute is excluded from the generated file.

    Args:
        generator (TerraformGenerator): The generator instance used to create Terraform files.
        output_dir (str): The directory where Terraform files are generated or deleted.
        repos_to_add (list[dict]): A list of repositories to add, represented as dictionaries.
        repos_to_update (list[dict]): A list of repositories to update, represented as dictionaries.
        repos_to_delete (list[dict]): A list of repositories to delete, represented as dictionaries.

    Raises:
        Exception: If an error occurs during any repository operation (add, update, delete).

    Example:
        process_repositories(
            generator=TerraformGenerator(template_dir="templates", output_dir="output"),
            output_dir="output",
            repos_to_add=[
                {"repository_name": "repo1", "visibility": "public", "description": "New repo", "gitignore_template": "Python"}
            ],
            repos_to_update=[
                {"repository_name": "repo2", "visibility": "private", "description": "Updated repo", "gitignore_template": "None"}
            ],
            repos_to_delete=[
                {"repository_name": "repo3"}
            ]
        )
    """
    try:
        # Process additions
        for repo in repos_to_add:
            try:
                generator.generate_repository(repo)
            except Exception as e:
                raise Exception(f"Error adding repository '{
                                repo.get('repository_name', 'unknown')}': {e}")

        # Process updates
        for repo in repos_to_update:
            try:
                generator.generate_repository(repo)
            except Exception as e:
                raise Exception(f"Error updating repository '{
                                repo.get('repository_name', 'unknown')}': {e}")

        # Process deletions
        for repo in repos_to_delete:
            try:
                tf_file = os.path.join(
                    output_dir, f"{repo['repository_name']}_repository.tf")
                if os.path.exists(tf_file):
                    os.remove(tf_file)
                    logger.info(f"Deleted Terraform file: {tf_file}")
                else:
                    logger.warning(
                        f"Terraform file not found for deletion: "
                        f"{tf_file}")
            except Exception as e:
                raise Exception(f"Error deleting repository '{
                                repo.get('repository_name', 'unknown')}': {e}")

    except Exception as e:
        raise Exception(f"Unexpected error processing repositories: {e}")


def process_teams(generator, output_dir, teams_to_add, teams_to_update, teams_to_delete):
    """
    Handle the lifecycle of teams: addition, update, and deletion.

    This function generates Terraform files for new or updated teams and removes
    Terraform files for deleted teams. Team attributes include `team_name`, `privacy`,
    `description`, and `members`.

    Args:
        generator (TerraformGenerator): The generator instance used to create Terraform files.
        output_dir (str): The directory where Terraform files are generated or deleted.
        teams_to_add (list[dict]): A list of teams to add, represented as dictionaries.
        teams_to_update (list[dict]): A list of teams to update, represented as dictionaries.
        teams_to_delete (list[dict]): A list of teams to delete, represented as dictionaries.

    Raises:
        Exception: If an error occurs during any team operation (add, update, delete).

    Example:
        process_teams(
            generator=TerraformGenerator(template_dir="templates", output_dir="output"),
            output_dir="output",
            teams_to_add=[
                {"team_name": "team1", "privacy": "closed", "description": "New team", "members": [{"username": "user1", "role": "maintainer"}]}
            ],
            teams_to_update=[
                {"team_name": "team2", "privacy": "secret", "description": "Updated team", "members": []}
            ],
            teams_to_delete=[
                {"team_name": "team3"}
            ]
        )
    """
    try:
        # Process additions
        for team in teams_to_add:
            try:
                generator.generate_team(team)
            except Exception as e:
                raise Exception(f"Error adding team '{
                                team.get('team_name', 'unknown')}': {e}")

        # Process updates
        for team in teams_to_update:
            try:
                generator.generate_team(team)
            except Exception as e:
                raise Exception(f"Error updating team '{
                                team.get('team_name', 'unknown')}': {e}")

        # Process deletions
        for team in teams_to_delete:
            try:
                tf_file = os.path.join(
                    output_dir, f"{team['team_name']}_team.tf")
                if os.path.exists(tf_file):
                    os.remove(tf_file)
                    logger.info(f"Deleted Terraform file: {tf_file}")
                else:
                    logger.warning(
                        f"Terraform file not found for deletion: {tf_file}")
            except Exception as e:
                logger.error(f"Error deleting team '{
                             team.get('team_name', 'unknown')}': {e}")

    except Exception as e:
        raise Exception(f"Unexpected error processing teams: {e}")


def process_memberships(generator, output_dir, memberships_to_add, memberships_to_update, memberships_to_delete):
    """
    GitHub Membership の追加・更新・削除を処理する
    """
    try:
        # 追加処理
        for membership in memberships_to_add:
            try:
                generator.generate_membership(membership)
            except Exception as e:
                raise Exception(
                    f"Error adding membership '{membership.get('username', 'unknown')}': {e}")

        # 更新処理
        for membership in memberships_to_update:
            try:
                generator.generate_membership(membership)
            except Exception as e:
                raise Exception(
                    f"Error updating membership '{membership.get('username', 'unknown')}': {e}")

        # 削除処理
        for membership in memberships_to_delete:
            try:
                tf_file = os.path.join(
                    output_dir, f"{membership['username']}_membership.tf")
                if os.path.exists(tf_file):
                    os.remove(tf_file)
                    logger.info(f"Deleted Terraform file: {tf_file}")
                else:
                    logger.warning(
                        f"Terraform file not found for deletion: {tf_file}")
            except Exception as e:
                raise Exception(
                    f"Error deleting membership '{membership.get('username', 'unknown')}': {e}")
    except Exception as e:
        raise Exception(f"Unexpected error processing memberships: {e}")


def process_repo_collaborators(generator, output_dir, collaborators_to_add, collaborators_to_update, collaborators_to_delete):
    """
    Handle the lifecycle of repository collaborators: addition, update, and deletion.
    """
    try:
        # Process additions
        for collab in collaborators_to_add:
            try:
                generator.generate_repository_collaborator(collab)
            except Exception as e:
                raise Exception(
                    f"Error adding repository collaborator '{collab.get('username', 'unknown')}' "
                    f"for repository '{collab.get('repository_name', 'unknown')}': {e}")
        # Process updates
        for collab in collaborators_to_update:
            try:
                generator.generate_repository_collaborator(collab)
            except Exception as e:
                raise Exception(
                    f"Error updating repository collaborator '{collab.get('username', 'unknown')}' "
                    f"for repository '{collab.get('repository_name', 'unknown')}': {e}"
                )
        # Process deletions
        for collab in collaborators_to_delete:
            try:
                tf_file = os.path.join(
                    output_dir, f"{collab['username']}_{collab['repository_name']}_collaborator.tf")
                if os.path.exists(tf_file):
                    os.remove(tf_file)
                    logger.info(f"Deleted Terraform file: {tf_file}")
                else:
                    logger.warning(
                        f"Terraform file not found for deletion: {tf_file}")
            except Exception as e:
                raise Exception(
                    f"Error deleting repository collaborator '{collab.get('username', 'unknown')}' "
                    f"for repository '{collab.get('repository_name', 'unknown')}': {e}")
    except Exception as e:
        raise Exception(
            f"Unexpected error processing repository collaborators: {e}")


def process_resources(template_dir, output_dir, resource_changes):
    try:
        generator = TerraformGenerator(template_dir, output_dir)
        # リポジトリの処理
        process_repositories(
            generator,
            output_dir,
            resource_changes.repos_to_add,
            resource_changes.repos_to_update,
            resource_changes.repos_to_delete,
        )
        # チームの処理
        process_teams(
            generator,
            output_dir,
            resource_changes.teams_to_add,
            resource_changes.teams_to_update,
            resource_changes.teams_to_delete,
        )
        # Membership の処理を追加
        process_memberships(
            generator,
            output_dir,
            resource_changes.memberships_to_add,
            resource_changes.memberships_to_update,
            resource_changes.memberships_to_delete,
        )
        process_repo_collaborators(
            generator,
            output_dir,
            resource_changes.repo_collaborators_to_add,
            resource_changes.repo_collaborators_to_update,
            resource_changes.repo_collaborators_to_delete,
        )
        logger.info("Resource processing completed successfully.")
    except Exception as e:
        raise Exception(f"Resource processing failed: {e}")
