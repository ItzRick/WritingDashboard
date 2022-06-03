import fitz

def getMistakesInformationStructure(mistakes, filePath):
    '''
        
        Attributes:
            listForDatabase: used for returning all database entries.
            doc: The document to get information from
            pageHeight: The total height starting at the first page of the document
            textInstances:  
            values:
        Arguments:
            mistakes:
            filePath:
        Return:
            listForDatabase:
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
        
        Attributes:

        Arguments:

        Return:

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
            
            # the coordinates of string that is wrong
            corWord = wordsInSentence[mistake[2]]
            # list contains coordinates, type number, explanation, 
            # mistake text and replacement(s)
            values = [corWord.x0, corWord.y0 + pageHeight, corWord.x1, corWord.y1, 0, 
                mistake[3], mistake[0], mistake[4]]
            
            # possible method for adding information to database here
            # addToDB(values)

            listForDatabase.append(values)

    return listForDatabase


def getMistakesInformationCohesion(mistakes):
    # cohesion = 1
    print('todo')