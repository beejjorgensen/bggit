# Appendix: Just Enough Vim {#vim-tutorial}

[fl[Vim|https://www.vim.org/]] is a very-commonly installed editor with
a steep learning curve.

This appendix is here just to give you enough Vim to be dangerous!

## Launching Vim

It could be you found yourself in Vim because you were committing and
you didn't use `-m` to specify a message. You'll know it if you see some
`~` characters down the left and some kind of status bar at the bottom.

Or you might have launched it yourself with something like this, to edit
`foo.c`:

``` {.default}
$ vim foo.c
```

## Modal Editing

Vim primarily exists in two modes:

* ***Insert Mode***: This is the mode where you're pressing keys and the
  corresponding letters appear in your document, just like you expect
  from any normal editor.

* ***Normal mode***: This is the special Vim mode that you're not
  familiar with in virtually all other editors. In this mode, keys have
  special meaning. For example, the `h` key moves the cursor one
  character to the left.

  **The editor starts in normal mode!** This is why when you get dumped
  into it none of the keys do what you want.

The power of Vim comes from memorizing *tons* of Normal Mode commands.
This allows you to move the cursor and edit at speed. The [fl[vimhelp
website has a reference of all the normal mode
commands|https://vimhelp.org/index.txt.html#normal-index]], just to give
you a rough idea of what's available.

But at first, when you barely know any Normal Mode commands, modal
editing just seems to get in the way. But as you get better at it,
you'll see it's actually a really powerful feature.

## Going Between Modes

Here are the two main modes:

* To get from *normal mode* to *insert mode*, press `i`.
* To get from *insert mode* back to *normal mode*, press `ESC`. (That's
  the "escape" key in the upper left of the keyboard.)

There! You've learned one normal mode command! `i` to insert some text!

> **Try it:** launch Vim, type `i`, then type `hello world!`, then hit
> `ESC` to get back to normal mode.

## Moving the Cursor

You can probably use the cursor keys. In fact, your version of Vim might
even allow you to use them without ever leaving insert mode.

*Real* Vim users move the cursor in normal mode with the following keys.

* Up: `k`
* Down: `j`
* Left: `h`
* Right: `l`

Muscle memory will eventually take over with these.

If you're in insert mode, the delete key should generally work as
expected, as well.

## More Modes

I said there were two main modes, but there are actually more. Here are
two more bonus modes:

* To get from *normal mode* to *command-line mode*, press `:`. More on
  this, below.
* To get from *normal mode* to *search mode*, enter `/`. Type a string
  to search for.

## Command Line Mode

As mentioned earlier, if you're in normal mode, you can hit `:` to get
to ***command line mode***.

This moves the cursor to the bottom of the screen and allows you to type
a command there.

So from now on in this chapter, when I say something like `:q!`, that
means to type those three characters from normal mode.

If you get into command line mode and want to get back to normal mode,
just press return without entering a command.

## Exiting Vim

There are a few ways, and all of them start from normal mode. (So hit
`ESC` after you're done entering text, then try to exit.)

* `ZZ` — exit, saving only if there have been changes
* `:wq` — exit, saving unconditionally ("write, quit")
* `:q` — exit, don't save
* `:q!` — exit, don't save even if there have been changes!

And one more that's of use for Git:

* `:cq` — exit with a non-zero (AKA error) exit status

If you do a `:cq` when entering a commit message in Vim, Git will think
something went wrong and not complete the commit. So if you find
yourself in Vim writing a commit message and think, "I didn't mean to do
this yet!" you can `:cq` to get out of it. The files will remain on the
stage.

## Learn More

If you have Vim installed, you already have Vim Tutor installed! This is
just a file that gets opened and directs you through using and learning
vim.

Launch it with:

``` {.default}
$ vimtutor
```

If you don't feel like messing with it right now, you can just `:q!` to
quit.

There's also an interactive online tutorial called
[fl[OpenVim|https://openvim.com/]] that gets you through the first
steps.

Finally, [fl[ChatGPT|https://chatgpt.com/]] or other AIs will be helpful
in finding new normal mode commands and answering questions.

> _"This your last chance. After this there is no turning back. You take
> the blue pill, the story ends. You wake up using your normal editor
> and edit files whatever way you want to. You take the red pill, you
> stay in Vim and I show you how deep the rabbit hole goes."_
>
> \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ —With apologies to Morpheus, _The Matrix_

