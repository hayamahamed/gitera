#  Gitera

**An umbrella of utility tools for Git VC.**


This tool relies on POSIX standards for functioning, so all Unix and Unix like operating systems should handle this program.

    pip install gitera

It will give three commands in total as `gitera`, `gitout`, `gitnuke`.

`gitera` is the parent command with no special ability.

```
gitera
```
```
Gitera v0.0.16
Usage: gitout / got : view all commits of a repo in a single scrollable view with enter as checking out.
Usage: gitnuke / gne : create numerous amount of specified commits for testing purposes.
None of these has any sub commands so you may try all of these directly
```

`gitout` lets user scroll through all commits of the repo's current branch and checkout on enter. It also checks back to the commit checked out at before running `gitout` when quite.

```
gitout
```
![gitout in action and quitting](Docs/got.png)


`gitnuke` creates a specified amount (in numeric) of commits (for testing purposes).

```
gitnuke
```
```
How many commits you want? 1000 #specify it. I specified 1000 if not specified it defaults to 100 commits.
Started 1,2,3...
Half way done...
Completed.
```
