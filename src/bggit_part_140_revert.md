# Reverting: Undoing Commits

Let's say you made some changes and committed them, but they actually
botched everything up. You want to just revert to an earlier version of
the file.

There's the cheesy way to do this that might have already occurred to
you: detach the head to an earlier commit where the file was like you
wanted it, make a copy of the file someplace safe, then reattach the
head to `main`, then copy the old file over the existing one in your
working tree. And add and commit!

But let's be more proper, and we can do that with `git revert`.

Reverting allows us to actually undo the changes of a single commit,
even if it wasn't the one that got you to the point you're at now. That
is, let's say you've made 30 commits, but it turns out you don't
actually want commit number 4 to be there any longer. You can revert
just that one!

Performing a standard revert will actually make a new commit, and
doesn't erase any old commits. In this way, it's not rewriting history
so using this method is safe to revert commits that have already been
pushed.

## Performing the Revert

It's pretty straightforward. You look back in the log for the commit ID
you're interested in reverting, and revert it.

For example, if you have this in the log:

``` {.default}
commit 9fef4fe6d42b91c12b5217829e8d98d738f84d61
Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
Date:   Fri Jul 26 16:59:44 2024 -0700

    Added Line 50
```

and you decided you didn't want that commit any longer, you could revert
it by its commit ID. Here I'll just type the first few characters of the
hash because that's enough:

``` {.default}
$ git revert 9fef4
  Auto-merging foo.txt
  [main de415f4] Revert "Added Line 50"
   1 file changed, 1 deletion(-)
```

There's no conflict (more on that, below) in this example, so it just
pops me into my editor and allows me to edit the commit message.
Remember that the revert makes a new commit!

``` {.default .numberLines}
Revert "Added Line 50"

This reverts commit 9fef4fe6d42b91c12b5217829e8d98d738f84d61.
```

I save the file and `git status` tells me we're clean.

Another `git log` will show the revert commit:

``` {.default}
$ git log
  commit de415f4f0cd645b1e551a6ac56e13f73850c88db (HEAD -> main)
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Jul 26 17:01:54 2024 -0700

    Revert "Added Line 50"

    This reverts commit 9fef4fe6d42b91c12b5217829e8d98d738f84d61.
```

You can revert any commit, even commits that were themselves reverts!
Revert the revert!

Now that was an example where the revert went smoothly. But what if
you've made some changes since the revert commit that were close to the
changes in the revert commit itself? Can it conflict? Of course it can!

## Revert Conflicts

Like with merging or rebasing, you can have conflicts with a revert. If
you're not familiar with conflict resolution, please review the
[Rebasing Conflicts](#rebasing-conflicts) section, because it's closest
to how revert conflicts work.

An example of a conflict might be that if you changed line 37 in your
code, then revert a commit that also changed line 37 in the code, Git
can't figure out what to do with that. Should it revert it to what it
was before your commit, or before the earlier commit?

So there's a revert conflict that must be resolved. And it works very
much like the other conflicts we've already seen.

If you try to revert and get a conflict, it will say something like
this:

``` {.default}
$ git revert 5af89a8985c001ec02409d77e093fb7be45495ff
  Auto-merging foo.txt
  CONFLICT (content): Merge conflict in foo.txt
  error: could not revert 5af89a8... Added Line 69
  hint: After resolving the conflicts, mark them with
  hint: "git add/rm <pathspec>", then run
  hint: "git revert --continue".
  hint: You can instead skip this commit with "git revert --skip".
  hint: To abort and get back to the state before "git revert",
  hint: run "git revert --abort".
  hint: Disable this message with
  hint: "git config advice.mergeConflict false"
```

And it points out we have a few options here. We can get even more info
with our friend `git status`:

``` {.default}
$ git status
  On branch main
  You are currently reverting commit 5af89a8.
    (fix conflicts and run "git revert --continue")
    (use "git revert --skip" to skip this patch)
    (use "git revert --abort" to cancel the revert operation)

  Unmerged paths:
    (use "git restore --staged <file>..." to unstage)
    (use "git add <file>..." to mark resolution)
	  both modified:   foo.txt

  no changes added to commit (use "git add" and/or "git commit -a")
```

So what we can do here is one of these:

* Edit the file, fix the conflict, then `git add` it, then `git revert
  --continue` to go to the next commit to be reverted (if any).
* Bail out completely with `git revert --abort`.
* Skip reverting this particular commit with `git revert --skip`. If you
  skip all the commits you were reverting, it's just like an abort.

If you fix the conflict, you'll get to enter a commit message for the
new commit just like before.

## Reverting Multiple Commits

You can specify multiple reverts at the same time on the command line.

Here's an example that reverts two commits:

``` {.default}
$ git revert 4c0b3 81d2a
  Auto-merging foo.txt
  [main ab3169d] Revert "Added Line 50"
   1 file changed, 1 deletion(-)
  Auto-merging foo.txt
  [main b63f003] Revert "Added Line 10"
   1 file changed, 1 deletion(-)
```

And there will be two new revert commits after that. You'll edit two
revert commit messages over the course of that revert.

You can also specify a range of commits. Be sure to do this in
oldest-to-newest order, or you'll get an `empty commit set passed`
error.

``` {.default}
$ git revert 4c0b3^..81d2a
  Auto-merging foo.txt
  [main ab3169d] Revert "Added Line 50"
   1 file changed, 1 deletion(-)
  Auto-merging foo.txt
  [main b63f003] Revert "Added Line 10"
   1 file changed, 1 deletion(-)
```

Again, that will make a lot of commits, one per revert. You can [squash
those commits](#squashing-commits) if you want to, or you can use `-n`
("no commit") to keep Git from committing until you're ready.

``` {.default}
% git revert -n ee71e 123e8
  Auto-merging foo.txt
  Auto-merging foo.txt
```

At this point, the file is staged with those two commits reverted. And
you can now make a single commit that holds them. And you can do the
same thing specifying a range.

Of course, there might a conflict, and you'll have to resolve those in
the super fun way we've already discussed.

