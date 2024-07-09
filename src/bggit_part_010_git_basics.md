# Git Basics

Welcome to the _Beej's Guide to Git_!

This guide has two goals, in no particular order:

1. Help you get some familiarity with Git syntax on the command line.
2. Help you get a mental model that describes how Git stores its
   information.

I feel the second of these is very important for becoming even remotely
adept at using Git, which is why I spend so much time talking about it.
Yes, you can get by with a cheat-sheet of common Git commands, but if
you want to fearlessly use the tool to its full effectiveness, you gotta
learn the internals!

## What is Git?

Git is a _source code control system_, also known as a _version control
system_.

Clear? OK, not really? Let's dive in a bit more, then!

Git's main job is to keep a log of _snapshots_ of the current state of
all your source code in a particular directory tree.

The idea is that you'll make some changes (to implement a feature, for
example), and then you'll _commit_ those changes to the _source code
repo_ (repository) once the feature is ready.

And if you ever change something you didn't want to, or your want to see
how things were implemented in the past, you can always _check out_ a
previous commit and take a look.

Git keeps a history of all the commits you've ever made. Assuming
nothing criminal is happening, this should be a great relief to you; if
you accidentally delete a bunch of code, you can look at a previous
commit and get it all back.

But that's not all! As we'll see, Git also works well as a remote backup
mechanism, and works wonderfully when cooperating with a team on the
same codebase.

Definitions:

* **Source Code Control System**/**Version Control System**: Software
  that manages changes to a software project potentially consisting of
  thousands of source files edited by potentially hundreds of
  developers. Git is a source code control system. There are many
  others.

* **Commit**: An explicit moment in time where a snapshot of the
  contents of all the source files are recorded in the source code
  control system.

* **Repo**/**Source Code Repository**: This is where a particular
  software project is stored in the source code control system.
  Typically each project has its own repo. For example, you might
  "create a Git repo" to hold a new project you're working on.

  Sometimes repos are local to your computer, and sometimes they're
  stored on other, remote computers.

* **Check out**: To look at a particular commit (or branch—more later).

## What is GitHub?

[fl[GitHub|https://github.com/]] is **not** Git.

## What is GitHub?

Oh, more?

[GitHub](https://github.com/) is a website that provides a front end to
a lot of Git features, and some additional GitHub-specific features, as
well.

It also provides remote storage for your repo, which acts as a backup.

Takeaway: GitHub is a web-based front-end to Git (specifically one that
works on the copy of your repo at GitHub—stay tuned for more on that
later).

> [fl[GitLab|https://gitlab.com]] is a competitor to GitHub.
> [fl[Gitea|https://docs.gitea.com/]] is an open-source competitor that
> allows you to basically run a GitHub-like front-end on your own
> server. None of this information is immediately important.

## The Most Basic Git Workflow

There's a super-common workflow that you'll use repeatedly:

1. _Clone_ a _remote_ repo. The remote repo is commonly on GitHub, but
   not necessarily.
2. Make some local changes.
3. Add those changes to the _stage_.
4. _Commit_ those changes.
5. _Push_ your changes back to the remote repo.
6. Go back to Step 2.

This is not the only workflow; there are others that are also not
uncommon.

Definitions:

* **Clone** (verb): to make a copy of a remote repo locally.

* **Clone** (noun): a local copy of a remote repo.

* **Remote**: In Git, a clone of a repo in another location.

* **Stage**: In Git, a place you add copies of files to in preparation
  for a commit. The commit will include all the files that you've placed
  on the stage. It will not include files you haven't placed on the
  stage, even if you've modified those files.

## What is Cloning?

First, some backstory.

Git is what's known as a _distributed_ version control system. This
means that, unlike many version control systems, there's no one central
authority for the data. (Though commonly Git users treat a site like
GitHub in this regard, loosely.)

Instead, Git has _clones_ of repos. These are complete, standalone
copies of the entire commit history of that repo. Any clone can be
recreated from any other. None of them are more powerful than any
others.

Looking back at The Most Basic Git Workflow, above, we see that Step 1
is to clone an existing repo.

If you're doing this from GitHub, it means you're making a local copy of
an entire, existing GitHub repo.

Making a clone is a one time-process, typically (though you can make as
many as you want).

Definitions:

* **Distributed Version Control System**: A VCS in which there is no
  central authority of the data, and multiple clones of a repo exist.

  This means after you clone a repo, there are two: one that is remote,
  and one that is local to your computer.

  These clones are completely separate and changes you make to your
  local repo will not be reflected in the remote clone. Unless, that is,
  you explicitly make them interact.

## How Do Clones Interact?

After you make a clone, there are two major operations you typically
use:

* **Push**: This takes your local commits and uploads them to the remote
  repo.

* **Pull**: This takes the remote commits and downloads them to your
  local repo.

Behind the scenes, there's a process going on called a _merge_, but
we'll talk more about that later.

Until you push, your local changes aren't visible on the remote repo.

Until you pull, the changes on the remote repo aren't visible on your
local repo.

## Actual Git Usage

Let's put all this into play. This section assumes you have the
command line Git tools installed. It also generally assumes you're
running a Unix shell like Bash or Zsh.

> Linux/BSD/Unix and Mac users will already have these shells.
> Recommendation for Windows users is to
> [fl[install and run Ubuntu with WSL|https://learn.microsoft.com/en-us/windows/wsl/]]
> to get a virtual Linux installation.

For this example, we'll assume we have a GitHub repo already in
existence that we're going to clone.

Recall the process in The Most Basic Git Workflow, above:

1. _Clone_ a _remote_ repo. The remote repo is commonly on GitHub, but
   not necessarily.
2. Make some local changes.
3. Add those changes to the _stage_.
4. _Commit_ those changes.
5. _Push_ your changes back to the remote repo.
6. Go back to Step 2.

### Step 0: One-time Setup

"Wait! You didn't say there was a Step 0!"

Yes, one time, before you start using Git, you should tell it what your
name and email address are. These will be attached to the commits
you make to the repo.

You can change them any time in the future, and you can even set them on
a per-repo basis. But for now, let's set them globally so Git doesn't
complain when you make a commit.

You just have to do this once then never again (unless you want to).

Type both of these on the command line, filling in the appropriate
information.

> **NOTE**: in this guide, things you type at the shell prompt are
> indicated by a prefaced `$`. Don't type the `$`; just type what
> follows it. Your actual shell prompt might be `%` or `$` or something
> else, but here we use the `$` to indicate it.

``` {.default}
$ git config --global user.name "Your Name"
$ git config --global user.email "your-email@example.com"
```

If you need to change them in the future, just run those commands again.

### Step 1: Clone an Existing Repo

Let's clone a repo! Here's an example one you can actually use. Don't
worry--you can't mess anything up on the remote repo even though (and
because) you don't own it.

> Like we said before, this isn't the only workflow. Sometimes people
> make a local repo first, add some commits, then create a remote repo
> and push those commits. But for this example, we'll assume the remote
> repo exists first, though this isn't a requirement.

Switch in a subdirectory where you want the clone created. This command
will create a new subdirectory out of there that will hold all the repo
files.

(In the example, anything that begins with `$` represents the shell
prompt indicating this is input, not output. Don't type the `$`; just
type in the part after it.)

``` {.default}
$ git clone https://github.com/beejjorgensen/git-example-repo.git
```

You should see some output similar to this:

``` {.default}
Cloning into 'git-example-repo'...
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 4 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), done.
```

Congratulations! You have a clone of the repo. Let's have a peek:

``` {.default}
$ cd git-example-repo
$ ls -la
```

And we see a number of files:

``` {.default}
total 16
drwxr-xr-x   5 user  user  160 Jan 26 11:50 .
drwxr-xr-x  14 user  user  448 Jan 26 11:50 ..
drwxr-xr-x  12 user  user  384 Jan 26 11:50 .git
-rw-r--r--   1 user  user   65 Jan 26 11:50 README.md
-rwxr-xr-x   1 user  user   47 Jan 26 11:50 hello.py
```

There are two files in this repo: `README.md` and `hello.py`.

> The directory `.git` has special meaning; it's the directory where Git
> keeps all its metadata and commits. You can look in there, but you
> don't have to. If you do look, don't change anything. The only thing
> that makes a directory a Git repo is the presence of a valid `.git`
> directory within it.

Let's ask Git what it things the current status of the local repo is:

``` {.default}
$ git status
```

Gives us:

``` {.default}
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

There's a lot of information here, surprisingly.

We haven't talked about branching yet, but this is letting us know we're
on branch `main`. That's fine for now.

It also tells us this branch is up to date with a branch called
`origin/main`. A branch in Git is just a reference to a certain commit
that's been made, like a PostIt note attached to that commit. (Recall
that a commit is a snapshot of the code repo at some time.)

We don't want to get caught up in the intricacies of branching right
now, but bear with me for a couple paragraphs.

`origin` is an alias for the remote repository that we originally cloned
from, so `origin/main` is "branch `main` on the repo you originally
cloned from".

There is one important thing to notice here: there are two `main`
branches. There's the `main` branch on your local repo, and there's a
corresponding `main` branch on the remote (`origin`) repo.

Remember how clones are separate? That is, changes you make on one clone
aren't automatically visible on the other? This is an indication of
that. You can make changes your your local `main` branch, and these
won't affect the remotes `origin/main` branch. (At least, not until you
push those changes!)

Lastly, it mentions we're up-to-date with the latest version of
`origin/main` (that we know of), and that there's nothing to commit
because there are no local changes. We're not sure what that means yet,
but it all sounds like vaguely good news.

### Step 2: Make Some Local Changes

Let's edit a file and make some changes to it.

> Again, don't worry about messing up the remote repo—you don't have
> permissions to do that. Your safety is completely assured from a Git
> perspective.

If you're using VS Code, you can run it in the current directory like so:

``` {.default}
$ code .
```

Otherwise, open the code in your favorite editor, which, admit it, is
[fl[Vim|https://www.vim.org/]].

Let's change `hello.py`:

It was:

``` {.py}
#!/usr/bin/env python

print("Hello, world!")
```

but let's add a line so it reads:

``` {.py}
#!/usr/bin/env python

print("Hello, world!")
print("Hello, again!")
```

And save that file.

Let's ask Git what the status is now.

``` {.default}
$ git status

On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   hello.py

no changes added to commit (use "git add" and/or "git commit -a")
```

This is telling us a couple important things.

First, Git has detected that we modified a file, namely `hello.py`,
which we did.

But it also says there are `no changes added to commit` (i.e. "there is
nothing to make a commit with"). What does that mean?

It means we haven't added anything to the _stage_ yet. Recall that the
stage is where we can place items that we wish to include in the next
commit. Let's try that.

### Step 3: Add Changes to the Stage

The Git status message, above, is trying to help us out. It says:

``` {.default}
no changes added to commit (use "git add" and/or "git commit -a")
```

It's suggesting that `git add` will add things to the stage—and it will.

Now we, the developers, know that we modified `hello.py`, and that we'd
like to make a commit that reflects the changes to that file. So we need
to first add it to the stage so that we can make a commit.

Let's do it:

``` {.default}
$ git add hello.py
$ git status

On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   hello.py
```

Now it's changed from saying "Changes not staged for commit" to saying
"Changes to be committed", so we have successfully copied `hello.py` to
the stage!

> There's also a helpful message there about how to _unstage_ the file.
> Let's say you accidentally added it to the stage and you changed your
> mind and wanted to not include it in the commit after all. You can run
>
> ``` {.default}
> $ git restore --staged hello.py
> ```
> <!-- ` vim markdown highlight bug workaround -->
>
> and that will change it back to the "Changes not staged for commit"
> state.

### Step 4: Commit those Changes

Now that we have something copied to the stage, we can make a commit.
Recall that a commit is just a snapshot of the state of the repo given
the modified files on the stage. Modified files not on the stage will
not be included in the snapshot. Unmodified files are automatically
included in the snapshot.

In short, the commit snapshot will contain all the unmodified files Git
currently tracks plus the modified files that are on the stage.

Let's do it:

``` {.default}
$ git commit -m "I added another print line"

[main 0e1ad42] I added another print line
 1 file changed, 1 insertion(+)
```

> The `-m` switch allows you to specify a commit message. If you don't
> use `-m`, you'll be popped into an editor, which will probably be Nano
> or Vim, to edit the commit message. If you're not familiar with those,
> see [Getting Out of Editors](#editor-get-out) for help.

And that's good news! Let's check the status:

``` {.default}
$ git status

On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

"Nothing to commit, working tree clean" means we have no local changes
to our branch.

But look! We're "ahead of 'origin/main' by 1 commit"! This means our
local commit history on the `main` branch has one commit that the remote
commit history on its `main` branch does not have.

Which makes sense—the remote repo is a clone and so it's independent of
our local repo unless we specifically try to sync them up. It doesn't
magically know that we've made changes to our local repo.

And Git is helpfully telling us to run `git push` if we want to update
the remote repo so that it also has our changes.

So let's try to do that. Let's push our local changes to the remote
repo.

### Step 5: Push Your Changes to the Remote Repo

Let's push our local changes to the remote repo:

``` {.default}
$ git push
```

And that produces:

``` {.default}
Username for 'https://github.com':
```

Uh oh—trouble brewing. Let's try entering our credentials:

``` {.default}
Username for 'https://github.com': my_username
Password for 'https://beejjorgensen@github.com': [my_password]
remote: Support for password authentication was removed on August
        13, 2021.
remote: Please see https://docs.github.com/en/get-started/getting-
        started-with-git/about-remote-repositories#cloning-with-
        https-urls for information on currently recommended modes
        of authentication.
fatal: Authentication failed for 'https://github.com/beejjorgensen/
       git-example-repo.git/'
```

Well, that's all kinds of not-working. Largely this is because you don't
have permission to write to that repo since you're not the owner. And,
notably, support for authenticating with a password seems to have been
removed in 2021 which, last I checked, was in the past.

So what do we do? Firstly, we should be the owner of the GitHub repo
that we've cloned and that'll solve some of the permission problems.
Secondly, we'd better find another way to authenticate ourselves to
GitHub that's not plain password.

Let's try that in the next section.

