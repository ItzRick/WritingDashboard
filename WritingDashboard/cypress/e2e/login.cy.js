describe('Test the login page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/')
        cy.get('[id="login"]')
        .click()
      })

    it('Checks if we are on the correct page.', () => {
        cy.url().should('include', '/Login')
    })

    it('Checks if all elements are present.', () => {
        cy.contains('Log in')
        cy.contains('Note: the TU/e mail is the username of TU/e students.')

        cy.contains('Username:')
        cy.get('[id="username"]')
        cy.contains('label', 'Username')

        cy.contains('Password:')
        cy.get('[id="password"]')
        cy.contains('label', 'Password')
    })

    it('Checks if we can add values to the textfields.', () => {
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
        cy.contains('Username:')
        cy.get('[id="username"]')
        .type('test@student.tue.nl')
        .should('have.value', 'test@student.tue.nl')
        cy.contains('label', 'Username')

        cy.get('[id="password"]')
        .type('test')
        .should('have.value', 'test')
        cy.contains('label', 'Password')

        cy.get('[id="login"]')
        .contains('Log in')
        .click()
        cy.contains('Invalid username and/or password')
    })

    it('Checks if we can go to the signup page.', () => {
        cy.contains('here').click()
        cy.url().should('include', '/SignUp')
        cy.contains('Sign Up')
    })

    //Requires the database to have an user with both the username and password set to admin
    it('Checks whether we can log in.', () => {
        cy.get('[id="username"]')
            .type('admin@tue.nl')
        cy.get('[id="password"]')
            .type('AdminPass1')
        cy.get('[id="login"]')
            .click()
        cy.url().should('include', '/Main')
    })

  })
