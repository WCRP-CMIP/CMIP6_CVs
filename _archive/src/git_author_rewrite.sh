#!/bin/sh

# PJD 11 Jul 2016   - See https://help.github.com/articles/changing-author-info/

git filter-branch --env-filter '
OLD_EMAIL="doutriaux1@llnl.gov"
CORRECT_NAME="Paul J. Durack"
CORRECT_EMAIL="durack1@llnl.gov"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
