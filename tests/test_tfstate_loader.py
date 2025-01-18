from utils.tfstate_loader import extract_resources


def test_extract_resources():
    """
    Test the extract_resources function.

    Test Cases:
    1. Verify that the function correctly extracts repository resources from the tfstate.
    2. Verify that the function correctly extracts team resources from the tfstate.
    """
    tfstate = {
        "resources": [
            {
                "type": "github_repository",
                "instances": [
                    {
                        "attributes": {
                            "name": "example-repo",
                            "description": "Example description",
                            "visibility": "public"
                        }
                    }
                ]
            },
            {
                "type": "github_team",
                "instances": [
                    {
                        "attributes": {
                            "name": "example-team",
                            "description": "Example team",
                            "privacy": "closed"
                        }
                    }
                ]
            }
        ]
    }

    result = extract_resources(tfstate)
    assert len(result["repositories"]) == 1
    assert result["repositories"][0]["repository_name"] == "example-repo"
    assert len(result["teams"]) == 1
    assert result["teams"][0]["team_name"] == "example-team"
