resource "github_team" "team1" {
  name        = "team1"
  description = "Updated team"
  privacy     = "closed"
}


resource "github_team_membership" "team1_user1" {
  team_id  = github_team.team1.id
  username = "user1"
  role     = "maintainer"
}
