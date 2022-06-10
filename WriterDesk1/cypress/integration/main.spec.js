describe('Test the homepage', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Main')
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Upload a document')
        cy.contains('Recent files')
        cy.contains('Progress')
    })

    it('Checks if we can go to the upload page.', () => {
        cy.get('[id="upload"]').click()
        cy.url().should('include', '/Upload')
        cy.contains('Upload')
    })

    it('Checks if basepage settings button allow us to go to the settings page', () => {
        cy.get('[id="settings"]').click()
        cy.url().should('include', '/settings')
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
    })

  })