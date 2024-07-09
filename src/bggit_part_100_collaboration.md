# Collaboration across Branches

Let's say you're on a team of coders and you all have access to the same
GitHub repo. (One person on the team owns the repo, and they've
[fl[added you all as
collaborators|https://docs.github.com/en/enterprise-server@3.9/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository]].)

How can you all structure your work so that you're minimizing conflicts?

There are a lot of ways to do this, and one of them is described in this
chapter.

## Communication and Delegation

Git can't save you from poor communication. The only way to minimize
conflicts in a shared project to communicate with your team and clearly
assign different tasks to people in a non-conflicting way.

Two people shouldn't generally be editing the same part of the same
file, or even any part of the same file. That's more of a guideline than
a rule, but if you follow it, you will never have a merge conflict.

Takeaway: without good communication and a good distribution of work on
your team, you're doomed. Make a plan and stick to it.

## The Plan

It's important to note that this is _a_ plan, and it most definitely can
be improved. There are many, many different collaboration patterns
possible with Git.

In this scenario, we treat `main` as the as-yet complete working code,
and we treat contributors' branches as where work is done. When a
contributor gets their code working, they merge it back into `main`.

Here we go:

* One person makes the GitHub repo
* The owner of the GitHub repo adds all the team members as
  collaborators.
* Everyone clones the repo.
* Everyone makes their own branch, possibly naming it after themselves.
* Everyone pushes their branch to GitHub, making them remote-tracking
  branches. (We do this so that your work is effectively backed up on
  GitHub when you push it.)
* Work is delegated to all collaborators. The work should be as
  non-overlapping as possible.
* As collaborators finish their tasks, they will:
  * Test everything on their branch.
  * Merge their functioning branch into `main`, but don't push.
  * Test `main`.
  * Fix their branch if necessary, and repeat the merge until working.
  * Push.

The result will look something like this to start, where all the
collaborators have made their own branches off of main:

``` {.default}
             +
            /+
           / #\
          /  + \
         /  /#  \
        /  / #   \
       /  /  #M  |c
      /  /   #A  |h
     /  b|   #I  |r
    a|  o|   #N  |i
    l|  b|   #   |s
    i|   |   #   |
    c|   |   #   |
    e|   |   #   |
     |   |   #   |
     :   :   :   :
```

Let's say Chris (on branch `chris`) finishes up their work and wants
other contributors to be able to see it. It's time to merge into `main`.

``` {.default}
     |  b|   #   |
    a|  o|   #   |c
    l|  b|   #   |h
    i|   |   #   |r
    c|   |   #M  |i
    e|   |   #A  |s
     |   |   #I  |
     |   |   #N  /
     |   |   #  /
     |   |   # /
     |   |   #/
     |   |   +
```

After that, other contributors looking at `main` will see the changes.

