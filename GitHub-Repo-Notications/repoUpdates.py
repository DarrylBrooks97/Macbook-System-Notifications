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
        if oldfile[i] == newfile[i]:
            Notifier.notify("Repository Updated", title=i)
            Notifier.remove(os.getpid())
            Notifier.list(os.getpid())
            with open("repos.json", "w") as r:     #Erases content in file
                r.close()
            with open("repos.json", "w") as n:
                n.write("{\n")
                for i in newfile:
                    n.write("\""+i+"\": ")               # Re writes file with updated repos
                    n.write("\""+newfile[i]+"\" ")
                n.write("\n}")
                n.close()
                exit()
            break
        else:
            print("No updates have occurred")


url = "https://api.github.com/users/DarrylBrooks97/repos"


# Checks to see if file is empty
if os.stat("repos.json").st_size == 0:
    Data = git.request(method='GET', url=url, data=None)
    oldInfo = Data.json()
    getRepos(oldInfo, storedRepos)

time.sleep(10)  # 2 minute intervals

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
exit()



