from app import app
import fitz
import os
import docx
import pdfplumber
import re
import bs4 as bs


# Methods used for extracting text from pdf and docx files and converting them to text files.
# Usage: call extract_string_from_file(path) or convert_file_to_txt(pathIn, pathOut) in a try/catch to catch type/value errors
# All paths should be absolute paths

# Retrieves text from a text file at path, returns a string with the text
def getTXTText(path):
    text = ""
    doc = open(path)
    text = doc.read()
    doc.close()
    return text


# Retrieves text from a pdf file at path, returns a string with the text
def getPDFText(path):
    text = ""
    first = True
    tableText = getTablesFromPDF(path)

    doc = fitz.open(path)
    for page in doc:
        pageText = ""
        dictionary = page.get_text("dict", sort=True)
        for i, block in enumerate(dictionary["blocks"]):
            try:
                if block["type"] == 1:  # Image block
                    raise NextPage
                elif dictionary["blocks"][i - 1]["type"] == 1:  # Empty block after image
                    raise NextPage
                elif isTextCaption(dictionary["blocks"], i):  # Caption
                    raise NextPage
                # Retrieve text from a block
                blockText = ""
                lines = block["lines"]
                for line in lines:
                    lineText = ""
                    spans = line["spans"]
                    for span in spans:
                        lineText = "".join([lineText, span["text"]])
                    if (isStringInTable(lineText, tableText)):
                        raise NextPage
                    blockText = "".join([blockText, lineText, " "])
                # Append text from block to the text of the page
                if first:
                    first = False
                    pageText = "".join([pageText, blockText])
                else:
                    pageText = "\n".join([pageText, blockText])
            except NextPage:
                continue
        # Remove text from tables
        for table in tableText:
            pageText = pageText.replace(table, "")
        # Append text from page to the text of the document
        text = "".join([text, pageText])
    return text


def getDOCXText(path):
    """
    Retrieves text from a docx file at path and returns a string with the text
    Attributes:
        fullText: String of extracted text
        stylesToRemove: List of styles to exclude from fullText
        doc: Word document
        para: Paragraph of text
        documentXML: document.xml of docx file
        tag: tags inside documentXML
    :param path: Path of docx file which will be extracted.
    :return: Text of docx file as a string.
    """

    fullText = ""
    stylesToRemove = ["Title", "Subtitle", "List Paragraph", "Quote", "Intense Quote"]

    try:
        # Read docx file
        doc = docx.Document(path)

        # iterate over paragraphs
        for para in doc.paragraphs:
            # Remove titles, headings, lists, quotes
            if not (para.style.name.startswith("Heading") or para.style.name in stylesToRemove):
                # Get document.xml from word file
                documentXML = bs.BeautifulSoup(para._p.xml)
                for tag in documentXML.findAll(["w:t", "w:br"]):
                    if tag.name == "w:t":
                        fullText += tag.text
                    else:
                        fullText += '\n'  # Add newline

                fullText += "\n"  # Add newline
    except Exception as e:
        # Invalid file or filename
        print("caught", repr(e), "when calling getDOCXText")

    fullText = re.sub(r'\n+', '\n\n', fullText).strip()
    return fullText


# Extracts text from pdf, docx and txt files. Returns text as string
# If file at path has a different extension, a type error is thrown
def extractStringFromFile(path):
    name, fileExtension = os.path.splitext(path)
    text = ""

    if fileExtension == ".txt":
        text = getTXTText(path)
    elif fileExtension == ".pdf":
        text = getPDFText(path)
    elif fileExtension == ".docx":
        text = getDOCXText(path)
    else:
        raise TypeError("File type is not pdf, docx or txt")
    return text


# Writes a string to a txt file at path
# If this is not possible an exception is thrown
def convertStringToTXT(string, path):
    try:
        with open(path, 'w') as f:
            f.write(string)
    except Exception as e:
        raise ValueError("Couldn't write to txt")


# Extracts text from file at path_in and writes to file at path_out
# If input file has a wrong type, a type error is thrown
# If writing to output file fails, a value error is thrown
def convertFileToTXT(pathIn, pathOut):
    try:
        string = extractStringFromFile(pathIn)
        convertStringToTXT(string, pathOut)
    except TypeError as e:
        raise TypeError(e.args[0])
    except ValueError as e:
        raise ValueError(e.args[0])


def isStringInTable(string, tableText):
    for table in tableText:
        if (string == table):
            return True
    return False


def getTablesFromPDF(path):
    tableText = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                text = ""
                for row in table:
                    rowText = ""
                    for cell in row:
                        rowText = "".join([rowText, cell, " "])
                    text = "".join([text, rowText, "\n"])
                tableText.append(text)
        return tableText


def isTextCaption(blocks, index):
    if index < 2:  # Caption can't be first text
        return False
    if blocks[index - 2]["type"] == 0:  # Caption is after image
        return False
    bboxImage = blocks[index - 1]["bbox"]
    bboxCaption = blocks[index]["bbox"]
    if bboxImage[3] - bboxCaption[1] > 20:  # Caption is close to image
        return False
    return True


class NextPage(Exception):
    pass
