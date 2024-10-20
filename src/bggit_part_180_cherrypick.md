# Cherry-Pick: Bringing in Specific Commits

Let's say you're working on `branch1` and you have made a bug fix to
`branch2`. You're not ready to merge _all_ the changes in from `branch2`
into `branch1`, but you really want just that bug fixed.

Luckily, there's a way to do that! You can merge a single commit into
your branch with `git cherry-pick`. You just have to tell it which
commit to bring in.

## Cherry-Pick Example

Let's have a file on the `main` branch called `foo.txt` that has the
following contents stored in an initial commit:

``` {.default}
Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
```

Very exciting file, that.

Now let's switch to another branch, call it `branch`, inspirationally.

And on this branch, we do some things. First, we add a couple lines to
the end and commit.

``` {.default}
Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
Branch: Line 101
Branch: Line 102
```

And then we add a line to the middle, and commit again.

``` {.default}
Line 1
Line 2
Line 3
Line 4
BRANCH: INSERTED LINE 5
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
Branch: Line 101
Branch: Line 102
```

**Additionally** let's create a branch here called `checkpoint` to make
this demo a little easier. You don't *have* to do this, but it'll enable
us to cherry-pick this commit by its branch name instead of by its
commit UUID. Or you could skip this step and use the UUID.

``` {.default}
$ git branch checkpoint
```

> **This doesn't switch branches.** It just makes a new branch on this
> commit. `HEAD` is still pointing to `branch` like before.

Lastly, let's add a couple more lines to the end, and commit one last
time.

So here's the file as it exists on `branch`:

``` {.default}
Line 1
Line 2
Line 3
Line 4
BRANCH: INSERTED LINE 5
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
Branch: Line 101
Branch: Line 102
Branch: Line 103
Branch: Line 104
```

And let's look at the log to see what we have:

``` {.default}
commit 9336292f73b4ace717644336f72458681c1bb761 (HEAD -> branch)
Author: Branch User Name <branch-user@example.com>
Date:   Sun Oct 20 13:08:30 2024 -0700

    branch: added line 103-104

commit 407f212f12f79902818431a174706cfdc30d509b (checkpoint)
Author: Branch User Name <branch-user@example.com>
Date:   Sun Oct 20 13:08:30 2024 -0700

    branch: inserted line 5

commit 9533e0bdd5cba7d65401c3180b34b01700a7906e
Author: Branch User Name <branch-user@example.com>
Date:   Sun Oct 20 13:08:30 2024 -0700

    branch: added line 101-102

commit d6953bd746c813f5ba545cf0fd6044fd78e2c617 (main)
Author: User Name <user@example.com>
Date:   Sun Oct 20 13:08:30 2024 -0700

    added
```

Okay—that's the set-up part of the demo. Now it's time to cherry-pick!

What we're going to want to do for the demo is switch back to `main` and
then cherry-pick the one commit that inserts line 5 in the middle. You
can always use its UUID (`407f2`) for this, but we left behind that
branch `checkpoint` there we can use instead.

Let's do it.

``` {.default}
$ git switch main
  Switched to branch 'main'

$ git cherry-pick checkpoint
  Auto-merging foo.txt
  [main 9254663] branch: inserted line 5
   Date: Sun Oct 20 13:08:30 2024 -0700
   1 file changed, 1 insertion(+)
```

What that *should* have done is bring in that newly-inserted line 5, and
none of the other changes. Let's look at `foo.txt` from `main`:

``` {.default}
Line 1
Line 2
Line 3
Line 4
BRANCH: INSERTED LINE 5
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
```

And there it is!

> **Wait—wasn't that just a merge?** Not quite! Notice that we had added
> lines 101-102 in `branch` *before* we inserted line 5. And yet that
> earlier commit is not reflected in `main`. We *cherry-picked* that
> single commit with line 5 out of the stream of commits, ignoring the
> other ones before and after it!

Now let's look at `git log` on `main`:

``` {.default}
commit 92546636d05fa85218ca18a0cd705ddc14fa8b64 (HEAD -> main)
Author: Branch User Name <branch-user@example.com>
Date:   Sun Oct 20 13:08:30 2024 -0700

    branch: inserted line 5

commit d6953bd746c813f5ba545cf0fd6044fd78e2c617
Author: User Name <user@example.com>
Date:   Sun Oct 20 13:08:30 2024 -0700

    added
```

There are two amazing things to notice here:

1. The author information was preserved in the log message. Notice it's
   `branch-user@example.com` and not `user@example.com`, even though it
   was the latter who did the cherry-pick. This might not be entirely
   surprising, except...

2. The cherry-picked commit UUID is different in `main` than in
   `branch`! In `branch`, it's `407f2`, and here it's `92546`. But it
   **has** to be that way because it's got all new content. That is,
   there's no other commit anywhere in the commit graph where `foo.txt`
   looks like this, so it has to have a unique UUID[^5472].

[^5472]: Even if the changes were identical, the UUID would still be
    different because the hash takes all kinds of other metadata into
    account.

But not every cherry-pick will go as smoothly as that!

## Cherry-Pick Conflicts

Yes, you can get conflicts with a cherry-pick, of course. This might
happen because you've changed some of the same lines as the commit
you're cherry-picking, or maybe because the cherry-picked commit has
some contextual lines of code that you don't have.

In any case, conflict resolution happens in the much the same way as
with `merge` or `rebase`. If you need to, refamiliarize yourself with
the content from those chapters.

But by now I hope the process seems familiar. First, make the file
_Right_, then add it, and then you'll _continue_ (like with a `rebase`)
with `git cherry-pick --continue`. Keep doing that until everything's
merged together cleanly.
