# Reset: Moving Branches Around

Before be begin, using `git reset` ***rewrites history***. This means
that you shouldn't use it on any branches that other people might have
copies of, i.e. branches that you have pushed.

Of course, this is a highly-recommended guideline, not a rule, and you
can reset anything provided you know what you're doing and have good
communication with your team.

But if you never reset a branch you haven't pushed, you won't get into
trouble.

So what it is?

Doing a reset allows you change where the `HEAD` and your current branch
point. You can move your current branch to a different commit!

When you move a branch to another commit, the branch "becomes" the repo
at the point of that commit, including all the history that led up to
that commit. The upshot is that all the commits that led to the old
branch point are now effectively gone, as shown in Figure 18.1.

![If we reset `main` to commit _2_, commits _3_ and _4_ will eventually be lost.](img_150_010.pdf "If we reset main to commit 2, commits 3 and 4 will eventually be lost.")

So be sure you mean it when you reset! You'll be losing commits[^d563]!

[^d563]: Git cleans up "unreachable" commits after some time has
    elapsed, so they won't be *instantly* destroyed. But they're on
    borrowed time unless you create a new branch to hold them.

When doing a reset, you can ask Git to move the current branch to
another commit, or to another branch, or to anything else that
identifies a commit.

Now, there is a question of what happens to the _difference_ between
your working tree at the old commit and whatever it would be at the new
commit.

And there we have some options: ***soft reset***, ***mixed reset***, and
***hard reset***.

And which you choose controls what happens to the branch, the stage, and
the working tree.

Note: in the following examples, we assume everything is committed and
the working tree and stage are clean.

Note: also in the following examples, I'm going to use the term "old
commit" to refer to where the branch was *before* the reset, and "new
commit" to refer to where it will be *after* the reset.

With all three variants, the current branch moves to the new (specified)
commit.

The summary of differences is:

* **Soft**:
  * Stage: old commit
  * Working tree: old commit

* **Mixed**:
  * Stage: new commit
  * Working tree: old commit
  
* **Hard**:
  * Stage: new commit
  * Working tree: new commit

## Soft Reset

When you run a `git reset --soft`, this resets the current branch to
point to the given commit, and makes the stage and working tree both
have the changes that were present in the old commit.

The upshot is that `git status` will show your old commit's changes as
staged, and none of the files as modified.

In other words, you'll see the old state of your files on the stage
ready to commit.

A common use for this might be to collapse some of your previous
commits similar to what we did with [rebase and squashing
commits](#squashing-commits).

Let's say we have commits like this (pretend the numbers are the commit
hashes):

``` {.default}
commit 555 (HEAD -> main)
   Fixed another typo again
commit 444
   Fixed another typo
commit 333
   Fixed a typo
commit 222
   Implemented feature
commit 111
   Added
```

That's a gnarly-looking commit history. It would be nice to rewrite it
(*but if and only if you haven't pushed it yet!*).

We can do that with a soft reset back to commit `111`.

If we do this soft reset:

``` {.default}
$ git reset --soft 111   # Again, pretend 111 is the commit hash
```

We'll then be in this point with all the other commits gone...

``` {.default}
commit 111 (HEAD -> main)
   Added
```

**Except importantly** our files *as they existed in commit 555* will
now be staged and ready to commit. That means with the soft reset the
changes weren't lost, but effectively commits 222-555 are all squished
together on the stage.

So we commit them:

``` {.default}
$ git commit -m "Implemented feature"
```

And now we're here with a nice commit history:
 
``` {.default}
commit 222 (HEAD -> main)
   Implemented feature
commit 111
   Added
```

And now, finally we can push, happy that our changes are presentable to
the general public.

> **Again, we've rewritten history here.** Don't do this if you've
> already pushed those commits past the one you're resetting to.

## Mixed Reset

When you run a `git reset --mixed`[^2472], this resets the current
branch to point to the given commit, and it modifies the stage to that
commit, and it **doesn't** change your working tree.

[^2472]: You can leave off the `--mixed` since it's the default.

The upshot is that it will show files as "modified" with the changes of
the old commit, and there will be nothing on the stage.

Now, thinking about this, since the branch has moved to a commit with
your files in one state, but your working tree has the files in another
state, the files must be _modified_ with respect to the commit the
branch now points to.

And this is what happens. Your changes at the old commit will show up as
modified files at the current commit.

It's like the soft reset, except instead of the old commit ending up on
the stage, it ends up in the working tree. You can stage it and commit
it from here.

But that's not all! Since the stage is also updated to the new commit,
it means the stage is effectively emptied.

In fact, this is the classic use for a mixed reset: `git reset HEAD`.
This moves files from staged state back to modified state.

> **In the glorious future past, a new command was introduced to do
> this**: `git restore --staged`. That's the preferred method to use
> now.

This will reset the current branch to where it already was (assuming
`HEAD` points to the current branch), and reset the stage to be the same
as that commit. This unstages the files that were there. And it changes
the working tree files to have the changes that were already present in
those files at that point, which would be any changes you introduced.

And that unstages the files!

Another use might be if you want to squash a bunch of unpushed commits
but simply don't want to stage the changes at the old commit yet,
leaving them as modified.

## Hard Reset

This resets everything to a particular commit. The branch moves there.
The stage is set to that commit. The files in the working tree are set
to that commit. All changes since that commit are lost.

Use this if you want to bail out. You've made some commits and decided
that was the wrong way, and you want to just roll them back entirely.

**Again, only do this if you haven't pushed!**

If you do a hard reset, it will simply move the branch and reset your
entire world (as it pertains to that branch) to that point as if nothing
had happened since. `git status` will report that everything is clean.

## Reset to a Divergent Branch

In the above examples, we've been resetting to a direct ancestor of our
current commit. This is the common case for using `git reset`.

But there's no reason why you couldn't reset to an entirely different
divergent branch. It just moves the branch there with exactly the same
rules for soft, mixed, and hard that we've already covered.

## Pushing Branch Changes to a Remote

TODO

TODO --force

TODO --force-with-lease

## Resetting Files

TODO

## Resetting Without Moving `HEAD`

Using the reset feature moves the `HEAD` around by necessity. What if
you just want to move a branch to another commit TODO

TODO can't move current branch
TODO


