describe('Test the signup page', () => {
    beforeEach(() => {
        cy.visit('localhost:3000/')
        cy.get('[id="signupButton"]')
        .click()
      })

    it('Checks if we are on the correct page.', () => {
        cy.url().should('include', '/SignUp')
    })

    it('Checks if all elements are present.', () => {
        cy.contains('Sign Up')

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
        const emailError = 'Must be a TU/e email-address'
        const repeatEmailError = 'Must match Email'
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

        const passWordErrorLength = 'Must contain at least 8 characters'
        const passWordErrorLower = 'Must contain at least 1 lowercase letter'
        const passWordErrorUpper = 'Must contain at least 1 uppercase letter'
        const passWordErrorNumber = 'Must contain at least 1 number'
        const repeatPassWordError = 'Must match Password'
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError).should('not.exist')

        //Password too short, repeat not the same
        cy.get('[id="password"]').clear().type('short')
        cy.contains(passWordErrorLength)
        cy.contains(repeatPassWordError)

        //Password missing lowercase
        cy.get('[id="password"]').clear().type('UPPERCASE')
        cy.contains(passWordErrorLower)
        cy.contains(repeatPassWordError)

        //Password missing uppercase
        cy.get('[id="password"]').clear().type('lowercase')
        cy.contains(passWordErrorUpper)
        cy.contains(repeatPassWordError)

        //Password missing number
        cy.get('[id="password"]').clear().type('NoNumber')
        cy.contains(passWordErrorNumber)
        cy.contains(repeatPassWordError)

        //Valid password, repeat not the same
        cy.get('[id="password"]').clear().type('ValidPass1')
        cy.contains(passWordErrorLength).should('not.exist')
        cy.contains(passWordErrorLower).should('not.exist')
        cy.contains(passWordErrorUpper).should('not.exist')
        cy.contains(passWordErrorNumber).should('not.exist')
        cy.contains(repeatPassWordError)

        //Valid password, repeat the same
        cy.get('[id="password2"]').clear().type('ValidPass1')
        cy.contains(repeatPassWordError).should('not.exist')
    })

    it('Checks if correct errors are displayed on clicking button', () => {
        //Empty fields
        cy.get('[id="password"]').clear()
        cy.contains('One or more fields are empty!').should('not.exist')
        cy.get('[id="signButton"]').click()
        cy.contains('One or more fields are empty!')

        //Non-empty invalid fields
        cy.get('[id="email"]').type('validemail@student.tue.nl')
        cy.get('[id="email2"]').type('validemail@student.tue.nl')
        cy.get('[id="password"]').type('invalidpassword')
        cy.get('[id="password2"]').type('invalidpassword')
        cy.contains('One or more fields are not complete!').should('not.exist')
        cy.get('[id="signButton"]').click()
        cy.contains('One or more fields are not complete!')
    })

    it('Checks if we can go to the login page..', () => {
        cy.contains('here').click()
        cy.url().should('include', '/Login')
        cy.contains('Log in')
    })

    it('Checks if we can create and delete an account'), () => {
        cy.get('[id="email"]').type('validemail@student.tue.nl')
        cy.get('[id="email2"]').type('validemail@student.tue.nl')
        cy.get('[id="password"]').type('validPassword1')
        cy.get('[id="password2"]').type('validPassword1')
        cy.get('[id="necData"]').click()
        cy.get('[id="signup"]').click()
        cy.get('[id="ok"]').click()
        cy.url().should('include', '/Login')
        cy.get('[id="username"]').type('validemail@student.tue.nl')
        cy.get('[id="password"]').type('validPassword1')
        cy.get('[id="login"]').click()
        cy.url().should('include', '/Main')
        cy.get('[id="settings"]').click()
        cy.get('[id="delete"]').click()
        cy.get('[id="yes"]').click()
        cy.url().should('include', '/Login')
    }

  })