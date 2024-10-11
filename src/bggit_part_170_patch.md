# Patch Mode

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

## `git add -p`

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
