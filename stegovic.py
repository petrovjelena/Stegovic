import argparse
from argparse import ArgumentParser
from PIL import Image
import requests


def txt2bin(text): #converts text into binary
    bin = ''.join(format(ord(i), '08b') for i in text)
    return bin


def bin2txt(binary): #converts binary into text
    text = ""
    for i in range(0,len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text


def rgb2bin(rgb_tuple): #converts binary values to binary
    bin_val = []
    for colour in rgb_tuple:
        bin_val.append(format(colour, '08b'))
    return bin_val


def encode_text(cover_img, txt_msg, out_img):
    image = Image.open(cover_img)
    width, height = image.size
    pixel = image.load()

    if len(bin_msg) > width * height * 3: #image must be 3 times larger than text
        raise ValueError("Image not large enough. Please choose another image or reduce length of text.")

    txt_msg += "Stegovic" #delimiter so code recognises the end of the message
    index = 0

    bin_msg = txt2bin(txt_msg)
    data_len = len(bin_msg)
    for row in image:
        for pixel in row:
            r, g, b = rgb2bin(pixel)
            if index < len(bin_msg):
                pixel[0] = int(r[:-1] + bin_msg[index], 2) #LSB for red pixel
                index += 1

            if index < len(bin_msg):
                pixel[1] = int(g[:-1] + bin_msg[index], 2) #LSB for green pixel
                index += 1
                
            if index < len(bin_msg):
                pixel[2] = int(b[:-1] + bin_msg[index], 2) #LSB for blue pixel
                index += 1
                
            if index >= data_len: #once data is all encoded, finish
                break
        return image
    image.save(out_img)


def decode_text(enc_img):
    image = Image.open(enc_img)
    width, height = image.size
    pixel = image.load()

    bin_msg = ""
    for row in image:
        for pixel in row:
            r, g, b = rgb2bin(pixel)
            bin_msg += r[-1]
            bin_msg += g[-1]
            bin_msg += b[-1]

        decoded_text = ""
        pic_bytes = [bin_msg[i:i+8] for i in range(0, len(bin_msg), 8)]
        for byte in pic_bytes:
            decoded_text += chr(int(byte, 2))
            if decoded_text[-5:] == "Stegovic":
                return decoded_text[:-5]


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
    print("\n")
    parser = argparse.ArgumentParser(description = "Welcome to Stegovic- an image steganography tool.")
    subparsers = parser.add_subparsers(dest='command')

    parser_request = subparsers.add_parser("-e", "--encode", help="Select to encode your data", action="store_true")
    parser_request = subparsers.add_parser("-dtxt", "--decodetext", help="Select to retrieve text from an image", action="store_true")
    parser_request = subparsers.add_parser("-dimg", "--decodeimg", help="Select to retrieve image from an image", action="store_true")

    parser_request.add_argument("-c", "--cover", help="The path for the image that will carry the hidden data", dest="Cover")
    parser_request.add_argument("-i", "--image", help="The path for the image that will be hidden", dest="SecretImage")
    parser_request.add_argument("-m", "--message", help="The text that will be hidden", dest="Message")
    parser_request.add_argument("-a", "--encimg", help="The path to an encoded image for decoding", dest="EncodedImage")
    parser_request.add_argument("-o", "--output", help="Provide path for the output encoded image", dest="Output")
    
    args = parser.parse_args()
    
    cover_img = args.Cover
    scr_img = args.SecretImage
    txt_msg = args.Message
    enc_img = args.EncodedImage
    out_img = args.Output
    

    if args.command == 'encode':
        if txt_msg:
            encode_text(args.cover_img, args.txt_msg, args.out_img)
            print ("Your text has been encoded.")

        else: parser.print_help()


    if args.command == 'decodetext':
        decoded_text = decode_text(args.enc_img)
        print("Decoded text:", decoded_text)

    else: parser.print_help()

