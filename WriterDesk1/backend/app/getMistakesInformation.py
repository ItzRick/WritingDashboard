import fitz

def getMistakesInformationStructure(mistakes, filePath):
    '''
        This function makes a list of lists that contains the coordinates, 
        writing skill number (2), explanation and mistake text of each occurence
        of each structure mistake in a specified document.
        Attributes:
            listForDatabase: used for returning all database entries.
            doc: The document to get information from.
            pageHeight: The total height starting at the first page of the 
            document.
            textInstances: all the Rect objects that contain the mistake text
            for every page of the document.
            values: list containing all the information needed for highlighting
            that is to be put in the database.
        Arguments:
            mistakes: a format of mistakes in a document for the structure
            writing skill.
            filePath: the path to the document to get information from.
        Return:
            listForDatabase: a list contain all values objects that can be put
            in the database.
    '''
    listForDatabase = []
    doc = fitz.open(filePath)

    for mistake in mistakes:
        pageHeight = 0
        for page in doc:
            textInstances = page.search_for(mistake)
            if page.number != 0:
                pageHeight += page.rect.y1

            for inst in textInstances:
                # list contains coordinates, type number, explanation and 
                # mistake text
                values = [inst.x0, inst.y0 + pageHeight, inst.x1, 
                inst.y1 + pageHeight, 2, mistakes[mistake], mistake]

                # possible method for adding information to database here
                # addToDB(values)

                listForDatabase.append(values)
    return listForDatabase

def getMistakesInformationStyle(mistakes, filePath):
    '''
        This function makes a list of lists that contains the coordinates, 
        writing skill number (0), explanation, mistake text and replacements of 
        each occurence of each language and style mistake in a specified 
        document.
        Attributes:
            listForDatabase: used for returning all database entries.
            doc: The document to get information from.
            word: The word that is wrong.
            sentence: The sentence that contains the word that is wrong.
            pageHeight: The total height starting at the first page of the 
            document.
            wordInstances: all the Rect objects that contain the word text
            for every page of the document.
            sentenceInstances: all the Rect objects that contain the mistake 
            text for every page of the document.
            wordsInSentence: all the Rect objects that are contained within the
            sentence the word that is wrong is in.
            corWord: The word that is at the correct location in the sentence.
            values: list containing all the information needed for highlighting
            that is to be put in the database.
        Arguments:
            mistakes: a format of mistakes in a document for the language and
            style writing skill.
            filePath: the path to the document to get information from.
        Return:
            listForDatabase: a list contain all values objects that can be put
            in the database.
    '''
    listForDatabase = []
    doc = fitz.open(filePath)

    for mistake in mistakes[0]:
        word = mistake[0]
        sentence = mistake[1]

        pageHeight = 0

        for page in doc:
            wordInstances = page.search_for(word)
            sentenceInstances = page.search_for(sentence)

            if page.number != 0:
                pageHeight += page.rect.y1

            wordsInSentence = []
            for i in sentenceInstances:
                for j in wordInstances:
                    if i.contains(j):
                        wordsInSentence.append(j)
            
            # if there are no mistakes on this page
            if len(wordsInSentence) == 0:
                continue
            # the coordinates of string that is wrong
            corWord = wordsInSentence[mistake[2]]
            # list contains coordinates, type number, explanation, 
            # mistake text and replacement(s)
            values = [corWord.x0, corWord.y0 + pageHeight, corWord.x1, 
                corWord.y1 + pageHeight, 0, mistake[3], mistake[0], mistake[4]]
            
            # possible method for adding information to database here
            # addToDB(values)

            listForDatabase.append(values)

    return listForDatabase


def getMistakesInformationCohesion(mistakes):
    # cohesion = 1
    print('todo')