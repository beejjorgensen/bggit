# Comparing Files with Diff {#diff}

[i[Diff]<]

The powerful `git diff` command can give you differences between two
files or commits. We mentioned it briefly at the beginning, but here
we're going to delve more deeply into all the things you can do with it.

It's not the easiest thing to read at first, but you do get used to it
after a while. My most common use case is to quickly scan to remember
what I've changed in the working tree so I know what to add to the stage
and what commit message to use.

## Basic Usage

[i[Diff-->Understanding the output]<]

The most basic use case is that you've modified some files in your
working tree and you want to see what the differences are between what
was there and what you added.

For example, let's say I've modified my `hello.py` file (but haven't
staged it yet). I can check out what I've changed like so:

``` {.default}
$ git diff
  diff --git a/hello.py b/hello.py
  index 4a8f53f..8ee1fe4 100644
  --- a/hello.py
  +++ b/hello.py
  @@ -1,4 +1,8 @@
   def hello():
  -    print("Hello, world!")
  +    print("HELLO, WORLD!")
  +
  +def goodbye():
  +    print("See ya!")

   hello()
  +goodbye()
```

What do we have there? Why, it's an impenetrable mess, of course!

_The End_

All right, take a deep breath and let's figure it out.

Since the output is plastered over with `hello.py`, we can safely
assume this is the file we're talking about. If the diff is reporting on
multiple files (e.g. you're comparing two commits), each file will have
its own section in the output.

> **The `index` line has the blob hashes and file permissions.** A blob
> hash is the hash of the specific file in the states being compared.
> This isn't something you need to worry about, typically. Or maybe not
> even ever.

After that we have a couple lines indicating that the old version of the
file `a/hello.py` is the one marked with minus signs, and the new
version (that you haven't staged yet) is `b/hello.py` and is marked with
plus signs.

Then we have `@@ -1,4 +1,8 @@`. This means that lines 1-4 in the old
version are shown, and lines 1-8 in the new version are shown. (So
clearly we've at least added some lines here.)

Finally, we get to the steak and potatoes of the whole thing—what has
actually changed? Remembering that the old version is minus and the new
version is plus, let's look at just that part of the diff again:

``` {.default}
   def hello():
  -    print("Hello, world!")
  +    print("HELLO, WORLD!")
  +
  +def goodbye():
  +    print("See ya!")

   hello()
  +goodbye()
```

Rules:

* If a line is prefixed with `-`, it means this is how the line was in
  the old version.

* If a line is prefixed with `+`, it means this is how the line is in
  the new, modified version.

* If a line is not prefixed with anything, it means it is unchanged
  between the versions.

> **The diff won't show you all the lines of the file!** It only shows
> you what's changed and some of the surrounding lines. If there are
> changes in different parts of the file, the unchanged parts of the
> file will be skipped over in the diff.

Another way to read the diff is that lines with a `-` have been removed
and lines with a `+` have been added.

[i[Diff-->Understanding the output]>]

## Diffing the Stage

[i[Diff-->The stage]<]

What if you've added some stuff to the stage and you want to diff it
against the previous commit?

Just typing `git diff` shows nothing!

Why? It's because diff, by default, is showing *the difference between
your working tree and the stage*. You just staged that file, copying it
from the working tree to the stage, so the two are identical. So a diff
shows no differences.

How do we diff the stage with the previous commit?

The answer is really easy: `git diff --staged`[^91c6]. Done.

[^91c6]: The `--staged` flag is more modern. Older versions of Git used
    `git diff --cached`.

But I want to use this subsection to dig a little deeper into what's
happening so you can improve your understanding of how this works.

Mental model time!

Let's say that these two things are true. Now, whether or not they're
true doesn't really matter.

> _"It's only a model."_\
> \ \ \ \ \ \ \ \ \ \ \ \ —Patsy, _Monty Python and the Holy Grail_

1. The stage contains a _copy_ of **all** unmodified files at your
   current commit.

2. A `git status` or `git diff` only shows files that differ between
   your working tree and the stage.

So if you don't have any modifications, `git diff` won't show any
differences. Because the stage and working tree are the same.

Now if you modify a file in your working tree and then `git diff`, you
*will* see some changes, because the working tree differs from the
stage.

But then if you add the modified file to the stage, then the stage and
working tree become the same again. And `git diff` will show no
differences.

*`git diff` **always** compares the working tree to the stage.* (Unless
you're diffing specific commits—see below.) And in this case, after
you've added your modified file to the stage, it's the same as the
working tree. So no diffs.

Contrast this to where you've modified the working tree but *haven't*
added the file to the stage. In this case, the file on the stage is just
like the last commit, which is different than your working tree. So `git
diff` shows the differences.

Well, okay, then... what if you *want* to diff what's on the stage with
the last commit?  That is, instead of diffing the working tree with the
stage, you want to diff the stage with the `HEAD`?

Back to the punchline:

``` {.default}
$ git diff --staged
```

And that'll do it. This will run a diff between what's on the stage and
the last commit, showing you the changes you've staged.

[i[Diff-->The stage]>]

## More Diff Fun

Let's speed through some examples of things you can do with diff.

### Diff Any Commits or Branches

[i[Diff-->Other commits]]
[i[Diff-->Other branches]]
You have more at your disposal than just diffing the working tree or
stage. You can actually diff any two commits. This will show you all the
differences between them.

For example, if you know the commit hashes, you can diff them directly:

``` {.default}
$ git diff d977 27a3
```

Or if you have two branch names:

``` {.default}
$ git diff main topic
```

Or mix and match:

``` {.default}
$ git diff main 27a3
```

Or use `HEAD`:

``` {.default}
$ git diff HEAD 27a3
```

Or relative `HEAD`... This one diffs the previous-to-`HEAD` commit with
the `HEAD`:

``` {.default}
$ git diff HEAD^ HEAD
```

And this one diffs four commits before `HEAD` with three commits before
`HEAD`:

``` {.default}
$ git diff HEAD~4 HEAD~3
```

### Diffing Order

These are both valid ways to diff, but they give different (inverted)
results:

``` {.default}
$ git diff main topic
$ git diff topic main
```

One way to think about this is that it's like:

``` {.default}
$ git diff FROM TO
```

That is, "Hey, Git, tell me the changes I need to make to get from
commit `FROM` to commit `TO`."

Let's say I made a file `foo.md` and committed it with a single line
`First` in it. And then I overwrote it with `Second` and committed it
again.

In this example, I can ask, "What do I have to change from the
previous-to-`HEAD` commit to the `HEAD` commit?"

``` {.default}
$ git diff HEAD^ HEAD
  diff --git a/foo.md b/foo.md
  index d00491f..495a7e9 100644
  --- a/foo.md
  +++ b/foo.md
  @@ -1 +1 @@
  -First
  +Second
```

It's telling me to get from previous-to-`HEAD` to `HEAD`, I would need
to delete `First` and add `Second`.

But if I reverse it and ask, "What do I have to change from `HEAD` to
get back to the previous-to-`HEAD` commit?" I'll get the opposite:

``` {.default}
$ git diff HEAD HEAD^
  diff --git a/foo.md b/foo.md
  index 495a7e9..d00491f 100644
  --- a/foo.md
  +++ b/foo.md
  @@ -1 +1 @@
  -Second
  +First
```

There it's telling me to get back to the previous-to-`HEAD` I'd need to
delete `Second` and add `First`.

So remember, `git diff FROM TO` is telling you the changes you have to
make to get from the `FROM` commit to the `TO` commit.

### Diffing with Parent Commit

[i[Diff-->Parent commit]]
We just showed this example:

``` {.default}
$ git diff HEAD~4 HEAD~3
```

But since `HEAD~4` is the parent of `HEAD~3`, is there some shorthand we
can use here? Yes!

``` {.default}
$ git diff HEAD~4 HEAD~3
$ git diff HEAD~3^!          # Same thing!
```

You can use it anywhere you want to compare a commit with its parent,
which is really showing just what changes were in that one particular
commit.

``` {.default}
$ git diff HEAD^!
$ git diff HEAD~3^!
$ git diff main^!
$ git diff 27a3^!
```

### More Context

[i[Diff-->Additional context]]
By default, `git diff` shows 3 lines of context around the changes. If
you want to see more, like 5 lines, use the `-U` switch.

``` {.default}
$ git diff -U5
```

### Just the File Names

[i[Diff-->File names only]]
If you just want a list of files that have changed, you can use the
`--name-only` option.

``` {.default}
$ git diff --name-only
```

### Ignoring Whitespace

[i[Diff-->Ignore whitespace]]
There might be a time when you get some tabs/spaces confusion in your
source code, which is always painful. Protip: stick to one and force
everyone else on the team to do the same under penalty of paying for
lunch.

But you can commit `git diff` to ignore whitespace in the comparison:

``` {.default}
$ git diff -w
$ git diff --ignore-all-space    # Same thing
```
### Just Certain Files

[i[Diff-->Specific files]]
You can just diff certain files.

One way is to just put the file names after a `--`:

``` {.default}
$ git diff -- hello.py
$ git diff -- hello.py another_file.py
```

You can also specify commits or branches before the `--`:

``` {.default}
$ git diff somebranch -- hello.py
```

That'll compare `hello.py` at `HEAD` with the version on `somebranch`.

Or you could give two commits or branches to compare the file there:

``` {.default}
$ git diff main somebranch -- hello.py
```

Finally, you can restrict to a file extension using a glob and single
quotes:

``` {.default}
$ git diff '*.py'
```

That will just diff the Python files.

### Inter-branch Diffs

[i[Diff-->Between branches]]
This is an interesting version of comparing two branches.

We already showed the following example for comparing the commits at two
branches:

``` {.default}
$ git diff branch1 branch2
```

But sometimes you want to know what changed in a branch *since the
branches diverged*.

That is, you don't want to know what's different *now* between `branch1`
and `branch2`, which is what the above would give you.

You want to know what `branch2` added or deleted that `branch1` did not.

In order to see this, you can use this notation:

``` {.default}
$ git diff branch1...branch2
```

This means "diff the common ancestor of `branch1` and `branch2` with
`branch2`."

In other words, tell me all the changes that were made in `branch2` that
`branch1` is unaware of. Don't show me anything that `branch1` has
changed since they diverged.

## Difftool

I know the diff output is tough to read. I recommend practice and offer
myself as living proof that with enough practice, the output becomes
penetrable. And eventually it even becomes easy to read, which might be
difficult to imagine. But it does!

That said, there are third-party tools that exist to make diffs more
manageable, and Git supports these tools. You can read more about it in
the [diff tool](#difftool) chapter.

[i[Diff]>]
