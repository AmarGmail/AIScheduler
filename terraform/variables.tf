variable "repo_name" {
  description = "AIScheduler -The name of the GITHUB repository"
  type        = string
  default     = "AIScheduler"
}

variable "topics" {
  description = "AIScheduler -The list of topics to create in the repository."
  type        = list(string)
  default     = ["python", "docker", "github-actions", "ai", "groq", "terraform", "test_topic"]

}

variable "groq_api_key" {
  description = "AIScheduler - The API key for GROQ, used as a GitHub Actions secret."
  type        = string
  sensitive   = true
}

