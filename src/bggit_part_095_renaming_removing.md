# Renaming and Removing Files

This is an extension of dealing with file states, so make sure you read
that chapter first!

Also, I'm going to interchangeably use the terms _rename_ and _move_ to
mean the same thing. Moving as a concept is a little more powerful
because not only can it rename, but it can also move files to other
directories. It's notable because the command to rename is `git mv`.

## Renaming Files

[i[Move]<]

You can use the OS rename command to rename files, but if they're in a
Git repo, it's better to `git mv` them so that Git has total awareness.

Git is confusingly unhelpful with this.

Let's rename `foo.txt` to `bar.txt` and get a status:

``` {.default}
$ git mv foo.txt bar.txt
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  renamed:    foo.txt -> bar.txt
```

So it knows the file is renamed, and the file has been moved to the
stage. Like so:

* **Unmodified** → `git mv foo.txt bar.txt` → **Staged** (as "renamed")

And if we look, we see the file has actually been renamed in the
directory to `bar.txt`, as well.

If we make a commit at this point, the file will be renamed in the repo.
Done.

[i[Move-->Reverting]]
But what if we want to undo the rename?

Git suggests `git restore --staged` to the rescue... But which file name
to use, the old one or new one? And then what? It turns out that while
you *can* use `git restore` to undo this by following it with multiple
other commands, you should, in this case, ignore Git's advice.

## Unrenaming Files from the Stage

[i[Move-->Unstaging]<]
Just remember this part: **the easiest way to undo a Staged rename is to
just do the reverse rename**.

Let's say we renamed and got here:

``` {.default}
$ git mv foo.txt bar.txt    # Rename foo.txt to bar.txt
$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  renamed:    foo.txt -> bar.txt
```

This easiest way to revert this change is to do this:

``` {.default}
$ git mv bar.txt foo.txt    # Rename it back to foo.txt
$ git status
  On branch main
  nothing to commit, working tree clean
```

And there you go.

In summary, the way to rename a file is:

* **Unmodified** → `git mv foo.txt bar.txt` → **Staged**
* **Staged** → `git commit` → **Unmodified**

And the way to back out of a Staged rename is to rename them back the
way they were:

* **Staged** → `git mv bar.txt foo.txt` → **Unmodified**

[i[Move-->Unstaging]>]
[i[Move]>]

## Removing Files

[i[Remove]<]

You can use the OS remove command to remove files, but if they're in a
git repo, it's better to `git rm` them so that Git has total awareness.

And what happens might seem a little strange.

Let's say we have a file `foo.txt` that has already been committed. But
we decide to remove it.

``` {.default}
$ git rm foo.txt
  rm 'foo.txt'         # This is Git's output
```

This actually removes the file—if you look in the directory, it's gone.

But let's check the status:

``` {.default}
$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  deleted:    foo.txt
```

So the now-deleted file is in Staged State, as it were.

If we do a commit here, the file is deleted. Done.

## Unremoving Files from the Stage

[i[Remove-->Unstaging]<]
But what if we want to undo the staging of the now-deleted file? There's
a hint for how to get it back with `git restore --staged`, as per usual.

Let's try it:

``` {.default}
$ git restore --staged foo.txt
$ git status
  On branch main
  Changes not staged for commit:
    (use "git add/rm <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working
    directory)
	  deleted:    foo.txt

  no changes added to commit (use "git add" and/or "git commit -a")
```

Hmmm. "Changes not staged for commit" are files in Modified State. This
means that `foo.txt` has been "modified", which is, in this context, a
friendlier way of saying "deleted".

So we've backed up from Staged State to Modified State. But looking
around, the file is still gone! I want my file back!

We want to move it back to Unmodified State, which Git once again hints
how to do in the status: `git restore`. Let's try:

``` {.default}
$ git restore foo.txt
$ git status
  On branch main
  nothing to commit, working tree clean
```

Git's telling us there are no Modified files here. Let's look and see:

``` {.default}
$ ls foo.txt
  foo.txt
```

There it is, back safe and sound.

So the process for deleting a committed file is a variant of what we've
already seen:

* **Unmodified** → `git rm foo.txt` → **Staged**
* **Staged** → `git commit` → The file is now gone

And you can undo a deleted file (as long as the delete hasn't yet been
committed) in the same way you can undo any other file states:

* **Staged** → `git restore --staged foo.txt` → **Modified**
* **Modified** → `git restore foo.txt` → **Unmodified**

[i[Remove-->Unstaging]>]

## Unremoving Files from Earlier Commits

[i[Remove-->Unremoving from earlier commits]<]
What if there's a file that was removed some time ago and you want it
back?

1. Find the commit hash where the file exists.
2. Restore the file from that commit.

Presumably you know the name of the file, but if you don't, you'll have
to painstakingly pore over the logs with `git log --name-only` until you
find it.

But let's say you know the name. In this case, you can get the log for
the deleted file like so (assuming the file we want is `foo.txt`):

``` {.default}
$ git log -- foo.txt
  commit 97bdb61727f7515d6953c965f56ef8329585f348
  Author: User <user@example.com>
  Date:   Sun Jan 12 11:08:33 2025 -0800

      Removed due to horrid commit messages

  commit 1c9bf4514ee90a0e65fb9b0a916765bb6c78dee6
  Author: User <user@example.com>
  Date:   Sun Jan 12 11:08:33 2025 -0800

      Add the barfsplant

  commit cc7a1940f13fca9092dbe9ce4a8e9012babd9314
  Author: User <user@example.com>
  Date:   Sun Jan 12 11:08:33 2025 -0800

      Initial splungification
```

There we see the history of the illustrious `foo.txt`.

We see it was removed in commit `97bdb`. So no point in restoring it
from there (it's already gone by then!). But the commit just _prior_ to
that (`1c9bf`) is the most recent version of `foo.txt` before it was
deleted. That's probably what we want. (Or maybe an earlier one if you
want to go back farther in time—no law against that.)

And the restore is pretty easy:

``` {.default}
$ git restore --source=1c9bf foo.txt
$ ls foo.txt
  foo.txt
```

There it is! But in what state?

``` {.default}
$ git status
  On branch main
  Untracked files:
    (use "git add <file>..." to include in what will be committed)
	  foo.txt
```

It's not even added yet. So if you want to bring it back to life, you'll
have to add and commit it just as if it were a brand new file.

[i[Remove-->Unremoving from earlier commits]>]

## A Note on Removing Secrets

[i[Remove-->Secrets]<]

We've seen that once something is committed and deleted, it's possible
to resurrect that thing.

Now, let's say you've committed some code that looks like this:

``` {.default}
MASTER_PASSWORD_FOR_THE_ENTIRE_COMPANY=7e56e476c58c
```

And then you make the horrible mistake of pushing it.

That's bad enough, but let's say it's even worse and you pushed it to a
repo on GitHub that has public access.

Now the entire world has your password! You're hosed!

"But wait! I'll just remove it real fast and push and no one will
notice!"

No. The company can't take that chance. Anyone can clone the repo and
look back in the history to get the deleted file. The only recourse is
to change that password immediately. Throughout the entire company. That
is what **must** happen. Your manager is not amused.

> **Protip: Never, EVER commit secrets to Git.** Use a dot-env file or
> literally anything other than committing the secret.

Let's make it less severe. Let's say you've pushed to GitHub, but it's a
private repo. It's still kinda bad. You have to trust everyone who has
access, and trust that no clones of the repo will ever end up in the
hands of anyone outside the company or those of any disgruntled
employees. The only recourse is to change that password.

Okay. Let's make it less severe, still. Let's say you've committed the
password to your repo, *but you haven't yet pushed*.

Now we can do something about it because there's no chance anyone other
than you has seen the code. You didn't push it, so no one can have
pulled it. But we'll not talk about that here; see the chapter on
[Amending Commits](#amend) for fixing the file before the push.

[i[Remove-->Secrets]>]

[i[Remove]>]

[i[Remove]>]
