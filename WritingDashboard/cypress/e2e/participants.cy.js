describe('Test the participants page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Participants"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Add participants')
        cy.contains('Download user data of selected participants')
        cy.contains('Username')
        cy.contains('Project ID')
        cy.contains('Actions')
    })

  })