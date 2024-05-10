# Contributing

## Repository Structure
TBD

## Branch Structure
This repo will use a trunk based workflow with "main" being the trunk.
Branches will be prefixed with a category name and can be categorized as such:

- `archive/name` Previous implementations of the exhibit for historical and reference. These branches will be rarely - if ever - modified
- `release/0.0.0` [Semver](https://semver.org/) release number. These branches denote stable releases and can have commits cherry-picked from `main` for bug-fixes as needed
- `bugfix/bug-name` Branch intended to fix a specific bug and intended to be cherry-picked to release branches after being merged into `main`
- `feature/feature-name` Branch intended to add a specific feature.

Repository maintainers can create bugfix and feature branches in the main repository or in their own fork.
Non-maintainers will have to create a fork and create their branches there.

## Pull Requests
Pull requests will occur before merging into main.
Work in Progress PRs to track progress and discus major features as they are developed are acceptable but should be marked as drafts and contain "WIP" in the title until they are ready for review.
The "Assignee" feature will be used to denote the person or people responsible for seeing the PR though - such as reaching out to reviewers to review, making requested changes, and generally taking responsibility for the request.
By default this is the developer who wrote the majority of the changes in the request.
WIP PRs without activity for a significant period of time will be closed. 

## Merging Pull Requests
Each PR must be reviewed by at least one maintainer before being accepted and merged.
Upon merging, the "Squash and Merge" option should be selected to maintain a clean git history.
After merging, the branch should be deleted if was not pulled from a fork.
