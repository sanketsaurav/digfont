from __future__ import with_statement

import selenium.webdriver

from PIL import Image
import base64
from io import BytesIO
import cStringIO

from google.appengine.api import files
from google.appengine.ext import blobstore

def take_screenshot(url):
    try:
        webdriver = selenium.webdriver.PhantomJS()
        webdriver.get(url)
        webdriver.set_window_size(1280,800)
        imagedata = webdriver.get_screenshot_as_base64()
        webdriver.close()
        webdriver.quit()
    except Exception, e:
        raise

    return process_screenshot(imagedata)

def process_screenshot(base64_img):

    basewidth = 220
    img = Image.open(BytesIO(base64.b64decode(base64_img)))
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img = img.crop((0,0,basewidth, basewidth))

    #saving the image into a cStringIO object to avoid writing to disk
    out_img=cStringIO.StringIO()
    img.save(out_img, 'PNG')

    return upload_to_blobstore(out_img)

def upload_to_blobstore(data, mime_type='image/png'):
    """
    Upload an image to the blobstore, and return its key
    """

    # create a PNG image file
    image_name = files.blobstore.create(mime_type=mime_type)

    # open the file and write the data
    with files.open(image_name, 'a') as f:
        f.write(data)

    # finalize the file before attempting to read it
    files.finalize(image_name)

    blob_key = files.blobstore.get_blob_key(file_name)
    return blob_key