describe('Test the feedback models page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/FeedbackModels')
      })

    it('Checks if all elements are present.', () => {
        cy.contains('To change the feedback model,' +
            ' go to github.com/XXXX and commit your changes there.')
    })

  })