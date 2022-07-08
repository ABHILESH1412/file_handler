import os
from os.path import splitext, exists, join
import sys
import time
import logging
import shutil
from numpy import source
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

sourceDir = "C:/Users/sabhi/Downloads"
destVideoDir = "C:/Users/sabhi/Downloads/Videos"
destImageDir = "C:/Users/sabhi/Downloads/Images"
destZipDir = "C:/Users/sabhi/Downloads/zip files"
destPdfDir = "C:/Users/sabhi/Downloads/Pdfs"
destDocumentDir = "C:/Users/sabhi/Downloads/Documents"
destGifDir = "C:/Users/sabhi/Downloads/Images/Gifs"

def makeUnique(dest, name):
  filename, extension = splitext(name)
  counter = 1

  while exists(f"{dest}/{name}"):
      name = f"{filename}({str(counter)}){extension}"
      counter += 1

  return name

def move(dest, entry, name):
  fileExists = os.path.exists(dest + "/" + name)

  if fileExists:
    uniqueName = makeUnique(dest, name)
    oldName = join(dest, name)
    newName = join(dest, uniqueName)
    os.rename(oldName, newName)

  shutil.move(entry, dest)

class MoveHandler(LoggingEventHandler):
  def on_modified(self, event):
    with os.scandir(sourceDir) as entries:
      for entry in entries:
        name = entry.name
        dest = sourceDir
        
        # videos
        if name.lower().endswith(".mkv") or name.lower().endswith(".mp4") or name.lower().endswith(".avi") or name.lower().endswith(".mov"):
          dest = destVideoDir
          move(dest, entry, name)
        # images
        elif name.lower().endswith(".png") or name.lower().endswith(".jpg") or name.lower().endswith(".jpeg") or name.lower().endswith(".svg"):
          dest = destImageDir
          move(dest, entry, name)
        # gifs
        elif name.lower().endswith(".gif"):
          dest = destGifDir
          move(dest, entry, name)
        # zips
        elif name.lower().endswith(".zip"):
          dest = destZipDir
          move(dest, entry, name)
        # pdfs
        elif name.lower().endswith(".pdf"):
          dest = destPdfDir
          move(dest, entry, name)
        # documents
        elif(name.lower().endswith(".docx")):
          dest = destDocumentDir
          move(dest, entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sourceDir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()