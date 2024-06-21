from PIL import Image
import img2pdf
import os
from pypdf import PdfMerger

def main():

    iterate_directory()
    convert_img_to_pdf()
    append_pdf()



def iterate_directory():
    for filename in os.listdir():
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image = Image.open(filename)
            new_image = resize_image(image)
            filename = filename[:-5] #remove .jpeg from the filename
            save_resized_image(new_image, filename)

def resize_image(img: Image.Image) -> Image.Image:
    new_image = img.resize((1240, 1748))

    new_image = add_white_borders(new_image)

    return new_image

def add_white_borders(old_img: Image.Image) -> Image.Image:
    new_img = Image.new("RGB", (1310, 1818), "White")
    box = tuple((n - o) // 2 for n, o in zip((1310, 1818), (1240, 1748)))
    new_img.paste(old_img, box)

    return new_img

def save_resized_image(img: Image.Image, filename: str):
    if not os.path.exists("resized_images"):
        os.makedirs("resized_images")
        os.chdir(f'{os.getcwd()}/resized_images')
        img.save(f'{filename}_a6.jpeg')
        os.chdir('..')
    elif os.path.exists("resized_images"):
        os.chdir(f'{os.getcwd()}/resized_images')
        img.save(f'{filename}_a6.jpeg')
        os.chdir('..')

def convert_img_to_pdf():
    os.chdir(f'{os.getcwd()}/resized_images')
    for filename in os.listdir():
        if filename.lower().endswith(('.jpg', '.jpeg')):
            img = Image.open(filename)
            filename = filename[:-5]
            pdf_bytes = img2pdf.convert(img.filename)
            file = open(f'{filename}.pdf', "wb")
        
            file.write(pdf_bytes)
            
            img.close()
            
            file.close()

def save_pdf_file_names_to_list() -> list[str]:
    lst = []
    for filename in os.listdir():
        if filename.lower().endswith(('.pdf')):
            lst.append(filename)
    return lst

def append_pdf():
    merger = PdfMerger()
    pdfs = save_pdf_file_names_to_list()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write("result.pdf")
    merger.close()
    print("PDF saved")

main()

