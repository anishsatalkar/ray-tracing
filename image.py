from PIL import Image

if __name__ == '__main__':
    image = Image.open("first_3.png")
    image = image.resize((250,250), resample=Image.ANTIALIAS)
    image.save("first_antialias.png")
    image.show()