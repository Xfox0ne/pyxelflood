import socket
import threading
from PIL import Image

HOST = 'box.pixel-competition.de'
PORT = 2342

xoffset = int(input("X Offset: "))
yoffset = int(input("Y Offset: "))
threadcount = int(input("Threads: "))

im = Image.open('image.jpg')
rgb_im = im.convert('RGB')
width = rgb_im.size[0]
heigth = rgb_im.size[1]

def pixel(command):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  send = sock.send

  send(b'%s' %(command))

stringList = []

for i in range(0, width):
  stringX = ""
  for j in range(0, heigth):
      r, g, b = rgb_im.getpixel((i, j))
      stringX.join('PX %d %d %02x%02x%02x\n' % (i,j,r,g,b))
  stringList.append(stringX)

currentText = 0

while True:
  threadList = []

  for i in range(0, threadcount):
    t = threading.Thread(target=pixel, args=stringList[currentText], daemon=True)
    t.start()
    threadList.append(t)
    currentText += 1

  for thread in threadList:
    thread.join()
