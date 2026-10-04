---
about:
  - console/cli/src/probes.rs#workspace_root
watch: [sig, logic]
---

# Every verb but `init` works on the nearest workspace above `--repo`

`--repo` defaults to `.`, and agents rarely stand at a workspace's root: a
task checks out a project under `repo/`, the agent `cd`s into it, and runs
`gmr check` from there. Taken literally, that directory has no `.anchor/`, so
`run` created a fresh `.anchor/state/` in it, opened an empty journal, and
reported `observed 0` — the answer of a workspace with nothing to watch,
printed for a workspace whose anchors had all moved. That is a silent failure
path, which [[layers]] does not allow: the world did not answer "nothing
moved"; we read the wrong journal.

`workspace_root` walks `start.ancestors()` and returns the first directory
holding `.anchor/`, the way git finds `.git/`. With none above it, `start` is
its own root and nothing changes for a repository that has not run `init`.

`init` is the one verb that keeps `--repo` literally. Its job is to create a
workspace where it was asked; resolving upward would turn `init` in a nested
project into a second `init` of the enclosing one. A nested workspace is a
deliberate thing, and the nearest one wins, as a nested git repository does.

The test is `console/cli/tests/subdirectory.rs`. It fails on the literal
reading by finding the stray `.anchor/` in the subdirectory, which is the
observable half of the bug; the `observed 0` half follows from it.

## When this changes, ask

Does a new verb that must not resolve upward get dispatched before the
`match` in `run`, the way `init` is? And would any new way of naming a
workspace (an env var, a config file) bypass this function and bring the
literal reading back?
