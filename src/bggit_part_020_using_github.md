# GitHub: How To Use It

Now, we've said that GitHub (which is a proprietary web front-end to Git
run and owned by Microsoft) is not Git, and it's true. It's also true
that you never even need to touch GitHub in order to use Git.

That said, it's *really* common for people to use GitHub, so we'll get
it set up in this chapter.

Here we'll make a new GitHub account and see how authentication works.
This involves some one-time setup.

If you already have a GitHub account, you can skip that section.

If you already have authentication set up with GitHub CLI or with SSH
keys, you can skip that section, as well.

If you don't need to use GitHub, you can skip the entire chapter!

## Making a GitHub Account

[i[GitHub-->Account creation]]

Head on over to [fl[GitHub|https://github.com/]] and click `Sign Up`.
Follow those instructions.

Eventually you'll end up on your home screen dashboard.

## Creating a New Repo on GitHub

[i[GitHub-->Repo creation]]

This will make a repository on GitHub that you own. It does not make a
local repository—you'll have to clone the repo for that, something we'll
do later.

In GitHub, there's a blue `New` button on the left of the dashboard.

Also, there's a `+` pulldown on the upper right center that has a "New
Repository" option. Click one of those.

On the subsequent page:

1. Enter a "Repository name", which can be anything as long as you don't
   already have a repo by that name. Let's use `test-repo` for this
   example.

2. Check the "Add a README file" checkbox.

   (In the future, you might already have a local repo you're going to
   push to this new repo. If that's the case, do **not** check this box
   or it'll prevent the push from happening.)

3. Click `Create repository` at the bottom.

And there you have it.

## Authentication

[i[GitHub-->Authentication]]

Before we get to cloning, let's talk authentication. In the previous
part of the intro, we say that username/password logins were disabled,
so we have to do something different.

There are a couple options:

* Use a tool called GitHub CLI
* Use SSH keys

GitHub CLI is likely easier. SSH keys are geektacular.

If you already have authentication working with GitHub, skip these
sections.

### GitHub CLI

[i[GitHub-->GitHub CLI setup]]

This is a command line interface to GitHub. It does a number of things,
but one of them is providing an authentication helper so you can do
things like actually push to a remote repo.

[fl[Visit the GitHub CLI page|https://cli.github.com/]] and follow the
installation instructions. If you're using WSL, Linux, or another Unix
variant, see their [fl[installation
instructions|https://github.com/cli/cli#installation]] for other
platforms.

Once you have it installed, you should be able to run 'gh --version' and
see some version information, e.g.:

``` {.default}
$ gh --version
  gh version 2.42.1 (2024-01-15)
  https://github.com/cli/cli/releases/tag/v2.42.1
```

Then you'll want to run the following two commands:

``` {.default}
$ gh auth setup-git
$ gh auth login
```

The first is one-time only.

The second command will take you through the login process. You'll have
to do this again if you log out.

When choosing the authentication type between SSH and HTTPS, you can
choose HTTPS or SSH. Remember your choice when you go to clone a repo
later.

### SSH Keys

[i[GitHub-->SSH setup]]

This is more involved, but has slightly more geek cred and doesn't
require you to install GitHub CLI.

If you already have an SSH keypair, you can skip the key generation
step. You'd know you had one if you ran `ls ~/.ssh` and you saw a file
like `id_rsa.pub` or `id_ed25519.pub`.

To make a new keypair, run the following command:

``` {.default}
$ ssh-keygen -t ed25519 -C youremail@example.com
```

(The `-C` sets a "comment" in the key. It can be anything, but an email
address is common.)

This results in a lot of prompts, but you can just hit ENTER for all of
them.

> **Best practice is to use a password to access this key**, otherwise
> anyone with access to the private key can impersonate you and access
> your GitHub account, and any other account you have set up to use that
> key. But it's a pain to type the password every time you want to use
> the key (which is any time you do anything with GitHub from the
> command line), so people use a _key agent_ which remembers the
> password for a while.
>
> If you don't have a password on your key, you're relying on the fact
> that no one can get a copy of the private portion of your key that's
> stored on your computer. If you're confident that your computer is
> secure, then you don't need a password on the key. Do you feel lucky?
>
> Setting up the key agent is outside the scope of this document, and
> the author in unsure of how it even works in WSL. [fl[GitHub has
> documentation on the
> matter|https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent]].
>
> For this demo, we'll just leave the password blank. All of this can be
> redone with a new key with a password if you choose to do that later.

Anyway, just hitting ENTER for all the prompts gets you something like
this:

``` {.default}
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in id_ed25519
Your public key has been saved in id_ed25519.pub
The key fingerprint is:
SHA256:/lrT43BQBRPJpUXxpTBFInhdtZSQjQwxU4USwt5c0Lw user@locahost
The key's randomart image is:
+--[ED25519 256]--+
|        .o.X^%^=+|
|        ..oo*^.=o|
|        ..o = o..|
|         . + E   |
|        S .      |
|       .   o     |
|        . + +    |
|         o = .   |
|        ... .    |
+----[SHA256]-----+
```

> **If you chose any file name other than the default for your key**,
> you'll have to do some [fl[additional configuration to get it to work
> with
> GitHub|https://www.baeldung.com/linux/ssh-private-key-git-command]].

> **What's that randomart thing with all the weird characters?** It's a
> visual representation of that key. There are ways to configure SSH so
> that you see the randomart every time you log in, say. And the idea is
> that if one day you see it looks different, something could be amiss
> security-wise. I doubt most people every look at it again once it's
> been generated, though.

Now if you type `ls ~/.ssh` you should see something like this:

``` {.default}
id_ed25519    id_ed25519.pub
```

The first file is your _private key_. This is never to be shared with
anyone. You have no reason to even copy it.

The second file is your _public key_. This can be freely shared with
anyone, and we're going to share it with GitHub in a second so that you
can log in with it.

> **If you have trouble in the following subsections**, try running
> these two commands:
>
> ``` {.default}
> $ chmod 700 ~/.ssh
> $ chmod 600 ~/.ssh/*
> ```
> <!-- ` -->
>
> You only have to do that once, but SSH can be a bit picky if the file
> permissions on those files aren't locked down.

Now in order to make this work, you have to tell GitHub what your public
key is.

First, get a copy of your public key in the clipboard. ***Be sure you're
getting the file with the `.pub` extension!***

``` {.default}
$ cat ~/.ssh/id_ed25519.pub
```

You should see something like this:

``` {.default}
ssh-ed25519 AAAC3N[a bunch of letters]V+znpoO youremail@example.com
```

Copy the entire thing into the clipboard so you can paste it later.

Now go to GitHub, and click on your icon in the upper right.

Choose "Settings".

Then on the left, choose "SSH and GPG keys".

Click "New SSH Key".

For the title, enter something identifying, like, "My laptop key".

Key type is "Authentication Key".

Then paste your key into the "Key" field.

And click "Add SSH key".

We'll be using SSH to clone URLs later. Remember that.

## Make a Local Clone of the Repo

[i[GitHub-->Cloning]]

We need to figure out the URL to the repo so we can clone it.

If you click on your icon in the upper right, then "My Repositories", you
should see a page with all your repos. At this point, it might just be
your `test-repo` repo. Click on the name.

And you should then be on the repo page. You can browse the files here,
among other things, but really we want to get the clone URL.

Click the big blue "Code" button.

What you do next depends on if you're using GitHub CLI or SSH keys.

### Cloning from GitHub with GitHub CLI

[i[GitHub-->Cloning with GitHub CLI]]

You have two options.

* **Option 1**: Earlier when we authenticated with `gh auth login` I
  said to remember if you chose HTTPS or SSH. Depending on which you
  chose, you should choose that tab on this window.

  Copy the URL.

  Go to the command line and run `git clone [URL]` where `[URL]` is what
  you copied. So it'll be this for HTTPS:

  ``` {.default}
  $ git clone https://github.com/user/test-repo.git
  ```

  or this for SSH:

  ``` {.default}
  $ git clone git@github.com:user/test-repo.git
  ```

* **Option 2**: Choose the "GitHub CLI" tab. Run the command as they
  have it, which will be something like:

  ``` {.default}
  $ gh repo clone user/test-repo
  ```

### Cloning from GitHub with SSH Keys

[i[GitHub-->Cloning with SSH]]

If you set up an SSH key earlier, you can use this method.

After hitting the blue "Code" button, make sure the "SSH" tab is
selected.

Copy that URL.

Go to the command line and run `git clone [URL]` where `[URL]` is what
you copied. So it'll be something like this:

``` {.default}
$ git clone git@github.com:user/test-repo.git
```

## Make Changes and Push!

[i[Pushing]]

Now that you've cloned the repo, you should be able to `cd` into that
directory, edit a file, `git add` it to the stage, then `git commit -m
message` to make a commit...

And then `git push` to push it back to the clone on GitHub!

And after that if you go to the repo page on GitHub and hit reload, you
should be able to see your changes there!

And now we're back to that standard common flow:

1. _Clone_ a _remote_ repo.
2. Make some local changes.
3. Add those changes to the _stage_.
4. _Commit_ those changes.
5. _Push_ your changes back to the remote repo.
6. Go back to Step 2.

## Collaboration on GitHub

[i[Collaboration-->with GitHub]]

There are two main techniques for this:

1. Fork/pull request
2. Add a collaborator

We'll talk about the first one in the future.

For now, the easiest way to add collaborators is to just add them to
your repo.

On the repo page on GitHub, choose "Settings", then "Collaborators" on
the left.

After authenticating, you can click "Add people". Enter the username of
the person you want to collaborate with.

They'll have to accept the invitation from their GitHub inbox, but then
they'll have access to the repo.

Be sure to only do this with people you trust!

