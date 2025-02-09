# Worktrees

[i[Worktree]<]

Let's say you have your code in one window and you're happily looking at
`main`. And then you think, "It would be nice to look at some files on
`foobranch` for a moment."

But you're in the middle of something on `main`. So you go through the
trouble of saving, stashing, switching to `foobranch`, looking at what
you need, and then switching back, popping the stash, and editing your
file.

And then precisely 2.3 seconds later, you realize you need to look at
`foobranch` again. Gah.

You can't have two branches checked out in the same working tree at the
same time. So what are you supposed to do if you want to look at both at
once?

Sure, you can make another clone, but that might be prohibitive if the
amount of data in the clone is large. You could do a shallow clone...
but now it just feels hackish.

Turns out *worktrees* give us a better way. With `git worktree`, you can
make another, separate working tree at a different branch. And then
looking at both of them is just a matter of `cd` or having two terminal
windows open at the same time.

## Worktree Rules and Regulations

Let's put a quick note here about some ground rules.

1. No two worktrees (on the same repo) may refer to the same branch at
   the same time. That is, all worktrees must refer to different
   branches. If you try to switch to, say, `main` on two worktrees
   simultaneously, Git will stop you.

2. [i[Worktree-->Choosing location]]You can put the new worktree
   anywhere you want. But my strong recommendation is that you place it
   *outside* the existing working tree, as a sibling directory.

3. You can run all regular Git commands from any of the working trees,
   including committing, pushing, and pulling.

4. A worktree is **not** a clone. It's another view into the repo.
   Commits made in one working tree are immediately available (but not
   automatically switched to) in the other because both working trees
   are looking at the same local repo! (Unlike a clone where two clones
   would be associated with the same *remote* repo.)

5. [i[Worktree-->`main` worktree]]Only one of the worktrees is the
   *real* one (called the "main working tree", no relation to the `main`
   branch). The others don't have a proper `.git` directory. Do not
   delete the real one unless you want to lose all your git metadata!
   Always use `git worktree remove` to remove worktrees because it'll
   refuse to remove the main one if you foolishly try to do so.

With that boring legalese out of the way, let's get something going!

## Making a New Worktree

[i[Worktree-->Creating]<]

Let's say you're in the root of a repo called `wumpus` on branch `main`.
And you want to look at another branch called `arrow` in a new working
tree.

We're going to use `git worktree add` and we're going to give it two
things.

1. The directory name of where the worktree should go. Since I'm
   checking out the `arrow` branch on the `wumpus` repo there, I'm going
   to just call it `../wumpus-arrow`. You could call it anything,
   though.

   Also note the `../`; that's to get us to the parent directory so that
   `wumpus-arrow` will be created as a sibling directory to `wumpus`.

2. We also need to give it the branch to switch to in that worktree.
   Again, this can't be a branch that's checked out in any other working
   tree.

Let's do it!

``` {.default}
$ git worktree add ../wumpus-arrow arrow 
  Preparing worktree (checking out 'arrow')
  HEAD is now at 7da9b7f fix arrow flight
```

There we have it. We can now `cd` to that directory and look around.

``` {.default}
$ cd ../wumpus-arrow
$ git status
  On branch arrow
  nothing to commit, working tree clean
```

Or you could have two windows open. One would be in the `wumpus/`
directory to see branch `main`, and the other would be in the
`wumpus-arrow/` directory to see branch `arrow`.

[i[Worktree-->Creating]>]

## Removing a Worktree

[i[Worktree-->Removing]<]

First, make sure you don't have any uncommitted modifications in the
condemned worktree. Then figure out the path to it. And then remove it.

Let's say we're in the `wumpus/` directory from the previous example.
From there, I could delete the `wumpus-arrow/` worktree like so:

``` {.default}
$ git worktree remove ../wumpus-arrow
```

And that would be that.

Again, this doesn't delete any commits that you made from that worktree;
the worktree is just a view onto the same repo as the main working tree,
so the commits are already "in" the main working tree the instant you
make them from any of the worktrees.

The path you specify for the `worktree remove` doesn't have to
character-per-character match the one you specified with `worktree add`.
It just has to be the same directory.

For example, if I were in the `wumpus/` directory, this would accomplish
the same thing as the first example:

``` {.default}
$ cd ..
$ git worktree remove wumpus-arrow
```

You can even blow away the worktree you're in right now:

``` {.default}
$ git worktree remove .
```

If you try to remove the main working tree, you're stopped by the Git
police.

``` {.default}
$ git worktree remove wumpus
  fatal: 'wumpus' is a main working tree
```

[i[Worktree-->Removing]>]

## Listing Worktrees

[i[Worktree-->Listing]<]

You can see all your worktrees and determine which one is the main
working tree with the `worktree list` command.

``` {.default}
$ git worktree list
  /home/user/wumpus        30d669a [main]
  /home/user/wumpus-arrow  7da9b7f [arrow]
```

That'll show you all the working trees with their directories on the
left, their commit hashes in the middle, and the branch names on the
right.

The first worktree listed is the main working tree.

[i[Worktree-->Listing]>]

## Worktrees and Detached `HEAD`

[i[Worktree-->Detached `HEAD`]<]

You can't have the same branch checked out in two worktrees on the same
repo because that would mean two worktrees would be fighting over the
placement of a single branch reference.

[i[`HEAD`-->Detached]<]

However, both worktrees do have their own `HEAD`! There's no conflict
there. So you could have one worktree on `main` and the other with a
detached `HEAD` on the same commit as `main`. Of course, any commits on
the detached `HEAD` won't move `main` at all, so there's no conflict.

``` {.default}
$ cd ../wumpus-arrow

$ git switch --detach main
  HEAD is now at 30d669a add drafts

$ git worktree list
  /home/user/wumpus        30d669a [main]
  /home/user/wumpus-arrow  30d669a (detached HEAD)
```

In that example, we see both worktrees are pointed at the same commit
`30d669a` but we're OK since they're not checked out at the same branch.

You can also add a new worktree with a detached `HEAD` like in the next
example where we detach the new worktree's `HEAD` at the `main` commit.

``` {.default}
$ git worktree add --detach ../wumpus-worktree main
```

Finally, if you specify a commit hash instead of branch when creating a
new worktree, it will be automatically be created with a detached
`HEAD`.

[i[Worktree-->Detached `HEAD`]>]
[i[`HEAD`-->Detached]>]
[i[Worktree]>]
