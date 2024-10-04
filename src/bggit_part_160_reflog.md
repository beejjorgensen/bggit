# The Reference Log, "reflog"

All this time you've been committing things, branching, doing whatever.
And Git's been watching you, listening like Big Brother, recording
everything you do.

And you can use this to your benefit.

Let's say you've done something like a hard reset because you wanted to
abandon the branch you were on.

But then, wait! You actually needed something from one of those commits
you just reset past! Is there any way to get back to it? There's no
branch there, and you can't remember the commit ID. And since it's not
an ancestor to anything, `git log` won't help you.

How can you get it back?

`git reflog` to the rescue!

The reflog contains a record of all manner of things you've done along
with commit IDs, and it keeps them for 90 days[^9721]. After that time,
orphan commits (that is commits with no branch above them) will be
garbage collected.

[^9721]: By default it's 90 days. You can configure this with the
    `gc.reflogExpire` config option.

## What Can We Use It For?

You can use it for all kinds of things.

* Looking at orphan commits
* Recreating deleted branches
* Recovering from a bad reset
* Exploring the order of operations on the repo, even if they're on
  other branches
* And more!

Basically it gives you a way to look back on the linear history of the
repo, and tells you the commit UUIDs along the way.

This means if you want to, say, hard reset the repo to some earlier
state, you could look up that earlier commit in the reflog[^ab30].

[^ab30]: Keeping in mind to never rewrite history on anything you've
    pushed, of course.

## Looking Back at an Orphan Commit

Let's run an example where we do the following:

1. Commit a file, `foo.txt`,  on the `main` branch.
2. Make a new branch, `topic1`.
3. In this new branch, add another file, `bar.txt`, and commit it.
4. Modify `bar.txt` and commit the modification.
5. Decide, at this point, you're giving up on `topic1`. Switch
   back to the `main` branch and force delete `topic1`.
6. Decide, at this point, that actually you need to look back at that
   commit in `topic1` for some reason. But you deleted the branch.
   Whoops.
7. Look in the reflog for the commit on `topic1` that you want.
8. Switch to that commit (detaching the `HEAD`).

And here that is in Git, at least the first five steps:

``` {.default}
$ echo 'Line 1' > foo.txt                  # Create foo.txt
$ git add foo.txt
$ git commit -m 'added foo.txt'
  [main (root-commit) 90bd7cc] added foo.txt
   1 file changed, 1 insertion($)
   create mode 100644 foo.txt
$ git switch -c topic1               # Switch to topic1
  Switched to a new branch 'topic1'
$ echo 'Line 1' > bar.txt                  # Create bar.txt
$ git add bar.txt
$ git commit -m 'added bar.txt'
  [topic1 4219f83] added bar.txt
   1 file changed, 1 insertion($)
   create mode 100644 bar.txt
$ echo 'Line 2' >> bar.txt                 # Modify bar.txt
$ git add bar.txt
$ git commit -m 'appended to bar.txt'
  [topic1 bf8b8cf] appended to bar.txt
   1 file changed, 1 insertion($)
$ git switch -                             # Switch back to main
  Switched to branch 'main'
$ git branch -D topic1               # Delete topic1
  Deleted branch topic1 (was bf8b8cf).
```

At this point let's say we want to look back at the commits we made on
`bar.txt`. Good luck with `git log`!

``` {.default}
% git log
commit 90bd7cc6c3c530798872827ba02cb7db4fd422c2 (HEAD -> main)
Author: User <user@example.com>
Date:   Fri Oct 4 16:24:56 2024 -0700

    added foo.txt
```

That's it? Where's all the `bar.txt` stuff? Well, it was on the
`topic1` commits, which were descendants from this commit `90bd7`.
Because `git log` only shows ancestors, we're not seeing any of the
`bar.txt` changes.

So, finally, we arrive at the entire topic of this chapter: the reflog.
Let's take a peek.

``` {.default}
$ git reflog
  90bd7cc (HEAD -> main) HEAD@{0}: checkout: moving from topic1 to
                                             main
  bf8b8cf HEAD@{1}: commit: appended to bar.txt
  4219f83 HEAD@{2}: commit: added bar.txt
  90bd7cc (HEAD -> main) HEAD@{3}: checkout: moving from main to
                                             topic1
  90bd7cc (HEAD -> main) HEAD@{4}: commit (initial): added foo.txt
```

Hey, that's more like it! I see the changes I made to `bar.txt` in
there! And I see the commit UUID on the left! This means I can switch
to that commit!

``` {.default}
$ git switch --detach bf8b8cf
  HEAD is now at bf8b8cf appended to bar.txt
$ git log
  commit bf8b8cf826bbf667cdd088cfcecbc1086c24de3b (HEAD)
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Oct 4 16:24:56 2024 -0700

      appended to bar.txt

  commit 4219f83f22f8a90cb8d57128501facb58b292003
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Oct 4 16:24:56 2024 -0700

      added bar.txt

  commit 90bd7cc6c3c530798872827ba02cb7db4fd422c2 (main)
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Oct 4 16:24:56 2024 -0700

      added foo.txt
```

There's the log... and we have the file contents?

``` {.default}
$ cat bar.txt
  Line 1
  Line 2
```
  
Yup!

Let's switch back to `main` and see what happens.

``` {.default}
$ git switch -
  Warning: you are leaving 2 commits behind, not connected to
  any of your branches:

    bf8b8cf appended to bar.txt
    4219f83 added bar.txt

  If you want to keep them by creating a new branch, this may be a good
  time to do so with:

    git branch <new-branch-name> bf8b8cf

  Switched to branch 'main'
```

This is Git telling us, "Hey, I'm going to garbage collect these two
commits after the 90 days are up. If you want to keep them, attach a
branch to them."

And it's helpfully telling us how to do that.

So even though we force deleted `topic1` earlier, we could now simply
recreate it if we didn't mean to do that. Let's do that.

``` {.default}
$ git branch topic1 bf8b8cf
$ git switch topic1
  Switched to branch 'topic1'
$ cat bar.txt
  Line 1
  Line 2
```

As you can see, the reflog can get you out of all kinds of trouble when
you thought you'd lost commits for good.

## Reflog Selectors

Let's take a look at that example reflog output again:

``` {.default}
$ git reflog
  598c84e (HEAD -> main) HEAD@{0}: checkout: moving from topic1 to
                                             main
  dc3d6a3 HEAD@{1}: commit: appended to bar.txt
  0789880 HEAD@{2}: commit: added bar.txt
  598c84e (HEAD -> main) HEAD@{3}: checkout: moving from main to
                                             topic1
  598c84e (HEAD -> main) HEAD@{4}: commit (initial): added foo.txt
```

See that `HEAD@{3}`-type stuff in there? You can use those to check out
specific commits (instead of using the UUID, for example).

Now, `HEAD@{3}` **doesn't** mean "3 commits before `HEAD`". But it is an
identifier you can use to switch to a particular commit.

``` {.default}
$ git switch --detach HEAD@{1}
  HEAD is now at dc3d6a3 appended to bar.txt
```

Just like that.
