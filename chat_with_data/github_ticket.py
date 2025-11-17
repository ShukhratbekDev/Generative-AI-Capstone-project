"""
GitHub Issues integration for creating support tickets.
"""
import os
import logging
from typing import List, Optional
from github import Github
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_github_issue(
    title: str,
    description: str,
    labels: Optional[List[str]] = None
) -> dict:
    """
    Create a GitHub issue for support tickets.
    
    Args:
        title: Issue title
        description: Issue description
        labels: Optional list of labels
        
    Returns:
        Dictionary with success status and issue URL or error message
    """
    github_token = os.getenv("GITHUB_TOKEN")
    repo_owner = os.getenv("GITHUB_REPO_OWNER")
    repo_name = os.getenv("GITHUB_REPO_NAME")
    
    if not all([github_token, repo_owner, repo_name]):
        logger.warning("GitHub credentials not configured. Returning mock response.")
        return {
            "success": True,
            "url": "https://github.com/example/issues/1",
            "message": "Support ticket created (mock - configure GitHub credentials for real tickets)"
        }
    
    try:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        
        issue = repo.create_issue(
            title=title,
            body=description,
            labels=labels or ["support"]
        )
        
        logger.info(f"Created GitHub issue #{issue.number}: {issue.html_url}")
        
        return {
            "success": True,
            "url": issue.html_url,
            "issue_number": issue.number,
            "message": f"Support ticket created successfully: {issue.html_url}"
        }
    except Exception as e:
        logger.error(f"Error creating GitHub issue: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "url": None
        }

