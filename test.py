# from pyzbar.pyzbar import decode
# from PIL import Image
# import cv2
# import platform
import os
# d = decode(Image.open('abc.png'))

# print(platform.system()) #Linux Windows

# print('============================', d[0].data.decode('ascii'))
# def get_download_path():
#     """Returns the default downloads path for linux or windows"""
#     if os.name == 'nt':
#         import winreg
#         sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
#         downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
#         with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#             location = winreg.QueryValueEx(key, downloads_guid)[0]
#         return location
#     else:
#         return os.path.join(os.path.expanduser('~'), 'Downloads')

# print(get_download_path())
'id|q,id|q'
import json 
data = [
    {
        "id":"8",
        "storeName":"SHP",
        "itemName":"Pork Steak Mince 400g",
        "qx":1,
        "actualqx":"10"
    },{"id":"6",
        "storeName":"SHP",
        "itemName":"Mentos",
        "qx":1,
        "actualqx":"5"
    }
]

y = json.dumps(data) #convert to string
print(y)

z = json.loads(y) #convert to python list
print(type(z))

import qrtools

# import pyqrcode
# qr = pyqrcode.create(data) #saving data in qr code
# qr.png('abc.png', scale=8) #saving qrcode image