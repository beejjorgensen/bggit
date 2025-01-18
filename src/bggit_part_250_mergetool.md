# Mergetool

[i[Mergetool]<]

Do you hate all those `>>>>>`, `=====`, and `<<<<<` things that Git puts
in your files during a merge conflict?

If so, using a _merge tool_ might be what you're after. A merge tool
will give you a graphical display showing your changes, the conflicting
changes, and the desired result of the merge. And it shows it in an
easy-to-digest form.

> **Personally, I dislike merge tools.** That seems nuts, but let me
> explain a moment. When you're in a merge conflict, the only thing you
> have to do is edit those files with the `=====` delimiters and make
> them _Right_, remember? You have to modify the file until it is
> correct, ripping out those delimiters as you go.
>
> It's just you and the file, that's it. No intermediaries messing with
> the contents. And when you're done, what you have is your final
> answer.
>
> But merge tools are intermediaries by their very nature. And we must
> trust that we're using them correctly to get the job done. And, for
> me, even after I've used them probably correctly, I still feel like I
> have to manually inspect the result to make sure it's _Right_.
>
> The benefit I do see is that with a merge tool you typically get a
> side-by-side view of the changes, as opposed to the up-and-down view
> you effectively get when editing the conflicting file. This can make
> the merge tool easier to use when you have a number of big conflicting
> hunks in a file.
>
> But in real life, I never use one. Also in real life, *lots* of people
> use them.

## Merge Tool Operations

Merge tools operate on a file-by-file basis. So when you're using on,
you're using it on a particular conflicting file.

They all tend to show you at least three panels:

* Your conflicting changes
* Their conflicting changes
* The result file that is _Right_

And they all tend to have the same core operations:

* **Go to next conflict**—all panels will move to the next conflict.
* **Go to previous conflict**
* **Choose yours**—copy _your_ conflicting changes into the final result,
  i.e. your changes are _Right_.
* **Choose theirs**—copy _their_ conflicting changes into the final
  result, i.e. your changes are _Right_.

In terms of usage, here's what we're going to do, assuming that the
merge tool starts you at the first conflict when it is launched:

1. Choose either "yours" or "theirs" to keep the _Right_ changes.
2. Go to the next conflict.
3. Repeat from Step 1 until all conflicts are resolved.

After you've gone through all the conflicts and chosen one or the other,
make sure the final result is _Right_ and then save/finish the result.

The merge tool will have staged the result for you, ready to commit and
finish the merge.

## Some Example Merge Tools

There are a lot of them, and I'll include some links here in
alphabetical order. Cross-platform unless otherwise noted.

* [fl[Araxis Merge|https://www.araxis.com/merge/index.en]]—Windows, Mac
* [fl[Beyond Compare|https://www.scootersoftware.com/]]
* [fl[Code Compare|https://www.devart.com/codecompare/]]—Windows
* [fl[KDiff3|https://invent.kde.org/sdk/kdiff3]]
* [fl[Meld|https://meldmerge.org/]]
* [fl[P4Merge|https://www.perforce.com/products/helix-core-apps/merge-diff-tool-p4merge]]
* [fl[Vimdiff|https://www.vim.org/]]
* [fl[WinMerge|https://winmerge.org/]]—Windows

In addition, IDEs like VS Code and IntelliJ often have their own
built-in merge tools that work independent of Git (no need to configure
anything in Git).

## Using Vimdiff as a Merge Tool

[i[Mergetool-->With Vimdiff]<]

We'll do a quick run-through of using Vimdiff as a merge tool since it
covers all the bases and has some tricky configuration. Other
third-party tools (except VS Code and other IDEs with this functionality
built-in) would have a similar configuration. Search the Internet for
the proper config for other tools.

> **This isn't a Vim tutorial.** So I'm just going to assume you know
> how to do things like save files and quit. I will say that to switch
> windows in Vim you use `CTRL-W` followed by a cursor direction, such
> as `CTRL-W` followed by `h` to move to the window to the left.

First things first, let's set up the configuration.

``` {.default}
$ git config --global set merge.tool vimdiff
$ git config --global set mergetool.vimdiff.cmd \
                             'vimdiff "$LOCAL" "$REMOTE" "$MERGED"'
$ git config --global set difftool.vimdiff.cmd \
                             'vimdiff "$LOCAL" "$REMOTE"
```

(Long commands split to fit in the book margins—it could be on a single
line.)

Note that last line is to explicitly set a two-panel view for `vimdiff`
and `difftool`. If it's not set, the `mergetool.vimdiff.cmd` directive
will make `difftool` have a three-panel display—probably not what you
wanted.

Once that's in place, let's say we have a merge conflict.

``` {.default}
$ git merge branch
  Auto-merging foo.txt
  CONFLICT (content): Merge conflict in foo.txt
  Automatic merge failed; fix conflicts and then commit the result.
```

At this point, we're in a classic run-of-the-mill merge conflict.

``` {.default}
$ git status
  On branch main
  You have unmerged paths.
    (fix conflicts and run "git commit")
    (use "git merge --abort" to abort the merge)

  Unmerged paths:
    (use "git add <file>..." to mark resolution)
	  both modified:   foo.txt

  no changes added to commit (use "git add" and/or "git commit -a")
```

But since we've set up our merge tool, let's use it:

``` {.default}
$ git mergetool
```

> **If Git is prompting you to ask if you really want to run the merge
> tool** (which you presumably do since you just ran `git mergetool`),
> you can turn off that "feature" with this config command:
>
> ``` {.default}
> $ git config --global set mergetool.prompt false
> ```
 
<!-- ` -->

This is going to bring up a Vim window with three panels. The left is
your local changes, the middle is the file as it exists in the repo, and
the right is the result of the merge.

The goal is to make the one on the right look _Right_. Now, you could
just do that outright by modifying the file there, but at that point,
why even use a merge tool?

So we'll follow the steps we outlined earlier.

When we first run `git mergetool`, we get dropped at the first conflict
with the cursor in the left window. The left window holds the changes we
made.

In the middle window, we'll see the corresponding changes that are in
the repo.

And in the right repo, we see what will be staged when we're done. Right
now in the right window, we see all the `=====` and `<<<<<` stuff. But
we'll change that in a moment.

*Move the cursor to the right window.* This is where the action will be.

Make sure the cursor is on a highlighted section (which probably will be
in multiple colors). This highlighted section is what we'll replace.

Let's choose which change to use.

If you want to keep your changes (and ditch the ones in the repo), use
this Vim command:

``` {.default}
:diffget LOCAL
```

If you want to discard your changes (and keep the ones in the repo), use
this command:

``` {.default}
:diffget REMOTE
```

When you run one of those, you'll see the content in the right window
change to what you wanted.

And then you can go to the next conflict with `]c`. (or to the previous
with `[c`.)

Do this until the right window is _Right_. Note that you are also free
to edit the right window directly all you want.

When you're done, save the right window and quit all the windows.

**Importantly** the second you exit the merge tool, Git will stage
whatever you saved in the rightmost window. If you exited too soon and
got stuff staged before you were done, use `git checkout --merge` with
the file in question to get it off the stage and back to "both modified"
state.

If there are multiple conflicting files, Git will bring up the merge
tool again to handle the next file in line.

And when you're done, the changes are made and you can finish the merge
with a commit as per usual.

But wait—what's that `.orig` file that wasn't there before? Read on!

[i[Mergetool-->With Vimdiff]>]

## Backing up the Originals

[i[Mergetool-->File backups]]

By default, when using a merge tool, Git will keep a backup of the file
before the merge tool touched it. You'll see these with a `.orig`
extension, like so:

``` {.default}
foo.txt.orig
bar.txt.orig
```

You can add these to your `.gitignore` if you want to, or you can
prevent the creation of them in the first place with this configuration
variable:

``` {.default}
$ git config --global set mergetool.keepBackup false
```

[i[Mergetool]>]
