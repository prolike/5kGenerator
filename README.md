# 5kGenerator
This script is used to make 5k websites eaiser and faster.
It will create your three repositories (source, stage and prod), edit your circle ci config, create or edit CNAME files, add the project to circle ci and start pushing to your stage repository.
It requires [Docker](https://www.docker.com/) installed to run.

## How to use
 - Clone this repository
 - Be logged in as the right Github user, as well as on cirlcle ci
 - Generate a [personal access token](https://github.com/settings/tokens) with the same name as you want your repo to be named
 - Get or create a circle ci api [token](https://circleci.com/account/api)
 - In your terminal navigate to where you cloned the repo
 - Create a config.yml or copy the template-config.yml
 - Use the template-config.yml as a guide to fill out the config but set the path to /app and cienvname to PHLOW_GHTOKEN
 - Once done, type in bash run.sh in your terminal to run the script
 - Clone the newly made repo and start working on it!
 
### Notes
If you are using code from outside of prolike, like a jekyll theme, it is recommended to set the htmlproofer to false. This is due to using unkown code that is not guaranteed to be compliant with the htmlproofer.
This script uses mk-phlow-defaults.sh and rm-gh-defaults.sh from [the-phlow](https://github.com/lakruzz/the-phlow)
