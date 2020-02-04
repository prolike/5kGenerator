import configparser
import os
import subprocess
import git
from git import Repo
import sys
import shutil
import glob

#Parsing
config = configparser.ConfigParser()
config.read('./config.ini')

#Variables from .ini
key = config.get('repo', 'key')
domain = config.get('repo', 'domain')
sourcePrivate = config.get('repo', 'sourcePrivate')
stagePrivate = config.get('repo', 'stagePrivate')
prodPrivate = config.get('repo', 'prodPrivate')
templateUser = config.get('repo', 'templateUser')
templateName = config.get('repo', 'templateName')
themeUser = config.get('repo', 'themeUser')
themeName = config.get('repo', 'themeName')
user = config.get('repo', 'user')
path = config.get('repo', 'path')


# #Create repos
# source ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"" + domain + "\", \"private\": " + sourcePrivate + "  }' https://api.github.com/user/repos "
# stage ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"stage." + domain + "\", \"private\": " + stagePrivate + " }' https://api.github.com/user/repos "
# prod ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"www." + domain + "\", \"private\": " + prodPrivate + " }' https://api.github.com/user/repos "

# os.system(source)
# os.system(stage)
# os.system(prod)

# #Clone repos and where to place them
# path  = ""+ path +""
# repo = "git clone git@github.com:" + user + "/" + domain + ""
# temp = "git clone git@github.com:" + templateUser + "/" + templateName + ".git"
# them = "git clone git@github.com:" + themeUser + "/" + themeName + ".git"

# #os.system("sshpass -p your_password ssh user_name@your_localhost")
# os.chdir(path) # Specifying the path where the cloned project needs to be copied
# os.system(repo) # Cloning the source repo
# os.system(temp) # Cloning template repo
# os.system(them) # Cloning theme repo

# #Directories for template, theme and source repo
# source = "" + path + "/" + templateName + "/"
# src_dir = "" + path + "/" + themeName + "/"
# dest_dir = "" + path + "/" + domain +"/"

# #Move files from template into source folder
# files = os.listdir(source)
# print('merging template')
# for f in files:
#     if f == ".git":
#         continue
#     shutil.move(source+f, dest_dir)

# print('merging theme')
# #Move files from template into source folder
# def move_over(src_dir, dest_dir):
#     fileList = os.listdir(src_dir)
#     for i in fileList:
#         if i == ".git":
#             continue
#         src = os.path.join(src_dir, i)
#         dest = os.path.join(dest_dir, i)
#         if os.path.exists(dest):
#             if os.path.isdir(dest):
#                 move_over(src, dest)
#                 continue
#             else:
#                 os.remove(dest)
#         shutil.move(src, dest_dir)

# move_over(src_dir, dest_dir)



def CNAMES():
    f = open("" + path + "/" "" + domain + "/" "CNAME", "w+")
    f.write("www." + domain + "")
    f.close()

    f = open("" + path + "/" "" + domain + "/" "CNAME.stage", "w+")
    f.write("stage." + domain + "")
    f.close()

CNAMES()


#Add, commit and push template to source repo
gitRepo = "" + path + "/" + domain +"/"
commitMSG = 'theme + template'

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