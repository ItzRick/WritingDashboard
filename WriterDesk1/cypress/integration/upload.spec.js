import 'cypress-file-upload';

describe('Test the upload page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin')
        cy.get('[id="password"]')
            .type('admin')
        cy.get('[id="loginButton"]').click()
        cy.get('[id="Upload"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Upload')
        cy.contains('or drag it here')
        cy.contains('Choose a file')
        cy.contains('Add')
        cy.contains('Remove')

        cy.get('[id="course"]')
        cy.contains('label', 'course')
    })

    it('Testing file upload', () => {
        cy.get('[id="add"]').click()
        cy.get('[id="remove"]').eq(1).click()
        cy.fixture('test.txt').then(fileContent => {
        cy.get('input[type="file"]').attachFile('test.txt');
        cy.get('[id="course"]')
            .type('test');
        cy.get('[id="upload"]').click();

        cy.visit('https://localhost:3000/documents');
        cy.contains('test.txt');
    });
});

  })