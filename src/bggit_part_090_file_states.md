# File States

[i[File States]<]

We've talked about this quite a bit in passing already.

If you create a new file, you have to `git add` it to the stage before
you commit.

If you modify a file, you have to `git add` it to the stage before you
commit.

If you add a file `foo.txt` to the stage, you can remove it from the
stage before you commit with `git restore --staged foo.txt`.

So clearly files can exist in a variety of "states" and we can move them
around between those states.

To figure out what state a file is in and get a hint on how to "undo" it
from that state, `git status` is your best friend (except in the case of
renaming, but more on that mess soon).

## What States Can Files in Git Be In?

There are four of them: **Untracked**, **Unmodified**, **Modified**, and
**Staged**.

* [i[File States-->Untracked]] **Untracked**: Git does not know anything
  about this file (e.g. you just created it in the repo). Git will
  ignore it, but you'll see it in the status.

  You can make Git aware of this file by moving it to Staged State with
  `git add`.

  Or you can simply remove the file if you don't want it to exist, or
  you can add it to your `.gitignore` if you want to leave it in place
  but still have Git ignore it.

* [i[File States-->Unmodified]] **Unmodified**: Git knows about this
  file and it's in the repo. But you haven't made any changes to it
  since it was last committed.

  You can move this file to Modified State by making changes to the file
  (and saving).

  You can remove this file with `git rm`, which changes the removed file
  to the Staged State. (Wait—removing the file puts it on the stage?
  Yes! More on that later.)

* [i[File States-->Modified]] **Modified**: Git knows about this file
  and knows that you've changed it. It's ready for you to stage those
  changes or to undo them.

  You can change the file to Staged State with `git add`.

  You can change the file to Unmodified State (throwing away your
  changes) with `git restore`.

* [i[File States-->Staged]] **Staged**: The file is ready to be included
  in the next commit.

  You can change to Unmodified State by making a commit with `git
  commit`.

  You can remove the file from the stage and back to Modified State with
  `git restore --staged`.

[i[Workflow-->File states]] A file typically goes through this process
to be added to a repo:

1. The user creates a new file and saves it. This file is **Untracked**.

2. The user adds the file with `git add`. The file is now **Staged**.

3. The user commits the file with `git commit`. The file is now
   **Unmodified** and is part of the repo and ready to go.

After it's in the repo, the typical file life cycle only differs by the
first step:

1. The user changes the file and saves it. The file is now **Modified**.

2. The user adds the file with `git add`. The file is now **Staged**.

3. The user commits the file with `git commit`. The file is now
   **Unmodified** and is part of the repo and ready to go.

Keep in mind that often a commit is a bundle of different changes to
different files. All those files would be added to the stage before the
single commit.

Here's a partial list of ways to change state:

* **Untracked** → `git add foo.txt` → **Staged** (as "new file")
* **Modified** → `git add foo.txt` → **Staged**
* **Modified** → `git restore foo.txt` → **Unmodified**
* **Unmodified** → `edit foo.txt` → **Modified**  (with your favorite editor)
* **Staged** → `git commit` → **Unmodified**
* **Staged** → `git restore --staged` → **Modified**

Again, `git status` will often give you advice of how to undo a state
change.

## Renaming Files

[i[Renaming]]

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

But what if we want to undo the rename?

Git suggests `git restore --staged` to the rescue... But which file name
to use, the old one or new one? And then what? It turns out that while
you *can* use `git restore` to undo this by following it with multiple
other commands, you should, in this case, ignore Git's advice.

[i[Renaming-->Reverting]] Just remember this part: **the easiest way to
undo a Staged rename is to just do the reverse rename**.

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

```
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

## Removing Files

[i[Removing files]]

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

But what if we want to undo the staging of the now-deleted file? There's
a hint for how to get it back with `git restore --staged`, as per usual.

Let's try it:

``` {.default}
$ git restore --staged foo.txt
$ git status
  On branch main
  Changes not staged for commit:
    (use "git add/rm <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
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

Later we'll talk about ways to recover a deleted file from an earlier
commit. But one way you already know: check out the earlier commit where
the file exists, copy the file into a new Untracked file, checkout the
branch where the file will be restored to, rename the Untracked file to
the name of the restored file, then add it and commit.

> **Note**: Just because you remove a file and push your changes doesn't
> mean the file is permanently gone. It's still in the repo, part of
> whatever commits it was previously seen with.
>
> If you accidentally commit something that should be secret, you should
> consider that secret compromised and change it where it is used. It
> will be visible to anyone who clones the repo and sees that commit.
>
> There are ways around this if you haven't yet pushed, but that's
> beyond the scope of this guide.

## Unmodified to Untracked

[i[Untracking files]]

A variation of `git rm` tells Git to remove the file from the repo but
leave it intact in the working tree. Maybe you want to keep the file
around but don't want Git to track it any longer.

To make this happen, you use the `--cached` switch.

Here's an example where we remove the file `foo.txt` from the repo but
keep it around in our working tree:

``` {.default}
$ ls
  foo.txt

$ git rm --cached foo.txt
  rm 'foo.txt'

$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  deleted:    foo.txt

  Untracked files:
    (use "git add <file>..." to include in what will be committed)
	  foo.txt

$ ls
  foo.txt
```

There you see in the `status` output that Git has staged the file for
deletion, but it's also mentioning that the file exists and is
untracked. And a subsequent `ls` shows that the file still exists.

At this point, you can commit and the file would then be in Untracked
state.

[i[File States]>]
