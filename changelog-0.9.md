# Changelog v0.8.2 -> v0.9

This time I will try to maintain a v0.8.x-branch in parallell with development on v0.9, so there may also be a v0.8.3-release, maybe even 0.8.4 - you never know.  However, all changes in v0.8.x will be backported into the v0.9-branch, including changelog entries.

## API changes

`save_todo`, `save_event` and `save_journal` now takes extra parameters, assumed to be equivalent with ical attributes as defined in the icalendar library, and may build icalendar data from scratch or enhance on the given icalendar data.

Github issues: https://github.com/python-caldav/caldav/issues/156 https://github.com/python-caldav/caldav/issues/155

Commits: eb8b7f877f4c5ca6181a177431b4a57f0a8c2039 b32f3ef3e15cd5edacca0ddaa9240c3814bc88ad

Credits: @Sigmun

## Refactoring

The digest vs basic auth is solved a bit differently in 0.8.2 and 0.9.  The code should basically do the same thing, but I feel the code in 0.9 is cleaner, but possibly a little bit bigger risk of breaking anything.

Github issues: https://github.com/python-caldav/caldav/issues/158

Commits: 1366e4e503180e10696f99ede6c2526451c7acab b3bde1c0e79d850acd5fa0615d3fbf6a3289c148 6be182800bbf7367a8da1005dad4b3e0b43967ca

## Bugfixes

* The string representation of any error class was hardcoded as "AuthorizationError".
* Concatinating an empty unicode string with an empty byte string will cause an exception.  The python_utilities.to_wire method would return an empty unicode string if given an empty unicode string.

Commits: eb708a9, 232acdd