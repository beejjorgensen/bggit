# Changing Identity {#changing-identity}

[i[Identity]<]

There are a few ways you're identified when you do work with Git.

They are held in:

* the `user.name` and `user.email` configuration variables
* the SSH key you use to authenticate with a remote server like GitHub
* the GPG key you use for signing commits (rare)

It's all well-and-good if you only ever use a single identity, but
sometimes you might want to use different ones. For example, maybe for
your personal fun work, you use one identity and SSH key, but then you
got a contract job and you want to use your professional email and have
to connect to a different server with a different SSH key.

Let's check out what the defaults are for all these, as well as how to
change them on a per repo basis.

## Changing the User Configuration Variables

[i[Configuration-->Name and email]]

You'll want to do this if you have, say, some repos for work and some for
play, or if you have multiple work or play emails you want to use
on a per-repo basis.

> **Everyone, including me, will tell you that you shouldn't use your
> work-assigned laptop for play**, and you double-especially shouldn't
> do that if your "play" is other work-for-hire. That said, contractors
> often have multiple things going on at once (and they own their
> hardware), and sometimes people doing their own for-fun work might
> want to use different emails on different projects.

We've already covered this in the configuration chapter, but it's easy
enough to change your local identify that's attached to each commit.
Just change `user.name` and `user.email` to whatever you want.

In the repo in question, set the local configuration to override your
global config:

``` {.default}
$ git config set user.name "My Alter Ego User Name"
$ git config set user.email "alterego@example.com"
```

And then when you make commits in this repo, that's the identity that
will be attached to them. Commits in other repos will still obey your
global username and email (unless you've overridden them, as well).

## Changing the SSH Authentication Key

[i[Configuration-->SSH identity]<]

You'll want to do this if you're connecting to someone's private remote
(e.g. they're running a Gitea site of their own or something), and you
need to set up a different SSH key just to access that site. But you
want to keep using your same SSH key for your personal GitHub. How can
we use the GitHub one for all my repos, and the alternate SSH key just
for this one repo?

This is slightly more involved, and [fl[there are a few ways to do
this|https://superuser.com/questions/232373/how-to-tell-git-which-private-key-to-use]],
but I'll share my favorite here.

First some background. When the `ssh` command runs, it needs to know
which identity it is running as. It uses a default identity (which is
in a file called `~/.ssh/id_something`, like `id_ed25519`) unless you
specify another one.

You can do this one the command line with the `-i` switch to `ssh`.

Let's say you have two private keys in your `.ssh` direcrtory,
`id_ed25519` and `id_alterego_ed25519`. The first one is the default key
SSH uses. But if we want to use the other one, we can specify it:

``` {.default}
$ ssh -i ~/.ssh/id_alterego_ed25519 example.com
```

Admittedly, that's a pain in the butt to type, so some people set up
their SSH config to use a particular key with a particular host name.
But we're not going down that route.

Instead, let's tell Git to use a particular identity by setting the
`core.sshCommand` variable locally for this repo. This variable just
holds the SSH command that Git uses to connect, which would normally be
`ssh`. Let's override:

``` {.default}
$ git config set core.sshCommand \
    "ssh -i ~/.ssh/id_alterego_ed25519 -F none"
```

(The command above is split into two lines to fit in the margins—it is
normally a single line and the `\` is Bash's line continuation.)

And—wait a second—what's that `-F none` on there? That's just a safety
that's telling SSH to ignore its default configuration file. Remember
how above I said people sometimes set an identity by domain in their SSH
config? This would override that since overriding is what we're trying
to do here.

The reason I like this approach is that you can easily do it on a
per-repo basis, and the config is stored with the repo (instead of in an
environment variable or in SSH's somewhat-unrelated configuration).

[i[Configuration-->SSH identity]>]

## Changing your GPG Signing Key {#gpg-signing}

[i[Configuration-->GPG signing key]<]

If you use your [fl[GPG key|https://www.gnupg.org/]] for signing you can
specify which key is used if you get its fingerprint (or probably email
or any other unique identifier recognized by GPG).

With apologies, setting up your GPG keypair is outside the scope of this
book. But the Git-side one-time setup looks like this:

``` {.default}
$ git config gpg.format gpg
$ git config commit.gpgsign true
```

First find the secret key you're interested in:

``` {.default}
$ gpg --list-secret-keys --keyid-format LONG
  /user/.gnupg/pubring.kbx
  ------------------------------
  sec   rsa4096/0123456789ABCDEF 2022-01-01 [SC] [expires: 2025-01-
        9993456789ABCDEF0123456789ABCDEF01234567
  uid     [ultimate] Personal User Name <personal@example.com>
  ssb   rsa4096/9993456789ABCDEF 2022-01-01 [E] [expires: 2025-01-0
  sec   ed25519/ABCDEF0123456789 2022-01-01 [SC] [expires: 2025-01-
        FFFDEF0123456789ABCDEF0123456789ABCDEF01
  uid     [ultimate] Professional User Name <professional@example.c
  ssb   rsa4096/FFFDEF0123456789 2022-12-06 [E] [expires: 2024-12-0
```

(Output has been cropped on the right to fit in the book.)

Look for the identity you want to use. In this case, let's say we want
to use "Professional User Name". We look for the `sec` line that's
associated with it (above it), and we copy that part of the secret line
after the type of encryption (usually `rsa4096` or `ed25519`). Here
that's `ABCDEF0123456789` in this fabricated example.

And then we locally configure this repo to use that key in particular.

``` {.default}
git config set user.signingkey ABCDEF0123456789
```

Then when you sign the commits, that key will be used.

[i[Configuration-->GPG signing key]>]

## Changing your SSH Signing Key

[i[Configuration-->SSH signing key]<]

In addition to GPG, you can also sign commits with SSH keys. You can
create a signing key with `ssh-keygen`:

``` {.default}
$ ssh-keygen -t ed25519
```

And then you have to do some one-time config if you haven't done so
already. Use `--global` if you want to set this up across all your
repos. This tells Git to use SSH keys and always sign commits:

``` {.default}
$ git config gpg.format ssh
$ git config commit.gpgsign true
``` 

Then we can set the key we use for signing. Change the path, below, to
point to the public key:

``` {.default}
$ git config user.signingkey ~/.ssh/id_ed25519_signing.pub
``` 

Lastly, we have to add your information to the `allowed_signers` file.
This file can go anywhere; in this example, we'll put it in `~/.ssh/`,
but you could do one-offs per repo if you wanted.

Firstly in this lastly step is to tell Git where your `allowed_signers`
file is.

``` {.default}
$ git config gpg.ssh.allowedSignersFile "~/.ssh/allowed_signers"
```

The contents of that file should have at least two fields. First the
email address found in your `user.email` config variable that you'll use
for the commits. Second, a copy of the public key from your
`user.signingkey` variable. Note that you want the *contents* of that
file, not the file name.

An example line in the `allowed_signers` file looks like this (line
truncated for formatting):

``` {.default}
user@example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAmaTS47vRmsKy
```

You can have multiple lines in that file for multiple identities.

[i[Configuration-->SSH signing key]>]

[i[Identity]>]
