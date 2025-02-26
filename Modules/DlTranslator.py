# referring https://github.com/xhluca/dl-translate
import dl_translate as dlt

def translator(text):
    mt=dlt.TranslationModel()
    return mt.translate(text,source=dlt.lang.KOREAN, target=dlt.lang.ENGLISH)

if __name__ == "__main__" : 
    text = "캘리포니아 느낌의 120bpm 펑키락"
    print(translator(text))