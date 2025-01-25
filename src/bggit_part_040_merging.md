# Merging and Conflicts {#merge}

[i[Merge]<]

We've seen how a fast-forward merge can bring to branches into sync with
no possibility of conflict.

But what if we can't fast-forward because two branches are not direct
ancestors? In other words, what if the branches have _diverged_? What if
a change in one branch _conflicts_ with a change in the other?

## An Example of Divergent Branches

[i[Branch-->Divergent]]

Let's look at a commit graph where things are still OK to fast-forward
in Figure_#.1.

![A direct ancestor branch.](img_040_010.pdf "[A direct ancestor branch.]")

<!--
``` {.default}
         [main]
           |
           v          [somebranch]
    (1)---(2)            |
            \            v
            (3)---(5)---(7)
```
-->

Yes, I've bent the graph a bit there, but we can merge `somebranch`
into `main` as a fast-forward because `main` is a direct ancestor and
`somebranch` is therefore a direct descendant.

But what if, **before** we merged, someone made another commit on the
`main` branch? And now it looks like it does in Figure_#.2.

<!--
``` {.default}
               [main]
                 |
                 v    [somebranch]
    (1)---(2)---(8)      |
            \            v
            (3)---(5)---(7)
```
-->

![Not a direct ancestor branch.](img_040_020.pdf "[Not a direct ancestor branch.]")

There's a common ancestor at commit `(2)`, but there's no direct line of
descent. `main` and `somebranch` have diverged.

Is all hope lost? How can we merge?

## Merging Divergent Branches

Turns out you do it the exact same way as always.

1. Check out the branch you want to merge _into_.
2. `git merge` the branch you want to merge _from_.

In our Figure_#.2 example above, let's say we've done this:

``` {.default}
$ git switch main
$ git merge somebranch    # into main
```

> The `#` is a shell comment delimiter. You can paste that in if you
> want, but it does nothing.

The difference here is that Git can't simply fast-forward. It has to
somehow, magically, bring together the changes from commit `(7)` **and**
commit `(8)` even if they're radically different than one other.

This means that after we bring those two commits together, the code will
look like it's never looked before, a combination of two sets of
changes.

And because it looks like it hasn't before, we need _another commit_
(another snapshot of the working tree) to represent the joining of both
sets of changes.

We call this the _merge commit_, and Git will automatically make it for
you. (When this happens, you'll see an editor pop up with some text in
it. This text is the commit message. Edit it (or just accept it as-is)
and save the file and exit the editor. See [Getting Out of
Editors](#editor-get-out) if you need help with this.

So after our merge, we end up with Figure_#.3.

![Creating a merge commit.](img_040_030.pdf "[Creating a merge commit.]")

<!--

``` {.default}
                         [main]
                           |
                           v    
    (1)---(2)---(8)-------(9)
            \             /
            (3)---(5)---(7)
                         ^
                         |
                      [somebranch]
```
-->

Commit labeled `(9)` is the merge commit. It contains both the changes
from `(8)` and `(7)`. And has the commit message you saved in the
editor.

And we see `main` has been updated to point to it. And that `somebranch`
is unaffected.

Importantly, we see that commit `(9)` has **two parents**, the commits
that were merged together to make it.

And look! If we want, we can now fast-forward `somebranch` to `main`
because it's now a direct ancestor!

In this example, Git was able to determine how to do the merge
automatically. But there are some cases where it cannot, and this
results in a _merge conflict_ that requires manual intervention. By you.

## Merge Conflicts

[i[Merge-->Conflicts]<]

If two branches have changes that are "far apart" from one another, Git
can figure it out. If I edit line 20 of a file in one branch, and you
edit line 3490 of the same file in another, Git can bring both edits in
automatically.

But let's say I edit line 20 in one commit, and you edit line 20 (the
same line) in another commit.

Which one is "right"? Git has no idea because it's just dumb software
and doesn't know our business needs.

So it asks us, during the merge, to fix it. After we fix it, Git can
complete the merge.

> **When you're merging, if a conflict occurs, _you're still merging_**.
> Git is in the "merge" state, waiting for more merge-specific commands.
>
> You can resolve the conflict then commit the changes to complete the
> merge. Or you can back out of the merge making as if you'd never
> started it in the first place.
>
> The important point is that you're aware Git is in a special state and
> you have to either complete or abort the merge to get back to normal
> before you continue to use it. 

Let's have an example where both `main` and `newbranch` have added a
line to end of file, i.e. they both added line 4. Git doesn't know which
one is correct, so there's a conflict.

``` {.default}
$ git merge newbranch
  Auto-merging foo.py
  CONFLICT (content): Merge conflict in foo.py
  Automatic merge failed; fix conflicts and then commit the result.
```

Now if I look at my status, I see we're in merge state, as noted by `You
have unmerged paths`. We're in the middle of merge; we have to either go
out the front or back out the back to get back to normal.

``` {.default}
$ git status
  On branch main
  You have unmerged paths.
    (fix conflicts and run "git commit")
    (use "git merge --abort" to abort the merge)

  Unmerged paths:
    (use "git add <file>..." to mark resolution)
	  both modified:   foo.py

  no changes added to commit (use "git add" and/or "git commit -a")
```

It's also hinting that I can do one of two things:

1. Fix conflicts and run `git commit`.
2. Use `git merge --abort` to abort the merge.

The second just rolls back the merge making it as if I hadn't run `git
merge` in the first place.

So let's focus on the first. What are these conflicts and how do I
resolve them?

## What a Conflict Looks Like

My error message above is telling me that `foo.py` has unmerged paths.
So look at what's happened with that file.

Before I started any of this, the file `foo.py` only had this in it on
branch `main`:

``` {.default}
print("Commit 1")
```

And I added a line so it looked like this:

``` {.default}
print("Commit 1")
print("Commit 4")
```

And committed it.

But what I didn't realize was that my teammate had also made another
commit on `newbranch` that added different lines to the bottom of the
file.

So when I went to merge `newbranch` into `main`, I got this conflict.
Git doesn't know which additional lines are correct.

**Here's where the fun begins.** Let's edit `foo.py` here in the middle
of the merge and see what it looks like:

``` {.default}
print("Commit 1")
<<<<<<< HEAD
print("Commit 4")
=======
print("Commit 2")
print("Commit 3")
>>>>>>> newbranch
```

What the giblets is all that? Git has totally screwed with the contents
of my file!

Yes, it has! But not for no reason; let's examine what's in there.

We have three delimiters: `<<<<<<`, `======`, and `>>>>>>`.

Everything from the top delimiter to the middle one is what's in `HEAD`
(the branch you're on and merging _into_).

Everything from the middle delimiter to the bottom one is what's in
`newbranch` (the branch you're merging _from_).

So Git has "helpfully" given us the information we need to make a
semi-informed decision about what to do.

And here's exactly the steps we must follow:

1. Edit the conflicting file(s), remove all those extra lines, and
   **make the file(s) Right**.
2. Do a `git add` to add the file(s).
3. Do a `git commit` to finalize the merge.

Now, when I say "make the file *Right*", what does that mean? It means
that I need to have a chat with my teammate and figure out what this
code is supposed to do. We clearly have different ideas, and only one of
them is right.

So we have a chat and hash it out. We finally decide the file should
look like this:

``` {.default}
print("Commit 1")
print("Commit 4")
print("Commit 3")
```

And then I (since I'm the one doing the merge), edit `foo.py` and remove
all the merge delimiters and everything else, and make it look exactly
like we agreed upon. I make it look *Right*.

Then I add the file to the stage:

``` {.default}
$ git add foo.py
$ git status
  On branch main
  All conflicts fixed but you are still merging.
    (use "git commit" to conclude merge)

  Changes to be committed:
	  modified:   foo.py
```

Notice that `git status` is telling me we're still in the merging state,
but I've resolved the conflicts. It tells me to `git commit` to finish
the merge.

> **What if I added the conflict file too soon?** For example, what if
> you add it but then you realize there are still unresolved conflicts
> or the file isn't _Right_? If you haven't committed yet, you have a
> couple options. (If you have committed, all you can do is
> [reset](#reset) or [revert](#revert).)
>
> One option is to just edit the file again, and re-add it when it's
> done. (After editing the file will show up as a "change not staged for
> commit" until you add it again.)
>
> Another option is to move the file off the stage with `git checkout
> --merge` on the file to get it back to the "both modified" state.
> Helpfully, this won't delete the changes you already added. This is
> especially useful if you're using a [merge tool](#mergetool).

So now that we've added the file, let's make the merge commit. Here
we're manually making the merge commit, unlike above where Git was able
to automatically make it.

``` {.default}
$ git commit -m "Merged with newbranch"
  [main 668b506] Merged with newbranch
```

And that's it! Let's check status just to be sure:

``` {.default}
$ git status
  On branch main
  nothing to commit, working tree clean
```

Success!

Just to wrap up, let's take a look at the log at this point:

``` {.default}
$ git log
  commit 668b5065aa803fa496951b70159474e164d4d3d2 (HEAD -> main)
  Merge: e4b69af 81d6f58
  Author: User Name <user@example.com>
  Date:   Sun Feb 4 13:18:09 2024 -0800

      Merged with newbranch

  commit e4b69af05724dc4ef37594e06d0fd323ca1b8578
  Author: User Name <user@example.com>
  Date:   Sun Feb 4 13:16:32 2024 -0800

      Commit 4

  commit 81d6f58b5982d39a1d92af06b812777dbb452879 (newbranch)
  Author: User Name <user@example.com>
  Date:   Sun Feb 4 13:16:32 2024 -0800

      Commit 3

  commit 3ab961073374ec26734c933503a8aa988c94185b
  Author: User Name <user@example.com>
  Date:   Sun Feb 4 13:16:32 2024 -0800

      Commit 1
```

We see a few things. One is that our merge commit is pointed to by
`main` (and `HEAD`). And looking down a couple commits, we see our
now-direct ancestor, `newbranch` back on Commit 3.

We also see a `Merge:` line on that top commit. It lists the UUIDs for
the two commits that it came from (the first 7 digits, anyway), since
the merge commit has two parents.

## Why Merge Conflicts Happen

Generally, it's because you haven't coordinated with your team about who
is responsible for which pieces of code. Generally two people shouldn't
be editing the same lines of code in the same file at once.

That said, there are absolutely cases where it does happen and is
expected. The key is to communicate with your team when resolving the
conflict if you don't know what is _Right_.

## Merging with IDEs or other Merge Tools

IDEs like VS Code might have a special merge mode where you can choose
one set of changes or another, or both. Likely "both" is what you want,
but make an informed decision on the matter.

Also, even when selecting "both", it could be that the editor puts them
in the wrong order. It's up to you to make sure the file is _Right_
before making the final commit to complete the merge.

You can do this by, after the tool has been used to resolve the
conflict, opening the file again in a new window and making sure it's as
you want it, and editing it to be if it's not.

For more information about merge tools, see the [Mergetool](#mergetool)
chapter.

## Merge Big Ideas

***DON'T PANIC!*** If you have a merge conflict, you can totally work it
out. They're a common occurrence, and the more of them you do, the
better at them you get.

Nothing to worry about. Everything is in Git's commit history, so even
if you botch it, you can always get things back the way they were.

[i[Merge-->Conflicts]>]
[i[Merge]>]
