import zlib
import base64

data = open('demo1.txt','r').read()
data_bytes = bytes(data,'utf-8')
compressed_data = base64.b64encode(zlib.compress(data_bytes))
decoded_data = compressed_data.decode('utf-8')
compressed_file = open('compressed.txt','w')
compressed_file.write(decoded_data)


decompressed_data = zlib.decompress(base64.b64decode(compressed_data))
print(decompressed_data)






# with  open('demo1.txt','rb') as file:
#         data_bytes = file.read()

# compressed_data = base64.b64encode(zlib.compress(data_bytes,9))
# decoded_data = compressed_data.decode('utf-8')

# with open('compressed.txt','w') as compressed_file:
#         compressed_file.write(decoded_data)