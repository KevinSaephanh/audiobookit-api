import pdfplumber

class PdfExtractor:
    def getTextFromPdf(self, pdf):
        pdf_obj = pdfplumber.open(pdf)
        list = []
        for page in pdf_obj.pages:
            list.append(page.extract_text())
        pdf_obj.close()
        return list

    def getTextFromPage(self, pdf, page_num):
        pdf_obj = pdfplumber.open(pdf)
        page = pdf_obj.pages[page_num - 1]
        text = page.extract_text()
        pdf_obj.close()
        return text

    def getPages(self, pdf):
        pdf_obj = pdfplumber.open(pdf)
        pages = pdf_obj.pages
        pdf_obj.close()
        return pages
