# Mergetool

Do you hate all those `>>>>>`, `=====`, and `<<<<<` things that Git puts
in your files during a merge conflict?

If so, using a _merge tool_ might be what you're after. A merge tool
will give you a graphical display showing your changes, the conflicting
changes, and the desired result of the merge. And it shows it in an
easy-to-digest form.

> **Personally, I dislike merge tools.*** That seems nuts, but let me
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

After you've gone through all the conflicts and chosen one or the other,
make sure the final result is _Right_ and then save/finish the result.

The merge tool will have staged the result for you, ready to commit and
finish the merge.

## Some Example Merge Tools

TODO

## Using Vimdiff as a Merge Tool

We'll do a quick run-through of using Vimdiff as a merge tool since it
covers all the bases and has some tricky configuration. Other
third-party tools (except VS Code) would have a similar configuration.

First things first, let's set up the configuration.

``` {.default}
$ git config --global set merge.tool vimdiff
$ git config --global set mergetool.vimdiff.cmd \
                             'vimdiff "$LOCAL" "$REMOTE" "$MERGED"'
```

(Second command split to fit in the book margins—it could be on a single
line.)

Search the Internet for the proper config for other tools.

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

TODO

## Backing up the Originals

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
