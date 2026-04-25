# 📋 Git Cheat Sheet

## Setup
| Command | Description |
|---------|-------------|
| `git config --global user.name "Name"` | Set global username |
| `git config --global user.email "email"` | Set global email |
| `git config --list` | View all config values |

## Basics
| Command | Description |
|---------|-------------|
| `git init` | Initialise a new repo |
| `git clone <url>` | Clone a remote repo |
| `git status` | Show working tree status |
| `git add .` | Stage all changes |
| `git add <file>` | Stage a specific file |
| `git commit -m "msg"` | Commit with message |

## Branching
| Command | Description |
|---------|-------------|
| `git branch` | List local branches |
| `git branch -a` | List all branches (local + remote) |
| `git checkout -b <name>` | Create and switch to branch |
| `git checkout <name>` | Switch to existing branch |
| `git branch -d <name>` | Delete a branch |
| `git push origin <name>` | Push branch to remote |

## Merging & Rebasing
| Command | Description |
|---------|-------------|
| `git merge <branch>` | Merge branch into current |
| `git merge --no-ff <branch>` | Merge with explicit merge commit |
| `git rebase <branch>` | Rebase current branch onto another |
| `git rebase --abort` | Abort an in-progress rebase |

## Stashing
| Command | Description |
|---------|-------------|
| `git stash` | Stash current changes |
| `git stash list` | List all stashes |
| `git stash pop` | Apply and remove latest stash |
| `git stash push -m "label"` | Stash with a name |
| `git stash drop stash@{0}` | Delete a specific stash |

## History & Inspection
| Command | Description |
|---------|-------------|
| `git log --oneline` | Compact commit history |
| `git log --oneline --graph --all` | Visual branch tree |
| `git log --author="Name"` | Filter by author |
| `git log --since="2 days ago"` | Filter by date |
| `git log --grep="feat"` | Filter by message keyword |
| `git log -p <file>` | History of a specific file |
| `git blame <file>` | See who changed each line |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |

## Undoing
| Command | Description |
|---------|-------------|
| `git reset --soft HEAD~1` | Undo commit, keep changes staged |
| `git reset --mixed HEAD~1` | Undo commit, keep changes unstaged |
| `git reset --hard HEAD~1` | Undo commit, discard all changes |
| `git revert HEAD` | Create a new undo commit (safe) |
| `git revert <hash>` | Revert a specific commit |

## Advanced
| Command | Description |
|---------|-------------|
| `git cherry-pick <hash>` | Copy a commit to current branch |
| `git fetch` | Download remote changes (no merge) |
| `git pull` | Fetch + merge remote changes |
| `git push --force-with-lease` | Safe force push |
| `git remote -v` | View remote URLs |

## Conventional Commit Types
| Type | When to use |
|------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `chore:` | Build, config, or tooling changes |
| `refactor:` | Code restructure (no feature/fix) |
| `test:` | Adding or updating tests |
| `style:` | Formatting, whitespace (no logic change) |