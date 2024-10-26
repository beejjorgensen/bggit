# Configuration {#configuration}

Waaaaay back at the beginning of this book, we did some Git
configuration. We did this:

``` {.default}
$ git config set --global user.name "Your Name"
$ git config set --global user.email "your-email@example.com"
```

When we did, it added that configuration information to a file and the
info in that file applies to all the Git repos on your system.

Unless you override them with a local config, that is. But stay tuned
for more on that later.

Let's look at one of those lines again:

``` {.default}
$ git config set --global user.name "Your Name"
                              ↑          ↑
                          variable     value
```

There are two main things in this line.

1. A *variable*, that is, the thing we're setting the value of.
2. A *value*, the value we're giving that variable.

In that case, the variable is `user.name` and the value is `"Your
Name"`.

> **What those two variables, `user.name` and `user.email`, are doing**
> is they're setting the values that will go in your commit messages!
> That's your identity when you commit! A side note here it that it's
> incredibly easy to impersonate anyone else in the world just by
> putting their name and email there. To mitigate this, one option is to
> [fl[digitally sign your commits|https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work]],
> but that's beyond the scope of this guide.

If the commands in this chapter are giving you errors, see the section
on [older Git versions](#config-old), below.

## Local Configuration

In those `git config` lines, above, you might have noticed the
`--global` switch:

``` {.default}
$ git config set --global user.name "Your Name"
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
$ git config set --global user.name "HAx0rBYnit3"
$ git config set --global user.email "l333T@example.com"
```

and that would be the default for all your repos. And then you might
have a new repo for a job:

``` {.default}
$ git init corporate_job_12
  Initialized empty Git repository in /user/corporate_job_12/.git/
```

And we pop in there, and we set the local config just for that repo
(it's local because we're not specifying `--global`):

``` {.default}
$ cd corporate_job_12
$ git config set user.name "Professional Name"
$ git config set user.email "professional@example.com"
```

And now, just in the `corporate_job_12` directory, we'll be using our
professional name and email in our commits. Everywhere else we'll be
using our elite hacker name.

You can override all the global configs on a per-repo basis by
specifying local configs.

Finally, the local config for a repo is found in the `.git/config` file
out of the repo's root directory.

## Listing the Current Config

You can view the current config with `git config list`. Add the
`--global` flag if you want to see the global config.

``` {.default}
$ git config list
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

## Getting, Setting, and Deleting Variables

An example "get":

``` {.default}
$ git config get user.name
  Professional Name
```

Note that it is only giving the active value (the local one in this
case) even though we saw with `git config list` that both the global and
local values were there.

And we've already seen a "set":

``` {.default}
$ git config set user.name "Alfred Manfrengensenton"
```

The double quotes are there so that the shell delivers the name as a
single argument. Normally it splits all arguments on spaces. You could
also use single quotes which is useful if the value has special shell
characters in it. The grotesquely oversimplified rule, with apologies to
shell enthusiasts, is to use quotes around the value if it has a space
in it.

Set will overwrite any previously-existing value of the name variable
name.

And last but not least, we can delete a variable with `unset`:

``` {.default}
$ git config unset user.name
```

## Some Popular Variables

To see which variables you can set, look in the manual page for the
appropriate command. You can usually get there by looking at the first
hit on your favorite search engine for `man git whatever`. For example,
you might find configuration variables for `git pull` by searching for
`man git pull` and bringing up the first hit.

That said, there's a [fl[big ol' list of them in the `git config` manual
page that you can
peruse|https://git-scm.com/docs/git-config#_variables]].

But here are some fun, common ones.

Variable        | Description
----------------|----------------------------------------------------------
`user.name`        | Your name
`user.email`       | Your email
`pull.rebase`      | Set to `true` to have a pull try to rebase. Set to `false` to have it try to merge.
`core.editor`      | Your default editor for commit messages, etc. Set to `vim`, `nano`, `code`, `emacs`, or whatever.
`merge.tool`       | Your default merge tool, e.g. `meld` or whatever.
`diff.tool`        | Your default diff tool, e.g. `vimdiff`
`difftool.prompt`  | Set to `false` to stop Git from always asking you if you want to launch your difftool.
`color.ui`         | Set to `true` for more colorful Git output
`core.autocrlf`    | Set to `true` if you're on Windows **and** not in WSL **and** the remote repo has Unix-style newlines **and** you want to use Windows-style newlines in your working directory. On other systems, set to `input`. This is all about working around Window's ancient newlines.
`commit.gpgsign`   | Set to `true` if you've configured GPG commit signing and want to always sign.
`help.autocorrect` | Set to `0` to show the command Git thinks you meant to type if you misspelled it. Set to `immediate` to have it run the corrected command right now. Set to `prompt` to ask you if you want to run it.

Again, there are a *lot* more of these. Peruse the docs for more.

## Editing the Config Directly

You can launch an editor (the one specified in the `core.editor`
variable) to edit the config file directly. Some people might find this
easier.

I can launch the editor like this:

``` {.default}
$ git config --edit
```

Add the `--global` flag to edit the global config file.

> **Like with the other commands, there's a new version of this one.**
> On newer Git installs, you can just say `git config edit` without the
> minus-minus.

When you get into the editor, you'll see a config file that might look
something like this:

``` {.default .numberLines}
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true

[user]
    name = Your Name
    email = user@example.com
```

If you look, you can see where `user.name` and `user.email` ended up.
That's how the config file is organized.

So you can edit it here and save those changes. Some people might find
this easier than adding or modifying variables on the command line.

> **If you corrupt your config with sloppy editing, you're in for an
> interesting time.** You won't be able to run `git config edit` again.
> You'll have to manually fix the config file in your favorite text
> editor.
>
> The local config file can be found relative to the root directory for
> the repo in question in `.git/config`.
>
> The global config file can be found at `~/.gitconfig` on Unix-like
> systems and `C:\Users\YourName\.gitconfig` on Windows.
>
> Bring the appropriate file up in your editor, fix the mistake, save
> it, and then `git config edit` should work again.

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

## Older Git Versions {#config-old}

I'm assuming you have a recent version of Git installed. But if you
don't, these commands might be different.

The [fl[Git manual page for `git config` has a complete summary of the
changes|https://git-scm.com/docs/git-config#_deprecated_modes]].

And here are the modern commands we use in this chapter:

```{.default}
git config get user.email                     # Get
git config set user.email "user@example.com"  # Set
git config unset user.email                   # Delete
git config list                               # List
git config edit                               # Edit
```

And here are the older equivalents:

``` {.default}
git config user.email                     # Get
git config user.email "user@example.com"  # Set
git config --unset user.email             # Delete
git config --list                         # List
git config --edit                         # Edit
```

Use the new ones if you can!

