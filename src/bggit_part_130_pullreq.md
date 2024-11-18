# GitHub: Forking and Pull Requests

[i[Forking]<]
[i[Pull requests]<]

What if you want to make changes to a repo on GitHub but you don't have
write permission? Here's how.

A ***fork*** is a clone of someone else's GitHub repo that you've made
on GitHub using their "Fork" command. It's a regular clone except that
GitHub is doing some bookkeeping to track which repo you forked from.

The ***upstream*** is by convention the name of the remote that you
forked from.

A ***pull request*** (or "PR" for short) is a way for you to offer
changes you've made to your fork to the owner of the original repo.

> **Forks and Pull Requests are a GitHub thing, not a Git thing.** It's
> some additional functionality that GitHub has implemented on their
> website that you can use.

Let's say, for example, you found an open source project you liked and
there was a bug in it. You don't have permission to write to the
project's GitHub repo, so how can you change it?

The process for someone making a pull request is:

1. On GitHub, fork the repo. Now you have your own clone of it.
2. Clone your repo to your local machine. Now you have two clones of it:
   your fork on GitHub and its clone on your local machine.
3. Make the fix on your local machine and test it.
4. Push your fix to your GitHub fork.
5. On GitHub, create a pull request. This informs the upstream owner
   that you have changes you'd like them to merge.
6. On GitHub, the upstream owner reviews your PR and decides if they
   want to merge it. If so, they merge it. Otherwise they comment and
   ask for changes, or delete it.
7. At this point, if you're done, you can optionally delete your fork.

Let's give it a try! Feel free to issue PRs on my sample repo, used
below. I'm just going to delete them (they won't be merged); don't take
it personally—I just don't have time to review them all.

## Making a Fork

[i[Fork-->Creating]]

Head on over to [fl[my test
repo|https://github.com/beejjorgensen/git-example-repo]] and let's do
this:

* In the upper right there should be a button labeled "Fork". Click it.
* Under "Owner", choose your user name.
* Under "Repository name", chose the default or make a new name.
* Click the "Create fork" button.

> **This can be done with impunity.** That is, you've made your own fork
> but the original owner is unaware that you did. You can delete it with
> no damage to the original repo. Remember that a fork is a clone on
> GitHub that you have ownership of independent of the original repo.

At this point, you should land on the project page for your fork, and
the fine print on the page reads: "forked from
beejjorgensen/git-example-repo".

And now we have our own version of that repo on GitHub to do with as we
please.

We can clone it as normal, pull, push, delete the repo, etc. The owner
of the original repo will not know about it—our changes affect our repo
alone. Later we'll see how to issue a pull request to try to get our
changes in the original upstream repo.

## Making Your Changes

Let's make some changes. First, we have to clone *our* repo (that is,
clone the fork we made) onto our local machine.

So pull down the "Code" button as usual and select the SSH link to clone
(or use the GitHub CLI variant if you're using that).

``` {.default}
$ git clone git@github.com:user/git-example-repo.git
  Cloning into 'git-example-repo'...
  remote: Enumerating objects: 4, done.
  remote: Counting objects: 100% (4/4), done.
  remote: Compressing objects: 100% (3/3), done.
  remote: Total 4 (delta 0), reused 4 (delta 0), pack-reused 0
  Receiving objects: 100% (4/4), done.
```

And then you can `cd` into that directory and see the files there.

``` {.default}
$ cd git-example-repo
$ ls
  hello.py    README.md
```

Let's modify `hello.py` to this:

``` {.py .numberLines}
#!/usr/bin/env python

print("Hello, world!")
print("This is my modification")
```

And let's add it, make a commit, and push.

``` {.default}
$ git add hello.py
$ git commit -m "modified"
  [main 5d3fe49] modified
   1 file changed, 1 insertion(+)
$ git push
  Enumerating objects: 5, done.
  Counting objects: 100% (5/5), done.
  Delta compression using up to 8 threads
  Compressing objects: 100% (3/3), done.
  Writing objects: 100% (3/3), 1.02 KiB | 1.02 MiB/s, done.
  Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
  To github.com:user/git-example-repo.git
     4332527..5d3fe49  main -> main
```

Again, this just pushed to our fork, not the upstream. You can look at
your fork's page on GitHub and see the change there.

## Syncing the Upstream with Your Fork

[i[Fork-->Syncing with Upstream]]

Are you ready to make a PR? Hold up just a moment!

What if the upstream owner has made changes to their repo in the
meantime? Don't you want to make sure your code works with the latest
version of their code?

Of course you do.

On your fork's page, you might have noticed that it has a "Sync fork"
button that you can pull down.

If you pull it down and it says "This branch is not behind the
upstream", then congratulations! You're already up to date! Go ahead and
make a PR, as outlined in the next section.

If you pull it down and it says "This branch is out-of-date" and offers
you an "Update branch" button, then congratulations! You're out of date,
but you can be brought up to date without a conflict. Click "Update
branch" and then go ahead and make a PR, as outlined in the next
section. (It might also offer you a "Discard" button, but don't press
that unless you want to discard your changes!)

If it instead says "This branch has conflicts that must be resolved",
bad news. You have some changes in your repo that conflict with someone
else's changes in the upstream. You have some options:

* The UI says you can open a pull request, which will give you a chance
  to resolve the conflict in-browser as outlined in the next section.
* It also says you can just throw away your changes and replace them
  with the upstream. Bummer.
* Aside from that, you can actually merge your branch from the upstream
  on the command line and take care of the conflict there without
  opening a PR first. See [Syncing on the Command Line](#sync-cl),
  below.

In general, it's a good idea to keep in sync with the upstream repo.
This way you can be sure your changes aren't conflicting with any
upstream changes as you go. It's way better than waiting to resolve them
all at the end when you're ready to issue a pull request.

## Making a Pull Request

[i[Pull request-->Creating]]

Now that we've modified our fork to our satisfaction, we can ask the
upstream maintainer if they're willing to accept it into the official
repo.

> **Maybe they aren't ready!** Don't take it personally if they don't
> answer or answer with ways they need your patch improved. Work with
> the owners to get the job done to both of your satisfactions.

Let's go!

* Click the "Contribute" button and then "Open pull request".
* Look for the text "This branch has conflicts that must be resolved".
  If you find that text, it means the upstream can't automatically apply
  your PR and they'll have to do manual work to make it happen. They're
  far more likely to just reject it. To avoid this, you have some options:
  * Don't open the PR, go back and sync with the upstream, fix the
    conflict, and try again.
  * Or click the "Resolve conflicts" button right there in the UI and
    use the in-browser editor to manually resolve.
* Add a nice title.
* Add a good description. You're asking someone to incorporate your code
  into their project, so you'll want to describe what the code does here
  to make their lives easier when they review it. (Since this example
  goes to my repo, you can just pretend you wrote something nice—I'm
  just going to close the PR.)
* Click "Create pull request"!

This lands us on the PR page. You can add more comments or close the
request (if you changed your mind about it).

The owner of the upstream will see the PR has been issued, and now you
have to wait for a response.

Maybe they respond with a comment asking for improvements or other
questions. Maybe they reject the PR and close it, unmerged. Or maybe
they accept! Happy days!

## Flipside: Merging a Pull Request

[i[Pull request-->Merging]]

As the upstream owner, if someone issues a PR you'll be notified (unless
you've turned those notifications off) with an email and in the
notifications in GitHub in the upper right.

When you do, you can visit your project page on GitHub and decide what
to do with the PR.

At the top of the project page, you'll see a "Pull requests" button with
a number next to indicating how many PRs are currently outstanding.

* Click the button to see the list.
* Click on a PR title to get to the PR.

Now we're looking at the PR. Read the description to see what it does,
and then, **very importantly** review the code!

> **You're about to accept code from someone you probably don't know.**
> On this planet, most people are friendly, but that doesn't mean there
> aren't some bad actors (the industry term is *a\-\-holes*) out there
> looking to take advantage of you by introducing some malicious code.
> Even if you've known the contributor for a year, they might be playing
> a long game, and if that seems unlikely to you,
> [flw[read about the XZ utils hack that took place in 2024|XZ_Utils_backdoor]].

To review the code, look right below the description to the
contributor's avatar and the commit message. Click on the commit message
and you'll see a diff[^6ec7]. Lines marked with a `+` are added, and
lines marked with `-` are removed.

[^6ec7]: A diff shows the difference between two files.

If you just want a straight up view of the file as it was edited by the
contributor, you can hit the "..." on the right and then "View file".

If it's almost right but you need to make a modification, you can also
hit "Edit file" and add commits directly to the PR.

If everything looks good, scroll down and hopefully you'll see some text
that reads "This branch has no conflicts with the base branch" and
"Merging can be performed automatically". This is good news.

If it says that, you can just click "Merge pull request", and that will
add the changes to your repo and close the PR. It's nice to also add a
comment thanking the contributor—they just gave you work for free, after
all!

> **Closing a PR doesn't delete the PR.** You can still reopen it.

But let's say the PR does conflict and can't be automatically merged.
GitHub complains that "This branch has conflicts that must be resolved"
and gives you some options.

As the upstream owner, you can click the "Resolve conflicts" button and
fix the issue if possible.

Or you can just reject the PR and ask the person who opened it to
resolve the conflict so that your life might be made easier with an
automatic merge.

## Making Many Pull Requests with Branches

[i[Pull request-->With branches]]

Here's the thing about pull requests: when you make one, it takes all
the changes you have on your branch and bundles them together in one.
Doesn't matter if the changes are doing radically different things; they
all get rolled into the same PR.

This is sometimes not so great from an administrative perspective. Maybe
I want a PR for issue #1 and a different PR for issue #2!

The way to make this happen is to make a local branch on the clone of
your fork for each individual PR, and push those branches to your fork.
Then when you create the PR, you choose the branch to use. Even if your
branch is named something like `feature1`, you can still merge it into
the `main` branch on the upstream.

So make a new branch for the feature:

``` {.default}
$ git switch -c feature1
  Switched to a new branch 'feature1'
```

Then make your changes, add, and commit.

``` {.default}
$ vim readme.txt
$ git add readme.txt
$ git commit -m "feature 1"
  [feature1 1ad9e92] feature 1
   1 file changed, 1 insertion(+)
```

Then push them to your repo, setting up a remote-tracking branch:

``` {.default}
$ git push -u origin feature1
  Enumerating objects: 5, done.
  Counting objects: 100% (5/5), done.
  Delta compression using up to 8 threads
  Compressing objects: 100% (2/2), done.
  Writing objects: 100% (3/3), 979 bytes | 979.00 KiB/s, done.
  Total 3 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
  remote: Resolving deltas: 100% (1/1), completed with 1 local
  remote: object.
  remote:
  remote: Create a pull request for 'feature1' on GitHub by
  remote: visiting:
  remote:      https://github.com/user/fork/pull/new/feature1
  remote:
  To github.com:user/fork.git
   * [new branch]      feature1 -> feature1
  branch 'feature1' set up to track 'origin/feature1'.
```

Now you can jump back to GitHub and issue a PR.

There might be a handy little popup there saying "feature1 had recent
pushes 4 minutes ago" and a button "Compare and pull request" you can
click to make the PR.

But if it's been too long and the popup is gone, not to worry. See the
branch selector button on the upper left that probably says "main" right
now? Pull it down and select the branch "feature1" that you want to
create the PR for. Then click "Contribute" and open the PR.

There's a line at the top of the PR that indicates the repo and branch
that will be merged into, and, on the right, your repo and branch name
that you'll be merging from.

The rest of the PR proceeds as normal.

**Don't delete your branch until after the merge!** Once it has been
safely merged, GitHub will pop up a "Delete branch" button for you on
the PR page. This will delete the branch on GitHub, but you'll still
have to delete `feature1` and `origin/feature1` on the command line.

## Deleting a Pull Request

[i[Pull request-->Deleting]]

Short answer: you can't.

Long answer: you can.

The irony is that the short answer is longer. I don't make the rules.

Proper long answer: you can if you are the upstream owner and the PR
contains sensitive information.

There's no way in the UI to delete PRs, whether you're the forker or
forkee. And this can be a bummer especially if you've accidentally
included some sensitive information like [flw[social security number
078-05-1120|Social_Security_number#SSNs_used_in_advertising]].

But hope is not all lost! The upstream owner can visit the virtual
assistant at GitHub and [fl[ask for a pull request
removal|https://support.github.com/request?q=pull+request+removals]]
which apparently works. I haven't tried it.

If there's a way as the forker to delete the PR they created, I haven't
seen it. You'll have to plead your case with the upstream owner and get
them to do it.

In any case, you most definitely should change your leaked credentials
right now and let that be a lesson to you.

## Syncing on the Command Line {#sync-cl}

[i[Fork-->Syncing with Upstream]]

GitHub has that nice Sync button to bring the upstream changes into your
fork, and this was a welcome addition. It used to be you had to do it
the hard way.

But the hard way has an additional benefit: if the upstream conflicts
with your changes, you can merge them locally before creating the PR.
The GitHub UI requires you create a PR to resolve the conflict.

Additionally, if you just like the command line and want to quickly sync
the upstream to your branch, this can do it.

The plan is this:

1. Add an `upstream` remote that points to the upstream repo.
2. Fetch the data from `upstream`.
3. Merge the upstream branch into your branch.
4. Resolve conflicts.
5. Push your branch.
6. Go issue a now-hopefully-non-conflicting PR.

Let's try. I'll be on my `main` branch, and try to sync it with the
upstream's `main` branch. I'll show what it's like when there's a
conflict. (If there were no conflict, the merge would succeed
automatically.)

First things first: if you haven't already, set up the `upstream` remote
to point to the original owner's repo. This is the repo that you forked
from. Since you won't be pushing to it, you can use the SSH or HTTP
methods to access it. (And this remote can be named anything, but
`upstream` is a common convention.)

``` {.default}
$ git remote add upstream https://github.com/other/upstream.git
```

And then we need to get the new commits from the upstream repo and merge
them into our stuff.

``` {.default}
$ git fetch upstream
  remote: Enumerating objects: 5, done.
  remote: Counting objects: 100% (5/5), done.
  remote: Compressing objects: 100% (1/1), done.
  remote: Total 3 (delta 1), reused 3 (delta 1), pack-reused 0
  Unpacking objects: 100% (3/3), 950 bytes | 950.00 KiB/s, done.
  From https://github.com/other/upstream
   * [new branch]      main       -> upstream/main

$ git switch main   # Make sure we're on the main branch

$ git merge upstream/main
  Auto-merging readme.txt
  CONFLICT (content): Merge conflict in readme.txt
  Automatic merge failed; fix conflicts and then commit the result.
```

(You could also rebase if you wanted.)

At this point, we should edit the file and resolve the conflict, and
complete the resolution as per usual.

And then we push back to our fork on GitHub!

``` {.default}
$ git push
  Enumerating objects: 7, done.
  Counting objects: 100% (7/7), done.
  Delta compression using up to 8 threads
  Compressing objects: 100% (2/2), done.
  Writing objects: 100% (3/3), 999 bytes | 999.00 KiB/s, done.
  Total 3 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
  remote: Resolving deltas: 100% (1/1), completed with 1 local
  remote: object.
  To github.com:user/fork.git
   8b2476c..c8a7e0a  main -> main
```

If we jump back to the GitHub UI at this point and open a PR, it should
tell us "These branches can be automatically merged" which is music to
everyone's ears.

Once you have the `upstream` remote set up, all you have to do to sync
in the future is do the `git fetch upstream` and then merge or rebase
your stuff with it.

[i[Pull requests]>]
[i[Forking]>]
