import re
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import requests
from flask import current_app
import os
from app.feedback.convertPdfToText import getPDFText



def sourceIntegration(text, references, englishStopwords):
    # Get the number of sources and number of paragraphs from the text
    # If enough: else, applicable score and explanation
    # Get the words from the text 
    # Get the words from the sources
    # TODO: apply get text from pdf
    # Calculate scores
    # Give explanations

    # Score: 
    # At least one source per 2 alineas? 
    # No: score 2, 1 per 4 alineas is 1, even less is 0.
    # Yes: sliding scale, 10% of the words of the text are also in the source: 10, 0%: 2.
    
    links, links_doi, numSources, numSourcesUsed = getUrlsSources(references)
    wordsReferences = getWordsSources(links, links_doi, englishStopwords)
    wordsFromText, numWordsText = wordsText(text, englishStopwords)


def getWordsSources(links, links_doi, englishStopwords):
    wordsReferences = set()
    for link in links:
        text = scrapePage(link)
        wordsReferences = wordsSource(text, wordsReferences, englishStopwords)
    for link_doi in links_doi:
        text = textDoi(link_doi)
        wordsReferences = wordsSource(text, wordsReferences, englishStopwords)
    
    return wordsReferences

def wordsSource(text, wordsWoStopwords, englishStopwords):
    text = re.sub('[,\.!?]', '', text)
    tokens = word_tokenize(text.lower())
    for t in tokens:
        if t not in englishStopwords:
            wordsWoStopwords.add(t)
    return wordsWoStopwords

def wordsText(text, englishStopwords):
    count = 0
    wordsWoStopwords = dict()
    text = re.sub('[,\.!?]', '', text)
    
    tokens = word_tokenize(text.lower())
    for t in tokens:
        if t not in englishStopwords:
            count += 1
            if t not in wordsWoStopwords.keys():
                wordsWoStopwords[t] = 1
            else:
                wordsWoStopwords[t] += 1

    return wordsWoStopwords, count

def countParagraphs(text):
    return text.count('\n\n') + 1

def textDoi(doi):
    userId = 123
    # basePath = os.path.join(current_app.config['UPLOAD_FOLDER'], userId)
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    basePath = os.path.join(BASEDIR, str(userId))
    tempPath = os.path.join(basePath, 'temp')
    filePath = os.path.join(tempPath, 'temp.pdf')
    if not os.path.isdir(tempPath):
        os.makedirs(tempPath)
    if downloadDoi(doi, filePath):
        text = getPDFText(filePath)
    # Delete the file if it exists and delete the folder if it is empty:
    if os.path.exists(filePath):
        os.remove(filePath)
        if not os.listdir(tempPath):
            os.rmdir(tempPath)
            if not os.listdir(basePath):
                os.rmdir(basePath)
    return text

def getUrlsSources(sourceString):
    '''
        Gets the urls of sources from a string with sources and returns the number of sources.
        Attributes:
            sources: All separate sources in an array, so sourceString split on the newline character.
            source: Individual element of the sources array.
            url: Search for https:// inside the string, so a re.match element of each link.
            url1: Retrieved the text of each url match element if there is a string in the source.
            url_doi: Search for the doi.org text inside a link, to see if we are working with a doi link.
        Arguments: 
            sourceString: String with all sources, where each source is split by a newline character.
        Returns:
            links: array with the links which do not contain the text "doi.org".
            links_doi: array with the links which do contain the text "doi.org" and therefore should be papers.
            numSources: the number of sources.
    '''
    # Get all the individual sources:
    sources = sourceString.split('\n\n')
    # Create arrays to store the results:
    links = []
    links_doi =[]
    # For each source:
    for source in sources:
        # Find the url:
        url = re.search('https?://.*', source)
        # If there is an url, look if this contains doi.org, if yes add to links_doi, else add to links:
        if not url == None:
            url1 = url.group(0)
            url_doi = re.search('.*doi.org.*', url1)
            if not url_doi == None:
                links_doi.append(url_doi.group(0))
            else: 
                links.append(url1)
    # Find the number of sources and return everything:
    numSources = len(sources)
    numSourcesUsed = len(links) + len(links_doi)
    return links, links_doi, numSources, numSourcesUsed

def downloadDoi(url, filePath):
    sci_hub_url = 'https://sci-hub.se/'
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    url = sci_hub_url + url
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    embed = soup.find(id='pdf')
    if embed:
        link = embed.get('src')
        if link:
            link = 'https:' + link
            r = requests.get(link, headers=headers)
            if r.status_code == 200:
                with open(filePath, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                return True
    return False

def scrapePage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'style'
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'link',
        'button',
        'form',
        'label',
        'amp-state', 
        'footer',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output

string = """The last decade has seen a wide spread of self-tracking technology, which allows people to collect and monitor data about themselves. This rise was enabled by technological advancements such as smaller sensors that are better and more often integrated into mobile devices, the ubiquity of access to information through the internet, and improvements in visualization techniques. As a result, self-tracking technology and systems that help people collect and reflect on their data are widely commercially available, particularly related to health and wellbeing. Examples are systems that help people keep track of sleep (Lullaby), physical fitness (Nike+, Fitbit, UbiFit), their food intake or diet (Loseit, Calorie Counter), and mood (Expereal, T2 Mood Tracker).\n
The most dedicated and well-organized community using these types of technology might be the Quantified-Self (QS) movement, seeking “self-knowledge through numbers”. This community of self-trackers and life-loggers experiments to find the best ways to collect data, and therefore insights, about themselves, and organizes 'meetups' to share knowledge and experiences. However, much more people keep track of some information about themselves than these ‘hard-core’ QS-users. In 2013, Fox and Duggan estimated that 69% of Americans keeps track of at least one health-related parameter for themselves or a loved one, and while no more recent numbers were found, we can imagine the rise in self-tracking technology has only increased this percentage. \n
All of these data, however, only become useful when it leads to better understanding, increased awareness, or the ability to make better decisions based on it. This is what the scientific field of Personal Informatics (PI) focuses on: how can technology facilitate users in the collection of personal data, and more importantly, reflection on this data, to promote behavior change towards healthier habits? In general, the PI and QS movements, therefore, have the same underlying motivation: knowing one’s data, one can learn from it, and use that new knowledge to make informed changes to one’s behavior – and eventually to reach health-related goals. Self-tracking Technology can help people to do this by enabling easy data collection, and by enabling the user to reflect on the data. For example, an activity tracker can help users to gain insight into when and how much they are active ("I'm never active on weekdays"). These insights can enable users to identify goals towards a healthier lifestyle ("I should be more active during workdays"), and find out how to change their behavior to reach these goals ("If I take a walk during my breaks, I will be active enough"). \n
However, reflection that leads to behavior change is a time-consuming and effortful process that does not happen automatically. While people using self-tracking devices often gain low-level insights, such as, when reflecting on their data, this only rarely results in the formulation of high-level health-related goals, or ways to reach these goals. This shows a gap between on the one hand the ability to collect and visualize data and on the other the ability to act upon these data and learn from it. As the main goal of self-trackers is to use their data to achieve informed behavior change, it is problematic that many users do not seem to be able to utilize their data in this way. \n
To support users in making this step from low-level insights to high-level resolutions or plans of action, the aforementioned gap needs to be bridged – by facilitating reflection. The two most influential models of Personal Informatics, lived-informatics model of PI) both name ‘Reflection’ as the step users need to make to move from examination of data to data-driven action. Additionally, Reflection is a key element of successful behavior change. Still, while different studies stress the importance of reflection and supporting it, they are not concrete about how this should be done. \n
An important first step in which reflection on data can be supported is by visualizing the self-tracked data, for example on a dashboard. Data dashboards have the potential to enhance higher-level reflections, resulting in healthy resolutions and goals, for example by reorganizing information, comparing behavior with personal goals, and by giving users the possibility to explore the data (sources). However, most dashboards are not designed with sufficient understanding of what users need to support them in this process, and simply ‘presenting’ the data is insufficient for reflection to occur. As a result, the higher-level reflection, that enables users to change their behavior, does not occur as often as it possibly could. \n
While many studies mention ideas on how to support reflection, there is little empirical evidence of the effectiveness of these suggestions. Additionally, most of these ideas mentioned in current literature are very abstract recommendations: they are not specific or validated. Thus, it is yet unclear how dashboards should be designed to effectively support users in reaching a higher level of reflection. \n
To enable users of self-tracking technology in taking informed action based on their data, it is essential to better understand how the process of reflection can be supported through dashboard design. Therefore, we will first look into what ‘reflection’ is and present an overview of reflection-supporting methods that are proposed in the literature (Chapter 2). Doing this, we will try to answer the question: “Which reflection-supporting methods are frequently described in the literature?" \n
Afterward, we will continue to evaluate the most promising of these reflection-supporting methods in practice to answer our main research question: “Can a reflection-supporting method built in a data- dashboard contribute to users reaching higher levels of reflection on their data? If so, how?”. The Method of this study will be described in Chapter 3, followed by the Results (Chapter 4), Conclusion, and Discussion (Chapter 5). """

example = """A Framework for Personal Science - Quantified Self. (n.d.). Retrieved June 17, 2021, from https://quantifiedself.com/blog/personal-science/ \n
Baumer, E. P. S. (2015). Reflective Informatics. 585–594. https://doi.org/10.1145/2702123.2702234 \n
Baumer, E. P. S., Khovanskaya, V., Matthews, M., Reynolds, L., Sosik, V. S., & Gay, G. (2014). Reviewing reflection: On the use of reflection in interactive system design. Proceedings of the Conference on Designing Interactive Systems: Processes, Practices, Methods, and Techniques, DIS, 93–102. https://doi.org/10.1145/2598510.2598598 \n
Choe, E. K., Lee, B., Kay, M., Pratt, W., & Kientz, J. A. (2015). SleepTight : Low-burden , Self-monitoring Technology for Capturing and Reflecting on Sleep Behaviors. September. https://doi.org/10.1145/2750858.2804266 \n
Choe, E. K., Lee, B., Zhu, H., Riche, N. H., & Baur, D. (2017). Understanding Self - Reflection : How People Reflect on Personal Data Through Visual Data Exploration. Proceedings of the 11th EAI International Conference on Pervasive Computing Technologies for Healthcare, 173–182. https://doi.org/10.1145/3154862.3154881 \n
Choe, E. K., Lee, N. B., Lee, B., Pratt, W., & Kientz, J. A. (2014). Understanding quantified-selfers’ practices in collecting and exploring personal data. Conference on Human Factors in Computing Systems - Proceedings, 1143–1152. https://doi.org/10.1145/2556288.2557372 \n
Cuttone, A., Petersen, M. K., & Larsen, J. E. (2014). Four data visualization heuristics to facilitate reflection in personal informatics. Lecture Notes in Computer Science (Including Subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics), 8516 LNCS(PART 4), 541–552. https://doi.org/10.1007/978-3-319-07509-9_51 \n
Epstein, D. A., Ping, A., Fogarty, J., & Munson, S. A. (2015). A lived informatics model of personal informatics. UbiComp 2015 - Proceedings of the 2015 ACM International Joint Conference on Pervasive and Ubiquitous Computing, 731–742. https://doi.org/10.1145/2750858.2804250 \n
Fleck, R., & Fitzpatrick, G. (2010). Reflecting on reflection: Framing a design landscape. ACM International Conference Proceeding Series, 216–223. https://doi.org/10.1145/1952222.1952269 \n
Fox, S., & Duggan, M. (2013). Tracking for Health. PEW Research Centre. https://www.pewresearch.org/internet/2013/01/28/tracking-for-health/ \n
Jansen, J. M., Niemantsverdriet, K., Burghoorn, A. W., Lovei, P., Neutelings, I., Deckers, E., & Nienhuijs, S. (2020). Design for co-responsibility: Connecting patients, partners, and professionals in bariatric lifestyle changes. DIS 2020 - Proceedings of the 2020 ACM Designing Interactive Systems Conference, 1537–1549. https://doi.org/10.1145/3357236.3395469 \n
Kersten-van Dijk, E. T., Westerink, J. H. D. M., Beute, F., & IJsselsteijn, W. A. (2017). Personal Informatics, Self-Insight, and Behavior Change: A Critical Review of Current Literature. Human-Computer Interaction, 32(5–6), 268–296. https://doi.org/10.1080/07370024.2016.1276456 \n
Kocielnik, R., Xiao, L., Avrahami, D., & Hsieh, G. (2018). Reflection Companion: A Conversational System for Engaging Users in Reflection on Physical Activity. Proceedings of the ACM on Interactive, 
Mobile, Wearable and Ubiquitous Technologies, 2(2), 1–26. https://doi.org/10.1145/3214273 \n
Li, I. (2010). Know Thyself : Monitoring and Reflecting on Facets of One ’ s Life. 4489–4492. \n
Li, I., Dey, A., & Forlizzi, J. (2010). A stage-based model of personal informatics systems. Conference on Human Factors in Computing Systems - Proceedings, 1(January), 557–566. https://doi.org/10.1145/1753326.1753409 \n
Li, I., Dey, A. K., & Forlizzi, J. (2011). Understanding my data, myself: Supporting self-reflection with ubicomp technologies. UbiComp’11 - Proceedings of the 2011 ACM Conference on Ubiquitous Computing, September, 405–414. https://doi.org/10.1145/2030112.2030166 \n
Mamykina, L., Mynatt, E. D., Davidson, P. R., & Greenblatt, D. (2008). MAHI: Investigation of social scaffolding for reflective thinking in diabetes management. Conference on Human Factors in Computing Systems - Proceedings, May 2014, 477–486. https://doi.org/10.1145/1357054.1357131 \n
Raj, S., Newman, M. W., Lee, J. M., & Ackerman, M. S. (2017). Understanding individual and collaborative problem-solving with patient-generated data: Challenges and opportunities. Proceedings of the ACM on Human-Computer Interaction, 1(CSCW). https://doi.org/10.1145/3134723 \n
Rapp, A., & Cena, F. (2016). Personal Informatics for Everyday Life : How Users without Prior Self-Tracking Experience Engage with Personal Data Personal informatics for everyday life : How users without prior self- tracking experience engage with personal data. Journal of Human Computer Studies, 94(December 2018), 1–17. https://doi.org/10.1016/j.ijhcs.2016.05.006 \n
Reitberger, W., Spreicer, W., & Fitzpatrick, G. (2014). Nutriflect: Reflecting collective shopping behavior and nutrition. Conference on Human Factors in Computing Systems - Proceedings, 3309–3318. https://doi.org/10.1145/2556288.2557384 \n
Rooksby, J., Rost, M., Morrison, A., & Chalmers, M. (2014). Personal Tracking as Lived Informatics. 1163–1172. \n
Wise, A. F., & Jung, Y. (2019). Teaching with analytics: Towards a situated model of instructional decision-making. Journal of Learning Analytics, 6(2), 53–69. https://doi.org/10.18608/jla.2019.62.4"""

# print(countParagraphs(string))
# english_stopwords = stopwords.words('english')
# print(wordsText('These texts can be longer, however then we must find more information etc. etc', english_stopwords))
# print(wordsSource('These texts can be longer, however then we must find more information etc. etc', set(), english_stopwords))
# print(countWordsText('These texts can be longer, however then we must find more information etc, etc', english_stopwords))
# print(getUrlsSources(example))
# print(sourceIntegration("This is some nice text, is this the correct format?",findWords("This is some nice text, is this the correct format?, some more formatting is required as is the followng format.")))
# print(wordsSource(scrape_page("https://dictionary.cambridge.org/dictionary/english/multitasking"), set(), english_stopwords))
# print(scrape_page("https://www.pewresearch.org/internet/2013/01/28/tracking-for-health/"))

# sourceIntegration(string, example, english_stopwords)
# print(textDoi('https://doi.org/10.1145/3214273'))
# print(downloadDoi('https://doi.org/10.1145/3214273', 'C:\\Users\\20192435\\Downloads\\SEP2021\\WriterDesk1\\backend\\app\\feedback\\123\\temp.pdf'))