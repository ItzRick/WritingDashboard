import 'cypress-file-upload';

describe('Test the documents page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="ViewDocuments"]').click()
      })

    it('Checks if we are on the correct page.', () => {
        cy.url().should('include', '/Documents')
    })

    it('Checks if all elements are present.', () => {
        cy.contains('Documents')
        cy.contains('Filename')
        cy.contains('FileType')
        cy.contains('Course')
        cy.contains('Language & Style score')
        cy.contains('Cohesion score')
        cy.contains('Structure score')
        cy.contains('Source Integration & Content score')
        cy.contains('Date')
        cy.contains('Actions')
    })

    it('Checks if we can go to the document page and delete a file.', () => {
        cy.get('[id="Upload"]').click()
        cy.get('[id="AddUploadRow"]').click()
        cy.get('[id="RemoveUploadRow"]').eq(1).click()
        cy.fixture('test.txt').then(fileContent => {
            cy.get('input[type="file"]').attachFile('test.txt');
            cy.get('[id="courseId"]')
                .type('test');
            cy.get('[id="uploadYourDocument(s)"]').click();
            cy.visit('localhost:3000/Documents')
            cy.get('[id="navigatetest.txt"]').click()
            cy.url().should('include', '/Document')
            cy.visit('localhost:3000/Documents')
            cy.get('[id="deletetest.txt"]').click()
            cy.get('[id="cancel"]').click()
            cy.contains('test.txt')
            cy.get('[id="deletetest.txt"]').click()
            cy.get('[id="agree"]').click()
            cy.contains('test.txt').should('not.exist')
        });

    })

  })
