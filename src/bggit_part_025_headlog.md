# The Git Log and `HEAD`
[i[Log]<]

When we make commits to a Git repo, it tracks each of those commits in a
log that you can visit. Let's take a look at that now.

## An Example Log

You can get the commit log by typing `git log`.

Let's say I'm in a repo with a single commit where I've just added a
file with the commit message "Added".

``` {.default}
$ git log
```

produces:

``` {.default}
commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2 (HEAD -> main)
Author: User Name <user@example.com>
Date:   Thu Feb 1 09:24:52 2024 -0800

    Added
```

If I make another commit, we get a longer log:

``` {.default}
commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
Author: User Name <user@example.com>
Date:   Thu Feb 1 12:36:13 2024 -0800

    More output

commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2
Author: User Name <user@example.com>
Date:   Thu Feb 1 09:24:52 2024 -0800

    Added
```

Notice that the most recent commit entry is at the top of the output.

## What's in the log?

There are a few things to notice in the log:

* The commit comment
* The date
* The user who made the commit

Also, we have those huge
[fl[hex|https://en.wikipedia.org/wiki/Hexadecimal]] numbers after the
word `commit`.

This is the _commit ID_ or _commit hash_. This is universally unique
number that you can use to identify a particular commit.

Normally you don't need to know this, but it can be useful for going
back in time or keeping track of commits in multi-developer projects.

We also see a bit at the top that says `(HEAD -> main)`. What's that
about?

[i[Log]>]

## The `HEAD` Reference

[i[`HEAD`]<]

We've seen that each commit has a unique and unwieldy identifier like
this:

`5a02fede3007edf55d18e2f9ee3e57979535e8f2`

Luckily, there are a few ways to refer to commits with more-human
symbolic names.

`HEAD` is one of these references. It indicates which branch or commit
you're looking at right now in your project subdirectory[^7b00].
Remember how we said you could go look at previous commits? The way you
do that is by moving `HEAD` to them.

[^7b00]: I'm stretching it a bit, here. `HEAD` looks at the commit
    you've switched to. This might not be quite the same as what's in
    your project subdirectory if you've modified some of the files since
    the moving `HEAD` to that commit. The commit is a snapshot, but that
    snapshot doesn't include modifications to files until you make
    another commit that contains them.

> **We haven't talked about branches yet, but the `HEAD` normally refers
> to a branch.** By default, it's the `main` branch. But since we're
> getting ahead of ourselves, I'm going to just keep saying that `HEAD`
> refers to a commit, even though it usually does it indirectly via a
> branch.
>
> So this is a bit of a lie, but I hope you forgive me.

Some terminology: the Git subdirectory you're looking at right now and
all the files within it is referred to as your _working tree_. The
working tree is the files as they appear at the commit pointed to by
`HEAD`, plus any uncommitted changes you might have made.

So if you switch `HEAD` to another commit, the files in your working
tree will be updated to reflect that.

> **Importantly, the data in the files in the working tree might differ
> from the data in the files at the current commit pointed to by
> `HEAD`.** This happens when you've modified a file in the working tree
> but haven't yet committed it.

Okay then, how do we know which commit `HEAD` is referring to? Well,
it's right there at the top of the log:

``` {.default}
commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
Author: User Name <user@example.com>
Date:   Thu Feb 1 12:36:13 2024 -0800

    More output
```

We see `HEAD` right there on the first line, indicating that `HEAD` is
referring to commit with ID:

`5e8cb52cb813a371a11f75050ac2d7b9e15e4751`

Again, that's a bit of a lie. The `HEAD -> main` means that
`HEAD` is actually referring to the `main` branch, and that `main` is
referring to the commit. `HEAD` is therefore indirectly referring to the
commit. More on that later.

## Going Back In Time and Detached `HEAD`

[i[`HEAD`-->Detached]]

Here's my full Git log:

``` {.default}
commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
Author: User Name <user@example.com>
Date:   Thu Feb 1 12:36:13 2024 -0800

    More output

commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2
Author: User Name <user@example.com>
Date:   Thu Feb 1 09:24:52 2024 -0800

    Added
```

If I look at the files, I'll see the changes indicated by the "More
output" commit. But let's say I want to go back in time to the previous
commit and see what the files looked like then. How would I do that?

> **Maybe there were some changes that existed back in an earlier
> commit** that had since been removed, and you wanted to look at them,
> for example.

I can use the [i[Switch]] `git switch` command to make that happen.

> **Before you switch branches, you should be all committed with `git
> status` telling you everything is clean.** If you're not, make a
> commit or [stash](#stash) your stuff before your switch.

Let's check out the first commit, the one with ID
`5a02fede3007edf55d18e2f9ee3e57979535e8f2`.

Now, I could say:

``` {.default}
$ git switch --detach 5a02fede3007edf55d18e2f9ee3e57979535e8f2
```

and that would work, but the rule is that you must specific at least 4
unique digits of the ID, so I could have also done this:

``` {.default}
$ git switch --detach 5a02
```

for the same result.

And that result is:

``` {.default}
HEAD is now at 5a02fed
```

Let's take a look around with `git log`:

``` {.default}
commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2 (HEAD)
Author: User <user@example.com>
Date:   Thu Feb 1 09:24:52 2024 -0800

    Added
```

That's all! Just one commit?! Where's the second commit I made? Is it
gone forever?!

No. Everything is fine. _[Soothing image of a kitten sleeping in the
sun.]_

When you have `HEAD` at a certain commit, you're looking at the world as
it looked at that snapshot in time. Future commits haven't "happened"
yet from this perspective. They are still out there, but you'll have to
change back to them by name. (It's like a flippin' _time machine_!)

Also, do you see anything different about that first line that reads
`(HEAD)`? That's right: no `main` to be seen.

That's because the `main` branch is still looking at the latest commit,
the one with the "More output" comment. So we don't see it from this
perspective.

Furthermore, this means that `HEAD` is no longer *attached* to `main`.
We call this state [i[`HEAD`-->Detached]] *detached head*. And `git
switch` doesn't let you do that unless you mean it, which is why we have
that `--detach` in there. (And reattaching is easy: just switch to the
branch you want to attach to.)

> **Remember earlier when I said it was a bit of a lie to say that
> `HEAD` points to a commit?** Well, detached head state is the case
> where it actually **does**. Detached head state is just what happens
> when `HEAD` is pointing to a commit instead of a branch. To reattach
> it, you have to change it to point to a branch again.

Let's reattach `HEAD` to the `main` branch. There are two options:

1. `git switch -`: this switches to wherever we were before this, which,
   in this case, was `main`.
2. `git switch main`: this explicitly switches to `main`.

Let's try:

``` {.default}
$ git switch main
  Previous HEAD position was 5a02fed Added
  Switched to branch 'main'
```

Notice there was no `--detach` in that `git switch`! We're reattaching
the head, not detaching it, so we don't have to tell Git we know what
we're doing.

> **Don't worry if you forget the `--detach`.** Git will tell you if you
> need it.
>
> ``` {.default}
> $ git switch 5a02
>   fatal: a branch is expected, got commit '5a02'
>   hint: If you want to detach HEAD at the commit, try again with
>         the --detach option.
> ```

<!-- ` -->

And now if we `git log`, we see all our changes again:

``` {.default}
commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
Author: User Name <user@example.com>
Date:   Thu Feb 1 12:36:13 2024 -0800

    More output

commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2
Author: User Name <user@example.com>
Date:   Thu Feb 1 09:24:52 2024 -0800

    Added
```

and our working tree will be updated to show the files as they are in
the `main` commit.

And you see the `HEAD -> main`? The arrow means `HEAD` is reattached to
`main`. (If `HEAD` were detached at the same commit as `main`, you'd see
`HEAD, main`.)

[i[`HEAD`]>]

## The Old Command: `git checkout`

[i[Checkout]<]

In ye olden days before `git switch` existed, there was a command to do
all that stuff called `git checkout`. `git checkout` did a lot of
things, and it still does. Because it does so much, the maintainers of
Git have been trying to break some of that functionality into `git
switch` and other commands.

> **There are still times when you need to use `checkout`**, but if your
> version of Git supports `switch`, this isn't one of them. Use `switch`
> if you can and skip this section.

But let's redo the previous section by using just `git checkout` instead
of `git switch`. Let's try:

``` {.default}
$ git checkout 5a02
```

and it says:

``` {.default}
Note: switching to '5a02fede3007edf55d18e2f9ee3e57979535e8f2'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 5a02fed Added
```

Well, that's a lot of scary stuff, but it's just Git telling us that
we're now in detached head state. Which of course we are since we just
detached the head from branch `main` by switching to a specific commit
hash.

And we can get back to the `main` branch with:

``` {.default}
$ git checkout main
```

You can also switch back with the aforementioned `git switch` variants,
but we're pretending those don't exist for this section.

[i[Checkout]>]

## Commits Relative to `HEAD`

[i[`HEAD`-->Commits relative to]]

There are a couple shortcuts to get to commits that are earlier than
`HEAD`, like, "I want to switch to the 3rd commit before this one."

Here's a pretty useless example that we'll start with:

[i[Switch]]

``` {.default}
$ git switch --detach HEAD
```

This moves `HEAD` to where `HEAD` was. That is, it moves it nowhere.
(Though it does have the effect of detaching it from the branch.)

But what if I wanted to move to the commit right *before* where `HEAD`
is now? You can do it with ***caret notation*** like this:

``` {.default}
$ git switch --detach HEAD^
```

And that gets you to the previous commit.

What if you wanted to get to the _third-previous_ commit? You can add
more carets!

``` {.default}
$ git switch --detach HEAD^^^
```

Or the 10th previous commit!

``` {.default}
$ git switch --detach HEAD^^^^^^^^^^
```

Or the 100th previous commit!

``` {.default}
$ git switch --detach HEAD^^^^^^^^^^^^^^^^^^^^forget this
```

Typing all these carets is wearing me out. Luckily there's *another*
shorthand we have at our disposal with ***tilde notation***. The two
following lines are equivalent:

``` {.default}
$ git switch --detach HEAD^^^
$ git switch --detach HEAD~3
```

After the tilde, you can just give the number of commits back you want
to go. So back to my example:

``` {.default}
$ git switch --detach HEAD~100   # Much easier
```

All this said, personally I usually just look at the log and go to a
specific commit instead of counting back.

> *"But that's just, like, my opinion, man."*\
> \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ —The Dude
