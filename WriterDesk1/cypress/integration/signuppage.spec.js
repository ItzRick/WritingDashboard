describe('Test the signup page', () => {
    beforeEach(() => {
        cy.visit('https://localhost:3000/')
        cy.get('[id="signupButton"]')
        .click()
      })
    
    it('Checks if we are on the correct page.', () => {
        cy.url().should('include', '/SignUp')
    })

    it('Checks if all elements are present.', () => {
        cy.contains('Sign up')

        cy.get('[id="email"]')
        cy.contains('label', 'example@mail.com')

        cy.get('[id="email2"]')
        cy.contains('label', 'example@mail.com')

        cy.get('[id="password"]')
        cy.contains('label', 'Password')  

        cy.get('[id="password2"]')
        cy.contains('label', 'Password')  
    })

    it('Checks if we can add values to the textfields.', () => {
        cy.get('[id="email"]')
        .type('test@student.tue.nl')
        .should('have.value', 'test@student.tue.nl')
        cy.contains('label', 'example@mail.com')

        cy.get('[id="email2"]')
        .type('test@student.tue.nl')
        .should('have.value', 'test@student.tue.nl')
        cy.contains('label', 'example@mail.com')

        cy.get('[id="password"]')
        .type('test')
        .should('have.value', 'test')
        cy.contains('label', 'Password')  

        cy.get('[id="password2"]')
        .type('test')
        .should('have.value', 'test')
        cy.contains('label', 'Password')  
    })

    it('Checks if we can go to the login page..', () => {
        cy.contains('here').click()
        cy.url().should('include', '/Login')
        cy.contains('Log in')
    })

  })