# Difftool

Admittedly, this diff output is hard to read. I swear, though, you do
get used to it. I use it all the time.

That said, it can be nicer to see something more *visual*, you know,
like the old version on the left and the new version on the right in a
way that's visually easier to comprehend.

> **If you're using VS Code or some other IDEs, you get some nice
> diffing for free and don't necessarily need to pay attention to this
> section.** See more in the VS Code chapter.

First, the bad news is that Git doesn't support this out of the box.

The good news is that there are a lot of third-party tools that do, and
you can easily hook them up so that they work with Git super easily.

How easy?

Once you set it up, you'll be able to just write `difftool` instead of
`diff` on the command line. For example:

``` {.default}
$ git difftool HEAD~3^!
```

And what does that get you? For me, where I use Vim and have Vimdiff set
up as my difftool, it gives me a screen like in Figure_#.1.

![Vimdiff as the difftool.](img_difftool.png "Vimdiff as the difftool.")

This might be a little tough to see in black and white, but what we have
is the old version on the left and the new version on the right. The
lines of minus signs on the left indicate lines that don't exist in the
old version, and we can see highlighted lines on the right that exist in
the new version.

But if you just try to run `git difftool` out of the box, it won't work.
You have to configure it first.

## Configuring

Firstly, Git normally prompts you before launching a third-party
difftool. This is annoying, so let's turn it off globally:

``` {.default}
$ git config --global difftool.prompt false
```

Secondly, we need to tell it which tool to use.

``` {.default}
$ git config --global diff.tool vimdiff
```

And that might be enough. If `vimdiff` (or whichever diff tool you're
using) is in your `PATH`[^43a2], you should be in business and you're
good to go.

[^43a2]: Setting the `PATH` is outside the scope of this tutorial, but
    the short of it is if you can run the diff tool command on the
    command line (e.g. by running `vimdiff`), then it is in the `PATH`.
    If it says `command not found` or some such, then it is **not** in
    the `PATH`. Search the Intertubes for how to add something to the
    `PATH` in Bash. Or set the Git path config explicitly, as shown in
    the following paragraph.

If it's not in your `PATH`, maybe because you installed it locally in
your home directory tree somewhere, you can either add it to your `PATH`
(search the Net for how to do this), *or* you can specify the full path
to your particular difftool. Here's an example with `vimdiff`, which is
redundant for me because `/usr/bin` is already in my `PATH`.

``` {.default}
$ git config --global difftool.vimdiff.path /usr/bin/vimdiff
```

If you're using a different difftool other than `vimdiff`, replace that
part of the config line with the name of the command.

Again, you only have to set the path if the tool isn't installed in a
standard place.

## Available Difftools

There are a number of diff tools out there you can choose from. Here's a
partial list, with the caveat that I've only ever used Vimdiff.

* [fl[Araxis Merge|https://www.araxis.com/merge/index.en]]
* [fl[Beyond Compare|https://www.scootersoftware.com/]]
* [fl[DiffMerge|https://sourcegear.com/diffmerge/]]
* [fl[Kdiff3|https://kdiff3.sourceforge.net/]]
* [fl[Kompare|https://apps.kde.org/kompare/]]
* [fl[Meld|https://meldmerge.org/]]
* [fl[P4Merge|https://www.perforce.com/products/helix-core-apps/merge-diff-tool-p4merge]]
* Vimdiff (comes with [fl[Vim|https://www.vim.org/]])
* [fl[WinMerge|https://winmerge.org/?lang=en]]

Some of these are free, some are paid, and some are free trial.

And remember, VS Code has this functionality without using difftool.

