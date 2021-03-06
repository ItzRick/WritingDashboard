from docx import Document
import re
import bs4 as bs

# Methods used for extracting text from txt and docx files and converting them to strings or text files.
# Usage: call extract_string_from_file(path) or convert_file_to_txt(pathIn, pathOut) in a try/catch to catch type/value errors
# All paths should be absolute paths

def getTXTText(path):
    '''
        Retrieves text from a text file at path, returns a string with the text
        Attributes:
            fullText: full text we are currently reading.
            linesDocument: Array that will contiain the document.
            document: The document we are currently reading.
            line: line in the document we are reading.
        Arguments: 
            path: absolute path of the .txt file that should be read. 
        Returns:
            True, if the text has been succesfully extracted. False and a string with the error message when this is not the case.
            fullText: full text from the file we are currently reading.
    '''
    fullText = ""
    try: 
        # Define array that will contain the document
        linesDocument = []
        with open(path, "rt", encoding="utf-8") as document: 
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
       return False, "Caught " + repr(e) + " when calling getTXTText."
    # Remove redundant newlines
    fullText = re.sub(r'\n+', '\n\n', fullText).strip()
    return True, fullText


def getDOCXText(path):
    """
    Retrieves text from a docx file at path and returns a string with the text
    Attributes:
        fullText: String of extracted text
        referencesText: String of extracted references text
        stylesToRemove: List of styles to exclude from fullText
        referencesParagraph: Boolean which is true if the current paragraph consists of references
        doc: Word document
        para: Paragraph of text
        documentXML: document.xml of docx file
        tag: tags inside documentXML
    Arguments:
        path: Path of docx file which will be extracted.
    Returns:
        True, if the text has been succesfully extracted. False and a string with the error message when this is not the case.
        fullText: Text of docx file as a string (does not contain references).
        referencesText: Text of references from docx file as a string.
    """

    fullText = ""
    referencesText = ""
    stylesToRemove = ["Title", "Subtitle", "List Paragraph", "Quote", "Intense Quote", "Caption"]
    referencesParagraph = False

    try:
        # Read docx file
        doc = Document(path)

        # iterate over paragraphs
        for para in doc.paragraphs:
            # Remove titles, headings, lists, quotes, captions
            if not (para.style.name.startswith("Heading") or para.style.name in stylesToRemove):
                fullText, referencesText = subtractTextFromParagraph(para, referencesParagraph, fullText, referencesText)

            elif para.style.name.startswith('Heading'):
                if 'references' in para.text.lower() or 'bibliography' in para.text.lower():
                    referencesParagraph = True  # Next paragraph is references
                else:
                    referencesParagraph = False

    except Exception as e:
        # Invalid file or filename
        return False, "Caught " + repr(e) + " when calling getDOCXText.", ""

    # Remove redundant newlines
    fullText = re.sub(r'\n+', '\n\n', fullText).strip()
    referencesText = re.sub(r'\n+', '\n\n', referencesText).strip()

    return True, fullText, referencesText


def subtractTextFromParagraph(para, referencesParagraph, fullText, referencesText):
    """
    Function to subtract text from a paragraph. Returns normal text and text from references in different strings.
    Attributes:
        documentXML: document.xml of paragraph
        textbox: text inside textbox
        tag: tags inside documentXML
    Arguments:
        para: Paragraph of text
        referencesParagraph: Boolean which is true if the current paragraph consists of references
        fullText: String of extracted text
        referencesText: Text of references from docx file as a string
    Returns:
        fullText: String of extracted text
        referencesText: Text of references from docx file as a string
        """
    # Get document.xml from word file
    documentXML = bs.BeautifulSoup(para._p.xml, 'lxml')

    # Find and remove textboxes
    for textbox in documentXML.find_all('w:txbxcontent'):
        textbox.decompose()

    if not referencesParagraph:  # Paragraph does not contain references
        # Find text and line breaks
        for tag in documentXML.findAll(["w:t", "w:br"]):
            if tag.name == "w:t":
                fullText += tag.text  # Append text to fullText
            else:
                fullText += '\n'  # Add newline
        fullText += "\n"  # Add newline

    else:  # Paragraph consists of references
        # Find text and line break
        for tag in documentXML.findAll(["w:t", "w:br"]):
            if tag.name == "w:t":
                referencesText += tag.text  # Append text to referencesText
            else:
                referencesText += '\n'  # Add newline
        referencesText += "\n"  # Add newline
    return fullText, referencesText
