# Collaboration across Branches

Let's say you're on a team of coders and you all have access to the same
GitHub repo. (One person on the team owns the repo, and they've
[fl[added you all as
collaborators|https://docs.github.com/en/enterprise-server@3.9/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository]].)

> I'm going to use the term _collaborator_ to mean "someone to whom you
> have granted write access to your repo".

How can you all structure your work so that you're minimizing conflicts?

There are a number of ways to do this.

* Everyone is a collaborator on the repo, and:
  * Everyone uses the same branch, probably `main`, or:
  * Everyone uses their own remote tracking branch and periodically
    merges with the main branch, or:
  * Everyone uses their own remote tracking branch and periodically
    merges with a development branch, which itself is periodically
    merged into `main` for each official release.
* Or everyone has their own repo (and are not collaborators on the same
  repo), and:
  * Everyone uses _pull requests_ or other synchronization methods to
    get their repos merged into the other devs'.

We'll look at the first few ways in this chapter, but we'll save pull
requests for later.

There's no one-size-fits-all approach to teamwork with Git, and the
methods outlined below can be mixed and matched with local topic
branches, or people having multiple remote tracking branches, or
whatever. Often management will have an approach they want to use for
collaboration which might be one of the ones in this section, or maybe
it's a variant, or maybe its something completely different.

In any case, the best strategy for you, the learner, is to just be
familiar with the tools (branching, merging, conflict resolution,
pushing, pulling, remote tracking branches) and use them for effect
where it makes the most sense.

And when you're first starting out, your intuition about "where it makes
the most sense" might not be dead-on, but it probably won't be lethal
and you'll figure it out in the school of hard knocks.

> "Oh great. Another f---ing learning experience." \
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;—Actual quote from my mother

## Communication and Delegation

Git can't save you from poor communication. The only way to minimize
conflicts in a shared project to communicate with your team and clearly
assign different tasks to people in a non-conflicting way.

Two people shouldn't generally be editing the same part of the same
file, or even any part of the same file. That's more of a guideline than
a rule, but if you follow it, you will never have a merge conflict.

As we've seen, it's not the end of the world if there is a merge
conflict, but life sure is easier if they're just avoided.

Takeaway: without good communication and a good distribution of work on
your team, you're doomed. Make a plan where no one is stepping on toes,
and stick to it.

## Approach: Everyone Uses One Branch

This is really easy. Everyone has push access to the repo and does all
their work on the `main` branch.

Benefits:

* Super simple to set up.
* Conceptually not much to juggle.
* All work instantly available to all collaborators upon push.

Drawbacks:

* More potential for merge conflicts.
* Unless you're rebasing (more on that later), you'll have a lot of
  merge commits.
* You can't push non-working code since it will break everything for
  everyone else.

Initial setup:

* One person makes the GitHub repo
* The owner of the GitHub repo adds all the team members as
  collaborators.
* Everyone clones the repo.

Workflow:

* Work is delegated to all collaborators. The work should be as
  non-overlapping as possible.
* Everyone periodically pulls `main` and resolves any merge conflicts.
* Everyone pushes their work to `main`.

In real life, this approach is probably only used on very small teams,
e.g. three people at most, with frequent and easy communication between
all members. If you're working on a small team in school, it could very
well be enough, but I'd still recommend trying a different approach just
for the experience.

The other approaches are not that much more complex, and give you a lot
more flexibility.

## Approach: Everyone Uses Their Own Branch

In this scenario, we treat `main` as the working code, and we treat
contributors' branches as where work is done. When a contributor gets
their code working, they merge it back into `main`.

Benefits:

* You get to work on your own branch without worrying about messing up
  other people's work.
* You can commit non-working code since no one else can see it. (You
  might be wrapping up the work day and want to push some incomplete
  code for a backup, for example.)
* Less merge conflict potential since fewer merges are happening than if
  everyone were committing to `main`.

Drawbacks:

* If your branch diverges too far from `main`, merging might become
  painful.
* Unless you're rebasing, the incremental work on your branch might
  "pollute" the commit history on `main` with a lot of tiny commits.

Initial setup:

* One person makes the GitHub repo
* The owner of the GitHub repo adds all the team members as
  collaborators.
* Everyone clones the repo.
* Everyone makes their own branch, possibly naming it after themselves.
* Everyone pushes their branch to GitHub, making them remote-tracking
  branches. (We do this so that your work is effectively backed up on
  GitHub when you push it.)

Workflow:

* Work is delegated to all collaborators. The work should be as
  non-overlapping as possible.
* As collaborators finish their tasks, they will:
  * Test everything on their branch.
  * Merge the latest `main` into their branch; do a pull to make sure
    you have it. (The collaborator might already have the latest `main`
    if no one else has merged into it, which will cause Git to say
    there's nothing to do. This is fine.)
  * Test everything, and fix it if necessary.
  * Merge their functioning branch into `main`.
  * Push.
    * If someone else has modified `main` while you were testing, Git
      will complain that you have to pull before you can push. If
      there's a conflict at this point, you'll have to resolve, test,
      and push it. And you'll have to merge `main` back into your branch
      so that your branch is up-to-date.

The result will look something like Figure_#.1 to start, where all the
collaborators have made their own branches off of `main`.

![Collaborators branching off `main`.](img_100_010.pdf "[Collaborators branching off main.]")

<!--
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
-->

Let's say Chris (on branch `chris`) finishes up their work and wants
other contributors to be able to see it. It's time to merge into `main`,
as we graphically see in Figure_#.2.

![Chris merges back into `main`.](img_100_020.pdf "[Chris merges back into main.]")

<!--
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
-->

After that, other contributors looking at `main` will see the changes.

## Approach: Everyone Merges to the Dev Branch

In this scenario, we treat `main` as the published code that we're
going to distribute, often tagged with a release version number, and we
treat a `dev` branch as the working, unreleased code. And, as in the
previous scenario, everyone has their own branches they're developing
on.

The idea is basically we're going to have two versions of the working
code:

1. The public, released version that's on `main`.
2. The private, internal version that's on `dev`.

And then, of course, we'll have one branch per collaborator.

Another way of thinking about it is that we're going to have our
internal build on `dev` that is good for testing and then, when it's all
ready, we'll "bless" it and merge it into `main`.

So there will be a lot of merges into `dev` from all the developer
branches, and then every so often there will be a merge from `dev` into
`main`.

*The developers will never directly merge into `main`!* Usually
that is performed by someone in a managerial role.

![Working on the `dev` branch.](img_100_030.pdf "[Working on the dev branch]")

Overall the process works as in Figure_#.3. This is a busy image, but
notice how Bob and Alice are only merging their work into the `dev`
branch, and then every so often, their manager merges the `dev` branch
into `main` and tags that commit with a release number. (More on tagging
later.)

Benefits:

* All the benefits of everyone having their own branch.
* You have an internal branch from which you can make complete builds
  for internal or external testing.

Drawbacks:

* A little more complexity and management.
* If your branch diverges too far from `dev`, merging might become
  painful.
* Unless you're rebasing, the incremental work on your branch might
  "pollute" the commit history on `dev` with a lot of tiny commits.

Initial setup:

* One person makes the GitHub repo
* The owner of the GitHub repo adds all the team members as
  collaborators.
* Everyone clones the repo.
* Everyone makes their own branch, possibly naming it after themselves.
* Everyone pushes their branch to GitHub, making them remote-tracking
  branches. (We do this so that your work is effectively backed up on
  GitHub when you push it.)

Workflow:

* Work is delegated to all collaborators. The work should be as
  non-overlapping as possible.
* As collaborators finish their tasks, they will:
  * Test everything on their branch.
  * Merge the latest `dev` into their branch; do a pull to make sure
    you have it. (The collaborator might already have the latest `dev`
    if no one else has merged into it, which will cause Git to say
    there's nothing to do. This is fine.)
  * Test everything, and fix it if necessary.
  * Merge their functioning branch into `dev`.
  * Push.
    * If someone else has modified `dev` while you were testing, Git
      will complain that you have to pull before you can push. If
      there's a conflict at this point, you'll have to resolve, test,
      and push it. And you'll have to merge `dev` back into your branch
      so that your branch is up-to-date.

Managerial Workflow:

* Coordinate with all devs to get a candidate release in `dev` tested
  out and ready.
* Merge that candidate release (some commit) from `dev` into `main`.
* Tag the `main` commit with some version number, optionally.

