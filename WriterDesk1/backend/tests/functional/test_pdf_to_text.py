from app.convertPdfToText import getPDFText
import os

def testGetPDFReferences(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text, references = getPDFText('referenceFile.pdf', returnReferences=True)
    assert text == '''Donec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum. Quisque condimentum cursus pharetra. Phasellus rutrum molestie dictum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nunc faucibus lobortis tortor non hendrerit. '''
    assert references == '''A Framework for Personal Science - Quantified Self. (n.d.). Retrieved June 17, 2021, from https://quantifiedself.com/blog/personal-science/ \nBaumer, E. P. S. (2015). Reflective Informatics. 585–594. https://doi.org/10.1145/2702123.2702234 \nBaumer, E. P. S., Khovanskaya, V., Matthews, M., Reynolds, L., Sosik, V. S., & Gay, G. (2014). Reviewing reflection: On the use of reflection in interactive system design. Proceedings of the Conference on Designing Interactive Systems: Processes, Practices, Methods, and Techniques, DIS, 93–102. https://doi.org/10.1145/2598510.2598598 '''

def testGetPDFImages(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('imageFile.pdf')
    assert text == '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat laoreet lacus id elementum. Nunc sagittis commodo ipsum, a scelerisque odio viverra ac. Nullam id congue leo, condimentum hendrerit nibh. Ut pulvinar diam ut dignissim malesuada. \nDonec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum. Quisque condimentum cursus pharetra. '''

def testGetPDFList(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('listFile.pdf')
    assert text == '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat laoreet lacus id elementum. Nunc sagittis commodo ipsum, a scelerisque odio viverra ac. Nullam id congue leo, condimentum hendrerit nibh. Ut pulvinar diam ut dignissim malesuada. \nLorum \nIpsum \nDonec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum. Quisque condimentum cursus pharetra. '''

def testGetPDFTable(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('tableFile.pdf')
    assert text == '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat laoreet lacus id elementum. Nunc sagittis commodo ipsum, a scelerisque odio viverra ac. Nullam id congue leo, condimentum hendrerit nibh. Ut pulvinar diam ut dignissim malesuada. \nDonec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum. Quisque condimentum cursus pharetra. '''

def testGetPDFEmptyFile(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('emptyFile.pdf')
    assert text == ''


def testGetPDFCorruptedFile(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('corruptedFile.pdf')
    assert text == ''


def testGetPDFInvalidFile(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('invalidFileName.pdf')
    assert text == ''


def testGetPDFInvalidExtension(testClient):
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getPDFText('invalidFileExtension.docx')
    assert text == ''
