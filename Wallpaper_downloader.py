import requests
import string
import random
import os
import sys
import ctypes
import struct
import time
import threading

#global variables
Directory = ""
flag = ""

#functions
def DownloadImage(ImageUrl, Path):
    print("the current path is" + Path)
    rData = requests.get(ImageUrl) 
    ID = generateName()
    Ext = os.path.splitext(ImageUrl)[1] # gets the extension of the image bec ause os.path.splitext returns ('url" , 'extension')
    FilePath = f"{Path}{ID}{Ext}"
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
    DirInput = input("Please enter a directory to store wallpapers e.g E:\WallpaperDownloads: ")
    DirInput = f"{DirInput}\\"
    if not os.path.isdir(DirInput):
        sys.exit("Directory must exist")
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
        if os.path.isdir(Dir):
            print(f"Directory exists, curent directory => {Dir}")
            Directory = Dir
            Dir.close()
        else:
            print('Current directory does not exist')
            Mkdir()
            Dir.close()
    elif not os.path.exists("Dir.txt"):
        print("No directory saved")
        Mkdir()
        
def SearchCmd():
    global Directory
    SearchInput = input('Enter a search query e.g landscape (incude "_" for spaces e.g cute_dogs, only one space afer each word): ')
    SearchInput.replace('_','+')

    downloadURL = WallpaperSearh(SearchInput)

    for url in downloadURL:
        print(url)
        print('storing in Directory' + Directory )
        DownloadImage(url, Directory)

    print('Download complete')
    
def ChangeImage(is_64_, Cy_time, ImList):
    global flag
    while flag != "s": 
            Image = random.choice(ImList)
            if is_64_:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, Image, 3)
            else:
                ctypes.windll.user32.SystemParametersInfoA(20, 0, Image, 3)
            print(f'current image is {Image}, enter "s" to stop anytime')
            time.sleep(Cy_time)
            
def CheckInput():
    global flag
    flag = input()
                
def CycleWallpaper():
    global Directory
    ImageList = os.listdir(Directory)
    
    Cycle_time = input('How long between image change? (enter time in minutes): ')
    if not Cycle_time.isnumeric():
        sys.exit('please enter a numerical value')
    
    
    def is_64_bit():
        return struct.calcsize('P') * 8 == 64

    t1.start(is_64_bit(), Cycle_time, ImageList)
    t2.start()

#threads
t1 = threading.Thread(target=ChangeImage)  
t2 = threading.Thread(target=CheckInput) 
#main
print('Welcome to this wallpaper script, powered by the wallhave.cc api')
CheckDir()
cmd = input('Please enter a command ("search"/"wallpaper_cycle"/"change_directory"): ')
if cmd == 'search':
    SearchCmd()
elif cmd == 'wallpaper_cycle':
    CycleWallpaper()
elif cmd == 'change_directory':
    Mkdir()
    CheckDir()
    
    







