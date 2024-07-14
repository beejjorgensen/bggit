# Ignoring Files with `.gitignore`

[i[`.gitignore` file]<]

What if you have files in your subdirectory you don't want Git to pay
any attention to? Like maybe you have some temporary files you don't
want to see in the repo. Or maybe you have an executable you built from
a C project and you don't want that checked in because your incredibly
strict instructor won't grade your project if the repo contains any
build products? For example.

That's what this part of the guide is all about.

## Adding a `.gitignore` File

In any directory of a project, you can add a `.gitignore` ("dot
gitignore") file.

This is a simple textfile that contains a list of file names to ignore.

Let's say I have a C project that builds and executable called "doom". I
wouldn't want to check that into my source repo because it's not source,
and it's just a big binary that takes a bunch of disk.

But when I get the status, it's annoying to see Git complaining about
it:

``` {.default}
$ git status
  On branch main
  Untracked files:
    (use "git add <file>..." to include in what will be committed)
	  doom

  nothing added to commit but untracked files present (use "git add"
  to track)
```

So I edit a `.gitignore` file in that directory and add this one line to
it:

``` {.default}
doom
```

Now I run status again:

``` {.default}
$ git status
  On branch main
  Untracked files:
    (use "git add <file>..." to include in what will be committed)
	  .gitignore

  nothing added to commit but untracked files present (use "git add"
  to track)
```

What? Same thing? Not quite! Read the fine print!

It used to be complaining that `doom` was untracked, but now it's not
complaining. So the `.gitignore` worked. Woo hoo!

But Git has found another untracked file in the brand new `.gitignore`.
So we should add that to the repo.

Always put your `.gitignore` files in the repo unless you have a
compelling reason not to. This way they'll exist in all your clones,
which is handy.

``` {.default}
$ git add .gitignore
$ git commit -m Added
  [main 07582ad] Added
   1 file changed, 1 insertion(+)
   create mode 100644 .gitignore
```

Now we get the status:

``` {.default}
$ git status
  On branch main
  nothing to commit, working tree clean
```

and we're all clear.

## Can I Specify Subdirectories in `.gitignore`?

[i[`.gitignore` file-->And subdirectories]]

Yes!

You can be as specific or as non-specific as you like with file matches.

Here's a `.gitignore` looking for a very specific file:

``` {.default}
subdir/subdir2/foo.txt
```

That will match anywhere in the project. If you want to only match a
specific file from the project root, you can prepend a slash:

``` {.default}
/subdir/subdir2/foo.txt
```

Note that means `subdir` in the root of the _project_, not the root
directory of your entire filesystem.

## Where do I Put the `.gitignore`?

[i[`.gitignore` file-->Location]]

You can add `.gitignore` files to any subdirectories of your project.
But how they behave depends on where they are.

The rule is this: *each `.gitignore` file applies to all the
subdirectories below it*.

So if you put a `.gitignore` in your project's root directory that has
`foo.txt` in it, every single `foo.txt` in every subdirectory of your
project will be ignored.

Use the highest-level `.gitignore` file to block things you know you
don't want **anywhere** in your project.

If you add additional `.gitignore` files to subdirectories, those only
apply to that subdirectory and below.

The idea is that you start with the most broadly applicable set of
ignored files in your project root, and then get more specific in the
subdirectories.

For simple projects, you're fine just having one `.gitignore` in the
project root directory.

## Wildcards

[i[`.gitignore` file-->Wildcards]]

Do I have to individually list all the files I don't want in the
`.gitignore`? What a pain!

Luckily Git supports _wildcards_ in ignored file naming.

For example, if we wanted to block all the files that ended with a
`.tmp` or `.swp` (Vim's temp file name) extension, we could use the `*`
("splat") wildcard for that. Let's make a `.gitignore` that blocks
those:

``` {.default}
*.tmp
*.swp
```

And now any files ending with `.tmp` or `.swp` will be ignored.

Turns out that Vim has two kinds of swap files, `.swp` and `.swo`. So
could we add them like this?

``` {.default}
*.tmp
*.swo
*.swp
```

Sure! That works, but there's a shorter way where you can tell Git to
match any character in a bracketed set. This is equivalent to the
above:

``` {.default}
*.tmp
*.sw[op]
```

You can read that last line as, "Match file names that begins with any
sequence of characters, followed by `.sw`, followed by either `o` or
`p`."

## Negated `.gitignore` Rules

[i[`.gitignore` file-->Negated rules]]

What if your root `.gitignore` is ignoring `*.tmp` files for the entire
project. No problem.

But then later in development you have some deeply nested subdirectory
that has a file `needed.tmp` that you really need to get into Git.

Bad news, though, since `*.tmp` is ignored at the root level across all
subdirectories in the project! Can we fix it?

Yes! You can add a new `.gitignore` to the subdirectory with
`needed.tmp` in it, with these contents:

``` {.default}
!needed.tmp
```

This tells Git, "Hey, if you were ignoring `needed.tmp` because of some
higher-up ignore rule, please stop ignoring it."

So while `needed.tmp` was being ignored because of the root level ignore
file, this more-specific file overrides that.

If you needed to allow all `.tmp` files in this subdirectory, you could
use wildcards:

``` {.default}
!*.tmp
```

And that would make it so all `.tmp` files in this subdirectory were not
ignored

## How To Ignore All Files Except a Few?

You can use the negated rules for that.

Here's a `.gitignore` that ignores everything except files called `*.c`
or `Makefile`:

``` {.default}
*
!*.c
!Makefile
```

The first line ignores everything. The next two lines negate that rule
for those specific files.


## Getting Premade `.gitignore` Files

[i[`.gitignore` file-->Boilerplate]]

[fl[Here's a repo|https://github.com/github/gitignore]] with a whole
bunch.

But you can also roll your own as needed. Use `git status` often to see
if any files are there you want to ignore.

When you create a new repo on GitHub, it also gives you the option to
choose a prepopulated `.gitignore`. **Warning!** Only do this if you're
not planning to push an already-existing repo into this newly-made
GitHub repo. If you plan to do this, GitHub's `.gitignore` will get in
the way.

[i[`.gitignore` file]>]
