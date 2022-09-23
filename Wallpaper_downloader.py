from requests import get
from string import ascii_lowercase
from random import choice
from os import path
from os import listdir
from sys import exit
from platform import architecture
from threading import Thread 
import ctypes
import time

class DirInfo:
    def Mkdir(self):
        DirInput = input("Please enter a directory to store wallpapers e.g E:\WallpaperDownloads: ")
        if not path.isdir(DirInput):
            exit("Directory must exist")
        else:
            DirFile = open("Dir.txt", "w")
            DirFile.write(DirInput)
            DirFile.close()
            self.GetDir()

    def GetDir(self):
        if path.exists("Dir.txt"):
            DirFile = open("Dir.txt", "r")
            Dir = DirFile.read()
            if path.isdir(Dir):
                print(f"Directory exists, current directory => {Dir}")
                self.Directory = Dir
            else:
                print('Current directory does not exist')
                self.Mkdir()
        elif not path.exists("Dir.txt"):
            print("No directory saved")
            self.Mkdir()
            
    @staticmethod           
    def CheckImgFile(imList):
        ValidFileTypes = ['.jpg', '.png', '.jpeg', '.jfif', '.pjpeg', '.pjp','.png','.webp']
        if len(imList) > 0:
            for file in imList:
                if path.splitext(file)[1] in ValidFileTypes:
                    return True
        else:
            return False
        
    def __init__(self):
        self.Directory = ''
        
class HandleDownloads:
    def DownloadImages(self):
        downloadURL = self.WallpaperSearh()

        for url in downloadURL:
            print(url + '\n' + 'downloading in Directory:' + self.Directory)
            self.DownloadFile(url, self.Directory)

        print('Download complete')
    
    def WallpaperSearh(self):
        url =  f"https://wallhaven.cc/api/v1/search?q={self.SearchQuery}"
        rData = get(url) #grabs the REST api data with a get request.
        JsonData = rData.json() # returns a json object of the result.
        downloadLinks = []
        for item in JsonData["data"]: # for each wallpaper(object) in the 'data' list 
            downloadLinks.append(item["path"])

        return downloadLinks #returns a list of wallpaper jpeg links
   
    @staticmethod
    def generateName():
        letters = ascii_lowercase
        result = 'Wallpaper_'
        for i in range(8):
            result += choice(letters)
        
        return result
    
    def DownloadFile(self,ImageUrl, Path):
        rData = get(ImageUrl) 
        ID = self.generateName()
        Ext = path.splitext(ImageUrl)[1] # gets the extension of the image bec ause os.path.splitext returns ('url" , 'extension')
        FilePath = f"{Path}\\{ID}{Ext}"
        open(FilePath, "wb").write(rData.content) 
    
    def __init__(self, Directory, SearchQuery):
        self.Directory = Directory
        self.SearchQuery = SearchQuery
         
class WallpaperChange:
    
    @staticmethod
    def is_64_bit():
        if architecture()[0] == '64bit':
            return True
        else:
            return False

              
    def ChangeImage(self):
        while self.flag != "s": 
            Image = choice(self.ImageList)
            Path = f'{self.Directory}\\{Image}'
            if self.is_64_ == True:
                print("is 64bit Windows")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, Path, 3)
            else:
                print("is 32bit Windows")
                ctypes.windll.user32.SystemParametersInfoA(20, 0, Path, 3)
                
            print(f'current image is {Image}, enter "s" to stop anytime')
            time.sleep(self.cycleTime)
       
    def CheckInput(self):
        self.flag = input()
        if self.flag == "s":
            print("wallpaper_cycle stopped.")
    
    def __init__(self,ImageList,cycleTime,Directory):
        self.flag = ''
        self.cycleTime = cycleTime
        self.ImageList = ImageList
        self.Directory = Directory
        self.is_64_ = WallpaperChange.is_64_bit()   
        self.t1 = Thread(target=self.ChangeImage) 
        self.t2 = Thread(target=self.CheckInput) 
    
    def CycleWallpaper(self):
        self.t1.start() #something wrong here
        self.t2.start()

class Main:
    DirInfo = DirInfo()
    
    @staticmethod
    def GetSearchInput():
        SearchInput = input('Enter a search query e.g landscape (incude "_" for spaces e.g cute_dogs, only one space after each word): ')
        SearchInput.replace(' ','+')
        return SearchInput
    
    @staticmethod
    def GetCycleTime():
        Cycle_time = input('How long between image change? (enter time in minutes): ')
        if not Cycle_time.isnumeric():
            exit('please enter a numerical value')
        else:
            Cycle_time = int(Cycle_time) * 60
            return Cycle_time
            
    def AskCmd(self): 
        cmd = input('Please enter a command ("search"/"wallpaper_cycle"/"change_directory"/"exit"): ')
        if cmd == 'search':
            self.DirInfo.GetDir()
            getImages = HandleDownloads(self.DirInfo.Directory,self.GetSearchInput())
            getImages.DownloadImages()
            self.AskCmd()
        elif cmd == 'wallpaper_cycle':
            self.DirInfo.GetDir()
            ImageList = listdir(self.DirInfo.Directory)
            HasFiles = self.DirInfo.CheckImgFile(ImageList)
            
            if  HasFiles == False:
                print('directory does not contain image files')
                self.AskCmd()
            else:
                print("cycling images in directory: " + self.DirInfo.Directory)
                wallCycle = WallpaperChange(ImageList, self.GetCycleTime(), self.DirInfo.Directory)
                wallCycle.CycleWallpaper()
                self.AskCmd() 
        elif cmd == 'change_directory':
            self.DirInfo.GetDir()
            self.DirInfo.Mkdir()
            self.AskCmd()
        elif cmd == 'exit':
            exit("Goodbie.")
        else:
            print('please enter a valid command')
            self.AskCmd()
            
#InitScript
print('Welcome')
Main = Main()
Main.AskCmd()



    
    







