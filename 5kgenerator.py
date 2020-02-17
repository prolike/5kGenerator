import os
import subprocess
import git
from git import Repo
import sys
import shutil
import json
import yaml
import regex as re
import requests
import stat


# Parsing
file = open('./config.yml', 'r')
cfg = yaml.load(file, Loader=yaml.FullLoader)

# Variables from .yml
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
citoken = cfg['repo']['citoken']
ciEnvName = cfg['repo']['cienvname']
htmlproofer = cfg['repo']['htmlproofer']
theme = cfg['repo']['theme']
circle = cfg['repo']['circle']




#Create repos
source ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"" + domain + "\", \"private\": " + sourcePrivate + "  }' https://api.github.com/user/repos "
stage ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"stage." + domain + "\", \"private\": " + stagePrivate + " }' https://api.github.com/user/repos "
prod ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"www." + domain + "\", \"private\": " + prodPrivate + " }' https://api.github.com/user/repos "

os.system(source)
os.system(stage)
os.system(prod)

os.system(f"git config --global ghi.token {key}")

#Clone repos and where to place them
path  = ""+ path +""
print(path)
repo = "git clone https://" + key + "@github.com/" + user + "/" + domain + ".git"
temp = "git clone https://" + key + "@github.com/" + templateUser + "/" + templateName + ".git"
if theme:
    them = "git clone https://" + key + "@github.com/" + themeUser + "/" + themeName + ".git"

print(repo)
print(temp)

#os.system("sshpass -p your_password ssh user_name@your_localhost")
os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system(repo) # Cloning the source repo
os.system(temp) # Cloning template repo
if theme:
    os.system(them) # Cloning theme repo


#Directories for template, theme and source repo
source = "" + path + "/" + templateName + "/"
if theme:
    src_dir = "" + path + "/" + themeName + "/"
dest_dir = "" + path + "/" + domain +"/"


#Move files from template into source folder
print(os.listdir(path))
files = os.listdir(source)
print('merging template')
for f in files:
    if f == ".git":
        continue
    shutil.move(source+f, dest_dir)

if theme:

    print('merging theme')
    #Move files from template into source folder
    def move_over(src_dir, dest_dir):
        fileList = os.listdir(src_dir)
        for i in fileList:
            if i == ".git" or i.endswith(".gemspec") or i == "Gemfile":
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

        if htmlproofer != True:
            print('skipping html proofer')
            pattern = re.compile(r'(?<=deliver:.*(\n.*){0,50}requires:.*(\n.*){0,7}\s+)- html-proofer')
            filedata = re.sub(pattern, f'#- html-proofer', filedata)


        pattern = re.compile(r'(?<=prod-deploy:(\n.*){0,7}PLAY_TARGET_GH_REPO:\s+)\S+')
        filedata = re.sub(pattern, f'{user}/www.{domain}', filedata)

        pattern = re.compile(r'(?<=prod-deploy:(\n.*){0,7}PLAY_USER_NAME:\s+)\S.*')
        filedata = re.sub(pattern, f'Circle CI by @{user}', filedata)

        pattern = re.compile(r'(?<=prod-deploy:(\n.*){0,7}PLAY_USER_EMAIL:\s+)\S+')
        filedata = re.sub(pattern, f'{email}', filedata)

        pattern = re.compile(r'(?<=jekyll-build:(\n.*){0,7}image:\s+)\S+')
        filedata = re.sub(pattern, f'carolineolivia94/jekyll-plus-plus', filedata)


    with open("" + path + "/" "" + domain + "/.circleci/config.yml", 'w') as file:
        file.write(filedata)

ciConfig()


#Add, commit and push template to source repo
if circle == True:
    gitRepo = "" + path + "/" + domain +"/"
    commitMSG = f'Copy {templateName} and {themeName} to {domain}'

    def git_push():
        print('pushing to source repo')
        try:
            os.system(f"git config --global user.email {email} ")
            os.system(f"git config --global user.name \"automated setup\" ")
            ##os.system(f"cd {domain} && git push --set-upstream origin master")
            os.system(f"cd {domain} && pwd")
            os.system("pwd")
            os.system(f"cd {domain} && git remote rm origin")
            os.system(f"cd {domain} && git remote add origin https://{user}:{key}@github.com/{user}/{domain}.git")
            os.system(f"cd {domain} && git add . && git commit -m \"{commitMSG}\" && git push origin master")
            # repo = Repo(gitRepo)
            # repo.git.add('--all')
            # repo.git.commit('-m', '' + commitMSG + '')
            # origin = repo.remote(name='origin')
            # origin.push()
        except:
            print('Some error occured while pushing the code')

    git_push()

if circle == True:
    def followci():
        url = f"https://circleci.com/api/v1.1/project/github/{user}/{domain}/follow?circle-token={citoken}"
        resp = requests.post(url)
        print('following project')

    followci()

    def addci():
        if citoken != "":
            url = f"https://circleci.com/api/v1.1/project/github/{user}/{domain}/envvar?circle-token={citoken}"
            data = {
            "name": ciEnvName,
            "value": key
            }
            resp = requests.post(url, data=data)
            print('project added to circle ci')
        else:
            print('skipped adding token to circle ci, please add manually')

    addci()

st = os.stat('rm-gh-defaults.sh')
os.chmod('rm-gh-defaults.sh', st.st_mode | stat.S_IEXEC)

st = os.stat('mk-phlow-defaults.sh')
os.chmod('mk-phlow-defaults.sh', st.st_mode | stat.S_IEXEC)


print(os.path.abspath(os.getcwd()))
subprocess.call(f"{os.path.abspath(os.getcwd())}/rm-gh-defaults.sh", cwd=f"{path}/{domain}/")
subprocess.call(f"{os.path.abspath(os.getcwd())}/mk-phlow-defaults.sh", cwd=f"{path}/{domain}/")