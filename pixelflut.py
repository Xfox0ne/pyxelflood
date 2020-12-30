import socket
import threading
from PIL import Image

HOST = '127.0.0.1'
PORT = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
send = sock.send

xoffset = int(input("X Offset: "))
yoffset = int(input("Y Offset: "))

xmotion = int(input("X Motion: "))
ymotion = int(input("Y Motion: "))

im = Image.open('image.jpg')
rgb_im = im.convert('RGB')
width = rgb_im.size[0]
heigth = rgb_im.size[1]

def pixel(x,y,r,g,b,a=255):
  if a == 255:
    send(b'PX %d %d %02x%02x%02x\n' % (x,y,r,g,b))
  else:
    send(b'PX %d %d %02x%02x%02x%02x\n' % (x,y,r,g,b,a))

threadList = []

for i in range(0, width):
    for j in range(0, heigth):
        r, g, b = rgb_im.getpixel((i, j))
        x = threading.Thread(target=pixel, args=(i + xoffset, j + yoffset, r, g, b), daemon=True)
        x.start()
        threadList.append(x)

while True:
    for thread in threadList:
      thread.join()
