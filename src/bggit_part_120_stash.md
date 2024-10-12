# Stashing: Temporarily Set Changes Aside

[i[Stashing]<]

If you're in the middle of working on something and you realize you want
to pull some changes in, but you're not ready to make a commit because
your stuff is still completely broken, `git stash` is your friend. It
takes the stuff you're working on and stashes it away on the side,
returning your working tree to the state of the last commit.

So your changes will look like they're gone—but don't worry, they're
safely stashed away and you can bring them back later.

Then you can pull the new stuff down so you're up-to-date, and then
unstash your stuff on top of it.

It's kind of like a mini rebase in spirit.

## Example

Let's say we're all caught up to the latest.

``` {.default}
$ git pull
```

Great. And we start hacking. We open an existing file `foo.rs` and add
some code to it as per usual.

Then Chris calls from the next desk over and says, "Hey wait—I just made
a critical update to `main` and you should use that!"

And you think, "Well, heck, I was in the middle of something." You're
not ready to commit, but you want Chris's changes.

So you save your files and then run this:

``` {.default}
$ git stash
  Saved working directory and index state WIP on main: c72c245
                                some very descriptive commit message
```

And, if you were watching, you might have seen your file in your editor
change back to what it used to be! Your changes have been undone and
stashed away!

If you git status at this point, you'll see:

``` {.default}
$ git status
  On branch main
  Your branch is up to date with 'origin/main'.

  nothing to commit, working tree clean
```

It's all clean, which means now you can pull and get the latest `main`.
So you do that.

``` {.default}
$ git pull
  remote: Enumerating objects: 5, done.
  remote: Counting objects: 100% (5/5), done.
  remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
  remote: (from 0)
  Unpacking objects: 100% (3/3), 943 bytes | 943.00 KiB/s, done.
  From /home/beej/tmp/origin
     10a8ad6..e286011  main       -> origin/main
  Updating 10a8ad6..e286011
  Fast-forward
   foo.rs | 1 +
   1 file changed, 1 insertion(+)
```

And now you're up to date.

Oh, wait. What was it we were working on? Oh yeah! We stashed it! Let's
unstash those changes with `pop`:

``` {.default}
$ git stash pop
  Auto-merging foo.rs
  On branch main
  Your branch is up to date with 'origin/main'.

  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working
    directory)
	  modified:   foo.rs

  no changes added to commit (use "git add" and/or "git commit -a")
  Dropped refs/stash@{0} (046ac112f8c02c3dc02984ad71d353a3e5be9a7a)
```

Auto-merging sounds good. Looks like things went well. And if we look at
our file now we'll see our changes brought out of the stash and
reapplied. Our file `foo.rs` is in "modified" state and ready for us to
work on, or add and commit.

## The Stash Stack

If you're familiar with [flw[stack abstract data
type|Stack_(abstract_data_type)]], your ears might have perked up when
you read `git stash pop`.

Yes, Git tracks stashes in a stack. If you're not familiar with a stack,
read up on it first.

* `git stash` pushes the working tree on the stash stack.
* `git stash pop` pops the top of the stash stack and applies it to the
  working tree.
* `git stash list` shows you the current stash stack.
* `git stash drop` deletes a particular stash stack entry.

Because of this, I could `stash`, then do something else, then `stash`
again, and we'll have two stashes on the stack.

``` {.default}
$ git stash list
  stash@{0}: WIP on main: 659b132 added repo1 another line
  stash@{1}: WIP on main: 659b132 added repo1 another line
```

The top of the stack is `stash@{0}`.

If I ran just plain `git stash pop`, it would take the stash at the top,
which is index `0`, removing it from the stack and applying it to the
working tree.

But you can also pop by stash name if you want to pop something from the
middle of the stack.

``` {.default}
$ git stash pop 'stash@{1}'
$ git stash pop --index 1       # same thing
```

Similarly `stash drop` will pop the top of the stack and **not** apply
the changes to the working tree, discarding them instead.

And `stash drop` can also operate on a particular stash by name if you
want to drop something from the middle of the stack.

## Conflicts

[i[Stashing-->Conflicts]]

Now that you've spent so much time reading about conflicts during merge
and rebase, you might start to get a little worried here.

What if I stash then pull, but then popping the stash does something
that conflicts with the changes I pulled? Can that happen?

Of course it can. Hooray.

When it happens, it looks like this:

``` {.default}
$ git stash pop
  Auto-merging foo.rs
  CONFLICT (content): Merge conflict in foo.rs
  On branch main
  Your branch is up to date with 'origin/main'.

  Unmerged paths:
    (use "git restore --staged <file>..." to unstage)
    (use "git add <file>..." to mark resolution)
	  both modified:   foo.rs

  no changes added to commit (use "git add" and/or "git commit -a")
  The stash entry is kept in case you need it again.
```

Sure looks like a merge conflict, and it looks doubly so in the editor.

``` {.rs .numberLines}
fn main() {
<<<<<<< Updated upstream
    println!("This is critically fixed");
=======
    println!("This is sorta working");
>>>>>>> Stashed changes
}
```

You can see our stashed changes below where were tried to fix it, but
then we see that conflicts with Chris's fix from upstream.

So we do the merge thing and make it *Right*, editing it to look the way
we want, and we save it. Our status is still not clean, though.

``` {.default}
$ git status
  On branch main
  Your branch is up to date with 'origin/main'.

  Unmerged paths:
    (use "git restore --staged <file>..." to unstage)
    (use "git add <file>..." to mark resolution)
	  both modified:   foo.rs

  no changes added to commit (use "git add" and/or "git commit -a")
```

Let's add it with `git add` to mark it resolved.

A couple things can happen at this point.

1. If you just accepted the pulled version (i.e. discarding your
   conflicting changes), nothing new will happen. After all, there's
   already a commit in your repo with their version, so Git it smart
   enough to just call it a day. `git status` reports clean.

2. If you accepted a version different than the one you pulled (i.e. you
   kept some or all of your changes), then `git status` will report that
   file as modified and staged to be committed.

   If you're not ready to commit at this point, use `git restore
   --staged` to unstage the file. That will change it to just be
   modified and you can work on it more before you commit it.

**In both conflict cases the stashed changes are still in the stash!**
Yes, you ran `stash pop`, but when there's a conflict, the stash remains
untouched and doesn't actually pop.

If you're done with it (and you probably are), you can use `git stash
drop` to discard the particular stash from the stack and get all cleaned
up.

## Stashing New Files

[i[Stashing-->New files]]

What if you've added a new file to your working tree but it's currently
untracked? Can stash see it?

No. You have to add it first. So do a `git add` (but not a commit!) then
stash it. The new file should disappear from the working tree.

[i[Stashing]>]
