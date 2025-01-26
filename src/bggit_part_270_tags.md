# Tags

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

## Lightweight Tags

TODO

## Annotated Tags

TODO

## Pushing Tags

TODO

## Deleting Tags

TODO just on the server
