<!-- Beej's guide to Git

# vim: ts=4:sw=4:nosi:et:tw=72
-->

<!-- No hyphenation -->
<!-- [nh[scalbn]] -->

<!-- Index see alsos -->
[is[Configuration-->Alias==>see Alias]]
[is[Branch-->on GitHub==>see GitHub, Branches]]
[is[Branch-->Diff==>see Diff, Between branches]]
[is[Detached `HEAD`==>see `HEAD`, Detached]]
[is[Fast-forward==>see Merge, Fast-forward]]
[is[Ignoring files==>see `.gitignore`]]
[is[Index==>see Stage]]
[is[`main`==>see Branch, `main`]]
[is[`master`==>see Branch, `master`]]
[is[`origin`==>see Remotes, `origin`]]
[is[`origin/main`==>see Branch, Remote tracking]]
[is[Recursion==>see Recursion]]
[is[Rename==>see Move]]
[is[Undelete==>see Remove, Undelete]]

[is[`git add`==>see Add]]
[is[`git add -p`==>see Patch mode]]
[is[`git blame`==>see Blame]]
[is[`git branch`==>see Branch]]
[is[`git checkout`==>see Checkout]]
[is[`git cherry-pick`==>see Cherry-pick]]
[is[`git clone`==>see Clone]]
[is[`git commit`==>see Commit]]
[is[`git config`==>see Configuration]]
[is[`git diff`==>see Diff]]
[is[`git fetch`==>see Fetch]]
[is[`git log`==>see Log]]
[is[`git merge`==>see Merge]]
[is[`git mv`==>see Move]]
[is[`git pull`==>see Pull]]
[is[`git push`==>see Push]]
[is[`git push --set-upstream`==>see Branch, Set upstream]]
[is[`git push -u`==>see Branch, Set upstream]]
[is[`git rebase`==>see Rebase]]
[is[`git reflog`==>see Reflog]]
[is[`git remote`==>see Remote]]
[is[`git reset`==>see Reset]]
[is[`git reset -p`==>see Patch mode]]
[is[`git restore`==>see Restore]]
[is[`git revert`==>see Revert]]
[is[`git rm`==>see Remove]]
[is[`git stash`==>see Stash]]
[is[`git status`==>see Status]]
[is[`git switch`==>see Switch]]
[is[`git tag`==>see Tag]]
[is[`git worktree`==>see Worktree]]

# Foreword

Hello again, everyone! In my role as an industry
professional-turned-college instructor, I definitely see my fair share
of students struggling with Git.

And who can blame 'em? It's a seemingly-overcomplicated system with lots
of pitfalls and merge conflicts and detached heads and remotes and
cherrypicks and rebases and an endless array of other commands that do
who-knows-what.

Which leads us directly to the goal: let's make sense of all this. We'll
start off easy (allegedly) with commands mixed in with some theory of
operation. And we'll see that understanding what Git does under the
hood is critical to using it correctly.

And I *promise* there's definitely a chance that after you get through
some of this guide, you might actually start to appreciate Git and like
using it.

I've been using it for years (I'm using it for the source code for this
guide right now) and I can certainly vouch for it becoming easier over
time, and then, even, second nature.

But first, some boilerplate!

## Audience

The initial draft of this guide was put online for the university
students where I worked (or maybe still work, depending on when you're
reading this) as an instructor. So it's pretty natural to assume that's
the audience I had in mind.

But I'm also hoping that there are enough other folks out there who
might get something of use from the guide as well, and I've written it
in a more general sense with all you non-college students in mind.

This guide assumes that you have basic POSIX shell (i.e. Bash, Zsh,
etc.) usage skills, i.e.:

* You know basic commands like `cd`, `ls`, `mkdir`, `cp`, etc.
* You can install more software.

It also assumes you're in a Unix-like environment, e.g. Linux, BSD,
Unix, macOS, WSL, etc. with a POSIX shell. The farther you are away from
that (e.g. PowerShell, Commodore 64), the more manual translation you'll
have to do.

Windows is naturally the sticking point, there. Luckily Git for Windows
comes with a Bash shell variant called Git Bash. You can also install
[fl[WSL|https://learn.microsoft.com/en-us/windows/wsl/]] to get a Linux
environment running on your Windows box. I wholeheartedly recommend this
for hacker types, since Unix-like systems are hacker-awesome, and
additionally I recommend you all become hacker types.

## Official Homepage

This official location of this document is (currently)
[fl[https://beej.us/guide/bggit/|https://beej.us/guide/bggit/]].

## Email Policy

I'm generally available to help out with email questions so feel free to
write in, but I can't guarantee a response. I lead a pretty busy life
and there are times when I just can't answer a question you have. When
that's the case, I usually just delete the message. It's nothing
personal; I just won't ever have the time to give the detailed answer
you require.

As a rule, the more complex the question, the less likely I am to
respond. If you can narrow down your question before mailing it and be
sure to include any pertinent information (like platform, compiler,
error messages you're getting, and anything else you think might help me
troubleshoot), you're much more likely to get a response.

If you don't get a response, hack on it some more, try to find the
answer, and if it's still elusive, then write me again with the
information you've found and hopefully it will be enough for me to help
out.

Now that I've badgered you about how to write and not write me, I'd just
like to let you know that I _fully_ appreciate all the praise the guide
has received over the years. It's a real morale boost, and it gladdens
me to hear that it is being used for good! `:-)` Thank you!

## Mirroring

You are more than welcome to mirror this site, whether publicly or
privately. If you publicly mirror the site and want me to link to it
from the main page, drop me a line at
[`beej@beej.us`](mailto:beej@beej.us).

## Note for Translators

[i[Translations]<]
If you want to translate the guide into another language, write me at
[`beej@beej.us`](mailto:beej@beej.us) and I'll link to your translation
from the main page. Feel free to add your name and contact info to the
translation.

Please note the license restrictions in the Copyright and Distribution
section, below.
[i[Translations]>]

## Copyright and Distribution

Beej's Guide to Git is Copyright © 2024 Brian "Beej Jorgensen" Hall.

With specific exceptions for source code and translations, below, this
work is licensed under the Creative Commons Attribution-Noncommercial-No
Derivative Works 3.0 License. To view a copy of this license, visit
[`https://creativecommons.org/licenses/by-nc-nd/3.0/`](https://creativecommons.org/licenses/by-nc-nd/3.0/)
or send a letter to Creative Commons, 171 Second Street, Suite 300, San
Francisco, California, 94105, USA.

One specific exception to the "No Derivative Works" portion of the
license is as follows: this guide may be freely translated into any
language, provided the translation is accurate, and the guide is
reprinted in its entirety. The same license restrictions apply to the
translation as to the original guide. The translation may also include
the name and contact information for the translator.

The programming source code presented in this document is hereby granted
to the public domain, and is completely free of any license restriction.

Educators are freely encouraged to recommend or supply copies of this
guide to their students.

Contact [`beej@beej.us`](mailto:beej@beej.us) for more information.

## Dedication

The hardest things about writing these guides are:

* Learning the material in enough detail to be able to explain it
* Figuring out the best way to explain it clearly, a seemingly-endless
  iterative process
* Putting myself out there as a so-called _authority_, when really
  I'm just a regular human trying to make sense of it all, just like
  everyone else
* Keeping at it when so many other things draw my attention

A lot of people have helped me through this process, and I want to
acknowledge those who have made this book possible:

* Everyone on the Internet who decided to help share their knowledge in
  one form or another. The free sharing of instructive information is
  what makes the Internet the great place that it is.
* Everyone who submitted corrections and pull-requests on everything
  from misleading instructions to typos.

Thank you! ♥
