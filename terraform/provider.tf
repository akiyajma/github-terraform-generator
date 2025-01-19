terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
  required_version = ">= 1.10.0"
}

provider "github" {
  token = var.github_token != "" ? var.github_token : getenv("GITHUB_TOKEN")
}
