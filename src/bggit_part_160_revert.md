# Reverting Changes

What if someone (ahem) made a commit earlier that you want to revert?
There might be ways to use `reset` to get there, but you can't rewrite
history if someone else has cloned it.

What you *can* do is make a new commit that undoes the old commit you no
longer want.

And `git revert` can do exactly that. TODO

## Revert Conflicts

Like with merges, rebases, and so many other things, doing a revert can
cause a conflict.

This happens when any subsequent commit to the reverted commit
conflicts. Let's have an example.

Let's say I have file with these commits:

``` {.default}
Line 1   # commit 1
Line 2   # commit 2
Line 3   # commit 3
```

Great! But then we decide that we want to undo the second commit, so we
try to `revert` it.

But here Git has trouble since the edit that made commit 2 is so close
to the edit that made commit 3.

Here's some real life output from such a revert:

``` {.default}
$ git revert d0bfb61
  Auto-merging foo.txt
  CONFLICT (content): Merge conflict in foo.txt
  error: could not revert d0bfb61... added line 2
  hint: After resolving the conflicts, mark them with
  hint: "git add/rm <pathspec>", then run
  hint: "git revert --continue".
  hint: You can instead skip this commit with "git revert --skip".
  hint: To abort and get back to the state before "git revert",
  hint: run "git revert --abort".
  hint: Disable this message with "git config advice.mergeConflict
  hint: false"
```

And then if we edit the file, we see something like this:

``` {.default}
Line 1   # commit 1
<<<<<<< HEAD
Line 2   # commit 2
Line 3   # commit 3
=======
>>>>>>> parent of d0bfb61 (added line 2)
```

Honestly, I find this a bit confusing. But what we have at the part
marked `HEAD` are the changes we're reverting, plus anything that
conflicts, namely commits 2 and 3.

And after the `=======` line, we have the stuff before the commit we're
reverting. And there was no "Line 2" or "Line 3" before that commit.
(There was a "Line 1", and you see that at the top before the conflict
markers.

But the goal here is, as always, to make the conflicting file look
_Right_. So we cut out the bits we don't want, and leave it like this:

``` {.default}
Line 1   # commit 1
Line 3   # commit 3
```

And then we follow the usual conflict-resolution process, except this
time with the revert.

```
$ git add foo.txt
$ git revert --continue
```

> **You can run `git status` at any time** if you're unclear on where
> you are in the revert conflict resolution process!

At this point we'll get a change to enter a commit message for the
revert commit, and then the log will show something like this:

``` {.default}
$ git log
  commit 368a236ecdd559dc86d48cb92b6168d152e29994 (HEAD -> main)
  Author: User <user@example.com>
  Date:   Tue Oct 1 17:49:32 2024 -0700

      Revert "added line 2"

      This reverts commit d0bfb61332ff54de77f3172427122afc6ae0993c.
```

And we're done!

