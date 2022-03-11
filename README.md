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
        uses: ./
        with:
          exempt_user_list: "github-actions[bot]"
          exempt_labels: "help wanted"
          token: ${{secrets.GITHUB_TOKEN}}
          labels: needs-triage
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

### Outputs
None