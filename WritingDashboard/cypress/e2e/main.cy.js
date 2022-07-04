describe('Test the homepage', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        Cypress.on('uncaught:exception', (err, runnable) => {
            return false
        })
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Upload a document')
        cy.contains('View documents')
        cy.contains('Progress')
    })

    it('Checks if we can go to the documents page.', () => {
        cy.get('[id="ViewDocuments"]').click()
        cy.url().should('include', '/Documents')
        cy.contains('Documents')
    })

    it('Checks if we can go to the progress page.', () => {
        cy.get('[id="progressLink"]').click()
        cy.url().should('include', '/Progress')
        cy.contains('Progress')
    })

    it('Checks if we can go to the upload page.', () => {
        cy.get('[id="UploadDocument"]').click()
        cy.url().should('include', '/Upload')
        cy.contains('Upload')
    })

    it('Checks if basepage settings button allow us to go to the settings page', () => {
        cy.get('[id="settings"]').click()
        cy.url().should('include', '/Settings')
        cy.contains('Settings')
    })

    it('Checks if navigation drawer works', () => {
        cy.get('[id="Upload"]').click()
        cy.url().should('include', '/Upload')
        cy.contains('Upload')

        cy.get('[id="Main"]').click()
        cy.url().should('include', '/Main')
        cy.contains('Homepage')

        cy.get('[id="Progress"]').click()
        cy.url().should('include', '/Progress')
        cy.contains('Progress')

        cy.get('[id="Documents"]').click()
        cy.url().should('include', '/Documents')
        cy.contains('Documents')

        cy.get('[id="Participants"]').click()
        cy.url().should('include', '/Participants')
        cy.contains('Participants')

        cy.get('[id="Feedback Models"]').click()
        cy.url().should('include', '/FeedbackModels')
        cy.contains('Feedback Models')

        cy.get('[id="Users"]').click()
        cy.url().should('include', '/Users')
        cy.contains('Users')

        cy.get('[id="Projects"]').click()
        cy.url().should('include', '/Projects')
        cy.contains('Projects')
    })

  })