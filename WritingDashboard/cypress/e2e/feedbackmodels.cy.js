describe('Test the feedback models page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/Login')
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]').click()
        cy.get('[id="Feedback Models"]').click()
      })

    it('Checks if all elements are present.', () => {
        cy.contains('To change the feedback model, go to https://github.com/ItzRick/WritingDashboard, ' +
            'create a new branch and change the code there. To change the feedback model, ' +
            'go to the WriterDesk1/backend/app/feedback/generateFeedback folder and change any of the feedbackmodels. ' +
            'These models are located inside the CohesionFeedback, IntegrationContentFeedback, LanguageStyleFeedback ' +
            'and StructureFeedback folders. It may also be necessary to make changes to the BaseFeedback class. ' +
            'Do not forget to change the feedbackversion to a higher number in the FEEDBACKVERSION variable in ' +
            'WriterDesk1/backend/config.py file. When you are done create test cases inside the ' +
            'WriterDesk1/backend/tests/feedbackModels folder. Then create a pull request and apply ' +
            'all feeedback of the reviewer. The current feedback model version is: 0.01.')
    })

    it('Checks if we can go to the github page', () => {
        cy.get('[id="link"]').click()
        cy.url().should('include', 'github')
    })

  })