import fitz
from structureCheck import getExplanationsStructure
import convertToText
import convertToText2

# doc = fitz.open('../writerdesk1/src/example2.pdf')

# text = ('Turtles is very cool animals, is that true? They can swim, but they can also walk. They are almost like humans.\n'
#     'This is an spelling mistake about turtles. This is another thing about turtles including a speling mistake about turtles. '
#     'This is an apple, this is any fruit, this is an mistake. '
#     'This is a very long paragraph that contains no interesting information about turtles. '
#     'This is a very long paragraph that contains no interesting information '
#     'about turtles. This is a very long paragraph that contains no interesting information about turtles. '
#     'This is a very long paragraph that contains no interesting information about turtles. This is a very '
#     'long paragraph that contains no interesting information about turtles. This is a very long paragraph '
#     'that contains no interesting information about turtles. This is a very long paragraph that contains no '
#     'interesting information about turtles. This is a very long paragraph that contains no interesting information '
#     'about turtles. This is a very long paragraph that contains no interesting information about turtles. This is a '
#     'very long paragraph that contains no interesting information about turtles. This is a very long paragraph that '
#     'contains no interesting information about turtles. This is a very long paragraph that contains no interesting '
#     'information about turtles. This is a very long paragraph that contains no interesting information about turtles. '
#     'This is a very long paragraph that contains no interesting information about turtles.')

# text = convertToText2.getPDFText('../writerdesk1/src/example2.pdf', includeLists=False)
# print(text)

def highlightStructure(path):
    doc = fitz.open(path)
    text = convertToText2.getPDFText(path, includeLists=False)

    structureExplanations = getExplanationsStructure(text)

    for key in structureExplanations.keys():
        
        for page in doc:
            text_instances = page.search_for(key)

            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors({"stroke":(100/255, 143/255, 255/255)})        
                highlight.update()

    #doc.save('../writerdesk1/src/highlightTest3.pdf', garbage=4, deflate=True, clean=True)
    doc.saveIncr()

def removeHighlight(path, skillColor):
    '''
        Removes all highlights of a certain color in a document.
        Attributes:
            doc: The document in which highlights will be removed.
            annot: Pointer to annotation, for deleting and checking its color.
        Arguments:
            path: The path to the document.
            skillColor: The color of the skill, for checking highlights.
    '''
    doc = fitz.open(path)
    for page in doc:
        annot = page.firstAnnot
        while annot:
            if annot.colors['stroke'] == skillColor: 
                page.delete_annot(annot)
            annot = annot.next
    print(doc.has_annots())
    doc.saveIncr()

# if showLanguageStyle:
#     languageStyleExplanations = (
#         [
#             ['is', 'Turtles is very cool animals, is that true?', 'Use "are" instead of "is".', ['are'], 0],
#             ['an', 'This is an spelling mistake about turtles.', 'Use "a" instead of "an".', ['a'], 0],
#             ['speling', 'This is another thing about turtles including a speling mistake about turtles.', 'Use "spelling" instead of "speling".', ['spelling'], 0],
#             ['an', 'This is an apple, this is any fruit, this is an mistake.', 'expl...', ['a'], 2],
#         ]
#         , 6.6)

#     for mistake in languageStyleExplanations[0]:
#         sentence = mistake[1]
#         word = mistake[0]

#         for page in doc:
#             sentence_instances = page.search_for(sentence)
#             word_instances = page.search_for(word)

#         sentenceList = []
#         for i in sentence_instances:
#             # highlight = page.addRectAnnot(i)
#             # highlight.setColors({"stroke":(0/255, 0/255, 0/255)})
#             # highlight.update()
#             sentenceList.append(i)

#         wordsInSentence = []
#         for i in sentenceList:

#             for j in word_instances:
#                 if i.contains(j):
#                     wordsInSentence.append(j)
#         # print(wordsInSentence)
#         # if len(wordsInSentence) <= mistake[4]:
#         #     continue

#         scaledRect = fitz.Rect(wordsInSentence[mistake[4]][0] + 2.5, 
#             wordsInSentence[mistake[4]][1] + 1.5, wordsInSentence[
#                 mistake[4]][2] - 2.5, wordsInSentence[mistake[4]][3] - 1.5)
#         highlight = page.addHighlightAnnot(scaledRect)
    
#         highlight.setColors({"stroke":(120/255, 94/255, 240/255)})   
#         highlight.update() 

# if showSourceIntegrationContent:
#     print('do stuff source integration & content')

# if showCohesion:
#     print('do stuff cohesion')   

path = '../writerdesk1/src/example2_highlighted.pdf'

highlightStructure(path)
# doc = fitz.open(path)
# page0 = doc.load_page(0)
# highlight = page0.add_highlight_annot(fitz.Rect(0, 0, 100, 100))
# highlight.set_colors({"stroke":(0, 1, 0)})        
# highlight.update()
# doc.saveIncr()
# page0.delete_annot(highlight)
removeHighlight(path, (0.3921569883823395, 0.5607839822769165, 1.0))

# showLanguageStyle = False
# showSourceIntegrationContent = False
# showCohesion = False          

# doc.save("../writerdesk1/src/highlightTest2.pdf", garbage=4, deflate=True, clean=True)