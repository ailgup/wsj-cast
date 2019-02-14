from pydub import AudioSegment

import urllib3
urllib3.disable_warnings()
import os
import cloudinary.uploader
http = urllib3.PoolManager()
#Min Breifing,Tech News Breifing, Whats News,  Your Money
podcast_urls=['http://feeds.panoply.fm/WSJ7928321669?limit=1','http://feeds.panoply.fm/WSJ8523681216?limit=1','http://feeds.panoply.fm/WSJ4886593505?limit=1','http://feeds.panoply.fm/WSJ8175120842?limit=1']
filenames=[]

def getLink(url):
  try:
    r = http.request('GET', url)
    r = r.data.decode()
    r = (r.split("<enclosure url=\"")[1]).split("\"")[0]
  except:
    r = None
    
  return(r)
 
def downloadUrl(url,name):
  r = http.request('GET', url, preload_content=False)
  with open(name, 'wb') as out:
      while True:
          data = r.read()
          if not data:
              break
          out.write(data)
          filenames.append(name)
          print ("Downloaded "+name)
  r.release_conn()

def concat_files(source,dest):
  total_sound=AudioSegment.from_mp3(source[0])[30000:]
  for s in source[1:]:
    total_sound=total_sound+AudioSegment.from_mp3(s)[30000:]
  total_sound.export(dest, format="mp3")
  
for l in podcast_urls:
  url=getLink(l)
  if url:
    downloadUrl(url,str(podcast_urls.index(l))+".mp3")
concat_files(filenames,"pod_combo.mp3")
print("Made pod_combo.mp3")
for f in filenames:
  try:
    os.remove(f)
  except OSError:
      pass    
responce=cloudinary.uploader.upload("pod_combo.mp3", resource_type='raw')

print(responce[url].decode())
exit(1)
  
