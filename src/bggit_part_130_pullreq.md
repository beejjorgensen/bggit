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

TODO

## Making Your Changes

TODO

## Making a Pull Request

TODO

## Flipside: Merging a Pull Request

TODO

## Making Many Pull Requests with Branches

TODO
