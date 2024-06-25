# Things to add

Git choosing default merge strategy
Git rebase

Collaboration

---

Maybe you've already addressed it in your Collaboration topic, but
here's a specific use case...

My capstone team has a main branch that we use for major versions, and a
dev branch where we merge our individual feature branches during code
reviews in weekly meetings. (So we only push to main once the code is
tidy and tested at the end of the term).

After finishing work on a feature, even if an individual is careful to
pull from the dev branch and take care of any conflicts on their working
branch before doing a final pull request, we still run into conflicts
during the meetings because sometimes we have 3-6 feature branches
getting merged back into dev.

Is there a recommended way to deal with this situation to speed our
process during the meetings? If so, that'd be a guide I'd follow every
week!

---

I think it would be worthwhile to cover how to securely connect your
GitHub repo to a remote machine that others have access to. Setting up
SSH keys, etc. For example, for Parallel Programming, you have to run
code on the OSU HPC but it is nice sometimes to write code locally, then
pull those changes to the HPC server.

---

Interactive rebasing is something I use a ton nowadays with my workflow,
but I also know it steps into danger land with pitfalls and advanced
topics. Reflog is another one of those useful tools but it likely
doesn't fit into the normal flow.

Remotes + CI/CD also tend to be a common workflow, but maybe outside of
just Git.

