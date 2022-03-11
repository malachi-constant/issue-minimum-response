import datetime
import logging
import os
from typing import List

from github import Github

_logger: logging.Logger = logging.getLogger(__name__)

exempt_user_list: List[str] = os.environ.get("INPUT_EXEMPT_USER_LIST").split(",")
exempt_labels: List[str] = os.environ.get("INPUT_EXEMPT_LABELS").split(",")
gh: Github = Github(os.environ.get("INPUT_TOKEN"))
minimum_response_time: int = os.environ.get("INPUT_MINIMUM_RESPONSE_TIME")  # days
needs_response_label: str = os.environ.get("INPUT_LABEL")
repo = gh.get_repo(os.environ.get("GITHUB_REPOSITORY"))
labeled_issues: List[str] = []


def label_issue(issue, needs_response_label: str = "needs-triage") -> None:
    """label issue"""
    for label in issue.labels:
        if label.name in exempt_labels or label is needs_response_label:
            _logger.debug(
                f"issue not to be labeled as it is exempt due to label: {label.name}"
            )
            return
    issue.add_to_labels(needs_response_label)
    labeled_issues.append(issue.number)


def needs_response(issue) -> bool:
    """determine if issue has had comments from another user besides the original poster"""

    _logger.debug(f"issue author: {issue.user.login}")
    for comment in issue.get_comments():
        _logger.debug(f"comment user: {comment.user.login}")
        if (
            comment.user.login != issue.user.login
            and comment.user.login not in exempt_user_list
        ):
            _logger.debug(f"issue: #{issue.number} already has a response")
            return False

    return True


def main():
    """main handler"""
    current_time: datetime = datetime.datetime.now()
    open_issues = repo.get_issues(state="open")
    for issue in open_issues:
        issue_age = (current_time - issue.created_at).days
        _logger.debug(
            f"issue: #{issue.number} is {(current_time - issue.created_at).days} days old"
        )
        if issue_age >= minimum_response_time or issue_age == 0:
            if needs_response(issue):
                label_issue(issue, needs_response_label=needs_response_label)

    print(f"issues labeled: {len(labeled_issues)}")
    for issue in labeled_issues:
        print(issue)


if __name__ == "__main__":
    main()
