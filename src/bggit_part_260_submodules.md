# Submodules

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
include FooLib as a submodule and make sure it's locked to that version.
Then even though another team might be updating FooLib, you'll always
have version 3.4.90 available to build against.

Then later when you're ready, you can update the submodule to the latest
version, say 4.0.1, and lock that one in place.

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
statement?))

And for now, that might be enough for you to get to work! All you really
needed to build the existing project was the repo and its submodules,
and you might not be in charge of the submodules and just need them to
exist for the build. So now you can get to work.

But in case you need to do more, read on!

## Creating a Submodule

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

TODO:
* Setting the commit for the submodule
* Updating to the latest
* Recursive updates
* Easy thing to do is just update the submodule from its own location
  and updated
* Updating the submodule from the submodule directory
* Deleting a submodule from a repo
* +/-
* Different submodule branches

```
git submodule add
git submodule init
git submodule update
git submodule update --init
git submodule update --recursive --init
git submodule update --remote
git pull --recurse-submodules
git clone --recurse-submodules
git submodule status
git submodule add -b <branch> <repository> <path>
git submodule foreach git status
```
