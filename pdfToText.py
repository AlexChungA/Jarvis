# importing required modules
import PyPDF2
import voice_interact as vi
from io import StringIO

# Read each line of the PDF
def readLines(path,inicio,fin):
    pdfContent = StringIO(getPDFContent(path,inicio,fin))
    for line in pdfContent.readlines():
        try:
            tts = vi.gTTS(text=line, lang='es')
            audio_file = "pdf.mp3"
            tts.save(audio_file)
            vi.playsound.playsound(audio_file)
            vi.os.remove(audio_file)
        except:
            pass
        

def getPDFContent(path,inicio,fin):
    # creating a pdf file object
    pdfFileObj = open(path, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    textoPDF = []

    for i in range(inicio,fin):
    # creating a page object
        pageObj = pdfReader.getPage(i)
        textoPaginaPDF = pageObj.extractText()
        textoPDF.append(textoPaginaPDF)
    # closing the pdf file object
    pdfFileObj.close()
    content = "".join(textoPDF)
    return content