describe('Test the participants page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Projects"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Add project')
        cy.contains('Projects')
        cy.contains('Project name')
        cy.contains('Nr. of participants')
        cy.contains('Actions')
    })

  })