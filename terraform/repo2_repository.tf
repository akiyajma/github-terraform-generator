resource "github_repository" "repo2" {
  name               = "repo2"
  description        = "This is repo2"
  visibility         = "public"
  
  gitignore_template = "Python"
  
}