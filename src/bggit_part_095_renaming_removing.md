# Renaming and Removing Files

This is an extension of dealing with file states, so make sure you read
that chapter first!

Also, I'm going to interchangeably use the terms _rename_ and _move_ to
mean the same thing. Moving as a concept is a little more powerful
because not only can it rename, but it can also move files to other
directories.

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

[i[Remove-->Reverting]]
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

[i[Remove]>]
