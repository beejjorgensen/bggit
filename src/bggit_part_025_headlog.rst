The Git Log and ``HEAD``
========================

When we make commits to a Git repo, it tracks each of those commits in a
log that you can visit. Let’s take a look at that now.

An Example Log
--------------

You can get the commit log by typing ``git log``.

Let’s say I’m in a repo with a single commit, where I’ve just added a
file with the commit message “Added”.

.. code:: default

   $ git log

produces:

.. code:: default

   commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2 (HEAD -> main)
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 09:24:52 2024 -0800

       Added

If I make another commit, we get a longer log:

.. code:: default

   commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 12:36:13 2024 -0800

       More output

   commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 09:24:52 2024 -0800

       Added

Notice that the most recent commit entry is at the top of the output.

What’s in the log?
------------------

There are a few things to notice in the log:

-  The commit comment
-  The date
-  The user who made the commit

Also we have those huge
[fl[hex|https://en.wikipedia.org/wiki/Hexadecimal]] numbers after the
word ``commit``.

This is the *commit ID* or *commit hash*. This is universally unique
number that you can use to identify a particular commit.

Normally you don’t need to know this, but it can be useful for going
back in time or keeping track of commits in multideveloper projects.

We also see a bit at the top that says ``(HEAD -> main)``. What’s that
about?

The ``HEAD`` Reference
----------------------

We’ve seen that each commit has a unique and unwieldy identifier like
this:

``5a02fede3007edf55d18e2f9ee3e57979535e8f2``

Luckily, there are a few ways to refer to commits with more human
symbolic names.

``HEAD`` is one of these references. It indicates which branch or commit
you’re looking at right now in your project subdirectory. Remember how
we said you could go look at previous commits? The way you do that is by
moving ``HEAD`` to them.

   We haven’t talked about branches yet, but the ``HEAD`` normally
   refers to a branch. By default, it’s the ``main`` branch. But since
   we’re getting ahead of ourselves, I’m going to just keep saying that
   ``HEAD`` refers to a commit, even though it usually does it
   indirectly via a branch.

   So this is a bit of a lie, but I hope you forgive me.

Some terminology: the files in your git subdirectory you’re looking at
right now is referred to as your *working tree*. The working tree is the
files as they appear at the commit pointed to by ``HEAD``, plus any
uncommitted changes you might have made.

So if you switch ``HEAD`` to another commit, the files in your working
tree will be updated to reflect that.

Okay, then, how do we know which commit ``HEAD`` is referring to? Well,
it’s right the at the top of the log:

.. code:: default

   commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 12:36:13 2024 -0800

       More output

We see ``HEAD`` right there on the first line, indicating that ``HEAD``
is referring to commit with ID:

``5e8cb52cb813a371a11f75050ac2d7b9e15e4751``

Again that’s a bit of a lie, though. The ``HEAD -> main`` means that
``HEAD`` is actually referring to the ``main`` branch, and that ``main``
is referring to the commit. ``HEAD`` is therefore indirectly referring
to the commit. More on that later.

Going Back In Time and Detached ``HEAD``
----------------------------------------

Here’s my full Git log:

.. code:: default

   commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 12:36:13 2024 -0800

       More output

   commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 09:24:52 2024 -0800

       Added

If I look at the files, I’ll see the changes indicated by the “More
output” commit. But let’s say I want to go back in time to the previous
commit and see what the files looked like then. How would I do that?

   Maybe there were some changes that existed back in an earlier commit
   that had been since removed, and you wanted to look at them, for
   example.

I can use the ``git checkout`` command to make that happen.

Let’s checkout the first commit, the one with ID
``5a02fede3007edf55d18e2f9ee3e57979535e8f2``.

Now, I could say:

.. code:: default

   $ git checkout 5a02fede3007edf55d18e2f9ee3e57979535e8f2

and that would work, but the rule is that you must specific at least 4
unique digits of the ID, so I could have also done this:

.. code:: default

   $ git checkout 5a02

for the same result.

And that result is:

.. code:: default

   Note: switching to '5a02'.

   You are in 'detached HEAD' state. You can look around, make experimental
   changes and commit them, and you can discard any commits you make in this
   state without impacting any branches by switching back to a branch.

   If you want to create a new branch to retain commits you create, you may
   do so (now or later) by using -c with the switch command. Example:

     git switch -c <new-branch-name>

   Or undo this operation with:

     git switch -

   Turn off this advice by setting config variable advice.detachedHead to false

   HEAD is now at 5a02fed Added

Looks sort of scary, but look—Git is telling us how to undo the
operation if we want, and so there’s really nothing to fear.

Let’s take a look around with ``git log``:

.. code:: default

   commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2 (HEAD)
   Author: Brian "Beej Jorgensen" Hall <beej@beej.us>
   Date:   Thu Feb 1 09:24:52 2024 -0800

       Added

That’s all! Just one commit?! Where’s the second commit I made? Is it
gone forever?!

No. Everything is fine.

When you have ``HEAD`` at a certain commit, you’re looking at the world
as it looked at that snapshot in time. Future commits haven’t “happened”
yet from this perspective. They are still out there, but you’ll have to
change back to them by name.

Also, do you see anything different about that first line that reads
``(HEAD)``? That’s right: no ``main`` to be seen.

That’s because the ``main`` branch is still looking at the latest
commit, the one with the “More output” comment. So we don’t see it from
this perspective.

   Remember earlier when I said it was a bit of a lie to say that
   ``HEAD`` points to a commit? Well, detached head state is the case
   where it actually **does**. Detached head state is just what happens
   when ``HEAD`` is pointing to a commit instead of a branch. To
   reattach it, you have to change it to point to a branch again.

Let’s get back to the ``main`` branch. There are three options:

1. ``git switch -``, just like the helpful message says.
2. ``git switch main``
3. ``git checkout main``

Git replies:

.. code:: default

   Previous HEAD position was 5a02fed Added
   Switched to branch 'main'

And now if we ``git log``, we see all our changes again:

.. code:: default

   commit 5e8cb52cb813a371a11f75050ac2d7b9e15e4751 (HEAD -> main)
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 12:36:13 2024 -0800

       More output

   commit 5a02fede3007edf55d18e2f9ee3e57979535e8f2
   Author: User Name <user@example.com>
   Date:   Thu Feb 1 09:24:52 2024 -0800

       Added

and our working tree will be updated to show the files as they are in
the ``main`` commit.

The New Command: ``git switch``
-------------------------------

In ye olden days, ``git checkout`` did a lot of things, and it still
does. Because it does so much, the maintainers of Git have been trying
to break some of that functionality into a new command, ``git switch``.

We could redo the previous section by using just ``git switch`` instead
of ``git checkout``. Let’s try:

.. code:: default

   $ git switch 5a02

and it says:

.. code:: default

   fatal: a branch is expected, got commit '5a02'
   hint: If you want to detach HEAD at the commit, try again with the
         --detach option.

Hmmm! ``git switch`` is warning us that we’re about to go into detached
head state, and is that what we really want? It’s not a crime or
anything to do so, but it’s just letting us know that we’re not going to
be on a branch any longer.

So we can override, just like it suggests:

.. code:: default

   $ git switch --detach 5a02
   HEAD is now at 5a02fed Added

All right! No big message about being detached, but we don’t need it
because we know it’s detached since we specified.

And like before, we can get back to the ``main`` branch with either:

1. ``git switch -``, switch to the previous state
2. ``git switch main``

Easy.
