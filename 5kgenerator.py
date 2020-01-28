import configparser
import os

config = configparser.ConfigParser()
config.read('./config.ini')

key = config.get('repo', 'key')
name = config.get('repo', 'name')
sourcePrivate = config.get('repo', 'sourcePrivate')
stagePrivate = config.get('repo', 'stagePrivate')
prodPrivate = config.get('repo', 'prodPrivate')


print (key)

source ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"" + name + "\", \"private\": " + sourcePrivate + "  }' https://api.github.com/user/repos "

stage ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"stage." + name + "\", \"private\": " + stagePrivate + " }' https://api.github.com/user/repos "

prod ="curl -i -H 'Authorization: token " + key + " ' -d '{ \"name\":\"prod-" + name + "\", \"private\": " + prodPrivate + " }' https://api.github.com/user/repos "

os.system(source)
os.system(stage)
os.system(prod)