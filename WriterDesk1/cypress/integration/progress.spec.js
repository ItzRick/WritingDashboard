describe('Test the progress page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Progress')
      })

    it('Checks if all elements are present.', () => {
        cy.contains('Progress')
        cy.contains('Average score per skill category')
        cy.contains('Progress over time')
    })

  })