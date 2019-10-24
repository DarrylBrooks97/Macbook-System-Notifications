import requests
import os
import time
import github_api_v3
import json
from pync import Notifier

git = github_api_v3
storedRepos = {}
tempRepos = {}
newfile = {}
oldfile = {}
repoNames = []

with open("config.json") as f:
    configuration = json.load(f)
    f.close()


def getRepos(repo, storedRepos):
    for i in repo:
        storedRepos.update({i['name']: i['updated_at']})
        if len(repoNames) < len(repo):
            repoNames.append(i['name'])
    with open("repos.json", 'r+') as k:
        k.write(str(storedRepos).replace("'", "\"").replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}"))
        k.close()


def incomingInfomation(repo):
    tempRepos = {}
    for i in repo:
        tempRepos.update({i['name']: i['updated_at']})
    with open("temp.json", "r+") as w:
        w.write(str(tempRepos).replace("'", "\"").replace(", ", ",\n").replace("{", "{\n").replace("}", "\n}"))
        w.close()


def updateChecker(oldfile, newfile):
    for i in repoNames:
        if oldfile[i] != newfile[i]:
            Notifier.notify("Repository Updated", title=i)
            Notifier.remove(os.getpid())
            Notifier.list(os.getpid())

        else:
            print("No updates have occurred")


url = "https://api.github.com/users/DarrylBrooks97/repos"

while 1:
    Data = git.request(method='GET', url=url, data=None)
    oldInfo = Data.json()
    getRepos(oldInfo, storedRepos)
    time.sleep(70)    # 2 minute intervals
    Data = git.request(method='GET', url=url, data=None)
    newInfo = Data.json()
    incomingInfomation(newInfo)
    with open('temp.json') as x:
        newfile = json.load(x)
        x.close()
    with open('repos.json') as y:
        oldfile = json.load(y)
        y.close()
    updateChecker(oldfile, newfile)



