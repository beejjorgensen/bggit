# Configuration

Waaaaay back at the beginning of this book, we did some Git
configuration. We did this:

``` {.default}
$ git config --global user.name "Your Name"
$ git config --global user.email "your-email@example.com"
```

When we did, it added that configuration information to a file[^bd88]
and the info in that file applies to all the Git repos on your system.

[^bd88]: On Unix-like systems, this file is called `~/.gitconfig` and is
    found in your home directory. On Windows it's in
    `C:\Users\YourUserName\.gitconfig`.

Unless you override them with a local config, that is. But stay tuned
for more on that later.

Let's look at one of those lines again:

``` {.default}
$ git config --global user.name "Your Name"
                          ↑          ↑
                         key       value
```

There are two main things in this line.

1. A *key*, that is, the thing we're setting the value of.
2. A *value*, the value we're giving that key.

In that case, the key is `user.name` and the value is `"Your Name"`.

> **What those two keys, `user.name` and `user.email`, are doing** is
> they're setting the values that will go in your commit messages!
> That's your identity when you commit! A side note here it that it's
> incredibly easy to impersonate anyone else in the world just by
> putting their name and email there. To mitigate this, one option is to
> [digitally sign your
> commits](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work),
> but that's beyond the scope of this guide.

## Local Configuration

In that `git config` line you might have noticed the `--global` switch:

``` {.default}
$ git config --global user.name "Your Name"
```

Unless you explicitly say `--global`, Git assumes you mean the local
configuration.

What is the local configuration? It's the configuration that applies to
the repo that you're currently in, and no others.

*Configuration options in the local config override the global config!*

Here's a practical example of why you might do this. Let's say you have
a personal email for your fun projects, and a contractor email that you
use for work-for-hire. But since you're an independent contractor, you
have all these projects on one computer.

However, you want to use your work identity (name and email) for your
contract work and your hacker identify for your fun work.

One thing you might do is set the following globally:

``` {.default}
$ git config --global user.name "HAx0rBYnit3"
$ git config --global user.email "l333T@example.com"
```

and that would be the default for all your repos. And then you might
have a new repo for a job:

``` {.default}
$ git init corporate_job_12
  Initialized empty Git repository in /user/corporate_job_12/.git/
```

And we pop in there, and we set the local config just for that repo
(it's local because we're not specifying `--global`:

``` {.default}
$ cd corporate_job_12
$ git config user.name "Profesional Name"
$ git config user.email "professional@example.com"
```

And now, just in the `corporate_job_12` directory, we'll be using our
professional name and email in our commits. Everywhere else we'll be
using our elite hacker name.

You can override all the global configs on a per-repo basis by
specifying local configs.

Finally, the local config for a repo is found in the `.git/config` file
out of the repo's root directory.

## Listing the Current Config

You can view the current config with `git config --list`. Add the
`--global` flag if you want to see the global config.

> **In newer versions of Git, the command is different.** It's merely
> `git config list`. As of Git 2.46.1, both methods work.

``` {.default}
$ git config --list
  user.name=HAx0rBYnit3
  user.email=l333T@example.com
  init.defaultbranch=main
  core.repositoryformatversion=0
  core.filemode=true
  core.bare=false
  core.logallrefupdates=true
  user.name=Professional Name
  user.email=professional@example.com
```

You can see in there that `user.name` and `user.email` appear twice. The
first is from the global config, which is overridden later by the value
in the local config.

## Getting, Setting, and Deleting Keys

Before we begin, a note on Newer Git Versions. Newer Git versions
use keywords `get`, `set`, and `unset` to do these actions. We've been
using the older Git syntax, and we'll keep using it until everyone is
updated.

So here are the *old* Git config commands for getting, setting, and
deleting keys. They still work as of Git version 2.46.1.

``` {.default}
git config user.email                     # Get
git config user.email "user@example.com"  # Set
git config --unset user.email             # Delete
```

And here are the *new* Git config commands for getting, setting, and
deleting keys. They already work with Git version 2.46.1. I don't know
when they were introduced, but ChatGPT (which can't be trusted with
facts) says they came in with Git 2.41. I haven't verified this.

```{.default}
git config get user.email                     # Get
git config set user.email "user@example.com"  # Set
git config unset user.email                   # Delete
```

An example "get":

``` {.default}
$ git config user.name
  Professional Name
```

Note that it is only giving the active value (the local one in this
case) even though we saw with `git config list` that both the global and
local values were there.

Someday they're going to deprecate the old versions of the commands, but
that day isn't here yet. And then after that someday they'll probably
remove them. My money's on... the year 2034. And if you're reading this
after that, how'd I do?

## Some Popular Keys

TODO

## Editing the Config Directly

TODO

## Conditional Configuration

This is more than I want to talk about, but it's neat enough to point
out.

In Git config files, you can *include* other config files. This gives
you a way, if your config files are bananas, to break them apart
logically.

You can also do *conditional includes*. That is, you can choose to
include a file based on some condition being true.

Testable conditions are:

* Which directory this repo is in
* If you're on a particular branch
* If there is a particular remote configured

This gives you all kinds of power. Personally, all of it is more than I
need, and I've never used this feature, but that's just me.

[fl[Get more info and examples in the official
book|https://git-scm.com/docs/git-config#_conditional_includes]].
