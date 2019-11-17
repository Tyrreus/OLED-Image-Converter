#!/usr/bin/env python3

from PIL import Image
import sys
import os

def PrintHelp():
    print("Usage: {:s} [image] [header_name]".format(sys.argv[0]))
    print("  image - is the name of the image which should be converted into the array")
    print("  header_name - is the name of the header - use without .h, just name")

def OpenImage(image_file_name):
    if not os.path.isfile(image_file_name):
        print("No such file: {:s}".format(image_file_name))
        exit(1)
    
    try:
        im = Image.open(image_file_name)
        if im.mode != "L":
            print("Wrong format: Image \"{:s}\" is not 8-byte B&W.)".format(image_file_name))
            im.close()
            exit(1)

        return im
    except:
        print("File \"{:s}\" is not an image!".format(image_file_name))
        exit(1)

def CloseImage(image):
    image.close()
    

def GenerateHeader(image):
    width, height = image.size
    pixel_values = list(im.getdata())
    
    c_img_array =  "#ifndef %s_h\n" % header_name
    c_img_array += "#define %s_h\n\n" % header_name
    c_img_array += "const int %sW = %d;\n" % (header_name, width)
    c_img_array += "const int %sH = %d;\n" % (header_name, height)
    c_img_array += "const char %sArr[] = { \n" % header_name
    c_img_array += "  "
    
    curr_val = 0
    curr_row= 0
    
    for byte in pixel_values:
        if curr_row > 80:
            c_img_array += "\n  "
            curr_row = 0
    
        if curr_val != (width * height) - 1:
            val_to_add = '{:3d}, '.format(byte)
            curr_row += len(val_to_add)
            c_img_array += val_to_add
        else:
            c_img_array += "%d };\n" % byte
        curr_val += 1
        curr_row += 1
    
    c_img_array += "\n#endif // %s_h\n" % header_name
    
    return c_img_array

def SaveHeaderToFile(header, file):
    if os.path.isfile(file):
       print("File \"{:s}\" already exists...".format(file))
       return
    else:
        header_file = open(header_name + ".h", "w")
        header_file.writelines(header)
        header_file.close()

# Application
arguments = len(sys.argv)
if arguments < 3:
    PrintHelp()
    exit (0)

image_file_name = sys.argv[1]
header_name = sys.argv[2]

im = OpenImage(image_file_name)
header = GenerateHeader(im)
SaveHeaderToFile(header, header_name + ".h")