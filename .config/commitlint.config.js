// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'chore', 'refactor']],
    'scope-empty': [2, 'never'],
    'subject-case': [2, 'never', ['sentence-case']]
  },
};
