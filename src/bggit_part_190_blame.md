# Who's to Blame for this Code?

[i[Blame]<]

Let's say you find something in the shared codebase that's just wrong.
Or, charitably, we'll say you found something _interesting_.

And you want to know who was to blame for that _incredible_ code.

This is where a simple Git command can enlighten you.

Here's some example truncated output (so that it fits in the book
margins):

``` {.default}
$ git blame --date=short foo.py
  8c96991f (Alice 2024-10-08  4) def encode_data(message, value):
  8c96991f (Alice 2024-10-08  5)     encoded_message = message.enco
  8c96991f (Alice 2024-10-08  6)     encoded_value = value.to_bytes
  3b0b0e76 (Chris 2024-10-09  7)     length = len(encoded_message) 
  3b0b0e76 (Chris 2024-10-09  8)     encoded_length = length.to_byt
  8c96991f (Alice 2024-10-08  9)
  8c96991f (Alice 2024-10-08 10)     data = encoded_length + encode
  8c96991f (Alice 2024-10-08 11)
  8c96991f (Alice 2024-10-08 12)     return data
```

I have the `--date=short` switch in there to compress it even more so it
fits in the book. Otherwise it would show a full time stamp.

What we see in this fabricated example is that Alice has checked in the
majority of this function, but the next day Chris came in and modified
or added those additional lines in the middle.

And now we know.

## More Bells and Whistles

You can use the `--color-lines` switch to get color output, alternating
colors between commits. Very exciting. If you want that to always
happen, you can set the `color.blame.repeatedLines` config option.

We already saw `--date=short` to chop the date down a bit.

You can show the email address of the contributor with `-e` or
`--show-email`.

You can reliably detect lines that were moved or copied within a file
with `-M`. And you can do the same thing across multiple files with
`-C`.

Finally, your IDE (like VS Code) might support blame, either natively or
via an extension. Some people just have this feature turned on all the
time.

[i[Blame]>]
