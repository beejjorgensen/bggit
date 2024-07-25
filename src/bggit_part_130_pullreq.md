# GitHub: Forking and Pull Requests

What if you want to make changes to a repo on GitHub but you don't have
write permission? Here's how.

A ***fork*** is a clone of someone else's GitHub repo that you've made
on GitHub using their "Fork" command. It's a regular clone except that
GitHub is doing some bookkeeping to track which repo you forked from.

The ***upstream*** is by convention the name of the remote that you
forked from.

A ***pull request*** (or "PR" for short) is a way for you to offer
changes you've made to your fork to the owner of the original repo.

> **Pull Requests are a GitHub thing, not a Git thing.** It's some
> additional functionality that GitHub has implemented on their website
> that you can use.

Let's say, for example, you found an open source project you liked and
there was a bug in it. You don't have permission to write to the
project's GitHub repo, so how can you change it?

The process for someone making a pull request is:

1. On GitHub: fork the repo. Now you have your own clone of it.
2. Clone your repo to your local machine. Now you have two clones of it:
   your fork on GitHub and its clone on your local machine.
3. Make the fix on your local machine and test it.
4. Push your fix to your GitHub fork.
5. On GitHub, create a pull request. This informs the upstream owner
   that you have changes you'd like them to merge.
6. On GitHub, the upstream owner reviews your PR and decides if they
   want to merge it. If so, they merge it. Otherwise they delete it.
7. At this point, if you're done, you can optionally delete your fork.

Let's give it a try! Feel free to issue PRs on my sample repo, used
below. I'm just going to delete them (they won't be merged); don't take
it personally—I just don't have time to review them all.

## Making a Fork

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

Are you ready to make a PR? Hold up just a moment!

What if the upstream owner has made changes to their repo in the
meantime? Don't you want to make sure your code works with the latest
version of their code?

Of course you do.

On your fork's page, you might have noticed that it has a "Sync fork"
button that you can pull down.

If you pull it down and it says "This branch is not behind the
upstream", then congratulations! You're already up to date! Go ahead and
make a PR, as outlined below.

If not, TODO

## Making a Pull Request

Now that we've modified our fork to our satisfaction, we can ask the
upstream maintainer if they're willing to accept it into the official
repo.

> **Maybe they aren't ready!** Don't take it personally if they don't
> answer or answer with ways they need your patch improved. Work with
> the owners to get the job done to both of your satisfactions.

Let's go!

* Click the "Contribute" button and then "Open pull request".
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

To do that, look right below the description to the contributor's avatar
and the commit message. Click on the commit message and you'll see a
diff[^A diff shows the difference between two files.]. Lines marked with
a `+` are added, and lines marked with `-` are removed.

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
What now?

TODO

## Making Many Pull Requests with Branches

TODO


## Deleting a Pull Request

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

