# Appendix: Making a Playground {#making-playground}

[i[Playground]<]

In programming circles in general, a *playground* is a place you can go
to mess with code and tech and not worry about messing up your
production system.

And there are places you can go online to find these, but with Git, I
find it's just as easy to make your own local repo.

Here's a way to make a new local repo called `playground` out of the
current directory. (You should **not** be under a Git repo at this
time; create the playground outside other existing repos.)

``` {.default}
$ git init playground
  Initialized empty Git repository in /user/playground/.git/
```

`playground` isn't a special name. You can call it `foo` or anything.
I'll just use it for this example.

What that command did was create a new subdirectory called `playground`
and create a Git repo in it.

Let's continue at the end: how do you delete the repo? You just remove
the directory.

```
$ rm -rf playground   # delete the playground repo
```

And let's create it again:

``` {.default}
$ git init playground
```

We have all the power!

> **Note:** This repo only exists on this computer; it has no remotes
> and no way to push. You could add that stuff later, if you wanted, but
> playgrounds tend to be temporary areas where you're just trying things
> out.

Let's go into the playground and check it out.

``` {.default}
$ cd playground
$ ls -la
  total 4
  drwxr-xr-x  3 user group   18 Jul 13 14:43 .
  drwxr-xr-x 22 user group 4096 Jul 13 14:43 ..
  drwxr-xr-x  7 user group  119 Jul 13 14:43 .git
```

There's a directory there called `.git` that has all the metadata in it.

> **Note:** If we wanted to change this directory from a Git repo to
> just a normal directory, we could run this:
>
> ``` {.default}
> $ rm -rf .git       # Delete the .git directory
> ```
>
> <!-- ` -->
> Again, we have all the power! But let's show some restraint and not do
> that yet.

What can we do?

What *can't* we do? Let's make a file and see where we stand:

``` {.default}
$ echo "Hello, world" > hello.txt   # Create a file

$ ls -l

  total 4
  -rw-r--r-- 1 user group 13 Jul 13 14:47 hello.txt

$ git status

  On branch main

  No commits yet

  Untracked files:
    (use "git add <file>..." to include in what will be committed)
      hello.txt

  nothing added to commit but untracked files present (use "git
  add" to track)
```

Now we have an untracked file.

We can `git add` it, we can `git commit` it, we can create branches, we
can merge them and make conflicts and resolve them and `git rebase` and
`git reset` and all kinds of stuff.

We don't have a remote, so the only things we can't do involve pushing
and pulling.

But it turns out we can even make that happen! Let's see how.

## Cloning Bare Repos

[i[Bare repo]] [i[Playground-->Cloning]]

A *bare repo* is one without a working tree. You can't go in there to
see files, because they don't exist in there in a normal sense. The only
thing that's there is metadata and the commit snapshots.

[i[Clone]]

You can clone, push, and pull bare repos.

Let's make one (again, you could name it anything you want), noting the
`--bare` command line option:

``` {.default}
$ git init --bare origin_repo
  Initialized empty Git repository in /user/origin_repo/
```

If you look in there (to be clear, you have no reason to) you'll just see
metadata and directories.

Before we can use it, we'd better clone it. For ease, we'll do this from
the same directory we created it.

``` {.default}
$ git clone origin_repo playground
  Cloning into 'playground'...
  warning: You appear to have cloned an empty repository.
  done.
```

It is empty, naturally. We haven't made any commits.

Now we have two repos in this directory:

* `origin_repo`: the bare repo we cloned, and:
* `playground`: the repo we cloned from it.

Let's jump in there and see what's up:

``` {.default}
$ cd playground
$ git remote -v
  origin    /user/origin_repo (fetch)
  origin    /user/origin_repo (push)
```

We have remotes! Of course we do. We cloned this repo, and Git
automatically sets up the `origin` remote.

And remember that `origin` is just an alias for some remote that's
identified somehow. We're used to seeing remotes that start with `https`
or `ssh`, but here's an example of a remote that's just another
subdirectory on your disk.

[i[Pushing]]

Let's make a file and commit it, and see if we can push!

``` {.default}
$ echo "Hello, world" > hello.txt
$ git add hello.txt

$ git commit -m added
  [main (root-commit) 4a82a14] added
   1 file changed, 1 insertion(+)
   create mode 100644 hello.txt

$ git push
  Enumerating objects: 3, done.
  Counting objects: 100% (3/3), done.
  Writing objects: 100% (3/3), 907 bytes | 907.00 KiB/s, done.
  Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
  To /user/origin_repo
   * [new branch]      main -> main

$ git branch -va
  * main                4a82a14 added
    remotes/origin/main 4a82a14 added
```

And we've successfully pushed our file up to `origin`.

Finally, let's make another clone. First we'll `cd` back down to where
`origin_repo` is and clone again this time into `playground2`:

``` {.default}
$ git clone origin_repo playground2
  Cloning into 'playground2'...
  done.
```

Let's `cd` in there and see what we have. It's a clone of the repo, so
we'd better see the `hello.txt` we pushed in there from `playground`
earlier.

``` {.default}
$ cd playground2 

$ ls
  hello.txt

$ cat hello.txt 
  Hello, world
```

*Voila!* It's there!

Since `playground` and `playground2` are both clones of the same repo,
you can push from one and pull from the other to get the changes.

[i[Pulling]]

You can even make conflicting changes and try to `git pull` or `git pull
--rebase` and see how things go wrong and how to fix them.

And if everything goes completely off the rails, you can just delete the
directories and start again. It's a playground!

## Automating Playground Builds

[i[Playground-->Automating]<] [i[Shell scripts]]

It can be tedious to continually destroy and recreate repos that you're
trying to learn from. I suggest putting your commands in a _shell
script_, which is just a text file that contains the commands to run.

Let's say you make a new text file called `buildrepo.sh` and you put
the following text in it:

``` {.default}
rm -rf playground    # Remove old playground
git init playground  # Create a new one
cd playground
echo "Hello, world!" > hello.txt   # Create hello.txt
echo "foobar" > foobar.txt         # Create foobar.txt
git add hello.txt foobar.txt
git commit -m added
echo "foobar again" >> foobar.txt  # Append text
git add foobar.txt
git commit -m updated
```

That's just a bunch of shell commands. But here's the fun bit: if you
run `sh` (the shell) with `buildrepo.sh` as an argument, it will run
all those commands in order!

``` {.default}
$ sh buildrepo.sh
  Initialized empty Git repository in /user/playground/.git/
  [main (root-commit) 2239237] added
   2 files changed, 2 insertions(+)
   create mode 100644 foobar.txt
   create mode 100644 hello.txt
  [main 0533186] updated
   1 file changed, 1 insertion(+)
```

> **To debug a shell script** you can run it like this: `sh -x
> buildrepo.sh` and it will show you the commands it is running.

After that, we can `cd` in there and see what happened:

``` {.default}
$ cd playground
$ git log
  commit 05331869d77973dfbac38a31c40a44f99225e85d
  Author: User Name <user@example.com>
  Date:   Sat Jul 13 15:19:42 2024 -0700

      updated

  commit 2239237cc44d11e9479dcc610e5d02ad283766ce
  Author: User Name <user@example.com>
  Date:   Sat Jul 13 15:19:41 2024 -0700

      added

$ cat foobar.txt 
  foobar
  foobar again
```

By putting the initialization commands in a shell script, it's almost
like having a "saved game" at that point. You can just rerun the shell
script any time you want the same playground set up.

[i[Playground-->Automating]>]

[i[Playground]>]
