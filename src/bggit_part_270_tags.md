# Tags

[i[Tags]<]

Tags are a way to annotate a particular commit. You can kind of think of
them like branches that don't move.

A very common case is to take a particular commit with a version number
like `1.2.3`.

I can't find any rules about what characters you can use in tag names,
but it seems safe to use ASCII upper and lower case, numbers, and
punctuation like `.`, `-`, and `_`, etc.

There are two types of tags:

* ***Lightweight***: Just a tag, e.g. `v3.14`.
* ***Annotated***: Also a tag, e.g. `v3.14`, but includes a message and
  author, like a commit.

You can generally use tags the same way you'd use branches (you can diff
them, switch to them, etc.) except they don't move.

[i[Tags-->Listing]<]

And you can see them in the log with the other branch information.

``` {.default}
commit 4fa1199d17a97990a7721eb8a73a4ee50 (HEAD -> main, tag: v3.14)
Author: User <user@example.com>
Date:   Sat Jan 25 19:04:43 2025 -0800

    Update the stuff

commit c265e0371b3fc11588e4183b35e0b96e3 (tag: v3.10)
Author: User <user@example.com>
Date:   Sat Jan 25 18:59:58 2025 -0800

    Add the stuff
```

Or get a list of all tags with just `git tag`.

[i[Tags-->Listing]>]

## Lightweight Tags

[i[Tags-->Creating]<]
[i[Tags-->Lightweight]<]

Adding a lightweight tag is easy enough. First, switch to the commit you
want to tag, and then run this, assuming you want a tag called
`tagname`:

``` {.default}
$ git tag tagname       # Tag HEAD commit with tagname
```

You can also tag a commit, or anything that refers to a commit (like a
branch or even another tag):

``` {.default}
$ git tag CPE1704TKS 4fa12    # tag commit 4fa23
$ git tag plover feature99    # tag branch feature99
```

[i[Tags-->Lightweight]>]

## Annotated Tags

[i[Tags-->Annotated]<]

Adding an annotated tag is just about as easy. Add the `-a` for
"annotate" switch.

Since an annotated tag is more like a commit, it's going to prompt for a
message. But you can also use `-m` to specify it on the command line.

``` {.default}
$ git tag -a v3490     # tag HEAD commit with v3490
```

Or if you want to specify the message on the command line:

``` {.default}
$ git tag -a v3490 -m "tag message"
```

[i[Tags-->Annotated]>]
[i[Tags-->Creating]>]

## Pushing Tags

[i[Tags-->Pushing]<]

By default, the tags only exist on your local repo, even if you do a
regular push. You have to tell it you want to push tags explicitly.

[i[Push-->Tags]]
If you want to push all new tags, you can:

``` {.default}
$ git push --tags
$ git push origin --tags  # Or you can specify a remote
```

If you want to just push one tag, you must specify the remote:

``` {.default}
$ git push origin tag3.14
```

After a tag is pushed, other collaborators will automatically get the
tags when they pull.

[i[Tags-->Pushing]>]

## Deleting Tags

[i[Tags-->Deleting]<]

You can delete a tag on your repo like this:

``` {.default}
$ git tag -d tagname
```

And that's easy enough. Except if you've already pushed on the server.
If you have, then the next time you pull you'll get the tag again.

So you'll have to delete the one on the remote, as well, which also must
be named explicitly:

[i[Push-->Tags]]

``` {.default}
$ git push origin -d tagname
```

That'll delete the tag on the server, but *it won't delete it from other
people's clones*. In fact, there's no easy way to do this.

The basic idea is that tags, once created, shouldn't be deleted. Now, if
you haven't yet pushed, no problem. Add, delete, and change all you
want. But once you've pushed (and someone has pulled), if you need to
change a tag, just make a new tag.

That's not a law; it's just more of a recommended guideline.

[i[Tags-->Deleting]>]
[i[Tags]>]
