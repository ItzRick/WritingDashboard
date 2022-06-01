describe('Test the signup page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/')
        cy.get('[id="signupButton"]')
        .click()
      })
    
    it('Checks if we are on the correct page.', () => {
        cy.url().should('include', '/Login')
    })

    it('Checks if all elements are present.', () => {
        cy.url().should('include', '/Login')
        cy.contains('Sign up')
        cy.contains('Note: the TU/e mail is the username of TU/e students.')

        cy.contains('Username:')
        cy.get('[id="username"]')
        cy.contains('label', 'Username')

        cy.contains('Password:')
        cy.get('[id="password"]')
        cy.contains('label', 'Password')  
    })

    it('Checks if we can add values to the textfields.', () => {
        cy.url().should('include', '/Login')
        cy.contains('Sign up')
        cy.contains('Note: the TU/e mail is the username of TU/e students.')

        cy.contains('Username:')
        cy.get('[id="username"]')
        .type('test@student.tue.nl')
        .should('have.value', 'test@student.tue.nl')
        cy.contains('label', 'Username')

        cy.get('[id="password"]')
        .type('test')
        .should('have.value', 'test')
        cy.contains('label', 'Password')     
    })

    it('Checks if we get an error message.', () => {
        cy.url().should('include', '/Login')
        cy.contains('Sign up')
        cy.contains('Note: the TU/e mail is the username of TU/e students.')

        cy.contains('Username:')
        cy.get('[id="username"]')
        .type('test@student.tue.nl')
        .should('have.value', 'test@student.tue.nl')
        cy.contains('label', 'Username')

        cy.get('[id="password"]')
        .type('test')
        .should('have.value', 'test')
        cy.contains('label', 'Password') 

        cy.get('[id="loginButton"]')
        .contains('Log in')
        .click()
        cy.contains('Invalid username and/or password')       
    })

  })