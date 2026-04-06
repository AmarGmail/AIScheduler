resource "github_repository" "repo" {
  name        = var.repo_name
  description = "AI News Agent with CI/CD pipeline and Docker support."
  visibility  = "public"
  has_issues = true
  topics      = var.topics
#  private     = false


#Prevent Terraform from deleting the repository if it already exists
#Prevents accidental deletion via Terraform
lifecycle {
    prevent_destroy = true
    }
}

#Manage Actions Secrets 
#Note: Value is sensitive, so we use variables or env vars

resource "github_actions_secret" "groq_key" {
  repository      = var.repo_name
  secret_name     = "GROQ_API_KEY"
  plaintext_value = var.groq_api_key
}

# Add similar blocks for EMAIL_USER and EMAIL_PASS if you wish to manage them via IaC
