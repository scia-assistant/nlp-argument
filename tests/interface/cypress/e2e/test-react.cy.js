describe('Tests de l’application React', () => {

  beforeEach(() => {
    cy.visit('http://localhost:8085');
  });

  it('Vérify error with bad login', () => {
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="login-error-display"]')
      .should('be.visible')
      .and('contain', 'Login or Password incorrect !');
  });

  it('Verify redirection with good login', () => {
    cy.get('[data-testid="login-username"]')
      .type('contextor')
    cy.get('[data-testid="login-password"]')
      .type('robot')

    cy.get('[data-testid="login-button"]').click();

    cy.url()
      .should('be.equal', 'http://localhost:8085/chat')

  })

  it('Verify chat communication', () => {
    cy.get('[data-testid="login-username"]')
      .type('contextor')
    cy.get('[data-testid="login-password"]')
      .type('robot')

    cy.get('[data-testid="login-button"]').click();

    cy.url()
      .should('be.equal', 'http://localhost:8085/chat')

    cy.get('[data-testid="chat-input"]')
      .type('hello')

    cy.get('[data-testid="chat-button"]').click();

    cy.get('[data-testid="message-0"]')
      .should('exist')
      .and('contain', 'hello');

    cy.get('[data-testid="message-1"]')
      .should('exist')
  })

  it('Verify redirection when token is not good', () => {
    cy.get('[data-testid="login-username"]')
      .type('contextor')
    cy.get('[data-testid="login-password"]')
      .type('robot')

    cy.get('[data-testid="login-button"]').click();

    cy.url()
      .should('be.equal', 'http://localhost:8085/chat')

    cy.window().then((w) => {
      w.localStorage.setItem('token', 'toto');
    });

    cy.get('[data-testid="chat-input"]')
      .type('hello')

    cy.get('[data-testid="chat-button"]').click();

    cy.url()
      .should('be.equal', 'http://localhost:8085/')

  })

});

