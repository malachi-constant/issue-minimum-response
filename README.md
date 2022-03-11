# Python Container Action Template
[![Actions Status](https://github.com/malachi-constant/issue-minimum-response/workflows/Lint/badge.svg)](https://github.com/malachi-constant/issue-minimum-response/actions)
[![Actions Status](https://github.com/malachi-constant/issue-minimum-response/workflows/Test%20Workflow/badge.svg)](https://github.com/malachi-constant/issue-minimum-response/actions)


## Usage


### Example workflow

```yaml
name: Test Workflow
on: push
jobs:
  first-job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Run Action
        uses: malachi-constant/issue-minimum-response@latest
        with:
          exempt_user_list: "github-actions[bot]"
          exempt_labels: "help wanted"
          token: ${{secrets.GITHUB_TOKEN}}
          labels: needs-triage
```

### Inputs

exempt_user_list: 
    required: false 
    default: ''
    description: List of github usernames to ignore comments from. (comma separated) 
  token:
    required: true
    description: Repo Token
  exempt_labels:
    required: false
    default: ''
    description: List of labels to make an issue exempt from processing.
  label:
    required: false
    default: 'needs-triage'
    description: Label to add to issue that need a response.
  minimum_response_time:
    required: false
    default: 5
    description: Minimum response time in days. Set to '0' to immmediately process issues.
  debug:
    required: false
    default: 'false'
    description: Enable 'dry-run' mode.

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `token` | API Token with permissions to read and write github issues & labels |
| `exempt_user_list` _(optional)_  | List of github usernames to ignore comments from. (comma separated) |
| `exempt_labels` _(optional)_  | List of labels to make an issue exempt from processing. (comma separated) |
| `label` _(optional)_  | Label to add to issue that need a response. Default: `needs-triage` |
| `minimum_response_time` _(optional)_  | Minimum response time in days. Set to '0' to immmediately process issues. Default: `5` |
| `debug` _(optional)_  | Enable 'dry-run' mode.. Default: `false` |


### Outputs
None