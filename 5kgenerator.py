import configparser
import os
import subprocess
import git
from git import Repo
import sys

config = configparser.ConfigParser()
config.read('./config.ini')

key = config.get('repo', 'key')
name = config.get('repo', 'name')
sourcePrivate = config.get('repo', 'sourcePrivate')
stagePrivate = config.get('repo', 'stagePrivate')
prodPrivate = config.get('repo', 'prodPrivate')
template = config.get('repo', 'template')
theme = config.get('repo', 'theme')
user = config.get('repo', 'user')
path = config.get('repo', 'path')

print (key)


#source ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"" + name + "\", \"private\": " + sourcePrivate + "  }' https://api.github.com/user/repos "

#stage ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"stage." + name + "\", \"private\": " + stagePrivate + " }' https://api.github.com/user/repos "

#prod ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"prod-" + name + "\", \"private\": " + prodPrivate + " }' https://api.github.com/user/repos "


path  = ""+ path +""
repo = "git clone git@github.com:" + user + "/" + name + ""
temp = "git clone git@github.com:" + template + ""
them = "git clone git@github.com:" + theme + ""

os.system("sshpass -p your_password ssh user_name@your_localhost")
os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system(repo) # Cloning the source repo
os.system(temp) # Cloning template repo
os.system(them) # Cloning theme repo


#os.system(source)
#os.system(stage)
#os.system(prod)