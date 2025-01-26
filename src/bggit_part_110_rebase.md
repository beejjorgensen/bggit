# Rebasing: Moving Commits {#rebase}

[i[Rebase]<]

I'm going to start with the Number One Rule of Rebasing: ***never rebase
anything that you have pushed***. That is, only rebase local changes
that no one else has seen. You can push them after the rebase.

This is more of a guideline than a rule in that you can rebase things
you've pushed *if you understand the consequences*. It's typically not a
great situation, though, so you'll want to generally avoid it.

The reason is that rebasing *rewrites history*. And that makes your
history get out of sync with the history of other devs who have cloned
the repo with the old history, and it makes syncing up quite
challenging.

There are other commands in Git that also rewrite history. And the
general rule is *never rewrite history on anything that's already been
pushed*. Unless you really know what you're doing.

## Contrasted to Merging

[i[Rebase-->Compared to merging]<]
[i[Merge-->Compared to rebasing]<]

But before we go run off in high spirits talking about rebasing, let's
do a quick merge refresher. Here's a variation of an earlier example
where we have two divergent branches, Figure_#.1. Let's say you're
working on the `topic` branch.

![Two divergent branches.](img_110_010.pdf "Two divergent branches.")

Then you hear that someone has made a change to `main` and you want to
roll those changes into your `topic` branch, but not necessarily get
your changes in `main` yet.

At this point, if we wanted to get the changes in `main` into `topic`,
our merge option was to make another commit, the *merge commit*. The
merge commit contains the changes from two parent commits (in this case
the commit labeled `(2)` and the one labeled `(4)` are the parents) and
makes them into a new commit, marked `(5)` in Figure_#.2.

![Two divergent branches, merged.](img_110_020.pdf "Two divergent branches, merged.")

If we look at our log at that point, we can see the changes from all the
other commits in the graph from the `topic` branch.

And we're good at this point. That worked, and it did what we wanted.
Merging is a completely acceptable solution to this problem.

But there are a couple drawbacks to doing the merge. See, we really just
wanted to get the latest stuff from `main` into our branch so we could
use it, but we didn't really want to commit anything. But here we've
made a new commit for everyone to see.

Not only that, but now the commit graph forms a loop, so the history is
a little more convoluted than perhaps we'd like it.

What really would have been nice is if I could just have taken commits
`(3)` and `(4)` from `topic` and just somehow applied those changes to
`(2)` on `main`. That is, could we pretend that instead of branching off
`(1)` like `topic` did, that we instead branched off `(2)`?

After all, if we branched off `(2)`, then we'd have those changes from
`main` that we wanted.

What we need is a way to somehow rewind our commits back to the branch
point at `(1)`, and then reapply them on commit `(2)`. That is, the base
of our `topic` branch, which was commit `(1)`, needs to be changed to
another base at commit `(2)`. We want to ***rebase*** it to commit
`(2)`!

[i[Rebase-->Compared to merging]>]
[i[Merge-->Compared to rebasing]>]

## How it Works

So let's do exactly that. Let's take the changes we made in commit `(3)`
and apply them to `main` at commit `(2)`. This will make a brand new
commit that includes changes from both commit `(2)` and commit `(3)`.
(Importantly, this commit didn't exist before; there was no commit that
contained changes from `(2)`and `(3)`.) We'll call this new commit
`(3')` ("three prime"), since it has the changes that we made in `(3)`.

After that, we'll do the same thing with commit `(4)`. We'll apply the
changes from old commit `(4)` to `(3')`, making a new commit `(4')`.

And if we do that, we end up with Figure_#.3.

![`topic` branch rebased on `main`.](img_110_030.pdf "topic branch rebased on main")

And there you see `(3')` and `(4')` now rebased onto `main`!

Again, these two commits have the same changes that you originally had
in commits `(3)` and `(4)`, but now they've been applied to `main` at
commit `(2)`. So the code is necessarily different since it now contains
the changes from `main`. This means your old commits `(3)` and `(4)` are
effectively gone, and the rebase has replaced them with two new commits
that contain the same changes, just on a different base point.

> **We just changed history.** When we mentioned rewriting history at
> the top of this chapter, this is what we were talking about. Imagine
> some other dev had your old commits `(3)` and `(4)` and was working
> off those making their own new commits. And then you rebased
> effectively destroying commits `(3)` and `(4)`. Now your commit
> history is different than the other dev's and all kinds of *Fun*™ will
> be had trying to sort if out.
>
> If you only rebase commits that you haven't pushed, you'll never get
> into trouble. But if some other dev has a copy of your commits
> (because you've already pushed them and they pulled them), don't
> rebase those commits!

## When Should I Do This?

[i[Rebase-->When to use]]
There's no fixed rule about this. Sometimes a shop will have one, saying
that everyone should rebase all the time so that the commit history has
a cleaner look (no merge commits, no loops).

Other shops will say to merge all the time so that the complete history
is preserved.

## Pulling and Rebasing

[i[Rebase-->And pulling]<]

If you might recall from way back when, doing a pull is actually a
couple operations: [i[Fetch]] *fetch* and *merge*.

The fetch downloads all the new data from the remote, but doesn't
actually merge anything into your branches or working tree. So you won't
see any local changes after a fetch.

But the pull follows it up with a standard merge so that you see the
remote tracking branch's changes in your local branch.

So, assuming you have everything set up and you're on your `main`
branch, when you do this:

``` {.default}
$ git pull
```

Git actually does something like this:

[i[Fetch]]

``` {.default}
git fetch                # Get all the information from origin
git merge origin/main    # Merge origin/main into main
```

(Recall that `origin/main` is your remote-tracking branch—it's the
version of `main` that's on `origin`, not the `main` on your local
machine.)

But merging isn't the only thing you can do there. Given that this is
the chapter on rebasing, you might correctly suspect that we can make it
do a rebase instead.

And here's how:

``` {.default}
$ git pull --rebase
```

That causes these two things to happen:

[i[Fetch]]

``` {.default}
git fetch                # Get all the information from origin
git rebase origin/main   # Rebase main into origin/main
```

If you want that to be the default behavior for the current repo, you
can run this one-time command:

``` {.default}
$ git config pull.rebase true
```

If you want it to be the default behavior for all repos, you can:

``` {.default}
$ git config --global pull.rebase true
```

If you've configured your repo to always rebase on a pull, you can
override that to force a merge (if you want) with:

``` {.default}
$ git pull --no-rebase  # Do a merge instead of a rebase
```

[i[Rebase-->And pulling]>]

## Conflicts {#rebasing-conflicts}

[i[Rebase-->Conflicts]<]

When you do a merge, there's a chance that you might conflict with some
of the changes in the other branch, and you have to resolve those, as
we've seen.

Can the same thing happen with a rebase?

Of course! If the commit you're trying to rebase onto conflicts with
your commit, you'll have the same trouble you'd have with a merge.

Luckily, Git will let you resolve the conflict in a way similar to the
merge.

Let's start with a simple example. I'm going to have a text file that
contains the following:

``` {.default}
The magic number is 1.
```

We'll have that in a commit on the `main` branch.

Then we'll make a new `topic` branch there.

Then on the `main` branch we'll change the number to `2` and commit.

And on the `topic` branch we'll change the number to `3` and commit.

So we'll have the scenario in Figure_#.4.

![Branches ready for conflict.](img_110_040.pdf "Branches ready for conflict")

Finally, we'll try to rebase `topic` onto `main`.

At that point, Git will become confused. It knows the last commit on
`main` has `2` and that `topic` is unaware of this (because it branched
off before that change). And it knows the last commit on `topic` has
`3`. So which one is right?

Let's try to rebase while we're on the `topic` branch and see what
happens.

``` {.default}
$ git rebase main
  Auto-merging magic.txt
  CONFLICT (content): Merge conflict in magic.txt
  error: could not apply 9f19221... Update to 3
  hint: Resolve all conflicts manually, mark them as resolved with
  hint: "git add/rm <conflicted_files>", then run "git rebase
  hint: --continue".
  hint: You can instead skip this commit: run "git rebase --skip".
  hint: To abort and get back to the state before "git rebase", run
  hint: "git rebase --abort".
  hint: Disable this message with "git config advice.mergeConflict
  hint: false"
  Could not apply 9f19221... Update to 3
```

Whoa, Nelly. OK, so it can't do that. It says we need to "Resolve all
conflicts manually", and then add them, and then we'll run rebase again
with the `--continue` flag to continue the rebase.

> **If you keep reading the hints**, you'll see there some more stuff in
> there. We'll get to `--skip` later, but do note that if the conflict
> is more than you want to take on right now, you can just run:
>
> ``` {.default}
> $ git rebase --abort
> ```
>
> <!-- ` -->
> to pretend you never started it in the first place.

This might sound a little familiar. It's basically the same process as
we went through with the merge conflict.

1. Edit the conflicting file and make it *Right*.
2. Add it.
3. Continue the rebase.

Let's do that. If I pop open that file `magic.txt` in my editor, I see:

``` {.default .numberLines}
<<<<<<< HEAD
The magic number is 2
=======
The magic number is 3
>>>>>>> 9f19221 (Update to 3)
```

That's just like in a merge conflict—Git is showing us the two choices
we have for this line. So we'll consult with the team and come to an
agreement on what should be in the file, and we delete everything that
shouldn't be there and we make it *Right*.

``` {.default}
The magic number is 3
```

And I save that.

Now, what were we supposed to do at this point, again? If you've
forgotten, it's fine. Just run `git status` to see where we're at.

``` {.default}
$ git status
  interactive rebase in progress; onto 6ceeefb
  Last command done (1 command done):
     pick 9f19221 Update to 3
  No commands remaining.
  You are currently rebasing branch 'topic' on '6ceeefb'.
    (fix conflicts and then run "git rebase --continue")
    (use "git rebase --skip" to skip this patch)
    (use "git rebase --abort" to check out the original branch)
  
  Unmerged paths:
    (use "git restore --staged <file>..." to unstage)
    (use "git add <file>..." to mark resolution)
	  both modified:   magic.txt
  
  no changes added to commit (use "git add" and/or "git commit -a")
```

Oh yeah! `--continue`, right?

``` {.default}
$ git rebase --continue
  magic.txt: needs merge
  You must edit all merge conflicts and then
  mark them as resolved using git add
```

What? Oh, we should have read more of the status message. It says to use
`git add` to mark resolution of the file `magic.txt`. Let's do that.

``` {.default}
$ git add magic.txt
$ git status
  interactive rebase in progress; onto 6ceeefb
  Last command done (1 command done):
     pick 9f19221 Update to 3
  No commands remaining.
  You are currently rebasing branch 'topic' on '6ceeefb'.
    (all conflicts fixed: run "git rebase --continue")

  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  modified:   magic.txt
```

That status looks nicer. Now `--continue`.

``` {.default}
$ git rebase --continue
```

This pops me into my editor to edit the commit message. This is your
opportunity to change the commit message if it no longer reflects the
commit. (That is, if you changed the commit when resolving the conflict
to be something entirely different, you might need to edit the message.)
Edit it if necessary and save it.

And Git says:

``` {.default}
[detached HEAD 443fa53] Update to 3
 1 file changed, 1 insertion(+), 1 deletion(-)
Successfully rebased and updated refs/heads/topic.
```

And `git status` shows we're all clear.

After all that, we see our new commit graph in Figure_#.5.

![After rebase conflict resolution.](img_110_050.pdf "After rebase conflict resolution.")

[i[Rebase-->Conflicts]>]

## Squashing Commits {#squashing-commits}

[i[Rebase-->Squashing commits]<]

This concept fits in with the notion of a clean commit history.

Let's say you were tasked with implementing a feature, namely adding an
alert box saying that the storage limit was exceeded.

No problem. You add it and commit with message "Added feature #121".
(And you don't push yet.)

``` {.default}
alert("Strrage limit exceeeded");
```

Then after the commit, you notice a typo. Heck.

So you fix it and commit with message "Fixed typo".

``` {.default}
alert("Storage limit exceeeded");
```

Done.

Wait! There's another typo! Are you kidding me?

So you fix it:

``` {.default}
alert("Storage limit exceeded");
```

And add another commit saying "Fixed another typo".

Now your local commit history reads:

``` {.default}
Fixed another typo
Fixed a typo
Added feature #121
```

That's not super clean, right? Really this was supposed to be one commit
that implemented feature #121.

But luckily you haven't pushed yet, which means you're still free to
rewrite that history!

You can use a feature of rebase called ***squashing*** to get this done.

What you want to do is squash those two typo fixes into the previous
commit, the one where you first tried to implement the feature.

First, let's look at the log.

``` {.default}
$ git log
commit c1820e6d0da19013208b389d264310162477b099 (HEAD -> main)
Author: User <user@example.com>
Date:   Wed Jul 17 11:53:10 2024 -0700

    Fixed another typo

commit c62c0db7b82e6b415d36bd0f00d568fd503164b7
Author: User <user@example.com>
Date:   Wed Jul 17 11:53:10 2024 -0700

    Fixed typo

commit ab84a428b8baae0078ee0647a67b34a89a6abed8
Author: User <user@example.com>
Date:   Wed Jul 17 11:53:10 2024 -0700

    Added feature #121

commit a95854659e31d203e2325eee61d892c9cdad767c
Author: User <user@example.com>
Date:   Wed Jul 17 11:53:10 2024 -0700

    Added
```

Since this is a rebase, we're going to rebase onto something, namely the
commit _prior_ to the added feature commit, the commit ID starting with
`a9585`.

And we want to do it _interactively_, which is a special rebase mode
that lets us do the squashing, and we get there with the `-i` flag.

``` {.default}
$ git rebase -i a9585
```

This brings us into an editor that has this information, and a huge
comment block below it full of instructions.

``` {.default .numberLines}
pick ab84a42 Added feature #121
pick c62c0db Fixed typo
pick c1820e6 Fixed another typo
```

Notice that they're listed in forward order instead of the reverse log
order we're used to.

Look at all those options! Pick, reword, edit, squash, fixup... so many
things to choose from. As you might imagine we're in a pretty powerful
history rewriting mode.

For now, though, let's just look at "squash" and "fixup", which are
almost the same thing.

Starting with "squash", what I want to do is take those typo fix commits
and work them into the "Added feature" commit. We can use the squash
mode to do this.

I'll edit the file to look like this:

``` {.default .numberLines}
pick ab84a42 Added feature #121
squash c62c0db Fixed typo
squash c1820e6 Fixed another typo
```

That will squash "Fixed another typo" into "Fixed typo" and then squash
that result into "Added feature #121".

And `pick` just means "use this commit as-is".

> **There are shorthand versions for all these commands.** I could have
> used `s` instead of `squash`.

After I save the file, I get launched right back into another editor
that has this in it:

``` {.default .numberLines}
# This is a combination of 3 commits.
# This is the 1st commit message:

Added feature #121

# This is the commit message #2:

Fixed typo

# This is the commit message #3:

Fixed another typo
```

We're making a new rebased commit here with the three commits squashed
into one, and so we get to write a new commit message. Helpfully, Git
has included all three commit messages. Let's hack it down to just have
the commit message we want.

``` {.default .numberLines}
Added feature #121
```

And saving gets us back out with a message.

``` {.default}
[detached HEAD 4bc6bca] Added feature #121
 Date: Wed Jul 17 11:53:10 2024 -0700
 1 file changed, 1 insertion(+)
 create mode 100644 foo.js
Successfully rebased and updated refs/heads/main.
```

Success is good. I like success.

> **What's that about detached HEAD?** Git detaches the `HEAD` briefly
> when doing a rebase. Don't worry—it gets reattached for you.

Now my commit history is all cleaned up.

``` {.default}
commit 4bc6bca6870d124b3eebc9afd32486a5a23189fc (HEAD -> main)
Author: User <user@example.com>
Date:   Wed Jul 17 11:53:10 2024 -0700

    Added feature #121

commit a95854659e31d203e2325eee61d892c9cdad767c
Author: User <user@example.com>
Date:   Wed Jul 17 11:53:10 2024 -0700

    Added
```

And you can see, if you look at the earlier log, that the "Added
feature" commit ID has changed. We did a rebase, after all, so those old
commits are gone, replaced by the new ones.

Finally, after all this, *now* you can push.

[i[Rebase-->Squashing commits]>]

### Squash versus Fixup

[i[Rebase-->Fixup]]

Now a quick note about `fixup` instead of `squash`. It's the same thing,
except only the squashed-into commit message is kept by default. So if I
ran this:

``` {.default .numberLines}
pick fbc1075 Added feature #121
fixup fd4ca42 Fixed typo
fixup 6a10e97 Fixed another typo
```

Git instantly returns with:

``` {.default}
Successfully rebased and updated refs/heads/main.
```

And Git log only shows the "Added feature #121" commit. With `fixup`,
Git automatically discards the squashed commit messages.

## Multiple Conflicts in the Rebase

[i[Rebase-->Conflicts]<]

When you merge with commit and there are multiple conflicts, you resolve
them all in one big merge commit and then you're done. You use `git
commit` to wrap it all up.

Rebase is a little different. Since rebase "replays" your commits onto
the new base one at a time, each replay is a merge conflict opportunity.
This means that *as you rebase, you might have to resolve multiple
conflicts one after another*.

For example, let's say on your topic branch you made a commit that
modified file `foo.txt`. And then you made *another commit* that
modified file `bar.txt`.

But unbeknownst to you, someone on the `main` branch has also modified
those two files, so they're bound to conflict when you rebase.

And so you begin `git rebase main`, and we're in trouble right off the
bat. It's telling us that `foo.txt` conflicts.

So you fix it up and then run `git rebase --continue` and edit the
commit message, and get on with it.

But all that does is move on to your *next* commit to `bar.txt` and try
to rebase that. And it conflicts, too!

So you fix it up and then run `git rebase --continue` and edit the
commit message, and get on with it. Again.

And finally you get the success message:

``` {.default}
[detached HEAD 31c3947] topic change bar
 1 file changed, 1 insertion(+)
Successfully rebased and updated refs/heads/topic.
```

This is why you can conclude a merge with a simple commit, but you have
to conclude a rebase by repeatedly running `git rebase --continue` until
all commits have been rebased cleanly.

Is this good or bad? It might be better in that you get a chance to
merge each commit in isolation so it might be easier to reason about and
avoid errors. But at the same time it's more legwork to get through it.

As always, use the right tool for the job!

[i[Rebase-->Conflicts]>]

[i[Rebase]>]
