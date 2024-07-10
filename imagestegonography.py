from PIL import Image

def hide_text_in_image(image_path, secret_text, output_image_path):
    img = Image.open(image_path)
    pixels = img.load()
    
    binary_secret_text = ''.join(format(ord(char), '08b') for char in secret_text)
    binary_secret_text += '1111111111111110' 
    
    max_bytes = img.width * img.height * 3 // 8
    if len(binary_secret_text) > max_bytes:
        raise ValueError("Text too large to be encoded in the image")
    
    index = 0
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            if index < len(binary_secret_text):
               
                img.putpixel((x, y), (r & ~1 | int(binary_secret_text[index]), 
                                      g & ~1 | int(binary_secret_text[index + 1]), 
                                      b & ~1 | int(binary_secret_text[index + 2])))
                index += 3
            else:
                img.putpixel((x, y), (r, g, b))
    
    img.save(output_image_path)
    print(f"Text hidden successfully in {output_image_path}")

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    
    binary_secret_text = ""
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            binary_secret_text += str(r & 1)
            binary_secret_text += str(g & 1)
            binary_secret_text += str(b & 1)
            
            if binary_secret_text[-16:] == '1111111111111110':
                decoded_text = ""
                for i in range(0, len(binary_secret_text) - 16, 8):
                    byte = binary_secret_text[i:i + 8]
                    decoded_text += chr(int(byte, 2))
                print(f"Extracted text: {decoded_text}")
                return
    
    print("No hidden text found in the image")

if __name__ == '__main__':
    hide_text_in_image('image.jpg', 'This is a hidden message!', 'encoded_image.png')
    
    extract_text_from_image('encoded_image.png')
