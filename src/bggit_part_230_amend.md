# Amending Commits {#amend}

Git gives you the power to relatively easily amend the last commit.

> **Caution!** This section talks about changing history, and let's not
> forget The One Rule Of Changing History: thou shalt not change history
> of anything that you've pushed, lest someone else might have already
> pulled thy earlier changes, causing your commit histories to become
> woefully out of sync and much shouting.
>
> In short, if you pushed a change, assume someone else has pulled it
> already and amending your commit (changing history) would cause lots
> of pain.
> 
> In shorter, if you pushed, it's too late. No more amending the commit.

So what are some use cases?

* Maybe you botched the commit message and you want to rewrite it.
* Maybe you forgot to add some files.

That kind of thing that none of us have ever done ever, right?

## Amending the Commit Message

This one is pretty easy. Let's take an example of a commit that I've
botched. Note that this is completely committed at this point—I've
already run `git commit`. But, crucially, I haven't pushed yet.

Let's get a status and see the log:

``` {.default}
$ git status
  On branch main
  nothing to commit, working tree clean
$ git log
  commit d7fba6838a689c3de15a27e272e8e4123d7c2460 (HEAD -> main)
  Author: User <user@example.com>
  Date:   Thu Nov 21 20:39:04 2024 -0800

    addded
```

That's one "d" too many in the commit message. Fixing it up is as easy
as this:

``` {.default}
$ git commit --amend
```

And that brings me right into my editor where I can change the message.

If I don't want to use the editor, I can do it on the command line:

``` {.default}
$ git commit --amend -m "the new commit message"
```

Note that doing this preserves the author of the commit. (Which is
probably what you want 99.9999% of the time since you were probably
already the author.) If you want to change the identity, you'll have to
reconfigure your identity with `git config` and then run:

``` {.default}
$ git commit --amend --reset-author
```

## Adding some Files to the Commit

Ugh! You just made that commit but you forgot to add one of the files to
it! You got `foo.c` and `bar.c` in there, but you left out `baz.h`!

Let's look.

``` {.default}
$ ls
  bar.c  baz.h  foo.c
$ git log --name-only
  commit b307686933dca3db718e6a3e3f8226be11e7e278 (HEAD -> main)
  Author: User <user@example.com>
  Date:   Thu Nov 21 20:47:08 2024 -0800

      added

  bar.c
  foo.c
```

OK, so how can we get `baz.h` in there? Like this:

1. `git add baz.h` to add it to the stage.
2. `git commit --amend` to get it into the commit.

This will bring you into an editor to edit the commit message. You can
just save it as is. Or you can specify the `-m` option on the command
line to give a new message.

Alternately, if you're just adding files, you might not need to change
the commit message at all. In that case you can just run:

``` {.default}
$ git commit --amend --no-edit
```

That'll run the amend and not edit the commit message at all.

And there we have it—you can easily amend the last commit. Just be sure
you haven't pushed it before you do.

