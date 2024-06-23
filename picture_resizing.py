from PIL import Image
import img2pdf
import os
from pypdf import PdfMerger
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

def main():

    iterate_directory()
    convert_img_to_pdf()
    append_pdf()



def iterate_directory() -> None:
    """
    Iterates through the current directory and processes image files.
    
    For each image file, it resizes the image and saves it in the 'resized_images' directory.
    """
    for filename in os.listdir():
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image = Image.open(filename)
            new_image = resize_image(image)
            filename = filename[:-5] #remove .jpeg from the filename
            save_resized_image(new_image, filename)

def resize_image(img: Image.Image) -> Image.Image:
    """
    Resizes the given image to 1240x1748
    
    Parameters
    ----------
        img : Image.Image
            The image to be resized
        
    Returns
    ----------
    Image.Image
        The resized image (with white borders)
    """

    new_image = img.resize((1240, 1748))

    new_image = add_white_borders(new_image)

    return new_image

def add_white_borders(old_img: Image.Image) -> Image.Image:
    """
    Adds white borders to the given image to fit it into 1310x1818 dimensions.
    
    Parameters
    ----------
        old_img : Image.Image
            The image to which white borders will be added
        
    Returns
    ----------
    Image.Image
        The image with white borders
    """
    new_img = Image.new("RGB", (1310, 1818), "White")
    box = tuple((n - o) // 2 for n, o in zip((1310, 1818), (1240, 1748)))
    new_img.paste(old_img, box)

    return new_img

def save_resized_image(img: Image.Image, filename: str) -> None:
    """
    Saves the resized image to the 'resized_images' directory with '_a6' appended to the filename
    Parameters
    ----------
        img : Image.Image
            The image to be saved
        filename : str
            The filename to be used
        
    """
    if not os.path.exists("resized_images"):
        os.makedirs("resized_images")
        os.chdir(f'{os.getcwd()}/resized_images')
        img.save(f'{filename}_a6.jpeg')
        os.chdir('..')
    elif os.path.exists("resized_images"):
        os.chdir(f'{os.getcwd()}/resized_images')
        img.save(f'{filename}_a6.jpeg')
        os.chdir('..')

def convert_img_to_pdf() -> None:
    """
    Converts all JPEG images in the 'resized_images' directory to PDF files
    """

    try:
        os.chdir(f'{os.getcwd()}/resized_images')
    except FileNotFoundError:
        os.makedirs("resized_images")
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
    """
     Saves the filenames of all PDF files in the current directory to a list
    
        
    Returns
    ----------
    List[str]
        A list of PDF filenames.
    """
    lst = []
    for filename in os.listdir():
        if filename.lower().endswith(('.pdf')):
            lst.append(filename)
    return lst

def append_pdf() -> None:
    """
    Merges all PDF files in the current directory into a single PDF file named 'result.pdf'
    
    """

    merger = PdfMerger()
    pdfs = save_pdf_file_names_to_list()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write("result.pdf")
    merger.close()
    logging.info("PDF saved")

main()

