describe('Test the participants page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin')
        cy.get('[id="password"]')
            .type('admin')
        cy.get('[id="loginButton"]').click()
        cy.get('[id="Participants"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Add participants')
        cy.contains('Download participants')
        cy.contains('Download user data')
        cy.contains('Download selected participants')
        cy.contains('Download user data of selected participants')

        cy.get('[id="project-add-participants"]')
        cy.contains('label', 'Project')

        cy.get('[id="project-down-participants"]')
        cy.contains('label', 'Project')
    })

  })