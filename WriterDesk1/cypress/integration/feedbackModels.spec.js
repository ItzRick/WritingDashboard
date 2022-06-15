describe('Test the feedback models page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin')
        cy.get('[id="password"]')
            .type('admin')
        cy.get('[id="loginButton"]').click()
        cy.get('[id="Feedback Models"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('To change the feedback model,' +
            ' go to github.com/XXXX and commit your changes there.')
    })

  })