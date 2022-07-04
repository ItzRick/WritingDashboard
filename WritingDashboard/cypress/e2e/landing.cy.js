describe('Test the frontpage', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/')
      })
    it('Checks if the name is on the site', () => {
        cy.contains('Writing')
        cy.contains('Dashboard')
    })
    it('Checks if the site displays general information', () => {
        cy.contains('Improve your academic writing.')
        cy.contains('TU/e students can improve their academic writing.')
    })
    it('Checks if we can go to the login page', () => {
        cy.get('[id="login"]')
        .click()
        cy.url().should('include', '/Login')
        cy.contains('Log in')
    })
    it('Checks if we can go to the signup page', () => {
        cy.get('[id="signup"]')
        .click()
        cy.url().should('include', '/SignUp')
        cy.contains('Sign Up')
    })
  })