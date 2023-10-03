import PyPDF2

def getPages(pdfFilename):
    pages = []
    with open(pdfFilename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_number in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page_number].extract_text()
            text = text.replace("\n", " ")
            text = text.replace("'", "")
            text = text.replace('\x00', '')
            pages.append(text)
            
        return pages