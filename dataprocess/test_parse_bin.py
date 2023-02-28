import struct
import os
import threading

filepath = '../data_bin/acv1.bin'
binfile = open(filepath, 'rb')  # 打开二进制文件

# print(struct.calcsize("s"))
size = os.path.getsize(filepath)  # 获得文件大小
# to_file=open('./file1.txt','a+')
out = []
for i in range(size):
    data = binfile.read(1)  # 每次输出一个字节
    data, = struct.unpack('1s', data)
    print(data)
    out.append(data)
    # to_file.write(str(data[0]))
binfile.close()

