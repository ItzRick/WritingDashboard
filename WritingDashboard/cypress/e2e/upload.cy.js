import 'cypress-file-upload';

describe('Test the upload page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Upload"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Upload')
        cy.contains('or drag it here')
        cy.contains('Choose a file')
        cy.contains('Add')
        cy.contains('Remove')

        cy.get('[id="courseId"]')
        cy.contains('label', 'Course ID')
    })

    it('Testing file upload', () => {
        cy.get('[id="AddUploadRow"]').click()
        cy.get('[id="RemoveUploadRow"]').eq(1).click()
        cy.fixture('test.txt').then(fileContent => {
        cy.get('input[type="file"]').attachFile('test.txt');
        cy.get('[id="courseId"]')
            .type('test');
        cy.get('[id="uploadYourDocument(s)"]').click();

        cy.visit('localhost:3000/documents');
        cy.contains('test.txt');
        cy.get('[id="deletetest.txt"]').click()
        cy.get('[id="cancel"]').click()
        cy.contains('test.txt')
        cy.get('[id="deletetest.txt"]').click()
        cy.get('[id="agree"]').click()
        cy.contains('test.txt').should('not.exist')
    });
});

  })