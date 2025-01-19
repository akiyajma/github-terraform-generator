resource "github_repository" "repo1" {
  name               = "repo1"
  description        = "Default repository"
  visibility         = "private"
  gitignore_template = "None"
}