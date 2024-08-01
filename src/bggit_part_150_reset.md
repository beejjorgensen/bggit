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

Note: in the following examples, we assume everything is committed and
the working tree and stage are clean.

## Soft Reset

When you run a `git reset --soft`, this resets the current branch to
point to the given commit, and stages the old commit's changes.

So when you do it, you'll see the old state of your files ready to
commit.

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
branch to point to the given commit, but it doesn't change your working
tree.

[^2472]: You can leave off the `--mixed` since it's the default.

Now, thinking about this, since the branch has moved to a commit with
your files in one state, but your working tree has the files in another
state, the files must be _modified_ with respect to the commit the
branch now points to.

And this is what happens. Your changes at the old commit 

TODO

## Hard Reset

TODO

## Reset to a Divergent Branch

TODO

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


