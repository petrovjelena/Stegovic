from PIL import Image

def txt2bin(text): #converts text into 8 bit binary
    return ''.join(format(ord(i), '08b') for i in text)

def encode_text(cover_img, txt_msg, password, out_img):

    password = ""
    
    cover_img = Image.open(cover_img)
    width, height = cover_img.size

    if len(txt_msg) > width * height * 3: #image must be 3 times larger than text
        raise ValueError("Image not large enough. Please choose another image or reduce length of text.")
    else:
        print("\n\033[92m>>>Encoding\033[0m\n\033[92m>>>Please wait\033[0m\n")
        data_index=0
    
    txt_msg += password
    bin_msg = txt2bin(txt_msg)
    data_len = len(bin_msg)

    for x in range(width):
        for y in range(height):
            r, g, b = cover_img.getpixel((x,y))
    
            if data_len > data_index:
                r = (r & ~1 | int(bin_msg[data_index]))
                data_index += 1
            if data_len > data_index:
                g = (g & ~1 | int(bin_msg[data_index]))
                data_index += 1
            if data_len > data_index:
                b = (b & ~1 | int(bin_msg[data_index]))
                data_index += 1
    
            cover_img.putpixel((x,y), (r,g,b))
    
            if data_index >= data_len:
                break
                
    cover_img.save(out_img)
    print("Success- your encoded image has been saved.")


def decode_text(enc_img, password):

    print("\n\033[92m>>>Decoding\033[0m\n\033[92m>>>Please wait\033[0m\n")
    
    enc_img = Image.open(enc_img)
    width, height = enc_img.size
    
    bin_data = ""

    for x in range(width):
        for y in range(height):
            r, g, b = enc_img.getpixel((x,y))
            bin_data += f"{r & 1}"
            bin_data += f"{g & 1}"
            bin_data += f"{b & 1}"
    
    bits = [bin_data[i:i+8] for i in range(0, len(bin_data), 8)]
    
    dec_msg = ""
    for bit in bits:
        dec_msg += chr(int(bit, 2))
        p = len(password)
        if dec_msg[-p:] == password:
            break         
    
    if password in dec_msg:
        print("Decoded message: ", dec_msg[:-p])
    else:
        print("Wrong password entered. Please try again.")


def encode_image(cover_img, scr_img, out_img):
    
    
    
    cover_img = Image.open(cover_img)
    scr_img = Image.open(scr_img)

    if cover_img.size[0] < scr_img.size[0]:
        print("Cover image must be larger than secret image- please choose different image(s).")
    elif cover_img.size[1] < scr_img.size[1]:
        print("Cover image must be larger than secret image- please choose different image(s).")
    else:
        print("\n\033[92m>>>Encoding\033[0m\n\033[92m>>>Please wait\033[0m\n")

    
    s_w = scr_img.size[0]
    s_h = scr_img.size[1]
    
    c_pix = cover_img.load()
    s_pix = scr_img.load()

    for x in range(s_w):
        for y in range(s_h):
            r, g, b = c_pix[x, y]
            ra, rb, rc = s_pix[x, y]
            o_r = (r & ~1) | (ra >> 7)
            o_g = (g & ~1) | ((rb >> 7) & 1)
            o_b = (b & ~1) | ((rc >> 7) & 1)
            c_pix[x, y] = (o_r, o_g, o_b)

    cover_img.save(out_img)
    print("Success- your encoded image has been saved.")


def decode_image(enc_img, out_img):

    print("\n\033[92m>>>Decoding\033[0m\n\033[92m>>>Please wait\033[0m\n")
    
    enc_img = Image.open(enc_img)
    scr_img = Image.new("RGB", enc_img.size)

    e_pix = enc_img.load()
    s_pix = scr_img.load()

    e_w = enc_img.size[0]
    e_h = enc_img.size[1]

    for x in range(e_w):
        for y in range(e_h):
            r, g, b = e_pix[x, y]
            s_pix[x, y] = ((r & 1) << 7, (g & 1) << 7, (b & 1) << 7)

    scr_img.save(out_img)
    print("Success- the decoded image has been saved.") 


def banner():
    banner = """
   ___________________________ _    ____________
  / ___/_  __/ ____/ ____/ __ \ |  / /  _/ ____/
  \__ \ / / / __/ / / __/ / / / | / // // /     
 ___/ // / / /___/ /_/ / /_/ /| |/ // // /___   
/____//_/ /_____/\____/\____/ |___/___/\____/   
                                                """
    print(banner)

if __name__ == "__main__":
    banner()
    print("Welcome to Stegovic- an image steganography tool.")
    print("\n")
    print("Please select one of the following options:")
    print("   1: Hide text in image")
    print("   2: Hide image in image")
    print("   3: Reveal hidden text in an image")
    print("   4: Reveal hidden image in an image")

    func = input()

    if func == '1':
        print("Type path for cover image:")
        cover_img = input()
        print("Type your secret message:")
        txt_msg = input()
        print("Enter a password to protect the encoded data:")
        password = input()
        print("Type path of where you want the encoded image to be saved:")
        out_img = input()
        encode_text(cover_img, txt_msg, password, out_img)

    elif func == '2':
        print("Type path for cover image:")
        cover_img = input()
        print("Type path for image to hide:")
        scr_img = input()
        print("Type path of where you want the encoded image to be saved:")
        out_img = input()
        encode_image(cover_img, scr_img, out_img)

    elif func == '3':
        print("Type path for image to be decoded:")
        enc_img = input()
        print("Enter password:")
        password = input()
        decode_text(enc_img, password)

    elif func == '4':
        print("Type path for image to be decoded:")
        enc_img = input()
        print("Type path of where you want the decoded image to be saved:")
        out_img = input()
        decode_image(enc_img, out_img)

    else:
        print("Please select from one of the 4 options and enter the corresponding number.")
        
