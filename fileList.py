import os
from datetime import timedelta, date

path="/data/backup"  # insert the path to the directory of interest


def findFile(dateday):
    str_dateday = str(dateday)
    str_dateday = str_dateday.replace("-", "")
    print "\t"+str_dateday
    dirList=os.listdir(path)
    for fname in dirList:
        if (fname.startswith(str_dateday) and fname.endswith("jpg")):
            print "\t\t"+fname
            

#findFile("20130913")

def findFromTo(start, end):
    d = date.today()
    td = timedelta(days=start)
    td2 = timedelta(days=end)
    
    dd = d+td
    
    while( dd < d+td2 ):
        print dd
        findFile(dd)
        dd = dd+timedelta(days=1)


findFromTo(-10, 0)