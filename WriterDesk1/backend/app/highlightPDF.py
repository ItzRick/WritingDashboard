import fitz
from structureCheck import getExplanationsStructure
import re

doc = fitz.open('../writerdesk1/src/example6.pdf')

text = ('Turtles is very cool animals, is that true? They can swim, but they can also walk. They are almost like humans.\n'
    'This is an spelling mistake about turtles. This is another thing about turtles including a speling mistake about turtles. '
    'This is an apple, this is any fruit, this is an mistake. '
    'This is a very long paragraph that contains no interesting information about turtles. '
    'This is a very long paragraph that contains no interesting information '
    'about turtles. This is a very long paragraph that contains no interesting information about turtles. '
    'This is a very long paragraph that contains no interesting information about turtles. This is a very '
    'long paragraph that contains no interesting information about turtles. This is a very long paragraph '
    'that contains no interesting information about turtles. This is a very long paragraph that contains no '
    'interesting information about turtles. This is a very long paragraph that contains no interesting information '
    'about turtles. This is a very long paragraph that contains no interesting information about turtles. This is a '
    'very long paragraph that contains no interesting information about turtles. This is a very long paragraph that '
    'contains no interesting information about turtles. This is a very long paragraph that contains no interesting '
    'information about turtles. This is a very long paragraph that contains no interesting information about turtles. '
    'This is a very long paragraph that contains no interesting information about turtles.')

showStructure = False
showLanguageStyle = True

if showStructure:
    structureExplanations = getExplanationsStructure(text)

    for key in structureExplanations.keys():
        
        for page in doc:
            text = key
            text_instances = page.search_for(text)

        for inst in text_instances:
            highlight = page.addHighlightAnnot(inst)
            highlight.setColors({"stroke":(100/255, 143/255, 255/255)})        
            highlight.update()

if showLanguageStyle:
    languageStyleExplanations = (
        [
            ['is', 'Turtles is very cool animals, is that true?', 'Use "are" instead of "is".', ['are'], 0],
            ['an', 'This is an spelling mistake about turtles.', 'Use "a" instead of "an".', ['a'], 0],
            ['speling', 'This is another thing about turtles including a speling mistake about turtles.', 'Use "spelling" instead of "speling".', ['spelling'], 0],
            ['an', 'This is an apple, this is any fruit, this is an mistake.', 'expl...', ['a'], 2],
        ]
        , 6.6)

    for mistake in languageStyleExplanations[0]:
        sentence = mistake[1]
        word = mistake[0]

        for page in doc:
            sentence_instances = page.search_for(sentence)
            word_instances = page.search_for(word)

        for i in sentence_instances:
            highlight = page.addRectAnnot(i)
            highlight.setColors({"stroke":(0/255, 0/255, 0/255)})
            highlight.update()

            wordsInSentence = []
            for j in word_instances:
                if j[1] >= i[1] and j[3] <= i[3] and j[0] >= i[0] and j[2] <= i[2]: 
                    wordsInSentence.append(j)
                    # this should be removed
                    scaledRect = fitz.Rect(j[0] + 2.5, j[1] + 1.5, j[2] - 2.5, j[3] - 1.5)
                    #highlight = page.addHighlightAnnot(j)
                    highlight = page.addHighlightAnnot(scaledRect)
                    highlight.setColors({"stroke":(120/255, 94/255, 240/255)})   
                    highlight.update()

            if len(wordsInSentence) <= mistake[4]:
                continue

            # highlight = page.addHighlightAnnot(wordsInSentence[mistake[4]])
            # highlight.setColors({"stroke":(120/255, 94/255, 240/255)})   
            # highlight.update()







        # for inst in word_instances:
        #     highlight = page.addRectAnnot(inst)
        #     highlight.setColors({"stroke":(0/255, 0/255, 0/255)})
        #     highlight.update()

            # for instance in word_instances:
            #     if instance[1] >= inst[1] and instance[3] <= inst[3] and instance[0] >= inst[0] and instance[2] <= inst[2]:
            #         for m in re.finditer(word, text):
            #             #print('m', m)
            #             location = m.start()
            #             #print(location)
            #             if location == mistake[4]:
            #                 #print(location)
            #             #print('instance', instance)
            #             #print(page.get_textbox(instance))
            #             # print("hallo")
            #             # print(instance)
            #                 highlight = page.addHighlightAnnot(instance)
            #                 highlight.setColors({"stroke":(120/255, 94/255, 240/255)})   
            #                 highlight.update()
                    

doc.save("../writerdesk1/src/highlightTest2.pdf", garbage=4, deflate=True, clean=True)