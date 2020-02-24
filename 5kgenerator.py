import git
import json
import os
import regex as re
import requests
import subprocess
import shutil
import stat
import sys
import yaml

from git import Repo


# Parsing
cfg = None
with open('./config.yml', 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    

def main():
    setup()
    createRepositories()
    cloneRepos()
    themeSetup()
    cnames()
    ciConfig()
    git_push()
    if circle:
        followci()
        addci()
    if label:
        labelSetup()

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
runningInDocker = cfg['repo']['runningInDocker']
label = cfg['repo']['label']

def setup():
    os.system(f"git config --global ghi.token {key}")

#Create repos
def createRepositories():
    gthUrl = 'https://api.github.com/user/repos'
    headers = {'Authorization': 'token ' + key}
    repoPrivate  = "{ \"name\":\"" + domain + "\", \"private\": " + sourcePrivate + "  }"
    repoStage = "{ \"name\":\"stage." + domain + "\", \"private\": " + stagePrivate + " }"
    repoProd = "{ \"name\":\"www." + domain + "\", \"private\": " + prodPrivate + " }"

    #Create repos
    requests.post(gthUrl, headers=headers, data=repoPrivate)
    requests.post(gthUrl, headers=headers, data=repoStage)
    requests.post(gthUrl, headers=headers, data=repoProd)

#Clone repos and where to place them
def cloneRepos():
    path = cfg['repo']['path']
    os.chdir(path)
    mainRepo = f'git clone https://{key}@github.com/{user}/{domain}.git'
    templateRepo = f'git clone https://{key}@github.com/{templateUser}/{templateName}.git'
    os.system(mainRepo)
    os.system(templateRepo)
    if cfg["repo"]["theme"]:
        themeRepo = f"git clone https://{key}@github.com/{themeUser}/{themeName}.git"
        os.system(themeRepo)


def themeSetup():
    #Directories for template, theme and source repo
    source = "" + path + "/" + templateName + "/"
    if theme:
        src_dir = "" + path + "/" + themeName + "/"
    dest_dir = "" + path + "/" + domain +"/"

    #Move files from template into source folder
    files = os.listdir(source)
    print('merging template')
    for f in files:
        if f == ".git":
            continue
        shutil.move(source+f, dest_dir)
    if theme:
        move_over(src_dir, dest_dir)

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

def cnames():
    with open("" + path + "/" "" + domain + "/" "CNAME", "w+") as f:
        f.write("www." + domain + "")

    with open("" + path + "/" "" + domain + "/" "CNAME.stage", "w+") as f:
        f.write("stage." + domain + "")

#Change CI config
def ciConfig():
    with open(path + "/" + domain + "/.circleci/config.yml", 'r') as file:
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


#Add, commit and push template to source repo
def git_push():
    gitRepo = f'{path}/{domain}/'
    commitMSG = f'Copying {templateName} and {themeName} to {domain}'
    try:
        if runningInDocker:
            os.system(f"git config --global user.email {email} ")
            os.system(f"git config --global user.name \"automated setup\"")
            os.system(f"cd {domain} && git remote rm origin")
            os.system(f"cd {domain} && git remote add origin https://{user}:{key}@github.com/{user}/{domain}.git")
            os.system(f"cd {domain} && git add . && git commit -m \"{commitMSG}\" && git push origin master")
        else:
            repo = Repo(gitRepo)
            repo.git.add('--all')
            repo.git.commit('-m', '' + commitMSG + '')
            origin = repo.remote(name='origin')
            origin.push()
    except Exception as e:
        print('Some error occured while pushing the code')
        print(e)

def followci():
    url = f"https://circleci.com/api/v1.1/project/github/{user}/{domain}/follow?circle-token={citoken}"
    requests.post(url)
    print('following project')

def addci():
    if citoken != "":
        url = f"https://circleci.com/api/v1.1/project/github/{user}/{domain}/envvar?circle-token={citoken}"
        data = {
            "name": ciEnvName,
            "value": key
        }
        requests.post(url, data=data)
        print('project added to circle ci')
    else:
        print('skipped adding token to circle ci, please add manually')

def labelSetup():
    st = os.stat('rm-gh-defaults.sh')
    os.chmod('rm-gh-defaults.sh', st.st_mode | stat.S_IEXEC)
    st = os.stat('mk-phlow-defaults.sh')
    os.chmod('mk-phlow-defaults.sh', st.st_mode | stat.S_IEXEC)
    subprocess.call(f"{os.path.abspath(os.getcwd())}/rm-gh-defaults.sh", cwd=f"{path}/{domain}/")
    subprocess.call(f"{os.path.abspath(os.getcwd())}/mk-phlow-defaults.sh", cwd=f"{path}/{domain}/")

if __name__ == '__main__':
    main()