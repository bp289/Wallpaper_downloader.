import requests

def WallpaperSearh(SearchQuery):
    url =  f"https://wallhave.cc/api/v1/search?={SearchQuery}"
    rData = requests.get(url) #grabs the REST api data. 
    json_data = rData.json() # returns a json object of the result.
    downloadLinks = []
    for item in json_data["data"]: # for each wallpaper(object) in the 'data' list 
        downloadLinks.append(item["path"])

    return downloadLinks #returns a list of wallpaper jpeg links

downloadURL = WallpaperSearh("anime")

for url in downloadURL:
    print(url)


