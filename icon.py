import os
import re
import urllib.request
import json
import requests #install requests 
import itertools
from PIL import Image #install Pillow
from progress.bar import IncrementalBar #install progress
import shutil 

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

path=input("Enter the path (Replace \ with \\\): ")
list_folder=[f.name for f in os.scandir(path) if f.is_dir()]
list_folder_scr=list()
new_movies=list()
print(list_folder)
print('\n')
for i in list_folder:
    i=re.sub(r' \(.*?\)',r'',i) 
    i=re.sub(r' \[.*?\]',r'',i)
    i=i.replace(' ','+')
    list_folder_scr.append(i)

bar=IncrementalBar('Searching',max=len(list_folder))
for (query,i) in zip(list_folder_scr,list_folder):
    if not os.path.exists(path+'\\'+i+'\\'+i+'.jpg'):
        new_movies.append(i)
        url='http://www.omdbapi.com/?t=' +query+'&apikey=f365ed0'
        r=requests.get(url).json()
        parsed_data=json.dumps(r)
        load=json.loads(parsed_data)
        if load["Response"]=="True":
                if load["Poster"]!="N/A":
                        urlpic = (load["Poster"])
                        urllib.request.urlretrieve(urlpic,path+'\\'+i+'\\'+i+'.jpg')
    if os.path.exists(path+'\\'+i+'\\'+i+'.jpg'):
        img=Image.open(path+'\\'+i+'\\'+i+'.jpg')
        new_img=make_square(img)
        new_img.save(path+'\\'+i+'\\'+i+'_icon'+'.ico')
    bar.next()
bar.finish()

if not os.path.exists(path+"\\batch.bat"):
    shutil.copyfile("batch.bat",path+"\\batch.bat")
print("\nNew folders or did not got:")
print(new_movies)
print("\nNow run the 'batch.bat' file to change the icon of the folder.\n")
