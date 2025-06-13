export default {
    '*.py': ['ruff check --fix --unsafe-fixes', 'ruff format'],
    '*.{js,jsx,ts,tsx}': ['eslint --fix', 'prettier --write'],
    '*.{json,md,yml,yaml,css,scss}': ['prettier --write'],
    '*.sh': ['shfmt -w']
    // lint-staged automatically stages changes after running commands
};
