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

TODO:
* Creating a new one
* Cloning one
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
