describe('Test the users page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Users"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Users')
        cy.contains('Download user data of selected users')
        cy.contains('Username')
        cy.contains('Role')
        cy.contains('Actions')
    })

  })