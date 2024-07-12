Using Subdirectories with Git
=============================

This is a shorter chapter, but we want to talk about Git’s behavior when
it comes to working in subdirectories and some gotchas that you probably
don’t want to get wrapped up in.

Repos and Subdirectories
------------------------

When you run a ``git`` command, Git looks for a special directory called
``.git`` (“dot git”) in the current directory. As we’ve already
mentioned, this is the directory, created when you create the repo, that
holds the metadata about the repo.

But what if you’re in a subdirectory in your project, and there’s no
``.git`` directory there?

Git starts by looking in the current directory for ``.git``. If it can’t
find it there, it looks in the parent directory. And if it’s not there,
it looks in the grandparent, etc., all the way back to the root
directory.

What about Subprojects?
~~~~~~~~~~~~~~~~~~~~~~~

One common student question is, “Should I make one single repo for CS101
with subdirectories for each project? Or should I make a different repo
for every project?”

Firstly, see if your instructor has a requirement or preference, but
other than that, it doesn’t technically matter which approach you use.

In real life, bigger repos (much bigger than you’ll typically be using
for a class) take a lot longer to clone due to their size.

What happens if you initialize a new Git repo *inside* an existing repo?
It’s not great. Don’t do this.

For mixing and matching different repos in the same hierarchy, Git has
the concept of
[fl[submodules|https://git-scm.com/book/en/v2/Git-Tools-Submodules]],
but that’s out of scope for this guide, and rarely used in school.

Accidentally Making a Repo in your Home Directory
-------------------------------------------------

Git won’t stop you from making a repo there, i.e. a repo that contains
everything in all your directories.

But that’s probably not what you wanted to do.

How does one make this mistake? Usually it’s with ``git init .`` in your
home directory. You can also make this error by launching VS Code from
your home directory and telling it to “Initialize Repository” in that
location.

This is particularly insidious because if you’re in a subdirectory that
you *think* is a standalone repo, you might have been misled since Git
searches parent folder for the ``.git`` directory and it could be
finding the spurious one you accidentally made in your home directory.

We recommend against one big repo from your home directory. You should
have separate subdirectories for each of your repos.

If you accidentally create a repo where you didn’t want to, changing a
Git repo to a regular subdirectory is as simple as removing the ``.git``
directory. Be careful that you’re removing the correct one when you do
this!

   One hack you can do to prevent Git from creating a repo in your home
   directory is to preemptively put an unwriteable ``.git`` directory
   there.

   .. code:: default

      $ mkdir ~/.git       # Make the .git directory
      $ chmod 000 ~/.git   # Take away all permissions

   .. raw:: html

      <!-- ` -->

   This way when Git tries to make its metadata folder there, it’ll be
   stopped because you don’t have write permission to that ``.git``
   directory.

Empty Subdirectories in Repos
-----------------------------

Turns out Git doesn’t support this. It only tracks files, so if you want
a subdirectory represented in your repo, you must have at least one file
in it.

A common thing to do is add an empty file called ``.gitkeep`` (“dot git
keep”) to the subdirectory, then add it to the repo. This will cause Git
to recreate the subdirectory when it clones or merges the ``.gitkeep``
directory.

   The file ``.gitkeep`` isn’t special in any way, other than
   convention. The file could be called anything. For example, if you
   know you’ll need to eventually put a ``.gitignore`` in that
   directory, you might just use that instead. Or a ``README``.
