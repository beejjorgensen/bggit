# Rebasing

[i[Rebasing]<]

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

## Contrasted to Merging

[i[Rebasing-->Compared to Merging]]
[i[Merging-->Compared to Rebasing]]

But before we go run off in high spirits talking about rebasing, let's
do a quick merge refresher. Here's a variation of an earlier example
where we have two divergent branches, Figure_#.1. Let's say you're
working on the `topic` branch.

![Two divergent branches.](img_110_010.pdf "Two divergent branches.")

Then you hear that someone has made a change to `main` and you want to
roll those changes into your `topic` branch, but not necessarily get your
changes in `main` yet.

At this point, if we wanted to get the changes in `main` into
`topic`, our merge option was to make another commit, the *merge commit*.
The merge commit contains the changes from two parent commits (in this
case the commit labeled *2* and the one labeled *4* are the parents) and
makes them into a new commit, marked *5* in Figure_#.2.

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

What really would have been nice is if I could just taken commits *3*
and *4* from `topic` and just somehow applied those changes to *2* on
`main`. That is, could we pretend that instead of branching off *1* like
`topic` did, that we instead branched off *2*?

After all, if we branched off *2*, then we'd have those changes from
`main` that we wanted.

What we need is a way to somehow rewind our commits back to the branch
point at *1*, and then reapply them on commit *2*. That is, the base of
our `topic` branch, which was commit *1*, needs to be changed to another
base at commit *2*. We want to ***rebase*** it to commit *2*!

## How it Works

So let's do exactly that. Let's take the changes we made in commit *3*
and apply them to `main` at commit *2*. This will make a brand new
commit that includes changes from both commit *2* and commit *3*.
(Importantly, this commit didn't exist before; there was no commit that
contained changes from *2* and *3*.) We'll call this new commit *3'*
("three prime"), since it has the changes that we made in *3*.

After that, we'll do the same thing with commit *4*. We'll apply the
changes from old commit *4* to *3'*, making a new commit *4'*.

And if we do that, we end up with Figure_#.3.

![`topic` branch rebased on `main`.](img_110_030.pdf "topic branch rebased on main")

And there you see *3'* and *4'* now rebased onto `main`!

Again, these two commits have the same changes that you originally had
in commits *3* and *4*, but now they've been applied to `main` at commit
*2*. So the code is necessarily different since it now contains the
changes from `main`. This means your old commits *3* and *4* are
effectively gone, and the rebase has replaced them with two new commits
that contain the same changes, just on a different base point.

> **We just changed history.** When we mentioned rewriting history at
> the top of this chapter, this is what we were talking about. Imagine
> some other dev had your old commits *3* and *4* and was working off
> those making their own new commits. And then you rebased effectively
> destroying commits *3* and *4*. Now your commit history is different
> than the other dev's and all kinds of *Fun*™ will be had trying to
> sort if out.
>
> If you only rebase commits that you haven't pushed, you'll never get
> into trouble. But if some other dev has a copy of your commits
> (because you've already pushed them and they pulled them), don't
> rebase those commits!

## When Should I Do This?

There's no fixed rule about this. Sometimes a shop will have one, saying
that everyone should rebase all the time so that the commit history has
a cleaner look (no merge commits, no loops).

Other shops will say to merge all the time so that the complete history
is preserved.

## Pulling and Rebasing

[i[Rebasing-->And pulling]]

If you might recall from way back when, doing a pull is actually a
couple operations: *fetch* and *merge*.

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

```
git fetch                # Get all the information from origin
git merge origin/main    # Merge origin/main into main
```

(Recall that `origin/main` is your remote-tracking branch—it's the
version of `main` that's on `origin`, not the `main` on your local
machine.)

But merging isn't the only thing you can do there. Given that this is
the chapter on rebasing, you might correctly suspect that we can make it
do a rebase, instead.

And here's how:

```
$ git pull --rebase
```

That causes these two things to happen:

```
git fetch                # Get all the information from origin
git rebase origin/main   # Rebase main into origin/main
```

If you want that to be the default behavior for the current repo, you
can run this one-time command:

```
$ git config pull.rebase true
```

If you want it to be the default behavior for all repos, you can:

```
$ git config --global pull.rebase true
```

If you've configured your repo to always rebase on a pull, you can
override that (if you want) with:

```
$ git pull --no-rebase  # Do a merge instead of a rebase
```

## Conflicts

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
`main` has `2` and that `topic` is unaware of this (because it
branched off before that change). And it knows the last commit on
`topic` has `3`. So which one is right?

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
conflicts manually, and then add them, and then we'll run rebase again
with the `--continue` flag to continue the rebase.

This might sound a little familiar. It's basically the same process as
we went through with the merge conflict.

1. Edit the conflicting file and make it *Right*.
2. Add it.
3. Continue the rebase.

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

Let's do that. If I pop open that file `magic.txt` in my editor, I see:

``` {.default}
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
commit. (That is, if you changed the commit when you resolving the
conflict to be something entirely different, you might need to edit the
message.) Edit it if necessary and save it.

And Git says:

``` {.default}
[detached HEAD 443fa53] Update to 3
 1 file changed, 1 insertion(+), 1 deletion(-)
Successfully rebased and updated refs/heads/topic.
```

And `git status` shows we're all clear.

After all that, we see our new commit graph in Figure_#.5.

![After rebase conflict resolution.](img_110_050.pdf "After rebase conflict resolution.")

## Squashing Commits

## Multiple Conflicts
