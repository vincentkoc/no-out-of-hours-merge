# ⏰ No Out of Hours Merge (Github Action)
This action blocks merging of pull requests outside of specified business hours or if the PR title does not contain 'hotfix:'.

## Usage

To use this action, add the following step to your workflow:

```yaml
- name: No Weekend Merge
  uses: your-github-username/no-weekend-merge-action@main
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    pr_title: ${{ env.CI_PR_TITLE }}
