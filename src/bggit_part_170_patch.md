# Patch Mode: Applying Partial Changes

A lot of Git commands obey the `-p` switch that puts them in ***patch
mode***. This is a powerful mode that allows you to select *some* of the
changes for a particular command, but not *all* of the changes.

Commands that use `-p` include `add`, `reset`, `stash`, `restore`,
`commit`, and more.

Basically any time you have changes to a file and you're thinking, "I
want to do something with just *some* of these changes", patch mode will
help you out.

Some terminology: Git calls a collection of close changes a *hunk*. An
example might be if you modified function `foo()` by adding a few lines
and modified function `bar()` by adding a few lines, you would likely
have two hunks, one for each group of changes.

Patch mode allows you to select which hunks will be operated on.

## Adding Files in Patch Mode

Let's say you had a commit that added `Line 1` to `Line 8` in a file:

``` {.default}
Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
```

And we make a couple changes, adding a line to the top and bottom:

``` {.default}
Line BEGIN
Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
Line END
```

And I'm about to add and commit, but I realize that I only want to add
`Line BEGIN` at this time, and not `Line END`.

If I did a regular `git add`, it would add both changes to the stage.
But if I do `git add -p`, we can select one or the other. Let's try it.

First let's have a look at our diff.

``` {.default}
$ git diff
  diff --git a/foo.txt b/foo.txt
  index a982fdc..125f6ac 100644
  --- a/foo.txt
  +++ b/foo.txt
  @@ -1,3 +1,4 @@
  +Line BEGIN
   Line 1
   Line 2
   Line 3
  @@ -6,3 +7,4 @@ Line 5
   Line 6
   Line 7
   Line 8
  +Line END
```

Poring over that, you see we've added `Line BEGIN` to the top and `Line
END` to the bottom. (Recall that lines with `+` in front of them are
additions in diff.)

Now let's do a patch add.

``` {.default}
$ git add -p
  diff --git a/foo.txt b/foo.txt
  index a982fdc..125f6ac 100644
  --- a/foo.txt
  +++ b/foo.txt
  @@ -1,3 +1,4 @@
  +Line BEGIN
   Line 1
   Line 2
   Line 3
  (1/2) Stage this hunk [y,n,q,a,d,j,J,g,/,e,p,?]? 
```

Well, that's a lot of options! The easy ones are `y` for "yes" and `n`
for "no". And also you can type `?` to get more detailed help.

Also we see that this is hunk 1 of 2, which makes sense because we have
one change at the top of the file and another at the bottom.

In our case, we do want to keep this first hunk, so we'll answer `y`.

And then we get to hunk 2 of 2:

``` {.default}
(1/2) Stage this hunk [y,n,q,a,d,j,J,g,/,e,p,?]? y
@@ -6,3 +7,4 @@ Line 5
 Line 6
 Line 7
 Line 8
+Line END
(2/2) Stage this hunk [y,n,q,a,d,K,g,/,e,p,?]?
```

And for this one, I'm going to say `n` to not stage it. Then we're back
out to the shell prompt.

Now I'm going to type `git status` to see where we are, but first I want
you to think about what it's going to tell us.

We have one of the changes staged, and the other change not staged. What
state are files in when they have unstaged changes? And when there are
staged changes? We have both right now, right?

``` {.default}
$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  modified:   foo.txt

  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
	  modified:   foo.txt
```

Sure enough! Because we only did a partial add of the changes in the
file, the added changes are on the stage, and the not-added changes are
still out in the working directory. It *has* to be this way because we
haven't staged *all* our changes!

At this point we can go ahead and commit the partially-added changes
that are on the stage.

## Resetting Files in Patch Mode

Kind of the opposite of `git add -p` is `git reset -p`. You can use
`reset -p` to selectively change hunks *on the stage*.

It's that last part that makes it a bit weird, but you can think of `add
-p` as selectively adding hunks to the stage from the working tree, and
`reset -p` as selectively removing hunks from the stage relative to a
particular commit.

That is, I can reset to an earlier commit, but choose what hunks to
reset.

> **This is not a hard, soft, or mixed reset.** It's its own thing. If
> you try to specify a certain type of reset in addition to `-p`, Git
> will complain. Arguably this should be a different command entirely,
> but that's Git for ya!

Let's say I have two commits. In the first one, I added `Line 1` through
`Line 8`, and in the second commit I added `Line BEGIN` and `Line END`,
just like in the earlier example.

But now I decide I want to reset the `Line END`, but it's part of
another commit. I can break it out with `git reset -p`. Let's do it.

Here's my log:

``` {.default}
commit d2d5899a253d5ce277d4d5981d03a43e68da6677 (HEAD -> main)
Author: User Name <user@example.com>
Date:   Fri Oct 11 16:12:26 2024 -0700

    updated

commit aae754f46130b6d86680e74caa98642becc88d6e
Author: User Name <user@example.com>
Date:   Fri Oct 11 16:12:04 2024 -0700

    added
```

I want to do a partial reset to the earlier commit `aae75`. And I'm
going to say "no" I don't want to reset the first hunk, and "yes" I want
to reset the second. Here's what it looks like:

``` {.default}
$ git reset -p aae75
  diff --git b/foo.txt a/foo.txt
  index 125f6ac..a982fdc 100644
  --- b/foo.txt
  +++ a/foo.txt
  @@ -1,4 +1,3 @@
  -Line BEGIN
   Line 1
   Line 2
   Line 3
  (1/2) Apply this hunk to index [y,n,q,a,d,j,J,g,/,e,p,?]? n
  @@ -7,4 +6,3 @@ Line 5
   Line 6
   Line 7
   Line 8
  -Line END
  (2/2) Apply this hunk to index [y,n,q,a,d,K,g,/,e,p,?]? y
```

The first question is asking, "Do you want to remove 'Line BEGIN'?" And
I said "no". And the second question is asking "Do you want to remove
'Line END'?" And I said "yes".

Where are we?

``` {.default}
$ git status
  On branch main
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
	  modified:   foo.txt

  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
	  modified:   foo.txt
```

Hmm. Let's check the difference between the stage and `HEAD`.

``` {.default}
$ git diff --staged
  diff --git a/foo.txt b/foo.txt
  index 125f6ac..e0e1d89 100644
  --- a/foo.txt
  +++ b/foo.txt
  @@ -7,4 +7,3 @@ Line 5
   Line 6
   Line 7
   Line 8
  -Line END
```

That's telling us that, compared to `HEAD`, the stage has the `Line END`
removed. Which is great, because that's what we asked for with `reset
-p`. So we're on track.

But why is `foo.txt` modified? Let's see:

``` {.default}
$ git diff
  diff --git a/foo.txt b/foo.txt
  index e0e1d89..125f6ac 100644
  --- a/foo.txt
  +++ b/foo.txt
  @@ -7,3 +7,4 @@ Line 5
   Line 6
   Line 7
   Line 8
  +Line END
```

This is telling us that, compared to the stage, the working tree has
`Line END` added to the end.

And sure enough, if we look at the `foo.txt` file in the working tree,
*it still has `Line END` in it*.

``` {.default}
$ cat foo.txt
  Line BEGIN
  Line 1
  Line 2
  Line 3
  Line 4
  Line 5
  Line 6
  Line 7
  Line 8
  Line END
```

What does it all mean? Well, it means `reset -p` messed with the stage,
but not with the working tree. Our working tree is still the same as it
was with the last commit. (`git diff HEAD` will show no changes.)

Now, admittedly, it's likely this isn't what you want. Maybe you wanted
to reset the hunk **and** get your working tree reset to that hunk, as
well.

But we can still get there! Remember that the reset hunk is on the stage
ready to be committed! Let's do that!

``` {.default}
$ git commit -m "remove END"
  [main 46badfe] remove END
   1 file changed, 1 deletion(-)
```

There. Now the stage and `HEAD` are the same, both having had `Line END`
removed. But `Line END` still exists in our working tree, like `status`
informs us:

``` {.default}
$ git status
  On branch main
  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
	  modified:   foo.txt
```

So how do we get the reset change back into our working tree? The answer
is right there in the hints.

``` {.default}
$ git restore foo.txt
```

There. Now we're all on the same page with the `Line END` removed
entirely.

> **There's another way to synchronize the stage and working tree during
> a patch reset.** After you do the `reset -p`, you can copy the file
> `foo.txt` from the stage to the working tree with:
>
> ``` {.default}
> git checkout -- foo.txt
> ```
>
> <!-- ` -->
> That will make the stage and working tree the same, so everything will
> all be on the same page when the commit is complete.

## Other Patch Mode Commands

You can use `-p` with `stash`, `restore`, `commit`, and more. The UI
behaves basically the same way as described above. See the manual pages
for any particular command to learn more about it.

