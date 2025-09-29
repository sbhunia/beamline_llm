# SPEC macros for ID4B

## Adding other git repositories

Macros files that have their own git repositories can be added to this reposity
by using git sub-modules.  To added a reposity run the following command

`git submodule add <repository_url> <path>`

## Auto-commit

Un-commited changes to this reposity will by auto-commited and push to GitLab on
a regular basis.  To se e the when the schedule cron task is run type
`crontab -l`.
