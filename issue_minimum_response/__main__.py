import datetime
import logging
import os
from typing import List

from github import Github

_logger: logging.Logger = logging.getLogger(__name__)

# environment variables
exempt_user_list: List[str] = os.environ.get("INPUT_EXEMPT_USER_LIST").split(",")
exempt_labels: List[str] = os.environ.get("INPUT_EXEMPT_LABELS").split(",")
gh: Github = Github(os.environ.get("INPUT_TOKEN"))
minimum_response_time: int = int(os.environ.get("INPUT_MINIMUM_RESPONSE_TIME"))  # days
needs_response_label: str = os.environ.get("INPUT_LABEL")
exempt_authors: List[str] = os.environ.get("INPUT_EXEMPT_AUTHORS").split(",")
exempt_assigned_issues: bool = False if os.environ.get("INPUT_EXEMPT_ASSIGNED_ISSUES").lower() == False else True
repo = gh.get_repo(os.environ.get("GITHUB_REPOSITORY"))

# logging mode
debug_mode = True if os.environ.get("INPUT_DEBUG").lower() == "true" else False
log_level = logging.INFO if debug_mode else logging.WARNING
logging.basicConfig(level=log_level, format="%(message)s")
line_break = f"{20*'='}"


# data storage
labeled_issues: List[str] = []


def _label_issue(
    issue, needs_response_label: str = "needs-triage", debug_mode: bool = False
) -> None:
    """label issue"""
    for label in issue.labels:
        if label.name in exempt_labels or label is needs_response_label:
            _logger.info(
                f"issue not to be labeled as it is exempt due to label: {label.name}"
            )
            return
    issue.add_to_labels(needs_response_label) if not debug_mode else _logger.info(
        f"*** #{issue.number} would be labeled with label: {needs_response_label} if it doesn't already exist"
    )
    labeled_issues.append(issue.number)


def _needs_response(issue, exempt_authors: List[str] = [], make_assigned_issues_exempt: bool = True) -> bool:
    """determine if issue has had comments from another user besides the original poster"""

    _logger.info(f"issue author: {issue.user.login}")
    if issue.user.login in exempt_authors:
        _logger.info("issue author is in exempt list")
        return False
    if issue.assignee and make_assigned_issues_exempt:
        _logger.info("issue is assigned ")
        return False
    for comment in issue.get_comments():
        _logger.info(f"comment user: {comment.user.login}")
        if (
            comment.user.login != issue.user.login
            and comment.user.login not in exempt_user_list
        ):
            _logger.info(f"issue: #{issue.number} already has a response")
            return False

    return True


def _print_config() -> None:
    """print config"""

    config = {
        "Label": needs_response_label,
        "Minimum Response Time": minimum_response_time,
        "Exempt User List": exempt_user_list,
        "Exempt Labels": exempt_labels,
        "Exempt Authors": exempt_authors,
        "Repo": repo.name,
        "Debug Mode": debug_mode,
    }

    print(f"{line_break}\nWorkflow Settings:\n")
    [print(f"{setting}: {value}") for setting, value in config.items()]
    print(f"{line_break}\n")


def main():
    """main handler"""
    current_time: datetime = datetime.datetime.now()
    open_issues = repo.get_issues(state="open")
    _print_config()
    for issue in open_issues:
        print(issue)
        _logger.info(line_break)
        issue_age = (current_time - issue.created_at).days
        _logger.info(
            f"issue: #{issue.number} is {(current_time - issue.created_at).days} days old"
        )
        #### debug 
        print(f"issue: #{issue.number} assignee: {issue.assignee}")
        #####

        if issue_age >= minimum_response_time or minimum_response_time == 0:
            if _needs_response(issue, exempt_authors, make_assigned_issues_exempt=exempt_assigned_issues):
                _label_issue(
                    issue,
                    needs_response_label=needs_response_label,
                    debug_mode=debug_mode,
                )

    print(
        f"{line_break}\n{'[DRYRUN_MODE] ' if debug_mode else ''}issues labeled: {len(labeled_issues)}"
    )
    for issue in labeled_issues:
        print(f"#{issue}")


if __name__ == "__main__":
    main()
