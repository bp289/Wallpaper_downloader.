import requests
import string
import random
import os
import sys
import ctypes

#global variables
Directory = ''

#functions
def DownloadImage(ImageUrl, Path):
    print("the current path is" + Path)
    rData = requests.get(ImageUrl) 
    ID = generateName()
    Ext = os.path.splitext(ImageUrl)[1] # gets the extension of the image bec ause os.path.splitext returns ('url" , 'extension')
    FilePath = f"{Path}\{ID}{Ext}"
    open(FilePath, "wb").write(rData.content)

def generateName():
    letters = string.ascii_lowercase
    result = 'Wallpaper_'
    for i in range(8):
        result += random.choice(letters)
    
    return result

def WallpaperSearh(SearchQuery):
    url =  f"https://wallhaven.cc/api/v1/search?q={SearchQuery}"
    rData = requests.get(url) #grabs the REST api data with a get request.
    JsonData = rData.json() # returns a json object of the result.
    downloadLinks = []
    for item in JsonData["data"]: # for each wallpaper(object) in the 'data' list 
        downloadLinks.append(item["path"])

    return downloadLinks #returns a list of wallpaper jpeg links

def Mkdir():
    DirInput = input("please enter a directory to store wallpapers e.g E:\WallpaperDownloads :")
    if not os.path.isdir(DirInput):
        sys.exit("directory must exist")
    else:
        DirFile = open("Dir.txt", "w")
        DirFile.write(DirInput)
        DirFile.close()
        CheckDir()

def CheckDir():
    global Directory
    if os.path.exists("Dir.txt"):
        DirFile = open("Dir.txt", "r")
        Dir = DirFile.read()
        choice = input(f"Current Directory => {Dir}, would you like to change the directory? (enter 'y' to change)")
        if choice == "y":
            Mkdir()
        else:
            print(f'Storing in directory {Dir}')
            Directory = Dir 
    elif not os.path.exists("Dir.txt"):
        Mkdir()
        
        
#main
CheckDir()
SearchInput = input('Enter a search query e.g landscape (incude "_" for spaces e.g cute_dogs, only one space afer each word):')
SearchInput.replace('_','+')

downloadURL = WallpaperSearh(SearchInput)

for url in downloadURL:
    print(url)
    print('storing in Directory' + Directory )
    DownloadImage(url, Directory)

print('download complete')
    







