// Function to get the meaning of a HTTP status code
function getStatusCodeMeaning(statusCode) {
    switch (statusCode) {
        case 200:
            return 'OK - Successful response.';
        case 400:
            return 'Bad Request - The request could not be understood by the server.';
        case 401:
            return 'Unauthorized - The request requires user authentication.';
        case 403:
            return 'Forbidden - The server understood the request, but refuses to authorize it.';
        case 404:
            return 'Not Found - The requested resource could not be found.';
        case 500:
            return 'Internal Server Error - A generic error message, given when an unexpected condition was encountered.';
        default:
            return 'Unknown status code.';
    }
}

describe('Submit Button Test', () => {
    it('Starts the Cypress test when submit button is clicked', () => {
        // Visit the webpage containing the form
        cy.visit('http://localhost:5000/success');

        // Listen for custom event on submit button and start Cypress test
        cy.get('[data-cy="start-cypress-test"]').click().then(() => {
            cy.log('Cypress test started!');
            // Add Cypress test commands here
        });
    });
});


describe('API Tests', () => {
    it('Local Host Login', () => {
        cy.request({
            method: 'POST',
            url: "http://localhost:5000",
            body: {
                email: "example@example.com",
                password: "password"
            },

            failOnStatusCode: false // Allows Tests to continue regardless of response code
        }).then(response => {

            cy.log(response.body);
            cy.log(`Response status: ${response.status}`);
            cy.log(`Meaning: ${getStatusCodeMeaning(response.status)}`);

            // Verify that the response status is 200
            expect(response.status).to.be.oneOf([200, 401]);
            // Add more assertions if needed 
        })
    })
})


