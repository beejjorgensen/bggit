# Appendix: Getting Out of Editors {#editor-get-out}

[i[Exiting editors]<]

If you try to `git commit` and don't specify `-m` for a message, or if
you `git pull` and there's a non-fast-forward merge, or if you `git
merge` and there's a non-fast-forward merge and you don't specify `-m`,
or what I'm sure are a host of other reasons, you might get popped into
an editor.

And you might not be familiar with that editor.

So here's how to get out of it.

* **Nano**: If the editor says "Nano" or "Pico" in the upper left, then
  edit the commit message (if you want), then then hit `CTRL-X`, and
  then hit `Y` to save, then `ENTER` to accept the given filename.

* **Vim**: If the screen has a bunch of `~` characters down the left and
  a crazy-looking file name at the bottom maybe with the word `All`,
  you're in Vim or some other vi ("vee eye") variant. Press `i`, then
  type a message (if you want), then hit the `ESC` key in the upper
  left, then type two capital `Z`s in a row. `ZZ`. That should save and
  exit.

  I love Vim. But it took a while. If you want to learn more, see the
  [Appendix on Using Vim](#vim-tutorial), that has the briefest of
  tutorials. I guess the previous paragraph was really the briefest, so
  we'll call it the second-briefest.

[i[Exiting editors]>]
