# Reverting Changes

What if someone (ahem) made a commit earlier that you want to revert?
There might be ways to use `reset` to get there, but you can't rewrite
history if someone else has cloned it.

What you *can* do is make a new commit that undoes the old commit you no
longer want.

And `git revert` can do exactly that.
