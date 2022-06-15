describe('Test the progress page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin')
        cy.get('[id="password"]')
            .type('admin')
        cy.get('[id="loginButton"]').click()
        cy.get('[id="Progress"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Progress')
        cy.contains('Average score per skill category')
        cy.contains('Progress over time')
    })

  })