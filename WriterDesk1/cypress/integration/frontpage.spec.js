describe('Test the frontpage', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/')
      })
    it('Checks if the name is on the site', () => {
        cy.contains('Writing')
        cy.contains('Dashboard')
    })
    it('Checks if the site displays general information', () => {
        cy.contains('Improve your academic writing.')
        cy.contains('TU/e students can improve their academic writing.')
    })
    it('Goes to and checks the login page', () => {
        cy.get('[name="loginButton"]')
        .contains('Log in')
        .click()

        cy.url().should('include', '/Login')
        cy.contains('Sign up')
        cy.contains('Note: the TU/e mail is the username of TU/e students.')

        cy.contains('Username:')
        // cy.get('MuiOutlinedInput-root').should('have.attr', 'Legend', 'Username')
        // cy.contains('Password:')
        
    })

  })