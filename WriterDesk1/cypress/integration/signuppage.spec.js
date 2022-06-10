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

    it('Checks if correct error messages are displayed', () => {
        const emailError = 'Must be a TUe email!'
        const repeatEmailError = 'Does not match Email!'
        cy.contains(emailError).should('not.exist')
        cy.contains(repeatEmailError).should('not.exist')

        //Invalid email, repeat not the same
        cy.get('[id="email"]').type('invalidemail')
        cy.contains(emailError)
        cy.contains(repeatEmailError)

        //Invalid email, repeat the same
        cy.get('[id="email2"]').type('invalidemail')
        cy.contains(emailError)
        cy.contains(repeatEmailError).should('not.exist')

        //Valid email
        cy.get('[id="email"]').type('validemail@student.tue.nl')
        cy.contains(emailError).should('not.exist')

        const passWordErrorLength = 'Must be at least 8 characters!'
        const passWordErrorUpper = 'Must contain at least 1 uppercase letter!'
        const passWordErrorNumber = 'Must contain at least 1 number!'
        const repeatPassWordError = 'Does not match Password!'
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError).should('not.exist')

        //Password too short, repeat not the same
        cy.get('[id="password"]').type('short')
        cy.contains(passWordErrorLength)
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError)

        //Password missing uppercase
        cy.get('[id="password"]').type('lowercase')
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorUpper)
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError)

        //Password missing number
        cy.get('[id="password"]').type('NoNumber')
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber)
        cy.contains(repeatPassWordError)

        //Valid password, repeat not the same
        cy.get('[id="password"]').type('ValidPass1')
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError)

        //Valid password, repeat the same
        cy.get('[id="password2"]').type('ValidPass1')
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError).should('not.exist')
    })

    it('Checks if correct errors are displayed on clicking button', () => {
        //Empty fields
        cy.contains('One or more fields are empty!').should('not.exist')
        cy.contains('Sign Up').click()
        cy.contains('One or more fields are empty!')

        //Non-empty invalid fields
        cy.get('[id="email"]').type('validemail@student.tue.nl')
        cy.get('[id="email2"]').type('validemail@student.tue.nl')
        cy.get('[id="password"]').type('invalidpassword')
        cy.get('[id="password2"]').type('invalidpassword')
        cy.contains('One or more fields are invalid!').should('not.exist')
        cy.contains('Sign Up').click()
        cy.contains('One or more fields are invalid!')

        //Valid fields, existing user

    })

    it('Checks if we are brought to the login page after registration', () => {
        cy.get('[id="email"]').type('validemail@student.tue.nl')
        cy.get('[id="email2"]').type('validemail@student.tue.nl')
        cy.get('[id="password"]').type('Validpass1')
        cy.get('[id="password2"]').type('Validpass1')
        cy.contains('Sign Up').click()
        .then(() =>{
            //After request
            cy.url().should('include', '/Login')
            cy.contains('Log in')
        })
    })

    it('Checks if we can go to the login page..', () => {
        cy.contains('here').click()
        cy.url().should('include', '/Login')
        cy.contains('Log in')
    })

  })