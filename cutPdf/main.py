
from PyPDF2 import PdfFileReader, PdfFileWriter
 

if __name__ == "__main__":
    readfile=r"../public/pdf/demo.pdf"
    pdfReader = PdfFileReader(open(readfile, 'rb'))
    pdfFileWriter = PdfFileWriter()
    numPages = pdfReader.getNumPages()
    pagelist=(numPages-2,numPages-1)   #剪切最后一页
    for index in range(0, numPages):
        if index not in pagelist:
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)
    pdfFileWriter.write(open(f"{readfile}_cat.pdf", 'wb'))