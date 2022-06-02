from WriterDesk1.backend.languageAndStyle import feedbackLanguageStyle


def testFeedbackLanguageAn():
    mistakes, score = feedbackLanguageStyle("This is an sentence with a mistake.")
    assert 0 <= score <= 10
    assert mistakes[0][0] == "an"
    assert mistakes[0][1] == "This is an sentence with a mistake."
    assert len(mistakes) == 1


def testFeedbackLanguageEmpty():
    mistakes, score = feedbackLanguageStyle('')
    assert score == 0
    assert len(mistakes) == 0


def testFeedbackLanguageMultipleSentences():
    mistakes, score = feedbackLanguageStyle("Hello, My name is Susan. I'm forteen and I life in germany.")
    assert 0 <= score <= 10

    assert mistakes[0][0] == "forteen"
    assert "fourteen" in mistakes[0][4]

    assert mistakes[1][0] == "life"
    assert "live" in mistakes[1][4]

    assert mistakes[2][0] == "germany"
    assert "Germany" in mistakes[2][4]

    assert len(mistakes) == 3


def testFeedbackLanguageMissingLetter():
    mistakes, score = feedbackLanguageStyle("The computr was hot and overheated.")
    assert 0 <= score <= 10

    assert mistakes[0][0] == "computr"
    assert mistakes[0][1] == "The computr was hot and overheated."
    assert "computer" in mistakes[0][4]

    assert len(mistakes) == 1


def testFeedbackLanguagePerfectSentence():
    mistakes, score = feedbackLanguageStyle("Are you opening the door?")
    assert score == 10

    assert len(mistakes) == 0

