# Comparing Files with Diff

The powerful `git diff` command can give you differences between two
files or commits. We mentioned it briefly at the beginning, but here
we're going to delve more deeply into all the things you can do with it.

It's not the easiest thing to read at first, but you do get used to it
after a while. My most common use case is to quickly scan to remember
what I've changed in the working tree so I know what to add to the stage
and what commit message to use.

## Basic Usage

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

After that we have a couple lines indicating the that old version of the
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

## Diffing the Stage

What if you've added some stuff to the stage and you want to diff it
against the previous commit?

Just typing `git diff` shows nothing!

Why?

The answer is really easy: `git diff --staged`. Done.

But I want to use this subsection to dig a little deeper into what's
happening so you can improve your understanding of how this works.

A good mental model here is to imagine that the stage **must** have one
of two things on it at all time, either of these:

1. A copy of a file from the last commit. If this is the case, `git
   status` will not show the file on the stage.
2. A copy of a file from the working tree, something modified from the
   last commit. In this case `git status` **will** show something on the
   stage.

So in this mental model, *something* is always on the stage. It's just
that you don't see it unless it's something different than the last
commit that you put there with `git add`.

OK? I know I'm asking you to just bear with me on faith, so thank you
for that.

Back to the question: if you have added some modified files to the
stage, why does `git diff` show nothing is changed?

*It's because `git diff` **always** compares the working tree to the
stage.* And in this case, after you've added your modified file to the
stage, it's the same as the working tree. So no diffs.

Contrast this to where you've modified the working tree but *haven't*
added the file to the stage. In this case, the file on the stage is just
like the last commit, which is different than your working tree. So `git
diff` shows the differences.

Got it?

Well, okay, then... what if you *want* to diff what's on the stage with
the last commit?  That is, instead of diffing the working tree with the
stage, you want to diff the stage with the `HEAD`?

Back to the punchline:

``` {.default}
$ git diff --staged
```

And that'll do it.

## Difftool

TODO

