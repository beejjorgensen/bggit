# Git Aliases

Some of these Git commands might be painstaking to type. So far, we
haven't had to do anything _too_ complicated, but we might eventually.

For example, let's say you want to see the names of the files that were
modified with `git log`. It's no problem; you can tell it to do that.

``` {.default}
$ git log --name-only
```

And that'll work.

But let's say for the sake of example that you find yourself doing that
a *lot*. It would get irksome.

Wouldn't it be easier if you could just make up a new command, like `git
logn` that would do the same thing?

That's what aliases are for.

## Creating an Alias

You do this through the configuration interface. Basically what you want
to set is the variable `alias.myname` where `myname` is the name of the
new command.

Let's say you want to make `git logn` an alias for `git log
--name-only`. You can do it like this:

``` {.default}
$ git config --global alias.logn 'log --name-only'
```

And at this point, you can run:

``` {.default}
$ git logn
```

and it will be an alias for `git log --name-only`, effectively running
that command.

I speculate that Git has a number of built-in command (like `log` and
`push`) and if you try to have it run something that is not a built-in,
it tries to find it as an `alias` variable. And if it does, it
substitutes that instead.

Since aliases are just regular configuration variables, getting,
setting, and deleting them happens as described in the [config
chapter](#configuration).

## Some Neat Sample Aliases

TODO

## Seeing Git's Alias Expansion

Let's say you've added an alias, but it's not working. When you run it,
it just gives some error and it's not super clear what's going on.

``` {.default}
% git logx
fatal: unrecognized argument: --foobar
```

You can ask Git to give you more information by adding `GIT_TRACE=1` to
the beginning of the command line.

> **This sets the environment variable `GIT_TRACE` to `1`,** but it only
> does it for this one command. It's not persistent. Git knows to look
> for `GIT_TRACE` and that it should alter its behavior if it finds it.

Here's some example output:

``` {.default}
% GIT_TRACE=1 git logx
  14:09:28.502707 git.c:758               trace: exec: git-logx
  14:09:28.502750 run-command.c:666       trace: run_command: git-l
  14:09:28.502905 git.c:416               trace: alias expansion: l
  14:09:28.502913 git.c:816               trace: exec: git log --fo
  14:09:28.502916 run-command.c:666       trace: run_command: git l
  14:09:28.502926 run-command.c:758       trace: start_command: /us
  14:09:28.504192 git.c:472               trace: built-in: git log 
  fatal: unrecognized argument: --foobar
```

Unfortunately I had to truncate the lines on the right so they fit in
the print version of the book, and that's what we really want to look
at. We'll get there in a moment.

For now, let's look on the left. What we see there is a timestamp and
some information about which part of the Git code is sending the trace
out. And the it ends with our error.

Let's scroll to the right and just look at the lines following the
`trace:`.

``` {.default}
trace: exec: git-logx
trace: run_command: git-logx
trace: alias expansion: logx => log --foobar
trace: exec: git log --foobar
trace: run_command: git log --foobar
trace: start_command: /usr/lib/git-core/git log --foobar
trace: built-in: git log --foobar
```

It might take some sifting through, but let's look just at the lines
with `run_command` and `alias expansion` in them:

``` {.default}
trace: run_command: git-logx
trace: alias expansion: logx => log --foobar
trace: run_command: git log --foobar
```

And there we can see exactly what's being expanded into what. And that
might be useful for debugging it.

It's probably a bit of overkill for this simple example, but there are
some aliases of extraordinary complexity for which this technique might
help.



