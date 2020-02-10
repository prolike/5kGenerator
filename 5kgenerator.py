import os
import subprocess
import git
from git import Repo
import sys
import shutil
import json
import yaml
import regex as re


#Parsing
file = open('./config.yml', 'r')
cfg = yaml.load(file, Loader=yaml.FullLoader)

#Variables from .yml
key = cfg['repo']['key']
domain = cfg['repo']['domain']
sourcePrivate = cfg['repo']['sourcePrivate']
stagePrivate = cfg['repo']['stagePrivate']
prodPrivate = cfg['repo']['prodPrivate']
templateUser = cfg['repo']['templateUser']
templateName = cfg['repo']['templateName']
themeUser = cfg['repo']['themeUser']
themeName = cfg['repo']['themeName']
user = cfg['repo']['user']
path = cfg['repo']['path']
email = cfg['repo']['email']


#Create repos
source ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"" + domain + "\", \"private\": " + sourcePrivate + "  }' https://api.github.com/user/repos "
stage ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"stage." + domain + "\", \"private\": " + stagePrivate + " }' https://api.github.com/user/repos "
prod ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"www." + domain + "\", \"private\": " + prodPrivate + " }' https://api.github.com/user/repos "

os.system(source)
os.system(stage)
os.system(prod)


#Clone repos and where to place them
path  = ""+ path +""
repo = "git clone git@github.com:" + user + "/" + domain + ""
temp = "git clone git@github.com:" + templateUser + "/" + templateName + ".git"
them = "git clone git@github.com:" + themeUser + "/" + themeName + ".git"

#os.system("sshpass -p your_password ssh user_name@your_localhost")
os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system(repo) # Cloning the source repo
os.system(temp) # Cloning template repo
os.system(them) # Cloning theme repo


#Directories for template, theme and source repo
source = "" + path + "/" + templateName + "/"
src_dir = "" + path + "/" + themeName + "/"
dest_dir = "" + path + "/" + domain +"/"


#Move files from template into source folder
files = os.listdir(source)
print('merging template')
for f in files:
    if f == ".git":
        continue
    shutil.move(source+f, dest_dir)

print('merging theme')
#Move files from template into source folder
def move_over(src_dir, dest_dir):
    fileList = os.listdir(src_dir)
    for i in fileList:
        if i == ".git":
            continue
        src = os.path.join(src_dir, i)
        dest = os.path.join(dest_dir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                move_over(src, dest)
                continue
            else:
                os.remove(dest)
        shutil.move(src, dest_dir)

move_over(src_dir, dest_dir)


#Change CNAME files
print('Creating CNAME files')
def CNAMES():
    f = open("" + path + "/" "" + domain + "/" "CNAME", "w+")
    f.write("www." + domain + "")
    f.close()

    f = open("" + path + "/" "" + domain + "/" "CNAME.stage", "w+")
    f.write("stage." + domain + "")
    f.close()

CNAMES()


#Change CI config
print('Changing Circle Ci files')
def ciConfig():

    with open("" + path + "/" "" + domain + "/.circleci/config.yml", 'r') as file:
        filedata = file.read()

        pattern = re.compile(r'(?<=stage-deploy:(\n.*){0,7}PLAY_TARGET_GH_REPO:\s+)\S+')
        filedata = re.sub(pattern, f'{user}/stage.{domain}', filedata)

        pattern = re.compile(r'(?<=stage-deploy:(\n.*){0,7}PLAY_USER_NAME:\s+)\S.*')
        filedata = re.sub(pattern, f'Circle CI by @{user}', filedata)

        pattern = re.compile(r'(?<=stage-deploy:(\n.*){0,7}PLAY_USER_EMAIL:\s+)\S+')
        filedata = re.sub(pattern, f'{email}', filedata)



        pattern = re.compile(r'(?<=prod-deploy:(\n.*){0,7}PLAY_TARGET_GH_REPO:\s+)\S+')
        filedata = re.sub(pattern, f'{user}/www.{domain}', filedata)

        pattern = re.compile(r'(?<=prod-deploy:(\n.*){0,7}PLAY_USER_NAME:\s+)\S.*')
        filedata = re.sub(pattern, f'Circle CI by @{user}', filedata)

        pattern = re.compile(r'(?<=prod-deploy:(\n.*){0,7}PLAY_USER_EMAIL:\s+)\S+')
        filedata = re.sub(pattern, f'{email}', filedata)

    with open("" + path + "/" "" + domain + "/.circleci/config.yml", 'w') as file:
        file.write(filedata)


ciConfig()


#Add, commit and push template to source repo
gitRepo = "" + path + "/" + domain +"/"
commitMSG = f'Copy {templateName} and {themeName} to {domain}'

def git_push():
    print('pushing to source repo')
    try:
        repo = Repo(gitRepo)
        repo.git.add('--all')
        repo.git.commit('-m', '' + commitMSG + '')
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')

git_push()