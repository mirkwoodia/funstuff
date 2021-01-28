import os #for directory control
import time

from saucenao_api import SauceNao
from saucenao_api.params import DB, Hide, BgColor
from saucenao_api.errors import (UnknownServerError, UnknownClientError, BadKeyError, BadFileSizeError, ShortLimitReachedError, LongLimitReachedError)

sauce = SauceNao(
    api_key="95782520162bd7e9685ae3eaf25ff151b11dff7c",
)

def fileRename(f, d, e, n=0):
    try:
        os.rename(f, d+'('+str(n)+')'+e)
    except FileExistsError:
        fileRename (f, d, e, n+1)


for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.getcwd(), filename), 'rb') as f: #loop every file in current directory as f
        name, ext = os.path.splitext(filename)
        if (ext == '.jpg' and '.png'):
            try:
                results = SauceNao().from_file(f)
            except ShortLimitReachedError:
                time.sleep(35)
                #results = SauceNao().from_file(f)
            print(results[0].title)
    fileRename (filename, results[0].title, ext)
    #try:
    #    os.rename(filename, results[0].title+ext)
    #except FileExistsError:
    #    os.rename
#Try to catch an error: file name already exists, then apprend a numero and try again. Try: except Error1: