describe('Test the participants page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Participants')
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Add participants')
        cy.contains('Download participants')
        cy.contains('Download user data')
        cy.contains('Download selected participants')
        cy.contains('Download user data of selected participants')

        cy.get('[id="projectName"]')
        cy.contains('label', 'Project name')

        cy.get('[id="projectName2"]')
        cy.contains('label', 'Project name')

        cy.get('[id="projectName3"]')
        cy.contains('label', 'Project name')

        cy.get('[id="startDate"]')
        cy.contains('label', 'Start date')

        cy.get('[id="endDate"]')
        cy.contains('label', 'End date')
    })

  })