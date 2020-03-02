# 5kGenerator
This script is used to make 5k websites eaiser and faster.
It will create your three repositories (source, stage and prod), edit your circle ci config, create or edit CNAME files, add the project to circle ci and start pushing to your stage repository.
The script run in a docker container by using bash run.sh or you can run it manually but typing 5kGenerator.py

## Config file
The script relies on a config file that must be made manually. This is due to the config file containing info that should not be made public.
In the project you will find a template-config file. Feel free to copy this file and rename it to config.yml or create a new one using the template-config.yml file as a reference.

### Your config should contain the following
 - key: This is a github access token that is needed to create repositories
 - domain: This will be the name of your repositories as well as your cname files
 - sourcePrivate, stagePrivate, prodPrivate: These variables are using for setting your repository to either private or false. Remeber to use ' ' around them.
 - user: This variable is used to find your newely made github repo while also used to change the circle ci config.
 - email: Used for the circle ci config
 - path: By default this is set to /app for the docker container but if you are running this outside the docker container you can freely choose your own path to where files are stored.
 - templateUser, templateName: The script is created with the mindset of taking a jekyll theme and merging them together with our jekyll template. With the templateUser variable being used to point to the owner of the template and templateName for the repository name.
 - theme: This step is needed if you were to choose a template that already contains html and css that you wish to keep. true or false to run or skip this step.
 - themeuser and themeName: Like templateUser and templateName this is needed to find the owner and repository name of your wanted theme. If theme is set to false, ignore these.
 - circle: Similar to theme, this is asking if you wish to utilise the circle ci part of your script in a true or false format.
 - citoken: Like the key variable this is a token used for running circle ci. If the circle variable is set to false, ignore this part
 - cienvname: This variable is needed for circle ci
 - htmlproofer: Like theme and circle variables this can skip the htmlproofer part if needed by setting it to false. You may find that you want to skip the htmlproofer if using html made outside of prolike as there is no guarantee for it to meet the htmlproofer standards.
 - runninginDocker: Simple true or false depending on if you're running this script in a container or not.
 - label: We at prolike uses custom GitHub labels, if you wish to use these set the variable to true.

## How to use
 - Clone this repository
 - Be logged in as the right Github user, as well as on cirlcle ci
 - Generate a [personal access token](https://github.com/settings/tokens) with the same name as you want your repo to be named
 - Get or create a circle ci api [token](https://circleci.com/account/api)
 - In your terminal navigate to where you cloned the repo
 - Create a config.yml or copy the template-config.yml
 - Use the template-config.yml as a guide to fill out the config, but if you're using docker keep the path to /app and
   cienvname to PHLOW_GHTOKEN
 - Once done, type in bash run.sh in your terminal to run the script
 - Clone the newly made repo and start working on it!
 
### Notes
This script uses mk-phlow-defaults.sh and rm-gh-defaults.sh from [the-phlow](https://github.com/lakruzz/the-phlow)
