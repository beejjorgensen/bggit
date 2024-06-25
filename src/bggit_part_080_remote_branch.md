# Remote Tracking Branches

We've seen how to create local branches that you do work on and then
merge back into the `main` branch, then `git push` it up to a remote
server.

This part of the guide is going to try to clarify what's actually going
on behind the scenes, as well as give us a way to push our local
branches to a remote for safe keeping.

## Branches on Remotes

First, some refresher!

Recall that the remote repo you cloned yours from is a complete copy of
your repo. The remote repo has a `main` branch, and therefore your
clone also has a `main` branch.

That's right! When you make a GitHub repo and then clone it, there are
**two** `main` branches!

How do we differentiate them?

Well, on your local clone, we just refer to branches by their plain
name. When we say `main` or `topic2`, we mean the local branch by that
name on our repo.

If we want to talk about a branch on a remote, we have to give the
remote name along with the branch using that slash notation we've
already seen:

``` {.default}
main            # main branch on your local repo
origin/main     # main branch on the remote named origin
upstream/main   # main branch on the remote named upstream
zork/mailbox    # mailbox branch on the remote named zork
mailbox         # mailbox branch on your local repo
```

Importantly, not only do the words `origin/main` refer to the `main`
branch on `origin` in casual conversation, but _you actually have a
branch on your local repo called `origin/main`_.

This is called a _remote-tracking branch_. It's your local copy of the
`main` branch on the remote. You can't move your local `origin/main`
branch directly; Git does it for you as a matter of course when you
interact with the remote (e.g. when you pull).

We're going to call the `main` branch on our local machines the _local
branch_, and we'll call the one on `origin` the _upstream branch_.

## Pushing to a Remote

Fun Fact: when you push or pull, you technically specify the remote and
the branch you want to use. This is me saying, "Push the branch I'm on
right now (presumably `main`) and merge it into `main` on `origin`.

``` {.default}
$ git push origin main
```

"But wait! I haven't been doing that!"

It turns out there's an option you can set to make it happen
automatically. Let's say you're on the `main` branch and then run this:

``` {.default}
$ git push --set-upstream origin main
$ git push -u origin main              # same thing, shorthand
```

This will do a couple things: 1) it'll push changes on your local `main`
to the remote server, and 2) it'll remember that the remote branch
`origin/main` is tracking your local `main` branch.

And then, from then on, from the `main` branch, you can just:

``` {.default}
$ git push
```

and it'll automatically push to `origin/main` thanks to your earlier
usage of `--set-upstream`.

And `git pull` has the same option, as well, though you only need to do
it once with either push or pull.

"But wait! I've never used `--set-upstream`, either!"

That's because by default when you clone a repo, Git automagically sets
up a local branch to track the `main` branch on the remote.

> **Bonus Info**: Depending on how you made your repo, you might also
> have a reference to `origin/HEAD`. It might be weird to think that
> there's a `HEAD` ref on a remote server that you can see, but in this
> case it's just referring to the branch that you'll be checking out by
> default when you clone the repo.

"OK, so what you're telling me is that I can just `git push` and `git
pull` like always and just ignore everything you wrote in this section?"

Well... yes. Ish. No. We're going to make use of this to push other
branches to the remote!

## Making a Branch and Pushing to Remote

I'm going to make a new local branch `topic99`:

``` {.default}
$ git switch -c topic99
Switched to a new branch 'topic99'
```

And make some changes:

``` {.default}
$ vim README.md        # Create and edit a README
$ git add README.md
$ git commit -m "Some important additions"
```

In our log, we can see where all the branches are:

``` {.default}
commit 79ddba75b144bad89e1cbd862e5f3b3409f6c498 (HEAD -> topic99)
Author: User Name <user@example.com>
Date:   Fri Feb 16 16:44:50 2024 -0800

    Some important additions

commit 3be2ad2c31b627b431af8c8e592c01f4b989d621 (origin/main, main)
Author: User Name <user@example.com>
Date:   Fri Feb 16 16:14:13 2024 -0800

    Initial checkin
```

`HEAD` refers to `topic99`, and that's one commit ahead of `main`
(local) and `main` (upstream on the `origin` remote), as far as we know.
And we know this because it's one commit ahead of our remote-tracking
branch `origin/main`.

Now let's push!

``` {.default}
$ git push
fatal: The current branch topic99 has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin topic99

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.
```

Ouch. The short of all this is that we said "push", and Git said, "To
what? You haven't associated this branch with anything on the remote!"

And we haven't. There's no `origin/topic99` remote-tracking branch, and
no  TODO

