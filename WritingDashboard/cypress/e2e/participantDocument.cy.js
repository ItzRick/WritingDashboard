import 'cypress-file-upload';

describe('Test if researcher can see participant documents', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        cy.get('[id="username"]')
            .type('part_3')
        cy.get('[id="password"]')
            .type('PartPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Upload"]').click()
    })

    it('Testing if researcher can see participant documents', () => {
        cy.fixture('test.txt').then(fileContent => {
            cy.get('input[type="file"]').attachFile('test.txt');
            cy.get('[id="course"]')
                .type('test');
            cy.get('[id="upload"]').click();

            cy.visit('https://localhost:3000/documents');
            cy.contains('test.txt');
        });
        cy.get('[id="settings"]').click()
        cy.get('[id="logout"').click()
        cy.url().should('include', '/Login')
        cy.get('[id="username")]')
            .type('researcher@tue.nl')
        cy.get('[id="password"]').type('ResearcherPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="documentspart_3"]').click()
        cy.get('id="deletetest.txt"]').click()
    })
})