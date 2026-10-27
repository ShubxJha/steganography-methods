#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
from itertools import islice


# In[2]:


def txt_encode(text):
    l=len(text)
    i=0
    add=''
    while i<l:
        t=ord(text[i])
        if(t>=32 and t<=64):
            t1=t+48
            t2=t1^170       #170: 10101010
            res = bin(t2)[2:].zfill(8)
            add+="0011"+res
        
        else:
            t1=t-48
            t2=t1^170
            res = bin(t2)[2:].zfill(8)
            add+="0110"+res
        i+=1
    res1=add+"111111111111"
    print("The string after binary conversion appyling all the transformation :- " + (res1))   
    length = len(res1)
    print("Length of binary after conversion:- ",length)
    HM_SK=""
    ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}      
    file1 = open("Sample_cover_files/cover_text.txt","r+")
    nameoffile = input("\nEnter the name of the Stego file after Encoding(with extension):- ")
    file3= open(nameoffile,"w+", encoding="utf-8")
    word=[]
    for line in file1: 
        word+=line.split()
    i=0
    while(i<len(res1)):  
        s=word[int(i/12)]
        j=0
        x=""
        HM_SK=""
        while(j<12):
            x=res1[j+i]+res1[i+j+1]
            HM_SK+=ZWC[x]
            j+=2
        s1=s+HM_SK
        file3.write(s1)
        file3.write(" ")
        i+=12
    t=int(len(res1)/12)     
    while t<len(word): 
        file3.write(word[t])
        file3.write(" ")
        t+=1
    file3.close()  
    file1.close()
    print("\nStego file has successfully generated")


# In[3]:


def encode_txt_data():
    count2=0
    file1 = open("Sample_cover_files/cover_text.txt","r")
    for line in file1: 
        for word in line.split():
            count2=count2+1
    file1.close()       
    bt=int(count2)
    print("Maximum number of words that can be inserted :- ",int(bt/6))
    text1=input("\nEnter data to be encoded:- ")
    l=len(text1)
    if(l<=bt):
        print("\nInputed message can be hidden in the cover file\n")
        txt_encode(text1)
    else:
        print("\nString is too big please reduce string size")
        encode_txt_data()


# In[4]:


def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


# In[5]:


def decode_txt_data():
    ZWC_reverse={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}
    stego=input("\nPlease enter the stego file name(with extension) to decode the message:- ")
    file4= open(stego,"r", encoding="utf-8")
    temp=''
    for line in file4: 
        for words in line.split():
            T1=words
            binary_extract=""
            for letter in T1:
                if(letter in ZWC_reverse):
                     binary_extract+=ZWC_reverse[letter]
            if binary_extract=="111111111111":
                break
            else:
                temp+=binary_extract
    print("\nEncrypted message presented in code bits:",temp) 
    lengthd = len(temp)
    print("\nLength of encoded bits:- ",lengthd)
    i=0
    a=0
    b=4
    c=4
    d=12
    final=''
    while i<len(temp):
        t3=temp[a:b]
        a+=12
        b+=12
        i+=12
        t4=temp[c:d]
        c+=12
        d+=12
        if(t3=='0110'):
            decimal_data = BinaryToDecimal(t4)
            final+=chr((decimal_data ^ 170) + 48)
        elif(t3=='0011'):
            decimal_data = BinaryToDecimal(t4)
            final+=chr((decimal_data ^ 170) - 48)
    print("\nMessage after decoding from the stego file:- ",final)


# In[6]:


def txt_steg():
    while True:
        print("\n\t\tTEXT STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            encode_txt_data()
        elif choice1 == 2:
            decrypted=decode_txt_data() 
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[7]:


def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result


# In[8]:


_BPCS_BLOCK_SIZE = 8
_BPCS_COMPLEXITY_THRESHOLD = 0.3
_BPCS_MAGIC = b"BPCS1"
_BPCS_CHECKERBOARD = np.indices((_BPCS_BLOCK_SIZE, _BPCS_BLOCK_SIZE)).sum(axis=0) % 2


def _bpcs_carrier_blocks(img):
    """Yield full 8x8 blocks in each channel bit-plane."""
    height, width, channels = img.shape
    for channel in range(channels):
        for bit_plane in range(8):
            for top in range(0, height - 7, 8):
                for left in range(0, width - 7, 8):
                    yield channel, bit_plane, top, left


def _bpcs_block_count(img):
    height, width, channels = img.shape
    return channels * 8 * (height // 8) * (width // 8)


def _bpcs_read_block(img, location):
    channel, bit_plane, top, left = location
    pixels = img[top:top + 8, left:left + 8, channel]
    return ((pixels >> bit_plane) & 1).astype(np.uint8)


def _bpcs_write_block(img, location, block):
    channel, bit_plane, top, left = location
    pixels = img[top:top + 8, left:left + 8, channel]
    mask = np.uint8(1 << bit_plane)
    img[top:top + 8, left:left + 8, channel] = (
        (pixels & np.uint8(255 ^ int(mask))) | (block.astype(np.uint8) * mask)
    )


def _bpcs_complexity(block):
    transformed = block ^ _BPCS_CHECKERBOARD
    transitions = np.count_nonzero(transformed[:, 1:] != transformed[:, :-1])
    transitions += np.count_nonzero(transformed[1:, :] != transformed[:-1, :])
    return transitions / 112.0


def _bits_to_bytes(bits):
    if len(bits) % 8:
        bits += "0" * (8 - len(bits) % 8)
    return bytes(int(bits[index:index + 8], 2) for index in range(0, len(bits), 8))


def encode_img_data(img):
    message = input("\nEnter the data to be Encoded in Image :")
    if not message:
        raise ValueError("Data entered to be encoded is empty")
    output_name = input("\nEnter the name of the New Image (PNG or BMP): ").strip()
    if not output_name.lower().endswith((".png", ".bmp")):
        raise ValueError("BPCS output must use a lossless .png or .bmp extension")

    payload = message.encode("utf-8") + b"*^*^*"
    payload_bits = "".join(format(byte, "08b") for byte in payload)
    data_block_count = (len(payload_bits) + 63) // 64
    flags_size = (data_block_count + 7) // 8
    header_size = len(_BPCS_MAGIC) + 8 + flags_size
    header_block_count = (header_size * 8 + 63) // 64
    available_blocks = _bpcs_block_count(img)
    required_blocks = header_block_count + data_block_count
    if required_blocks > available_blocks:
        raise ValueError(
            f"Message is too large: BPCS needs {required_blocks} blocks, "
            f"but this image has {available_blocks}."
        )
    locations = list(islice(_bpcs_carrier_blocks(img), required_blocks))

    flags = []
    encoded_blocks = []
    for index in range(data_block_count):
        bits = payload_bits[index * 64:(index + 1) * 64].ljust(64, "0")
        block = np.fromiter((int(bit) for bit in bits), dtype=np.uint8).reshape((8, 8))
        transformed = block ^ _BPCS_CHECKERBOARD
        conjugated = _bpcs_complexity(transformed) < _BPCS_COMPLEXITY_THRESHOLD
        if conjugated:
            transformed = 1 - transformed
        flags.append(conjugated)
        encoded_blocks.append(transformed ^ _BPCS_CHECKERBOARD)

    conjugation_map = bytearray(flags_size)
    for index, conjugated in enumerate(flags):
        if conjugated:
            conjugation_map[index // 8] |= 1 << (7 - index % 8)
    header = _BPCS_MAGIC + len(payload).to_bytes(8, "big") + bytes(conjugation_map)
    header_bits = "".join(format(byte, "08b") for byte in header)
    for index in range(header_block_count):
        bits = header_bits[index * 64:(index + 1) * 64].ljust(64, "0")
        block = np.fromiter((int(bit) for bit in bits), dtype=np.uint8).reshape((8, 8))
        _bpcs_write_block(img, locations[index], block)
    for index, block in enumerate(encoded_blocks):
        _bpcs_write_block(img, locations[header_block_count + index], block)

    if not cv2.imwrite(output_name, img):
        raise OSError(f"Could not write image: {output_name}")
    print(f"Encoded the data with BPCS and saved the image as {output_name}")


def decode_img_data(img):
    if _bpcs_block_count(img) < 2:
        raise ValueError("Image is too small to contain a BPCS message")
    prefix_locations = list(islice(_bpcs_carrier_blocks(img), 2))
    prefix_bits = "".join(
        str(bit) for location in prefix_locations
        for bit in _bpcs_read_block(img, location).flat
    )
    prefix = _bits_to_bytes(prefix_bits)[:13]
    if not prefix.startswith(_BPCS_MAGIC):
        raise ValueError("No BPCS message header found in this image")
    payload_length = int.from_bytes(prefix[5:13], "big")
    if payload_length < 5:
        raise ValueError("Invalid BPCS message length")
    payload_block_count = (payload_length * 8 + 63) // 64
    flags_size = (payload_block_count + 7) // 8
    header_size = len(_BPCS_MAGIC) + 8 + flags_size
    header_block_count = (header_size * 8 + 63) // 64
    required_blocks = header_block_count + payload_block_count
    if required_blocks > _bpcs_block_count(img):
        raise ValueError("BPCS header declares data beyond the image capacity")
    locations = list(islice(_bpcs_carrier_blocks(img), required_blocks))

    header_bits = "".join(
        str(bit) for location in locations[:header_block_count]
        for bit in _bpcs_read_block(img, location).flat
    )
    header = _bits_to_bytes(header_bits)[:header_size]
    conjugation_map = header[13:]
    payload_bits = ""
    for index in range(payload_block_count):
        block = _bpcs_read_block(img, locations[header_block_count + index])
        transformed = block ^ _BPCS_CHECKERBOARD
        conjugated = bool(conjugation_map[index // 8] & (1 << (7 - index % 8)))
        if conjugated:
            transformed = 1 - transformed
        payload_bits += "".join(str(bit) for bit in (transformed ^ _BPCS_CHECKERBOARD).flat)

    payload = _bits_to_bytes(payload_bits)[:payload_length]
    if not payload.endswith(b"*^*^*"):
        raise ValueError("BPCS payload marker is missing; the image may be damaged")
    try:
        message = payload[:-5].decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("BPCS payload is not valid UTF-8; the image may be damaged") from error
    print("\nThe Encoded data which was hidden in the Image was :--  ", message)


# In[10]:


def img_steg():
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS\n") 
        print("1. Encode the Text message") 
        print("2. Decode the Text message") 
        print("3. Exit")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1:
            image=cv2.imread("Sample_cover_files/cover_image.jpg")
            if image is None:
                raise ValueError("Could not read Sample_cover_files/cover_image.jpg")
            encode_img_data(image)
        elif choice1 == 2:
            image1=cv2.imread(input("Enter the Image you need to Decode to get the Secret message :  "))
            if image1 is None:
                raise ValueError("Could not read the selected image")
            decode_img_data(image1)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[11]:


def encode_aud_data():
    import wave

    nameoffile=input("Enter name of the file (with extension) :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    data = input("\nEnter the secret message :- ")

    res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))     
    print("\nThe string after binary conversion :- " + (res))   
    length = len(res)
    print("\nLength of binary after conversion :- ",length)

    data = data + '*^*^*'

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0,len(result),1): 
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4]== result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1
    
    frame_modified = bytes(frame_bytes)

    stegofile=input("\nEnter name of the stego file (with extension) :- ")
    with wave.open(stegofile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    print("\nEncoded the data successfully in the audio file.")    
    song.close()


# In[12]:


def decode_aud_data():
    import wave

    nameoffile=input("Enter name of the file to be decoded :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    extracted = ""
    p=0
    for i in range(len(frame_bytes)):
        if(p==1):
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2]==0:
            extracted+=res[len(res)-4]
        else:
            extracted+=res[len(res)-1]
    
        all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was :--",decoded_data[:-5])
                p=1
                break  


# In[13]:


def aud_steg():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            encode_aud_data()
        elif choice1 == 2:
            decode_aud_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[14]:


def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S


# In[15]:


def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key


# In[16]:


def preparing_key_array(s):
    return [ord(c) for c in s]


# In[17]:


def encryption(plaintext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext


# In[18]:


def decryption(ciphertext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext


# In[19]:


def embed(frame):
    data=input("\nEnter the data to be Encoded in Video :") 
    data=encryption(data)
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame


# In[20]:


def extract(frame):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return 


# In[21]:


def encode_vid_data():
    cap=cv2.VideoCapture("Sample_cover_files/cover_video.mp4")
    vidcap = cv2.VideoCapture("Sample_cover_files/cover_video.mp4")    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter('stego_video.mp4',fourcc, 25.0, size)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the frame number where you want to embed data : ")
    n=int(input())
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)
    
    print("\nEncoded the data successfully in the video file.")
    return frame_


# In[22]:


def decode_vid_data(frame_):
    cap = cv2.VideoCapture('stego_video.mp4')
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n=int(input())
    vidcap = cv2.VideoCapture('stego_video.mp4')
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            extract(frame_)
            return


# In[23]:


def vid_steg():
    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            a=encode_vid_data()
        elif choice1 == 2:
            decode_vid_data(a)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[24]:


def main():
    print("\t\t      STEGANOGRAPHY")   
    while True:  
        print("\n\t\t\tMAIN MENU\n")  
        print("1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}")  
        print("2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}")  
        print("3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}")
        print("4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}")
        print("5. Exit\n")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1: 
            img_steg()
        elif choice1 == 2:
            txt_steg()
        elif choice1 == 3:
            aud_steg()
        elif choice1 == 4:
            vid_steg()
        elif choice1 == 5:
            break
        else:
            print("Incorrect Choice")
        print("\n\n")


# In[27]:


if __name__ == "__main__":
    main()


# In[ ]:




