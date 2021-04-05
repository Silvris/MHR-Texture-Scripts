from pathlib import Path
import os
from struct import pack, unpack

nativesPath = r"D:/MHRiseLogs/Final/re_chunk_000"
streamingPath = r"D:/MHRiseLogs/Final/re_chunk_000/natives/NSW/streaming/"

def writeFile(baseFile,streamFile,newFile):
    magic = baseFile.read(4)
    version = baseFile.read(4)#could convert, but its a constant so no need
    width = unpack('H',baseFile.read(2))[0]
    height = unpack('H',baseFile.read(2))[0]
    unkn00 = baseFile.read(2)
    imageCount = baseFile.read(1)
    baseFile.read(1)
    headerEnd = baseFile.read(24)#the rest of this doesn't need to be interpreted, as it should be the same as the main tex
    texture = streamFile.read()
    texSize = len(texture)
    #this should be all of the information needed for the texture
    newFile.write(magic)
    newFile.write(version)
    newFile.write(pack('H',width*2))
    newFile.write(pack('H',height*2))
    newFile.write(unkn00)
    newFile.write(imageCount)
    newFile.write(b'\x10')
    newFile.write(headerEnd)
    newFile.write(pack('Q',newFile.tell()+16))
    newFile.write(pack('I',texSize))
    newFile.write(pack('I',width*height))
    newFile.write(texture)


for path in Path(nativesPath).rglob("*.28"):
    #print(path)
    if "streaming" not in str(path): #make it only look at files not in streaming (and therefore with proper headers)
        postNswPath = str(path).split("NSW\\")[-1]
        if os.path.exists(streamingPath+postNswPath):
            print(path.stem)
            newPath = (streamingPath+"header\\"+postNswPath).split(path.stem)[0]
            os.makedirs(newPath,exist_ok=True)
            baseFile = open(path,'rb')
            streamFile = open(streamingPath+postNswPath,'rb')
            newFile = open(streamingPath+"header\\"+postNswPath,'wb')
            writeFile(baseFile,streamFile,newFile)
            baseFile.close()
            streamFile.close()
            newFile.close()