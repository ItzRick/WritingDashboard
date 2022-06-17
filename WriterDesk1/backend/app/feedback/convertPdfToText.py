import fitz
import os
# import docx
# import pdfplumber
import re
import bs4 as bs
import regex
from collections import Counter
from copy import deepcopy
from app.feedback.convertDocxTxtToText import getTXTText, getDOCXText


# Methods used for extracting text from pdf files and converting them to strings or text files.
# Usage: call extract_string_from_file(path) or convert_file_to_txt(pathIn, pathOut) in a try/catch to catch type/value errors
# All paths should be absolute paths


def getPDFText(path, returnReferences=False, includeTables=False, includeCaptions=False, includeLists=True):
    """
    Retrieves text from a pdf file at path and returns a string with the text.
    If returnReferences is True, also returns a string with the references.
    Attributes:
        returnReferences: Whether a string with the references should be returned
        includeTables: Whether text from tables should be included in the returned string
        includeCaptions: Whether text from captions should be included in the returned string
        includeLists: Whether text from lists should be included in the returned string
        text: String of extracted text
        doc: PDF document
        xNormal: Most frequent x-coordinate of lines of text
        pageText: String of text of a single page
        firstBlock: Whether an extracted block is the first on the page
        table: Holder of blocks which potentially are a table
        dictionary: PDF document in a python dictionary form
        blocks: Assumed paragraphs of document text
        blockText: String of text of a single block
        referenceSplit: Split of the extracted string into normal text and reference text
        referenceText: String of text containing references
    Arguments: 
        path: Path of pdf file which will be extracted
        returnReferences: True if the references should also be returned.
    Returns: 
        text: Text of pdf file as a string.
        referenceText: Text with only the references form the pdf file. 
    """

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
                    table.append(getBlockText(block, includeLists))
                    continue
                else:
                    if len(table) < 2 or includeTables:
                        for row in table:
                            pageText = "\n".join([pageText, row])
                    table = []

                #Retrieve text from block
                blockText = getBlockText(block, includeLists)

                #Ignore empty blocks and captions
                if blockText == "" or (isTextCaption(blockText) and not includeCaptions):
                    continue
                
                #Append text from block to the text of the page
                #No new line if this is the first block or the first sentence was started in previous block 
                if firstBlock or not regex.search(r"^[\P{L}]*\p{Lu}", blockText):
                    firstBlock = False
                    pageText = "".join([pageText, blockText])
                else:
                    pageText = "\n".join([pageText, blockText])

            #Append text from page to the text of the document
            if regex.search(r"[^\.\?\!\p{Pf}\p{N}]$", text.rstrip()):
                text = "".join([text.rstrip(), " ", pageText])
            else:
                text = "".join([text, "\n", pageText])
    except Exception as e:
        # Invalid file or filename
        print("caught", repr(e), "when calling getPDFText")

    text = postProcessText(text)
    #Split references
    referenceSplit = regex.split(r"\n\P{L}*((?i)references|(?i)bibliography)[\n\s]", text)
    if len(referenceSplit) > 1:
        text = referenceSplit[0].strip()
        referenceText = referenceSplit[len(referenceSplit)-1]
    if returnReferences:
        return text, referenceText
    return text


def extractStringFromFile(path):
    """
    Retrieves text from a pdf, docx or txt file at path and returns a string with the text.
    If file at path has a different extension, a type error is thrown
    Attributes:
        name: Name of file at path without file extension
        fileExtension: File extension of file at path
        text: String of text extracted from file at path
    Arguments:
        path: Path of file which will be extracted
    Returns:
        text: Text of file as a string
    """

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

def convertStringToTXT(string, path):
    """
    Writes string to txt file at path.
    If this is not possible an exception is thrown.
    Arguments:
        string: String to write
        path: Path of file to which the string is written
    """

    try:
        with open(path, 'w') as f:
            f.write(string)
    except Exception as e:
        raise ValueError("Couldn't write to txt")

def convertFileToTXT(pathIn, pathOut):
    """
    Retrieves text from a pdf, docx or txt file at path as string and writes to txt file at pathOut.
    If input file has a wrong type, a type error is thrown. 
    If writing to output file fails, a value error is thrown.
    Attributes:
        string: String of text extracted from file at pathIn
    Arguments: 
        pathIn: Path of file which will be extracted
        pathOut: Path of file to which result will be written
    """

    try:
        string = extractStringFromFile(pathIn)
        convertStringToTXT(string, pathOut)
    except TypeError as e:
        raise TypeError(e.args[0])
    except ValueError as e:
        raise ValueError(e.args[0])

def splitBlocks(blocks):
    """
    Splits blocks with empty lines into separate blocks, as they are separate paragraphs.
    Attributes:
        blocksNew: Holder of new blocks
        newBlock: Block with lines between empty lines
        lastBreak: Index of last empty line
        lineText: Text of a single line
    Arguments:
        blocks: List of original blocks
    Returns: 
        blocksNew: List of new blocks
    """

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

def getFrequencyX(doc):
    """
    Gets x-coordinates of blocks in doc with their frequency in a Python Counter object.
    Attributes:
        xlist: List of x-coordinates
    Arguments:
        doc: PDF document to get blocks from
    Returns:
        Counter(xlist): Counter object with x-coordinates and their frequency
    """
    
    xlist = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    xlist.append(line["bbox"][0])
    return Counter(xlist)

def postProcessText(text):  
    """
    Filters string on hyphenated words, number references, empty lines, excess spaces and in-text citations
    using regular expressions. Replaces new lines with double new lines for consistency with docx and txt files
    Attributes:
        text: String that is filtered
        oneSource: Regex for finding in-text citations with one source
        multipleSources: Regex for finding in-text citations with multiple sources
    Arguments:
        text: String that needs to be filtered
    Returns:
        text: String that is filtered
    """   

    #Combine broken words together
    text = regex.sub(r"-\s*\n\s*", "", text)
    #Remove number references
    text = regex.sub(r"\s\[\d*\]", "", text)
    #Remove empty lines
    text = regex.sub(r"^(\s)*\n", "", text)
    text = regex.sub(r"\n(\s)*\n", "\n", text)
    #Remove Excess spaces
    text = regex.sub(r" ( )+", " ", text)
    #Remove in-text citations
    oneSource = r"([^\)]*(\n[^\)]*)?,[\s\n]*)?(\d{4}|n\.d\.)"
    multipleSources = r"(("+ oneSource +r"|\setc\.)(;[\s\n]*)?)+"
    text = regex.sub(r"(?<=[^\.])\s\((" + oneSource + "|" + multipleSources + r")\)", "", text)
    #Replace new lines with double new lines
    text = regex.sub(r"\n+", r"\n\n", text).strip()
    return text

def getLineText(line):
    """
    Retrieves text from a line in a pdf and returns a string with the text
    Attributes:
        lineText: Text from a single line
        spans: List of spans from line
        spanText: Text from a single span
    Arguments:
        line: Line of which text is extracted
    Returns:
        lineText: Text of line as a string
    """

    lineText = ""
    spans = line["spans"]
    #Retrieve text from a line
    for span in spans:
        spanText = span["text"]
        lineText = "".join([lineText, spanText])
    return lineText

def filterLineList(lineText, includeLists=True):
    """
    Removes list symbols from a line, or entire line if includeLists is False
    Attributes:
        listRegex: Regex to find list symbols
    Arguments:
        lineText: Text to filter
        includeLists: Whether text after list symbols should be included in the text
    Returns:
        lineText: Text of line as a string
    """

    listRegex = r"^\s*(\p{N}+\.|\p{L}\.|[^\p{L}\p{N}&%#])(\p{N}+)*((\.|:))?\s(?=\p{L})"
    if regex.search(listRegex, lineText):
        if includeLists:
            lineText = regex.sub(listRegex, "", lineText)
        else:
            lineText = ""
    return lineText

def filterLineNoLetters(lineText):
    """
    Removes a line if it contains no letters or punctuation
    Attributes:
        noLetterRegex: Regex to find absence of letters and punctuation
    Arguments:
        lineText: Text to filter
    Returns: 
        lineText: Text of line as a string
    """

    noLetterRegex = r"^[^,:\(\)\p{L}]*$"
    if regex.search(noLetterRegex, lineText):
        lineText = regex.sub(noLetterRegex, "", lineText)
    return lineText

def getBlockText(block, includeLists):
    """
    Retrieves text from a block in a pdf and returns a string with the text 
    with list symbols, without lines without letters and punctuation.
    Attributes:
        blockText: Text from a single block
        lines: List of lines from block
        unfilteredLineText: Raw text from a single line
        lineText: Text from a single line, filtered
        previousLineSpans: List of spans from previous line
    Arguments:
        line: Line of which text is extracted
    Returns:
        blockText: Text of line as a string
    """

    blockText = ""
    lines = block["lines"]
    for i, line in enumerate(lines):
        unfilteredLineText = getLineText(line)
        lineText = filterLineList(unfilteredLineText, includeLists)
        lineText = filterLineNoLetters(lineText)
        if unfilteredLineText != lineText:
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

def isBlockTable(block, xNormal, yTolerance=3):
    """
    Checks whether a block is potentially part of a table.
    Assumes row in table has 2+ columns at same y coordinate 
    and does not start at normal x coordinate .
    Attributes:
        lines: List of lines from block
        y: Y-coordinate of first line from block
    Arguments:
        block: Block to check
        xNormal: X-coordinate of normal text
        yTolerance: Maximum difference lines can have to be considered a table row
    Returns:
        Whether a block is potentially part of a table
    """

    lines = block["lines"]
    if len(lines) > 0:
        if lines[0]["bbox"][0] == xNormal:
            return False
        lineText = getLineText(lines[0]) 
        if lineText != filterLineList(lineText) or regex.search(r"^[^\p{L}\p{N}]*$", lineText):
            return False
        if len(lines) > 1:
            y = lines[0]["bbox"][1]
            for line in lines:
                if abs(line["bbox"][1] - y) > yTolerance:
                    return False
            return True
    return False

def isTextCaption(block):
    """
    Checks whether a block contains a caption.
    Assumes captions start with Figure, Fig. or Table.
    Attributes:
        reg: Regex to find captions
    Arguments:
        block: Block to filter for captions
    Returns:
        Whether block contains a caption
    """
    reg = r"^(T(?i:able)|F(?i:igure)|F(?i:ig)\.)\s*\d+(\.\d*)*(\.|:)?\s*(?=\p{Lu})"
    return regex.search(reg, block.lstrip())