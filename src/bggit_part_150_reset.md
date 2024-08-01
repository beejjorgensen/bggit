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
point. It can also keep track of changes after the reset point, either
adding them to the stage, adding them to your working tree, or
discarding those changes entirely.

When you move a branch to another commit, the branch "becomes" the repo
at the point of that commit, including all the history that led up to
that commit. The upshot is that all the commits that led to the old
branch point are now effectively gone, as shown in Figure 18.1.

![If we reset `main` to `topic1`, commits 4 and 6 will eventually be lost.](img_150_010.pdf "If we reset main to topic1, commits 4 and 6 will eventually be lost.")

So be sure you mean it when you reset! You'll be losing commits[^d563]!

[^d563]: Git cleans up "unreachable" commits after some time has
    elapsed, so they won't be *instantly* destroyed. But they're on
    borrowed time unless you create a new branch to hold them.

## Soft Reset

TODO

## Mixed Reset

TODO

## Hard Reset

TODO

## Reset to a Divergent Branch

TODO

## Pushing Branch Changes to a Remote

TODO

TODO --force

TODO --force-with-lease

## Resetting Without Moving `HEAD`

Using the reset feature moves the `HEAD` around by necessity. What if
you just want to move a branch to another commit TODO

TODO can't move current branch
TODO


