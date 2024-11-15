# Remotes: Repos in Other Places

[i[Remotes]<]

A _remote_ is just a name for a remote server you can clone, push, and
pull from.

We identify these by a URL. With GitHub, this is a URL we copied when we
went to clone the repo initially.

It's possible to use this URL to identify the server in our Git usage,
but it's unwieldy to type. So we give the remote server URLs nicknames
that we just tend to call "remotes".

A remote we've already seen a bunch of is [i[Remotes-->`origin`]] `origin`. This is the nickname
for the remote repo you cloned from, and it gets set automatically by
Git when you clone.

## Remote and Branch Notation

[i[Remotes-->Remote branches]]

Before we begin, note that Git uses slash notation to refer to a
specific branch on a specific remote: `remotename/branchname`.

For example, this refers to the `main` branch on the remote named
`origin`:

``` {.default}
origin/main
```

And this refers to the branch named `feature3490` on a remote named
`nitfol`:

``` {.default}
nitfol/feature3490
```

We'll talk more about this in the Remote Tracking Branches chapter.

## Getting a List of Remotes

[i[Remotes-->Listing]]

You can run `git remote` with the `-v` option in any repo directory to
see what remotes you have for that repo:

``` {.default}
$ git remote -v
  origin    https://github.com/example-repo.git (fetch)
  origin    https://github.com/example-repo.git (push)
```

We see that we're using the same URL for the remote named `origin` for
both push (part of which is `fetch`) and pull. Having the same URL for
both is super common.

And that URL is the exact same one we copied from GitHub when cloning
the repo in the first place.

## Renaming a Remote

[i[Remotes-->Renaming]]

Remember that a remote name is just an alias for some URL that you
cloned the repo from.

Let's say that you are all set up with your SSH keys to use GitHub for
both push and pull, but you accidentally cloned the repo using the HTTPS
URL. In that case, you'll see the following remote:

``` {.default}
$ git remote -v
origin    https://github.com/example-repo.git (fetch)
origin    https://github.com/example-repo.git (push)
```

And then you try to push, and GitHub tells you that you can't push to an
HTTPS remote... dang it!

You meant to copy the SSH URL when you cloned, which for me looks like:

``` {.default}
git@github.com:beejjorgensen/git-example-repo.git
```

Luckily it's not the end of the world. We can just change what the alias
points to.

(The example below is split into two lines so that it's not too wide for
the book, but it can be on a single line. The backslash lets Bash know
that the line continues.)

``` {.default}
$ git remote set-url origin \
             git@github.com:beejjorgensen/git-example-repo.git
```

And now when we look at our remotes, we see:

``` {.default}
$ git remote -v
origin    git@github.com:beejjorgensen/git-example-repo.git (fetch)
origin    git@github.com:beejjorgensen/git-example-repo.git (push)
```

And now we can push! (Assuming we have our SSH keys set up.)

## Adding a Remote

[i[Remotes-->Adding]]

There's nothing stopping you from adding another remote.

A common example is if you _forked_ a GitHub Project (more on that
later). A fork is a GitHub construct that enables you to easily clone
someone else's public repo into your own account, and gives you a handy
way to share changes you make with the original repo.

Let's say I forked the Linux source repo. When I clone my fork, I'll
see these remotes:

``` {.default}
origin    git@github.com:beejjorgensen/linux.git (fetch)
origin    git@github.com:beejjorgensen/linux.git (push)
```

I don't have access to the real Linux source code, but I can fork it and
get my own copy of the repo.

Now, if Linus Torvalds makes changes to his repo, I won't automatically
see them. So I'd like some way to get his changes and merge them in with
my repo.

I need some way to refer to his repo, so I'm going to add a remote
called `reallinux` that points to it:

``` {.default}
$ git remote add reallinux https://github.com/torvalds/linux.git
```

Now my remotes look like this:

``` {.default}
origin    git@github.com:beejjorgensen/linux.git (fetch)
origin    git@github.com:beejjorgensen/linux.git (push)
reallinux    https://github.com/torvalds/linux.git (fetch)
reallinux    https://github.com/torvalds/linux.git (push)
```

> Normally when setting up a remote the refers to the source of a forked
> repo on GitHub, people tend to call that remote `upstream`, whereas
> I've clearly called it `reallinux`.
>
> I did this because when we subsequently talk about remote tracking
> branches, we're going to use "upstream" to mean something else, and I
> don't want the two to be confusing.
>
> Just remember IRL when you set up a remote to point to the forked-from
> repo, it's relatively customary to call that remote `upstream`.

Now I can run this to get all the changes from Linus's repo:

``` {.default}
$ git fetch reallinux
```

And I can merge it into my branch (the Linux repo uses `master` for the
`main` branch):

``` {.default}
$ git switch master           # My local master
$ git merge reallinux/master   # Note the slash notation!
```

That will merge the `master` branch from the `reallinux` into my local
master, once we've dealt with any conflicts.

At this point if I did a `git log`, I'd see that the latest commit would
indicate that my `HEAD` was attached to my `master` branch, and it was
pointing to the same commit as the `reallinux/master`:

``` {.default}
(HEAD -> master, reallinux/master)
```

This is expected, since I just merged `reallinux/master` into my
`master`, so they definitely should be pointing to the same commit.

But looking farther down, I'd see the `master` branch on my origin
lagging behind a few commits:

``` {.default}
(origin/master, origin/HEAD)
```

> You might or might not have `origin/HEAD` depending on how you made
> your repo.

At this point I'd do a `git push` to get them all on the same commit, so
the top commit would show:

``` {.default}
(HEAD -> master, reallinux/master, origin/master, origin/HEAD)
```

And now we're all happily pointing to the same commit.

It's interesting that my local `master` can be out of sync from the
`master` on `origin`, right?

We'll look at this in the Remote Tracking Branches chapter.

[i[Remotes]>]
