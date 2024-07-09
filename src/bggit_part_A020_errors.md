# Appendix: Errors and Scary Messages

## Detached Head

Did you get this alarmingly guillotinesque message?

``` {.default}
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 0da5af9 line 1
```

This means that you've checked out a commit directly instead of checking
out a branch. That is, your `HEAD` is no longer attached to a branch,
i.e. it is "detached".

To get out of this, you can:

1. Undo the checkout that got you detached:

   ``` {.default}
   git switch -
   ```

2. Switch to another branch entirely:

   ``` {.default}
   git switch main
   ```

3. Make a new branch here and check it out:

   ``` {.default}
   git switch -c newbranch
   ```

And now your `HEAD` is no longer detached.

## Upstream Branch Name Doesn't Match Current

Did you accidentally run `git branch -c newbranch` when you meant to run
`git switch -c newbranch`? Because if you did, it could land you here:

``` {.default}
fatal: The upstream branch of your current branch does not match
the name of your current branch.  To push to the upstream branch
on the remote, use

    git push origin HEAD:main

To push to the branch of the same name on the remote, use

    git push origin HEAD

To choose either option permanently, see push.default in 'git help config'.

To avoid automatically configuring an upstream branch when its name
won't match the local branch, see option 'simple' of branch.autoSetupMerge
in 'git help config'.
```

Let's check our branch names to see what's going on:

``` {.default}
$ git branch -vv
  main      fc645f2 [origin/main] line 2
* newbranch 7c21054 [origin/main: behind 1] line 1
```

That tells us our local branch names and, in brackets, the corresponding
remote-tracking branch. Notice anything fishy?

It seems `main` corresponds with `origin/main`.

And that `newbranch` **also** corresponds with `origin/main`! How?!

Well, when you did `git branch -c newbranch`, that _copies_ the current
branch (`main` in this example) into the other branch, _including its
remote-tracking branch_. Bad news, since you really want `newbranch` to
correlate to `origin/newbranch`, if anything.

You have a few options.

1. You want to push `newbranch` up to the `origin` and track it as
   `origin/newbranch`.

   Just do this to push and change the remote-tracking branch name:

   ``` {.default}
   $ git push -u origin newbranch
   ```

2. You just want this to be a local branch and don't need it on the
   remote.

   In this case, just unset the upstream:

   ``` {.default}
   $ git branch --unset-upstream newbranch
   ```

## Current Branch Has No Upstream Branch

Trying to push and getting this message?

``` {.default}
fatal: The current branch topic1 has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin topic1

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'
```

This just means there's no upstream tracking branch for `topic1`—it's
just a local branch.

If you do want to push this branch, just follow the suggested
instruction.

If you are pushing from the wrong branch by accident, switch to the
right one first.
