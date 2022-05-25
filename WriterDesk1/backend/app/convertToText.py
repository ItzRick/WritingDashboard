#from app import app
import fitz
import os
import docx
import pdfplumber
import re
import bs4 as bs
import regex
from collections import Counter
from copy import deepcopy


# Methods used for extracting text from txt, pdf and docx files and converting them to strings or text files.
# Usage: call extract_string_from_file(path) or convert_file_to_txt(pathIn, pathOut) in a try/catch to catch type/value errors
# All paths should be absolute paths

# Retrieves text from a text file at path, returns a string with the text
def getTXTText(path):
    fullText = ""
    try: 
        # Define array that will contain the document
        linesDocument = []
        with open(path, 'rt') as document: 
            # Split the document into lines
            document = document.read().splitlines()
            for line in document: 
                # If there is a whiteline
                # that line should turn into "\n"
                # If the last element of a string is not a space
                # then that should be added
                if line == "": 
                    line = "\n"
                elif line[-1] != " ":
                    line = line+" "
                linesDocument.append(line)
        # Ensure that before a newline character (\n)
        # there is no space at the end of the previous line
        i = 0
        while i < len(linesDocument):
            if i > 0 and linesDocument[i] == "\n":
                linesDocument[i-1] = linesDocument[i-1][:-1]
            i = i + 1
        # Ensure that the last character of a string
        # is not a space 
        last = len(linesDocument) - 1
        linesDocument[last] = linesDocument[last][:-1]
        fullText = ''.join(linesDocument)
    except Exception as e:
        # Invalid file or filename
        print("caught", repr(e), "when calling getTXTText")
    # Remove redundant newlines
    # fullText = re.sub(r'\n+', '\n\n', fullText).strip()
    return fullText

# Retrieves text from a pdf file at path, returns a string with the text
# If returnReferences is True, also returns a string with the references
def getPDFText(path, returnReferences=False, includeTables=False, includeCaptions=False):
    text = referenceText = ""
    try:
        doc = fitz.open(path)
        xNormal = getFrequencyX(doc).most_common(1)[0][0]
        for page in doc:
            pageText = ""
            firstBlock = True
            table = []
            dictionary = page.get_text("dict", flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES & fitz.TEXT_INHIBIT_SPACES & fitz.TEXT_DEHYPHENATE)
            blocks = splitBlocks(dictionary["blocks"])

            for i, block in enumerate(blocks):
                #Check for potential tables
                if isBlockTable(block, xNormal):
                    table.append(getBlockText(block))
                    continue
                else:
                    if len(table) < 2 or includeTables:
                        for row in table:
                            pageText = "\n".join([pageText, row])
                    table = []

                #Retrieve text from block
                blockText = getBlockText(block)

                #Ignore empty blocks and captions
                if blockText == "" or (isTextCaption(blockText) and not includeCaptions):
                    continue
                
                #Append text from block to the text of the page
                #No new line if this is the first block or the first sentence was started in previous block 
                if firstBlock or not regex.search("^[\P{L}]*\p{Lu}", blockText):
                    firstBlock = False
                    pageText = "".join([pageText, blockText])
                else:
                    pageText = "\n".join([pageText, blockText])

            #Append text from page to the text of the document
            if regex.search("[^\.\?\!\p{Pf}]$", text.rstrip()):
                text = "".join([text.rstrip(), " ", pageText])
            else:
                text = "".join([text, "\n", pageText])
    except Exception as e:
        # Invalid file or filename
        print("caught", repr(e), "when calling getPDFText")

    text = postProcessText(text)
    #Split references
    referenceSplit = regex.split("\n\P{L}*([Rr]eferences|[Bb]ibliography)\P{L}*\n", text)
    if len(referenceSplit) > 1:
        text = referenceSplit[0]
        referenceText = referenceSplit[len(referenceSplit)-1]
    if returnReferences:
        return text, referenceText
    return text

def getDOCXText(path):
    """
    Retrieves text from a docx file at path and returns a string with the text
    Attributes:
        fullText: String of extracted text
        stylesToRemove: List of styles to exclude from fullText
        referencesParagraph: Boolean which is true if the current paragraph consists of references
        doc: Word document
        para: Paragraph of text
        documentXML: document.xml of docx file
        tag: tags inside documentXML
    :param path: Path of docx file which will be extracted.
    :return: Text of docx file as a string.
    """

    fullText = ""
    stylesToRemove = ["Title", "Subtitle", "List Paragraph", "Quote", "Intense Quote", "Caption"]
    referencesParagraph = False

    try:
        # Read docx file
        doc = docx.Document(path)

        # iterate over paragraphs
        for para in doc.paragraphs:
            # Remove titles, headings, lists, quotes, captions and references
            if not (para.style.name.startswith("Heading") or para.style.name in stylesToRemove) and not referencesParagraph:
                # Get document.xml from word file
                documentXML = bs.BeautifulSoup(para._p.xml, 'lxml')

                # Find and remove textboxes
                for textbox in documentXML.find_all('w:txbxcontent'):
                    textbox.decompose()

                # Find text and line breaks
                for tag in documentXML.findAll(["w:t", "w:br"]):
                    if tag.name == "w:t":
                        fullText += tag.text
                    else:
                        fullText += '\n'  # Add newline
                fullText += "\n"  # Add newline

            elif para.style.name.startswith('Heading'):
                if 'references' in para.text.lower() or 'bibliography' in para.text.lower():
                    referencesParagraph = True  # Next paragraph is references
                else:
                    referencesParagraph = False

    except Exception as e:
        # Invalid file or filename
        print("caught", repr(e), "when calling getDOCXText")

    # Remove redundant newlines
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

#Split blocks at empty lines, as they are separate paragraphs
#Returns list of new blocks 
def splitBlocks(blocks):
    blocksNew = []
    for block in blocks:
        if block["type"] == 0:
            newBlock = deepcopy(block)
            lastBreak = 0
            for i, line in enumerate(block["lines"]):
                lineText = getLineText(line).strip()
                if lineText == "":
                    if i != 0:
                        newBlock["lines"] = block["lines"][lastBreak:i]
                        blocksNew.append(deepcopy(newBlock))
                    lastBreak = i
                    continue
                if i == len(block["lines"])-1:
                    newBlock["lines"] = block["lines"][lastBreak:]
                    blocksNew.append(deepcopy(newBlock))
    return blocksNew

# Gets frequencies of x-coordinates of blocks in a Python Counter object
def getFrequencyX(doc):
    xlist = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                xlist.append(block["lines"][0]["bbox"][0])
    return Counter(xlist)

# Combines broken words, filters out number references, in-text citations and empty lines
# using regular expressions
def postProcessText(text):     
    #Combine broken words together
    text = regex.sub("-\s*\n\s*", "", text)
    #Remove number references
    text = regex.sub("\s\[\d*\]", "", text)
    #Remove empty lines
    text = regex.sub("^(\s)*\n", "", text)
    text = regex.sub("\n(\s)*\n", "\n", text)
    #Remove Excess spaces
    text = regex.sub(" ( )+", " ", text)
    #Remove in-text citations
    oneSource = "([^\)]*(\n[^\)]*)?,[\s\n]*)?(\d{4}|n\.d\.)"
    multipleSources = "(("+ oneSource +"|\setc\.)(;[\s\n]*)?)+"
    text = regex.sub("(?<=[^\.])\s\((" + oneSource + "|" + multipleSources + ")\)", "", text)
    return text

# Retrieves text from a pdf line as string
def getLineText(line):
    lineText = ""
    spans = line["spans"]
    #Retrieve text from a line
    for span in spans:
        spanText = span["text"]
        lineText = "".join([lineText, spanText])
    return lineText

# Retrieves text from a pdf block as string,
# with list symbols, lines without letters and punctuation out
def getBlockText(block):
    blockText = ""
    lines = block["lines"]
    for i, line in enumerate(lines):
        lineText = getLineText(line)
        #Remove list symbols
        listRegex = "^\s*(\p{N}+\.|\p{L}\.|[^\p{L}\p{N}&%#])(\p{N}+)*((\.|:))?\s(?=\p{L})"
        if regex.search(listRegex, lineText):
            lineText = regex.sub(listRegex, "", lineText)
            blockText = "".join([blockText, "\n", lineText])
            continue

        #Remove lines without letters and punctuation
        noLetterRegex = "^[^,:\(\)\p{L}]*$"
        if regex.search(noLetterRegex, lineText):
            lineText = regex.sub(noLetterRegex, "", lineText)
            if lineText != "":
                blockText = "".join([blockText, "\n", lineText])
            continue

        #Start line with different fontsize on new line
        if i != 0 and lineText.strip() != "":
            previousLineSpans = lines[i-1]["spans"]
            if line["spans"][0]["size"] != previousLineSpans[len(previousLineSpans)-1]["size"]:
                blockText = "".join([blockText, "\n", lineText, " "])
                continue

        #Add line to blockText
        blockText = "".join([blockText, lineText, " "]).replace("  ", " ")
    return blockText

#Checks if block could be part of a table
#Assumes row in table has 2+ columns at same y coordinate
#and does not start at normal x coordinate 
def isBlockTable(block, xNormal, yTolerance=3):
    lines = block["lines"]
    if len(lines) > 0:
        if lines[0]["bbox"][0] == xNormal:
            return False 
        if len(lines) > 1:
            y = lines[0]["bbox"][1]
            for line in lines:
                if abs(line["bbox"][1] - y) > yTolerance:
                    return False
            return True
    return False

#Checks if block is caption
#Assumes captions start with Figure, Fig. or Table
def isTextCaption(block):
    reg = "^(Table|Figure|Fig\.)\s*\d*(\.\d*)*(\.|:)?\s*(?=\p{Lu})"
    return regex.search(reg, block.lstrip())