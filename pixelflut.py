import socket
import threading
from PIL import Image

HOST = ''
PORT = 1234

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
  while True:
    send(bytes(command, 'utf-8'))

stringList = []

for x in range(0, threadcount):
  stringList.append("")

x = 0
for i in range(0, width):
  for j in range(0, heigth):
      r, g, b = rgb_im.getpixel((i, j))
      stringX = ('PX %d %d %02x%02x%02x\n' % (i,j,r,g,b))
      stringList[x] += stringX
      x += 1
      if(x >= threadcount):
        x = 0

threadList = []
print(stringList[0])
for x in range(0, threadcount):
  t = threading.Thread(target=pixel, args=(stringList[x], ), daemon=True)
  t.start()
  threadList.append(t)

for thread in threadList:
  thread.join()
