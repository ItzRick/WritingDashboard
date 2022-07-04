describe('Test the progress page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Progress"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Progress')
        cy.contains('Average score per skill category')
        cy.contains('Progress over time')
    })

  })