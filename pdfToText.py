# importing required modules
import PyPDF2
import voice_interact as vi
from io import StringIO

# Read each line of the PDF
def readLines(path):
    pdfContent = StringIO(getPDFContent(path))
    for line in pdfContent:
        tts = vi.gTTS(text=line.strip(), lang='es')
        print(line.strip())
        audio_file = "pdf.mp3"
        tts.save(audio_file)
        vi.playsound.playsound(audio_file)
        vi.os.remove(audio_file)

def getPDFContent(path):
    # creating a pdf file object
    pdfFileObj = open(path, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    textoPDF = []

    for i in range(6,39):
    # creating a page object
        pageObj = pdfReader.getPage(i)
        textoPaginaPDF = pageObj.extractText()
        textoPDF.append(textoPaginaPDF)
    for i in range(42,43):
        pageObj = pdfReader.getPage(i)
        textoPaginaPDF = pageObj.extractText()
        textoPDF.append(textoPaginaPDF)
    for i in range(45,46):
        pageObj = pdfReader.getPage(i)
        textoPaginaPDF = pageObj.extractText()
        textoPDF.append(textoPaginaPDF)
    pageObj = pdfReader.getPage(48)
    textoPaginaPDF = pageObj.extractText()
    textoPDF.append(textoPaginaPDF)
    for i in range(51,53):
        pageObj = pdfReader.getPage(i)
        textoPaginaPDF = pageObj.extractText()
        textoPDF.append(textoPaginaPDF)
    # closing the pdf file object
    pdfFileObj.close()
    content = "".join(textoPDF)
    return content