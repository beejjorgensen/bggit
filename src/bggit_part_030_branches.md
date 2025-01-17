# Branches and Fast-Forward Merges

## What is a Branch?

[i[Branch]]

Normally you think of writing code as a linear sequence of changes. You
start with an empty file, add some things, test them, add some more,
test some more, and eventually the code is complete.

![A simple commit graph.](img_030_010.pdf "[A simple commit graph.]")

<!--
``` {.default}
    (1)---(2)---(3)---(4)---(5)
```
-->

In Git we might think of this as a sequence of commits. Let's look at a
graph (Figure_#.1) where I've numbered commits 1-5. There, `(1)` was the
first commit we made on the repo, `(2)` is some changes we made on top
of `(1)`, and `(3)` is some changes we made on top of `(2)`, etc.

Git always keeps track of the parent commit for any particular commit,
e.g. it knows the parent commit of `(3)` is `(2)` in the above graph. In
this graph, the parent relationship is indicated by an arrow. "The
parent of commit 3 is commit 2", etc. It's a little confusing because
clearly commit 3 came _after_ commit 2 in terms of time, but the arrow
points to the parent, which is the opposite of the nodes' temporal
relationship.

A _branch_ is like a name tag stuck on one **specific** commit. You can
move the name tag around with various Git operations.

The default branch is called `main`.

> The default branch used to be called `master`, and still is called
> that in some older repos.

![The main branch on a commit.](img_030_020.pdf "[The main branch on a commit.]")

<!--
``` {.default}
                           [main]
                             |
                             v
    (1)---(2)---(3)---(4)---(5)
```
-->

So to make it a little more complete, we can show that branch in
Figure_#.2. There's our `main` branch attached to the commit labeled
`(5)`.

> It's tempting to think of the whole sequence of commits as "the
> branch", but this author recommends against it. Better to keep in mind
> that the branch is just a name tag for a single commit, and that we
> can move that name tag around.

But Git offers something more powerful, allowing you (or collaborators)
to pursue multiple branches simultaneously.

![Lots of branches.](img_030_030.pdf "[Lots of branches.]")

<!--
``` {.default}
               [main]
                 |
                 v    [somebranch]
    (1)---(2)---(8)      |
            \            v
            (3)---(5)---(7)
              \
              (4)---(6)
                     ^
                     |
              [anotherbranch]
```
-->

So there might be multiple collaborators working on the project at the
same time.

And then, when you're ready, you can [i[Merge]] _merge_ those branches
back together. In Figure_#.4, we've merged commit 6 and 7 into a new
commit, commit 9. Commit 9 contains the changes of both commits 7 and 6.

![After merging `somebranch` and `anotherbranch`.](img_030_040.pdf "[After merging somebranch and anotherbranch.]")

<!--
``` {.default}
               [main]
                 |
                 v      [somebranch|anotherbranch]
    (1)---(2)---(8)            |
            \                  v
            (3)---(5)---(7)---(9)
              \               /
              (4)-----------(6)
```
-->

In that case, `somebranch` and `anotherbranch` both point to the same
commit. There's no problem with this.

And then we can keep merging if we want, until all the branches are
pointing at the same commit (Figure_#.5).

![After merging all branches.](img_030_050.pdf "[After merging all branches.]")

<!--
``` {.default}
                     [main|somebranch|anotherbranch]
                                 |
                                 v
    (1)---(2)---(8)-------------(10)
            \                   /
            (3)---(5)---(7)---(9)
              \               /
              (4)-----------(6)
```
-->

And maybe after all this we decide to delete `somebranch` and
`anotherbranch`; we can do this safely because they're fully merged, and
can do this without affecting `main` or any commits (Figure_#.6).

![After deleting merged branches.](img_030_060.pdf "[After deleting merged branches.]")

<!--
``` {.default}
                               [main]
                                 |
                                 v
    (1)---(2)---(8)-------------(10)
            \                   /
            (3)---(5)---(7)---(9)
              \               /
              (4)-----------(6)
```
-->

This chapter is all about getting good with branching and partially
good with merging.

If you like interactive tutorials, Peter Cottle has put together a great
website called [fl[Learn Git
Branching|https://learngitbranching.js.org/]]. I highly recommend it
before, during, and/or after reading this chapter.

## A Quick Note about `git pull`

[i[Pull-->Force rebase or merge]]

When you do a pull, it actually does two things: (a) _fetch_ all the
changes from the remote repo and (b) _merge_ those changes.

If two or more people are committing to the same branch, eventually `git
pull` is going to have to merge. And it turns out there are a few ways
it can do this.

For now, we're going to tell `git pull` to always classically merge
divergent branches, and you can do that with this one-time command:

``` {.default}
$ git config set --global pull.rebase false
```

If you don't do that, Git will pop up an error message complaining about
it the first time it has to merge on a pull. And you'll have to do it
then. (Leave the word `set` out of that command if it fails on older
Gits.)

When we talk about rebasing later, this will make more sense.

## `HEAD` and Branches

[i[`HEAD`-->With branches]]

We said earlier that `HEAD` refers to a specific commit, namely the
commit you're looking at right now in your unmodified working tree.

And we also said that was a bit of a lie.

In normal usage, `HEAD` points to a branch, not to a commit. In detached
head state, `HEAD` points to a commit.

If we look at Figure_#.7, we see `HEAD` is pointing to a branch as per
normal.

![`HEAD` pointing to a branch.](img_030_070.pdf "[HEAD pointing to a branch.]")

<!--
``` {.default}
                     [main]<--HEAD
                       |
                       v
    (1)---(2)---(3)---(4)
```
-->

But if we check out an earlier commit that doesn't have a branch, we end
up in detached head state, and it looks like Figure_#.8.

![`HEAD` pointing to a commit.](img_030_080.pdf "[HEAD pointing to a commit.]")

<!--
``` {.default}
               HEAD   [main]
                 |     |
                 v     v
    (1)---(2)---(3)---(4)
```
-->

So far, we've been making commits on the `main` branch without really
even thinking about branching. Recalling that the `main` branch is just
a label for a specific commit, how does the `main` branch know to
"follow" our `HEAD` from commit to commit?

It does it like this: the branch that `HEAD` points to follows the
current commit. That is, when you make a commit, the branch `HEAD`
points to moves along to that next commit.

If we were here back at Figure_#.7, when `HEAD` was pointing to the
`main` branch, we could make one more commit and get us to Figure_#.9.

![`HEAD` moving with a branch.](img_030_090.pdf "[HEAD moving with a branch.]")

<!--
``` {.default}
                           [main]<--HEAD
                             |
                             v
    (1)---(2)---(3)---(4)---(5)
```
-->

[i[`HEAD`-->Detached]]
Contrast that to detached head state, back in Figure_#.8. If we were
there, a new commit would get us to Figure_#.10, leaving `main` alone.

![A commit with detached `HEAD`.](img_030_100.pdf "[A commit with detached HEAD.]")

<!--
``` {.default}
                      [main]
                       |
                       v
    (1)---(2)---(3)---(4)
                  \
                  (5)
                   ^
                   |
                  HEAD
```
-->

At this point, there's nothing stopping you from creating a new branch
at the same commit as `HEAD`, if you want to do that. Or maybe you are
just messing around and decide to switch back to `main` later,
abandoning the commits you've made in detached `HEAD` state.

Now that we have the abstract theory stuff laid out, let's talk
specifics.

## Listing All Your Branches

[i[Branch-->Listing]<]

Before we start, let's see how to list branches.

``` {.default}
$ git branch
  * main
```

This is telling you there's one branch, and you have it checked out (the
`*` lets you know that.

If I make a new branch called `foobranch` and switch to that, I'll see
this:

``` {.default}
% git branch
  * foobranch
    main
```

If I then detach the `HEAD`, I end up here:

``` {.default}
% git branch              
  * (HEAD detached at 10b6242)
    foobranch
    main
```

[i[Branch-->Listing]>]

## Creating a Branch

[i[Branch-->Creating]]

When you make the first commit to a new repo, the `main` branch is
automatically created for you at that commit.

But what about new branches we want to make?

> **Why make a branch?** A common case is that you want to work on your
> own commits without impacting the work of others. (In this case you're
> really just putting off the work until you merge your branch with
> theirs, but it's a good workflow.)
>
> Another case is that you want to mess around with some changes but
> you're not sure if they'll work. If they end up not working, you can
> just delete the branch. If they do work, you can merge your changes
> back into the non-messing-around branch.

The most common way to make new branches is this:

1. Switch to the commit or branch from which you want to make the new
   branch.

2. Make the new branch there and switch `HEAD` to point to the new
   branch.

Let's try it. Let's branch off `main`.

You might already have `main` checked out (i.e. `HEAD` points to
`main`), but let's do it again to be safe, and then we'll create a
branch with `git switch`:

``` {.default}
$ git switch main
$ git switch -c newbranch
```

Normally you can just switch to another branch (i.e. have `HEAD` point
to that branch) with `git switch branchname`. But if the branch doesn't
exist, you use the `-c` switch to create the branch before switching to
it.

> **Make sure all your local changes are committed before switching
> branches!** If you `git status` it should say "working tree clean"
> before you switch. Later we'll learn about another option with `git
> stash`.

So after checking out `main`, we have Figure_#.11.

![`HEAD` pointing to `main`.](img_030_070.pdf "[HEAD pointing to main.]")

<!--
``` {.default}
                      [main]<--HEAD
                       |
                       v
    (1)---(2)---(3)---(4)
```
-->

And then with `git switch -c newbranch`,  we create and switch to
`newbranch`, and that gets us to Figure_#.12.

![`HEAD` pointing to `newbranch`.](img_030_110.pdf "[HEAD pointing to newbranch.]")

<!--
``` {.default}
                      [main]
                       |
                       v
    (1)---(2)---(3)---(4)
                       ^
                       |
                   [newbranch]<--HEAD
```
-->

That's not super exciting, since we're still looking at the same commit,
but let's see what happens when we make some new commits on this new
branch.

> **The branches we're making here exist only on your local clone**;
> they're not automagically propagated back to wherever you cloned the
> repo from.
>
> The upshot is that if you accidentally (or deliberately) delete your
> local repo, when you `git clone` again, all your local branches will
> be gone (along with any commits that aren't part of `main` or any
> other branches pushed to the server).
>
> There is a way to set up that connection where your local branches are
> uploaded when you push, called _remote-tracking branches_. `main` is
> an example of a remote-tracking branch, which is why `git push` from
> `main` works while `git push` from `newbranch` gives an error. But
> we'll talk about all this later.

## Make Some Commits on a Branch

This is not really that different than what we were doing with our
commits before. Before we made a branch, we had `HEAD` pointing to
`main`, and we were making commits on `main`.

Now we have `HEAD` pointing to `newbranch` and our commits will go
there, instead.

Right after creating `newbranch`, we had the situation in Figure_#.12.
Now let's edit something in the working tree and make a new commit. With
that, we'll have the scenario in Figure_#.13.

![Adding a new commit to `newbranch`.](img_030_120.pdf "[Adding a new commit to newbranch.]")

<!--
``` {.default}
                      [main]
                       |
                       v
    (1)---(2)---(3)---(4)
                       ^
                       |
                   [newbranch]<--HEAD
```

``` {.default}
                      [main]
                       |
                       v
    (1)---(2)---(3)---(4)---(5)
                             ^
                             |
                         [newbranch]<--HEAD
```
-->

Right? Let's make another commit and get to Figure_#.14.

![Adding another commit to `newbranch`.](img_030_130.pdf "[Adding another commit to newbranch.]")

<!--
``` {.default}
                      [main]
                       |
                       v
    (1)---(2)---(3)---(4)---(5)---(6)
                                   ^
                                   |
                               [newbranch]<--HEAD
```
-->

We can see that `newbranch` and `main` are pointing at different
commits.

> If we wanted to see the state of the repo from `main`'s perspective,
> what would we have to do? We'd have to `git switch main` to look at
> that branch.

Now for another question. Let's say we've decided that we're happy with
the changes on `newbranch`, and we want to merge them into the code in
the `main` branch. How would we do that?

## Merging: Fast-Forward

[i[Merge-->Fast-forward]<]

Bringing two branches back into sync is called _merging_.

The branch you're on is the branch you're bringing other changes _into_.
That is, if you're on Branch A, and you tell git to Merge Branch B,
Branch B's changes will be applied onto Branch A. (Branch B remains
unchanged in this scenario.)

But in this section we're going to be talking about a specific kind of
merge: the _fast-forward_. This occurs when the branch you're merging
from is a direct ancestor of the branch you're merging into.

Let's say we have `newbranch` checked out, like from the previous
example in Figure_#.14.

<!--
``` {.default}
                      [main]
                       |
                       v
    (1)---(2)---(3)---(4)---(5)---(6)
                                   ^
                                   |
                               [newbranch]<--HEAD
```
-->

I decide I want to merge `main`'s changes into `newbranch`, so (again,
having `newbranch` checked out):

``` {.default}
$ git merge main
  Already up to date.
```

Nothing happened? What's that mean? Well, if we look at the commit
graph, above, all of `main`'s changes are already in `newbranch`, since
`newbranch` is a direct ancestor.

Git is saying, "Hey, you already have all the commits up to `main` in
your branch, so there's nothing for me to do."

But let's reverse it. Let's check out `main` and then merge `newbranch`
into it.

``` {.default}
$ git switch main
```

Now we've moved `HEAD` to track `main`, as shown in Figure_#.15.

![Checking out `main` again.](img_030_140.pdf "[Checking out `main` again.]")

<!--
``` {.default}
                      [main]<--HEAD
                       |
                       v
    (1)---(2)---(3)---(4)---(5)---(6)
                                   ^
                                   |
                               [newbranch]
```
-->

And `newbranch` is **not** a direct ancestor of `main` (it's a
descendant). So `newbranch`'s changes are **not** yet in `main`.

So let's merge them in and see what happens (your output may vary
depending on what files are included in the merge):

``` {.default}
$ git merge newbranch
  Updating 087a53d..cef68a8
  Fast-forward
   foo.py | 4 +++-
   1 file changed, 3 insertions(+), 1 deletion(-)
```

And now we're at Figure_#.16.

![After merging `newbranch` into `main`.](img_030_150.pdf "[After merging newbranch into main.]")

<!--
``` {.default}
                                 [main]<--HEAD
                                   |
                                   v
    (1)---(2)---(3)---(4)---(5)---(6)
                                   ^
                                   |
                               [newbranch]
```
-->

Wait a second—didn't we say to merge `newbranch` into `main`, like take
those changes and fold them into the `main` branch? Why did `main`
move, then?

We did! But let's stop and think about how this can happen in the
special case where the branch you're merging _into_ is a direct ancestor
of the branch you're merging _from_.

It used to be that `main` didn't have commits `(5)` or `(6)` in the
graph, above. But `newbranch` has already done the work of adding `(5)`
and `(6)`!

The easiest way to get those commits "into" `main` is to simply
_fast-forward_ `main` up to `newbranch`'s commit!

Again, this only works when the branch you're merging into is a direct
ancestor of the branch you're merging from.

That said, you certainly can merge branches that are not directly
related like that, e.g. branches that share a common ancestor but have
both since diverged.

Git will automatically fast-forward if it can. Otherwise it does a
"real" merge. And while fast-forward merges can never lead to _merge
conflicts_, regular merges certainly can.

But that's another story.

[i[Merge-->Fast-forward]>]

## Deleting a Branch

[i[Branch-->Deleting]]

If you're done merging your branch, it's easy to delete it. **Importantly,
this doesn't delete any commits; it just deletes the branch "label"
so you can't use it any longer**. You can still use all the commits.

Let's say we've finished the work on our `topic1` branch and we
want to merge it into `main`. No problem:

``` {.default}
$ git commit -m "finished with topic1"   # on topic1 branch
$ git switch main
$ git merge topic1                       # merge topic1 into main
```

At this point, assuming a completed merge, we can delete the `topic`
branch:

``` {.default}
$ git branch -d topic1
  Deleted branch topic1 (was 3be2ad2).
```

Done!

> [i[Branch-->Topic]]**A *topic* branch is what we call a local branch
> made for a single topic like a feature, bug fix, etc.** In this guide
> I'll name branches literally `topic` to indicate that it's just an
> arbitrary branch. But in real life you'd name the topic branch after
> what it is you're doing, like `bugfix37`, `newfeature`, `experiment`,
> etc.

But what if you were working on a branch and wanted to abandon it before
you merge it into something? For that, we have the more imperative
Capital `D` option, which means, "I _really_ mean it. Delete this
unmerged branch!"

``` {.default}
$ git branch -D topic1
```

Use lowercase `-d` unless you have reason to do otherwise. It'll at
least tell you if you're about to lose your reference to your unmerged
commits!

