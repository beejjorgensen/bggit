# Submodules

[i[Submodules]<]

You can't really have a Git repo _inside_ a Git repo. I mean, yes, you
can make one, but when you try to add it to the outer repo, Git will
have a lot to say about it.

``` {.default}
warning: adding embedded git repository: inner
hint: You've added another git repository inside your current
hint: repository. Clones of the outer repository will not contain
hint: the contents of the embedded repository and will not know how
hint: to obtain it. If you meant to add a submodule, use:
hint:
hint: 	git submodule add <url> inner
hint:
hint: If you added this path by mistake, you can remove it from the
hint: index with:
hint:
hint: 	git rm --cached inner
hint:
hint: See "git help submodule" for more information.
hint: Disable this message with "git config advice.addEmbeddedRepo
hint: false"
```

So it's probably not what you want, but Git offers a hint: maybe you
wanted something to do with submodules, instead!

Submodules give you a way to make a completely separate repo appear
inside the working tree of your current repo. Not only that, it allows
the current working tree to have a specific commit of the submodule
represented in that submodule's tree.

The canonical use case for this is when your project depends on a
library that you also have the source for. You can include the library's
repo as a submodule of your repo, and effectively pin it to a particular
version (specifically to a particular commit).

For example, maybe your code works with FooLib version 3.4.90. So you
include FooLib as a submodule and make sure it's pinned to that version.
Then even though another team might be updating FooLib, you'll always
have version 3.4.90 available to build against.

Then later when you're ready, you can update the submodule to the latest
version, say 4.0.1, and pin that one in place.

It's important to note that a submodule is just another regular Git
repo. Nothing special about it. The only thing that's notable is that
we've decided to effectively clone it inside another repo, and logically
tie it to that repo.

## Using a Repo with Submodules

Let's start by talking about what happens when you clone a repo that
already uses submodules. In this case, someone else has done the work of
putting the repo together with its submodules, but you have to do a
little bit of extra effort after cloning it so you get all the
submodules, as well.

Later we'll talk about how to add submodules to a project.

Luckily, for demonstration purposes, I have a repo you can clone that
already has a submodule defined within it. (Fork the repo before you
clone it if you want to be able to push back.)

Let's say you already know that the repo you're about to clone has
submodules. (Because someone told you it did.) You can then clone with a
flag saying you want to get all the submodule repos, too, please. You do
this with the `--recurse-submodules` switch:

``` {.default}
$ git clone --recurse-submodules \
        git@github.com:beejjorgensen/git-example-submodule-repo.git
```

(Above command split into two lines to fit in the margins.)

And that will clone the repo in question, and it will also clone all
repos listed as submodules of that repo. Go ahead and run it—it's a real
repo you can clone.

After you run it and go into the repo directory, you'll see a
`git-example-repo` directory in there. That's a completely separate repo
inside this one as a submodule. You can `cd` into it and look at the
files!

> **Any Git commands you run in the submodule directory tree apply only
> to the submodule!** Be extra careful making commits in the submodule
> directory tree—`HEAD` commonly gets detached with submodules. More on
> that later.

But let's say you forget to specify `--recurse-submodules`, or you just
plain didn't realize there were submodules here. Not to worry! You can
get them after the fact. The above command is the same as these two (or
three) commands:

``` {.default}
$ git clone \
        git@github.com:beejjorgensen/git-example-submodule-repo.git
$ cd git-example-submodule-repo
$ git submodule update --recursive --init
```

That will also get the submodules cloned. (`--recursive` is in case the
submodules have submodules (!!) and the `--init` does some necessary
bookkeeping work in your local repo. How's that for a handwavy
statement?)

And for now, that might be enough for you to get to work! All you really
needed to build the existing project was the repo and its submodules,
and you might not be in charge of the submodules and just need them to
exist for the build. So now you can get to work.

But in case you need to do more, read on!

## Creating a Submodule

[i[Submodules-->Creating]<]

Let's say you have a repo already, but you've decided you want to
include another repo as a submodule.

Again, a use case for this might be if your main repo project depends on
another one for the build, e.g. like a library. And you don't want to
use the binary form of the library (or maybe it doesn't exist), so you
need to build it.

If you didn't use submodules, anyone who wanted to build your repo would
need to also clone the library repo and juggle all that. Wouldn't it be
nicer if they could just add that `--recurse-submodules` flag to their
`clone` command and have it all set up an ready to build?

So let's go through the steps of adding a submodule to an existing repo
and see how that all works.

Feel free to use my sample repo as your submodule, use one of your own,
or anyone else's. No one knows when you make a submodule out of their
repo.

First, let's create a new repo for testing and put a commit in there for
fun:

``` {.default}
$ git init test_repo
  Initialized empty Git repository in /frotz/test_repo/.git/
$ cd test_repo
$ echo Hello, world > foo.txt
$ git add foo.txt
$ git commit -m added
```

And let's add a submodule!

``` {.default}
$ git submodule add \
                  git@github.com:beejjorgensen/git-example-repo.git
  Cloning into '/home/beej/tmp/test_repo/git-example-repo'...
  remote: Enumerating objects: 4, done.
  remote: Counting objects: 100% (4/4), done.
  remote: Compressing objects: 100% (3/3), done.
  remote: Total 4 (delta 0), reused 4 (delta 0), pack-reused 0 (from 0)
  Receiving objects: 100% (4/4), done.
```

There you go! Well, almost, anyway. Let's check our status:

``` {.default}
$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  new file:   .gitmodules
	  new file:   git-example-repo
```

What are those things on the stage? Well, `git-example-repo` is the
submodule. It's a little strange because Git is calling it a "file" when
it's a directory, but that's just part of the special treatment
submodules get.

And there's another file in there called `.gitmodules` that holds
information about all the submodules you've added.

Both of these files (treating `git-example-repo` like a file) should be
committed to your repo so that other people who clone it get the
submodule information.

``` {.default}
$ git commit -m "added submodule"
  [main cedea64] added submodule
   2 files changed, 4 insertions(+)
   create mode 100644 .gitmodules
   create mode 160000 git-example-repo
```

Now you're set! Anyone who clones the repo gets that submodule
information.

You can even do it with your test repo. Change directory to the parent
of the test repo and clone it:

``` {.default}
$ git clone --recurse-submodules test_repo test_repo2
```

After that you can `cd` into `test_repo2` and see the submodule there.

> **Can I Make a Local Repo a Submodule?** No! Git prohibits that
> because there's some security risk there that, to be honest, I haven't
> really read about. There's supposed to be a way to override that with
> a config setting, which I thought would be quite useful for messing
> around to see how submodules worked, but apparently that config
> setting doesn't work as of late 2024. So you'll have to use
> network-remote repos for submodules.

[i[Submodules-->Creating]>]

## Setting the Commit for the Submodule {#set-submodule-commit}

[i[Submodules-->Setting the commit]<]

What does this section even mean?

Here's the deal: the containing repo refers to a specific commit within
the submodule. That is, the submodule is always checked out to a
particular commit as defined in the containing repo. (The submodule
`HEAD` might be attached to a branch, but it also very well might not
be.)

The upshot of this is that when we make a repo with a submodule, we get
to dictate which exact commit of that submodule our repo is using. And
then, importantly, when someone clones our repo, they'll be looking at
the submodule at the exact same commit as we are.

This lets us do things like choose a very particular version of a
library as a submodule, and then everyone who clones our repo will get
that same version _regardless of whether or not the submodule repo was
changed elsewhere_. Someone else could move `main` wherever they want,
but we'll still use the one commit we're pinned to, even if we fetch the
new `main` commit into our submodule.

We effectively pin our submodule to a particular commit. And we probably
want to do that so that someone else developing the submodule on the
side doesn't introduce some change that breaks our containing repo's
build.

How do we do that? It's pretty easy:

1. Go to the submodule directory.
2. Switch to the commit that you want to use. You can refer to this
   commit by branch name, UUID, tag, or any other thing that `git
   switch` takes. Use `--detach` if you're detaching the `HEAD`.
3. Go back to the containing module directory.
4. Add the submodule directory.
5. Commit.

If you want to mess around with this using my test repos on GitHub, be
sure to fork them first so you have write access.

Let's do the same thing we did in the last section and create the
`test_repo` repo.

And then do the `clone` into `test_repo2` just so we have two to mess
with. (Don't forget the `--recurse-submodules` flag!)

> **We're cloning a non-bare repo, which is weird.** It's OK to clone
> it—the Git Police aren't going to show up. You just won't be able to
> push to it. And that's perfectly good enough for this demo. But it's
> something that you wouldn't normally do.

> **Also notice the detached `HEAD` in the cloned submodule repo!** If
> you look in `test_repo2/git-example-repo` and do a `git log`, you'll
> see this on the first line:
>
> ``` {.default}
> (HEAD, origin/main, origin/HEAD, main)
> ```
> <!-- ` -->
>
> See how `HEAD` is detached from `main`?
>
> Now, I'd be lying if I said I knew the exact rules for when the `HEAD`
> in a submodule gets detached, but it's not uncommon. In fact, you
> should just generally assume it's detached and attach it to a branch
> if you have to. More on this later.

Now in `test_repo`, let's go into the submodule directory and check out
an earlier version of the submodule repo. In this case, we'll just check
out the previous commit from `main`.

``` {.default}
$ cd test_repo/git-example-repo
$ git log
  commit cd1bf77d2ef08115b18d7f15a9c172dace1b2222
                           (HEAD -> main, origin/main, origin/HEAD)
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Dec 6 15:07:43 2024 -0800

      very important clarification

  commit d8481e125e6ef49e2fa8041b16b9dd3b8136b550
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Dec 6 15:07:13 2024 -0800

      improve functionality

  commit 433252748b7f9bf85e556a6a0196cdf38198fc43
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Jan 26 13:30:08 2024 -0800

      Added
```

Let's move this to the earlier commit.

``` {.default}
$ git switch --detach d8481e
  HEAD is now at d8481e1 improve functionality
```

So far so good. Now let's `cd` back to the containing repo and have a
look at where we stand.

``` {.default}
$ cd ..
$ git status
  On branch main
  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working
    directory)
	  modified:   git-example-repo (new commits)

  no changes added to commit (use "git add" and/or "git commit -a")
```

Look at that! The submodule directory is listed as modified. It says
"new commits", but that's just telling us that "things have changed
in the submodule from the commit that I was pinned onto before"

So let's add that and commit it.

``` {.default}
$ git add git-example-repo
$ git commit -m "update submodule commit"
  [main dd69bb8] update submodule commit
   1 file changed, 1 insertion(+), 1 deletion(-)
```

And now let's pull those changes in our clone, `test_repo2`—note the
`--recurse-submodule` option on the pull!

``` {.default}
$ cd ../test_repo2
$ git pull --recurse-submodules
  Fetching submodule git-example-repo
  Already up to date.
  Submodule path 'git-example-repo': checked out'
                         'd8481e125e6ef49e2fa8041b16b9dd3b8136b550'
```

And now on `test_repo2` if we jump into the `git-example-repo`
submodule, we can check the log:

``` {.default}
$ git log
  commit d8481e125e6ef49e2fa8041b16b9dd3b8136b550 (HEAD)
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Dec 6 15:07:13 2024 -0800

      improve functionality

  commit 433252748b7f9bf85e556a6a0196cdf38198fc43
  Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
  Date:   Fri Jan 26 13:30:08 2024 -0800

      Added
```

And we see `HEAD` is on commit `d8481e`, just like we set it to in
`test_repo`. (And we also do not see `main`. It's the child commit from
where `HEAD` is now, so it's not appearing in the log. We could still
switch to it if we wanted, of course.)

What have we done? We've changed the commit the submodule is pinned at
in one repo, and then we've pulled that change into another repo!

[i[Submodules-->Setting the commit]>]

## Getting Submodule Latest

[i[Submodules-->Getting latest]<]

Let's say someone else has updated the commit that the submodule is
pinned at in your repo. And you want to get up to speed.

Two steps to make that happen:

1. In the containing repo, `git pull`. This will get you the latest
   version of the containing repo that has the new pinned commit numbers
   for the submodule.

2. In the containing repo (again), run:

   ``` {.default}
   git submodule update --init --recursive
   ```

   This will fetch the submodule data and set you up to point at the
   correct commit. 

[i[Submodules-->Getting latest]>]

## Updating the Actual Submodule Itself

[i[Submodules-->Updating]<]

What do I mean by this? Let's say the submodule holds some library, and
you need to make a bug fix in the library. And you need people who use
this repo as a submodule (or otherwise) to get the changes.

So how to make this happen?

Either do it from a standalone repo, or you can also do it _in situ_ in
submodule directory.

### Modify the Submodule Repo Elsewhere

The way that's easiest for my tiny human brain is to clone the submodule
independently of any other repos. That is, clone it like it's not a
submodule at all.

Then you can push, pull, modify, etc. all you want.

[i[Fetch]] And then when you have it all fixed, you can go to the
submodule directory and do a `git fetch` to pull down the new commits.

At that point, it might be convenient to run this:

``` {.default}
$ git log HEAD^..origin/main
```

This will show you all the commits between `HEAD` and `origin/main`,
inclusive so you can see what's been done. (Assuming they're related,
that is. If they're on divergent branches you'll have to get more
creative.)

Then you choose the commit you want to pin `HEAD` to, switch to that,
and run an `add`/`commit` from the containing repo, as outlined in
[Setting the Commit for the Submodule](#set-submodule-commit), above.

### Modify the Submodule Repo in the Submodule Directory

But wait! If the submodule is a full-blown repo itself, can't you just
edit in the submodule directory?

Yes! You totally can.

The only weird part is that you might have a detached `HEAD` in your
submodule, so be sure to check out a branch that you can push if you
want to go this route.

For example:

``` {.default}
$ git switch main
```

Then make your changes and push them (from the submodule directory).

At this point, the containing repo is still pinned to the old commit. So
you'll want to run an `add`/`commit` from the containing repo, as
outlined in [Setting the Commit for the
Submodule](#set-submodule-commit), above.

[i[Submodules-->Updating]>]

## Getting the Submodule Status

[i[Submodules-->Status]<]

When it comes to which commit the submodule is pinned to, there are some
commands that are quite helpful.

The first is `git submodule status`. This will tell you where the
submodule `HEAD` is currently.

For example, running from the containing repo:

``` {.default}
$ git submodule status
898650e74c18cf4b30bdd07297d638de4a6fc7dd mysubmod (heads/main)
```

This tells me that `HEAD` in the `mysubmod` directory is at commit
`89865`.

But what if you see this with a `+` sign in front:

``` {.default}
$ git submodule status
+1c10d608190194b7f9fbb9a442abd5c63c74cdfa mysubmod (heads/main)
```

That `+` means that, although `HEAD` in the submodule is at commit
`1c10d`,  the containing repo has the submodule pinned to a
different commit! You might see this happen after you pull a submodule
(thus moving `HEAD`), but haven't updated the containing repo to match.

If you see the `+`, `git status` will also tell you more:

``` {.default}
$ git status
  On branch main
  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working
    directory)
	  modified:   mysubmod (new commits)

  no changes added to commit (use "git add" and/or "git commit -a")
```

Sure enough—we have changed `HEAD` in the submodule so its directory
shows as `modified`.

You can get rid of the plus by either pinning the repo to a new commit
as outlined in [Setting the Commit for the
Submodule](#set-submodule-commit), above, or by moving the submodule
`HEAD` back to where the containing module expects it.

> **There can also be a `-` in front of the UUID.** This means the
> submodule hasn't been initialized or downloaded. Try a `git submodule
> update --recursive --init`.

How do we figure out where the containing module expects the submodule
`HEAD` to be? With this handy command:

``` {.default}
$ git ls-tree HEAD mysubmod
  160000 commit 898650e74c18cf4b30bdd07297d638de4a6fc7dd   mysubmod
```

[i[Submodules-->Status]>]

## Some Behind the Scenes

Not really behind the scenes, actually, but I wanted to point out the
historic steps to initialize the submodule that we've shortcutted by
using some command line switches.

For example, when we cloned the repo with the submodule initially, we
used this:

``` {.default}
$ git clone --recurse-submodules \
        git@github.com:beejjorgensen/git-example-submodule-repo.git
```

That `--recurse-submodules` did a lot of work for us, cloning the
submodule and setting everything up so it was ready to use.

We also noted that if we forgot that switch, we could still pull it off:

``` {.default}
$ git clone \
        git@github.com:beejjorgensen/git-example-submodule-repo.git
$ cd git-example-submodule-repo
$ git submodule update --recursive --init
```

So `--recurse-submodules` was going that work for us.

But the rabbit hole goes farther! That `--init` does a bunch for us,
too. Let's break it down into a full by-hand process. Don't worry—it's
just a couple steps:

``` {.default}
$ git clone \
        git@github.com:beejjorgensen/git-example-submodule-repo.git
$ cd git-example-submodule-repo
$ git submodule init
$ git submodule update --recursive
```

So that `--recurse-submodules` switch to `git clone` was actually
running a bunch of commands for us behind the scenes.

A little breakdown:

When you first clone the containing repo, there's a `.gitmodules` file
in there indicating the directory name and the URL of the submodule
remote. But that's not enough info. You have to do a `git submodule
init` to cause Git to parse that file and set up some internal
bookkeeping.

After that, you can run `git submodule update` to bring in the submodule
data to use.

## Deleting a Submodule

[i[Submodules-->Deleting]<]

This is a bit clunky, but not too bad if you follow the steps.

All this action takes place from the containing repo. Let's say for this
example we want to delete the module `mysubmod`—substitute the name of
your module in the following commands.

1. De-initialize the submodule. If the submodule `HEAD` is not where the
   containing module expects, you can add `-f` to force this.

   ``` {.default}
   $ git submodule deinit mysubmod
   ```
   
   This is partially undoing `git submodule init`.

2. Remove the bookkeeping information from the Git internals for the
   containing repo.

   ``` {.default}
   $ rm -rf .git/modules/mysubmod
   ```

   This is the rest of undoing `git submodule init`.

3. Fix up `.gitmodules` by removing the section about the submodule. You
   can either do this by hand in an editor, or you can ask Git to do it
   like so:

   ``` {.default}
   $ git config -f .gitmodules --remove-section submodule.mysubmod
   ```

   This is undoing `git submodule add`.

4. Add the `.gitmodules` file to the stage.

   ``` {.default}
   $ git add .gitmodules
   ```

5. Delete the submodule tree from Git. This will also add the deletion
   to the stage.

   ``` {.default}
   git rm --cached mysubmod
   ```

   This is sort of like undoing `git submodule update`.

6. Do a `git status` to make sure we're set.

   ``` {.default}
   $ git status
     On branch main
     Changes to be committed:
       (use "git restore --staged <file>..." to unstage)
	         modified:   .gitmodules
	         deleted:    mysubmod
   ```

   Looks good.

7. Commit and push (if appropriate).

   ``` {.default}
   $ git commit -m "remove mysubmod submodule"
   $ git push
   ```

And that's the end of the submodule.

[i[Submodules-->Deleting]>]

[i[Submodules]>]
