import fitz


def extract_text_from_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text