Git Style Guidelines
====================
For Git, we try to follow a general pattern for commit messages and branch naming to make things organized.
- - -
## Commit Messages ##
All commit messages should:
* Start with a capital letter.
* Never end in puncuation.
* Be in the present tense.
* Have a title less than 100 characters.
* End in a new line.

If a description is provided in the commit message, it should be separated from the title by a blank line. If the commit addresses an issue, its issue number should be referenced at the end of the commit message's description.

Whenever possible, commit messages should be prefixed with a group name.

For example: ```Root: ```, ```ToonBase: ```, ```Tools: ```

## Branch Naming ##
All branch names should:
* Be entirely lower case.
* Use **-** as a separator.
* Be categorized into one of the following groups:
    * wip
    * bugfix
    * test
    * enhancement
    * feature

For example: ```feature/parties```, ```bugfix/toontorial```, ```enhancement/fix-memory-leak```
