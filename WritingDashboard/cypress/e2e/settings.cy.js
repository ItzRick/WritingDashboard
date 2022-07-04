describe('Test the settings page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Settings"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Settings')
        cy.contains('Data setting')
        cy.contains('Change password')
        cy.contains('Change email')
        cy.contains('Delete account')
    })

  })