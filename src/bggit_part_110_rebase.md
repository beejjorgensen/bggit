# Rebasing

So far we've talked about how to merge two branches together, but it
turns out there's another way: to ***rebase***.

But before we go there, let's do a quick merge refresher. Here's a
variation of an earlier example where we have two divergent branches,
Figure_#.1. Let's say you're working on the `topic` branch.

![Two divergent branches.](img_110_010.pdf "Two divergent branches.")

Then you hear that someone has made a change to `main` and you want to
roll those changes into your `topic` branch, but not necessarily get your
changes in `main` yet.

At this point, if we wanted to get the changes in `main` into
`topic`, our merge option was to make another commit, the *merge commit*.
The merge commit contains the changes from two parent commits (in this
case the commit labeled `2` and the one labeled `4` are the parents) and
makes them into a new commit, marked `5` in Figure_#.2.

![Two divergent branches, merged.](img_110_020.pdf "Two divergent branches, merged.")

And there we have it. If we look at our log, we can see the changes from
all the other commits in the graph from the `topic` branch.

Frankly, we're fine at this point. That worked, and it did what we
wanted.

But there are a couple drawbacks to doing the merge. See, we really just
wanted to get the latest stuff from `main` into our branch so we could
use it, but we didn't really want to commit anything. But here we've
made a new commit for everyone to see.

Not only that, but now the commit graph forms a loop.

What really would have been nice is if I could just taken commits `3`
and `4` from `topic` and just somehow applied those changes to `2` on
`main`. That is, could we pretend that instead of branching off `1` like
`topic` did, that we instead branched off `2`?

After all, if we branched off `2`, then we'd have those changes from
`main` that we wanted.

What we need is a way to somehow rewind our commits back to the branch
point at `1`, and then reapply them on commit `2`. That is, the base of
our `topic` branch, which was commit `1`, needs to be changed to another
base at commit `2`. We want to ***rebase*** it to commit `2`!

And if we do that, we end up with Figure_#.3.

![`topic` branch rebased on `main`.](img_110_020.pdf "topic branch rebased on main")

Looking at that figure, you might see something strange. Notably,
commits `3` and `4` are gone, and I've replaced them with commits `3'`
and `4'`.

These commits have the same changes that you originally had in commits
`3` and `4`, but now they've been applied to `main` at commit `2`. So
the code is necessarily different since it now contains the changes from
`main`. This means your old commits `3` and `4` are effectively gone,
and the rebase has replaced them with two new commits that contain the
same changes, just on a different base point.
