# File States {#file-states}

[i[File States]<]

We've talked about this quite a bit in passing already.

If you create a new file, you have to `git add` it to the stage before
you commit.

If you modify a file, you should `git add` it to the stage before you
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
  about this file (e.g. you just created it in the working tree and
  haven't added it). Git will ignore it, but you'll see it in the
  status.

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
* **Unmodified** → edit `foo.txt` → **Modified**  (with your favorite editor)
* **Staged** → `git commit` → **Unmodified**
* **Staged** → `git restore --staged` → **Modified**

Again, `git status` will often give you advice of how to undo a state
change.

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

## Files In Multiple States

[i[File States-->Multiple]]
A file can actually sort of exist in multiple states at once. To be more
technically accurate, there can be copies of files which are in
different states than one another. For instance, you might have one
version of a file on the stage, and another version of that file, with
different modifications, in your working tree *at the same time*.
Technically these are actually different files since they don't contain
the same data.

Just remember that when you stage a file, it effectively stages a
**copy** of that file as it exists right then. There is nothing stopping
you from making another modification to the file in the working tree and
ending up like this, where one version of the file is on the stage ready
to commit, and another one is in the working tree with additional
changes not-yet-staged:

``` {.default}
$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  modified:   foo.txt

  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working
    directory)
	  modified:   foo.txt
```

You can overwrite the version on the stage by adding it again. And
various incantations of `restore` can change the files in different
ways. Look up the `--staged` and `--worktree` options for `git restore`.

I'll leave how to move files around in these simultaneous states as an
exercise to the reader, but I wanted you to at least be aware of it.

[i[File States]>]
