# Quick Reference

<!-- BOOKMARK: alias -->

Quickly look up commands based on what you want to do! Caveat: this list
is grotesquely incomplete! See your man pages for more info!

In this reference section we use the following substitutions:

* `URL`: Some URL either SSH, HTTP, or even a local file, usually the
  URL you cloned from.
* `FILE`: Path to file, e.g. `foo/bar.txt`, etc.
* `DIR`: Path to directory, e.g. `foo/`, etc.
* `PATH`: Path to directory or file
* `BRANCH`: Some branch name, e.g. `main`, etc.
* `REMOTE`: A remote name, e.g. `origin`, `upstream`, etc.
* `UUID`: Some commit UUID—you can get a commit UUID from `git log` or
  `git reflog`.
* `CMMT`: a UUID, branch, etc. Anything that refers to a commit.
  Officially this is called a _tree-ish_, but that was more letters than
  I wanted to repeatedly type.
* `VARIABLE`: a Git config variable name, usually words separated by
  periods.
* `VALUE`: an arbitrary value for Git configs.

Also, don't type the `$`—it's the shell prompt. And everything after a
`#` is a comment. A backslash `\` at the end of a line indicates that it
continues on the next line.

## Glossary 

* **Clone**: a duplicate (or to duplicate) a remote repo, commonly for
  local use.
* **Commit**: a snapshot of all the files in the repo at a point in
  time.
* **Fork**: a GitHub construct to make a clone of someone else's GitHub
  repo under your GitHub account.
* **`HEAD`**: the commit that is currently checked out/switched to.
* **Index**: another name for the *stage*.
* **`main`**: the default name of the first branch created.
* **`master`**: the historical name for `main`.
* **`origin`**: the default name for the remote from which this repo was
  cloned.
* **Pull request**: a way to get changes you made in your fork of a repo
  back into the repo you forked from.
* **Remote**: an alias for a URL to another repo. Usually an HTTP or SSH
  URL.
* **Stage**: where you collect files to be bundled into a
  commit.
* **`upstream`**: the conventional name of the remote that you forked
  from. Not set up automatically.
* **Working Tree**: the collection of files you can see, which might
  have changes from the commit at `HEAD`.
* **WT**: shorthand for working tree.

## File States

* **Untracked** to:
  * Unmodified: `git add FILE`
* **Unmodified** to:
  * Modified: Edit with your editor and save
  * Untracked/deleted: `git rm --cached FILE`
* **Modified** to:
  * Staged: `git add FILE`
  * Unmodified: `git restore FILE` (discards changes)
  * Untracked/deleted: `git rm --cached FILE`
* **Staged**
  * Unmodified: `git commit FILE` (finalize commit)
  * Modified: `git restore --staged FILE` (unstage)
  * Both modified: `git checkout --merged FILE` (during merge)

## Configuration

For all `git config` commands, specify `--global` for a universal
setting or leave it off to set the value just for this repo.

``` {.default}
$ git config set VARIABLE VALUE
$ git config get VARIABLE
$ git config list
$ git config unset VARIABLE
$ git config --edit
```

### Set identity

Username and email:

``` {.default}
$ git config set --global user.name "Your Name"
$ git config set --global user.email "your-email@example.com"
```

SSH identity:

``` {.default}
$ git config set core.sshCommand \
    "ssh -i ~/.ssh/id_alterego_ed25519 -F none"
```

### Set default pull behavior to merge or rebase

``` {.default}
$ git config set --global pull.rebase false   # Merge
$ git config set --global pull.rebase true    # Rebase
```

### Set default editor, difftool, and mergetool

Set the default editor to Vim, and the default mergetool and difftool to
Vimdiff, turn off prompting for the tools, and turn off mergetool
backups:

``` {.default}
$ git config set core.editor vim
$ git config set diff.tool vimdiff
$ git config set difftool.prompt false
$ git config set difftool.vimdiff.cmd 'vimdiff "$LOCAL" "$REMOTE"'
$ git config set merge.tool=vimdiff
$ git config set mergetool.vimdiff.cmd \
                             'vimdiff "$LOCAL" "$REMOTE" "$MERGED"'
$ git config --global set mergetool.keepBackup false
```

### Colorful Git output

``` {.default}
$ git config set color.ui true   # Or false
```

### Autocorrect

Autocorrect will automatically run the command it thinks you meant. For
example, if you `git poush`, it will assume you meant `git push`.

``` {.default}
$ git config set help.autocorrect 0   # Ask "Did you mean...?"
$ git config set help.autocorrect 7   # Wait 0.7 seconds before run

$ git config set help.autocorrect immediate  # Just guess and go
$ git config set help.autocorrect prompt     # Prompt then go
$ git config set help.autocorrect never      # Turn autocorrect off
```

### Newline translation

Handle automatic newline translation. Recommend set to true for Windows
(not WSL) and false everywhere else.

``` {.default}
$ git config set core.autocrlf true  # Windows (non-WSL)
$ git config set core.autocrlf false # WSL, Linux, Mac, C64, etc.
```

Obsolete commands for older versions:

``` {.default}
git config user.email                     # Get
git config user.email "user@example.com"  # Set
git config --unset user.email             # Delete
git config --list                         # List
git config --edit                         # Edit
```

### Aliases

Setting aliases, some examples:

``` {.default}
$ git config set --global alias.logn 'log --name-only'
$ git config set alias.aa "add --all"
$ git config set alias.logc "log --oneline --graph --decorate"
$ git config set alias.diffs "diff --staged"
$ git config set alias.lol "log --graph"\
" --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s"\
" %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

Getting aliases:

``` {.default}
$ git config get alias.logx
$ git config get --all --show-names --regexp '^alias\.'
$ git config set alias.aliases \
    "config get --all --show-names --regexp '^alias\.'"
```

Tracing an alias run:

``` {.default}
$ GIT_TRACE=1 git logx
```

## Creating and Cloning Repos

``` {.default}
$ git clone URL       # Clone a URL
$ git clone URL DIR   # Clone a URL to directory
$ git init DIR        # Init repo at directory
$ git init .          # Init repo in the current directory
```

## Adding, Renaming, Deleting, Committing

``` {.default}
$ git add PATH             # Add PATH to the repo
$ git mv FILE1 FILE2       # Rename ("Move") FILE1 to FILE2
$ git mv FILE2 FILE1       # Undo the above rename
$ git rm FILE              # Delete ("Remove") FILE
$ git add -p FILE          # Add file in patch mode

$ git commit               # Commit files on stage
$ git commit -m "message"  # Commit with a message
```

Amending commits—don't amend commits you have pushed unless you know
what you're getting into!

``` {.default}
$ git commit --amend               # Amend last commit
$ git commit --amend -m "message"  # Amend with commit message
$ git commit --amend --no-edit     # Don't change commit message
```

To undelete a staged file, run these two commands in sequence:

``` {.default}
$ git restore --staged FILE
$ git restore FILE
```

To undelete a deleted file, you could manually recover it from an old
commit, or revert the commit that deleted it.

## Getting Status

``` {.default}
$ git status             # Show current file states
$ git log                # Show the commit logs
$ git log --name-only    # Also list changed files
$ git log CMMT           # Show log from a specific branch
$ git log CMMT1 CMMT2    # Show logs from multiple branches

$ git log CMMT1..CMMT2   # Show logs from CMMT2 since it
                         # diverged from CMMT1
$ git log CMMT1...CMMT2  # Show logs from CMMT1 and CMMT2
                         # since they diverged
```

## Getting a Diff

``` {.default}
$ git diff                # Diffs between working tree and stage
$ git diff HEAD^          # Diff from the previous commit to here
$ git diff HEAD^^         # Diff from the 2nd last commit to here
$ git diff HEAD~3 HEAD~2  # Diff from 3rd last to 2nd last commit
$ git diff CMMT           # Diff between CMMT and now
$ git diff CMMT1 CMMT2    # Diff between two commits (older first)

$ git diff CMMT1...CMMT2  # Diff between CMMT2 and the common
                          # ancestor of CMMT1 and CMMT2

$ git diff HEAD~3^!       # Diff between HEAD~3 and its parent
$ git diff -- FILE        # Run a diff just for a specific file
$ git diff HEAD^ -- FILE  # Run a diff just for a specific file

$ git diff -U5          # Show 5 lines of context
$ git diff -w           # Ignore whitespace
$ git diff --name-only  # Only show filenames of changed files
$ git diff --staged     # Diffs between stage and repo
$ git difftool          # Diffs using the configured difftool
```

## Branches

A local branch looks like `branchname`. A remote tracking branch looks
like `remote/branchname`.

``` {.default}
$ git switch BRANCH         # Switch to a branch
$ git switch --detach UUID  # Detach HEAD to a commit
$ git switch -              # Switch back to previous commit
```

``` {.default}
$ git switch --detach HEAD^   # Switch to previous commit
$ git switch --detach HEAD^^  # Switch to 2 commit ago
$ git switch --detach HEAD~3  # Switch to 3 commits ago
$ git switch --detach HEAD~99 # Switch to 99 commits ago
```

``` {.default}
$ git switch main   # Reattach HEAD to main
```

``` {.default}
$ git branch -v   # List all branches
$ git branch -va  # List all including remote tracking branches
```

``` {.default}
$ git switch -c BRANCH        # Create and switch to BRANCH
$ git branch BRANCH           # Create BRANCH at HEAD
$ git branch BRANCH1 BRANCH2  # Create BRANCH1 at BRANCH2
```

``` {.default}
$ git branch -d BRANCH   # Delete fully merged branch
$ git branch -D BRANCH   # Force delete unmerged branch
```

Obsolete style (use `switch` if you can):

``` {.default}
$ git checkout CMMT      # Detach HEAD to a commit
$ git checkout HEAD^     # Detach HEAD to previous commit
$ git checkout HEAD~2    # Detach HEAD to second previous commit
```

## Pulling and Pushing, and Fetching

``` {.default}
$ git pull               # Pull from remote and merge or rebase
$ git pull --ff-only     # Only allow fast-forward merges
$ git pull --rebase      # Force a rebase on pull
$ git pull --no-rebase   # Force a merge on pull
```

``` {.default}
$ git push                     # Push this branch to its remote

$ git push REMOTE BRANCH       # Create remote tracking branch and
                               # push to remote

$ git push -u REMOTE BRANCH    # Create remote tracking branch and
                               # push to remote, and use subsequent
                               # `git push` commands for this local
                               # branch

$ git push -u origin branch99  # Example
```

``` {.default}
$ git fetch        # Get data from remote but don't merge or rebase
$ git fetch REMOTE # Same, for a specific remote

```
## Merging

``` {.default}
$ git merge CMMT     # Merge commit or branch into HEAD
$ git merge --abort  # Rollback the current merge
$ git mergetool      # Run mergetool to resolve a conflict

$ git checkout --merged FILE   # Unstage resolved files
```

In a conflict occurs, you can always `--abort`. Otherwise:

1. Fix the conflict.
2. Add the fixed files.
3. Commit to complete the merge.

## Remotes

``` {.default}
$ git remote -v                       # List remotes
$ git remote set-url REMOTE URL       # Change remote's URL
$ git remote add REMOTE URL           # Add a new remote
$ git remote rename REMOTE1 REMOTE2   # Rename REMOTE1 to REMOTE2
$ git remote remove REMOTE            # Delete REMOTE
```

## Ignoring Files

Add a `.gitignore` file to your repo. It applies to this directory and
all non-submodule subdirectories below it. Add descriptions of files to
ignore to this file. Comments behind `#` are allowed. Blank lines are
ignored.

Example `.gitignore`:

``` {.default}
foo.aux     # Ignore specific file "foo.aux"
foo.*       # Ignore all files that start with "foo."
*.tmp       # Ignore all files that end with ".tmp"
frotz/      # Ignore all files in the "frotz" directory
foo[12].txt # Ignore "foo1.txt" and "foo2.txt"
foo?        # Ignore "foo" followed by any single character
frotz/bar   # Ignore file "bar" in directory "frotz"
*           # Ignore everything
```

Exceptions to earlier rules, also useful in `.gitignore` files in
subdirectories to override rules from parent directories:

``` {.default}
*.txt       # Ignore all text files
!keep.txt   # Except "keep.txt"
```

## Rebasing

``` {.default}
$ git rebase CMMT        # Rebase changes onto commit

$ git rebase -i CMMT     # Interactive rebase (squashing commits)

$ git rebase --continue  # Continue processing from conflict
$ git rebase --skip      # Skip a conflicting commit
$ git rebase --abort     # Bail out of rebasing

$ git pull --rebase      # Force a rebase on pull
$ git pull --no-rebase   # Force a merge on pull
```

## Stashing

Stashes are stored on a stack.

``` {.default}
$ git stash push    # Stash changed files
$ git stash         # Effectively the same as "push"
$ git stash FILE    # Stash a specific file
$ git stash pop     # Replay stashed files on working tree
$ git stash list    # List stashed files

$ git stash pop 'stash@{1}'   # Pop stash at index 1
$ git stash pop --index 1     # Same thing
$ git stash drop 'stash@{1}'  # Drop stash at index 1
$ git stash drop --index 1    # Same thing
```

## Reverting

``` {.default}
$ git revert CMMT     # Revert a specific commit
$ git revert -n CMMT  # Revert but don't commit (yet)

$ git revert CMMT1 CMMT2    # Revert multiple commits
$ git revert CMMT1^..CMMT2  # Revert a range (oldeest first)

$ git revert --continue  # Continue processing from conflict
$ git revert --skip      # Skip a conflicting commit
$ git revert --abort     # Bail out of reverting
```

## Resetting

All resets move `HEAD` and the current checked out branch to the
specified commit.

``` {.default}
$ git reset --mixed CMMT  # Set stage to CMMT, don't change WT
$ git reset CMMT          # Same as --mixed
$ git reset --soft CMMT   # Don't change stage or working tree
$ git reset --hard CMMT   # Set stage and WT to CMMT

$ git reset -p CMMT       # Reset file in patch mode
```

Obsolete usage:

``` {.default}
$ git reset FILE   # Same as "git restore --staged FILE"
```

## The Reflog

``` {.default}
$ git reflog      # Look at the reflog
```

…I admit this section could use a bit more information.

## Cherry-pick

``` {.default}
$ git cherry-pick CMMT   # Cherry-pick a particular commit
```

## Blame

``` {.default}
$ git blame FILE                # Who is responsible for each line
$ git blame --date=short FILE   # Same, shorter date format
```

