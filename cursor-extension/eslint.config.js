export default [
    {
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: 'module',
            globals: {
                // VSCode extension globals
                vscode: 'readonly',
                require: 'readonly',
                module: 'readonly',
                exports: 'readonly',
                __dirname: 'readonly',
                __filename: 'readonly',
                process: 'readonly',
                Buffer: 'readonly',
                console: 'readonly',
                setTimeout: 'readonly',
                clearTimeout: 'readonly',
                setInterval: 'readonly',
                clearInterval: 'readonly'
            }
        },
        rules: {
            // Code quality rules
            'no-unused-vars': [
                'warn',
                {
                    argsIgnorePattern: '^_',
                    varsIgnorePattern: '^_'
                }
            ],
            'no-console': 'off', // Allow console for extension logging
            'no-debugger': 'warn',
            'no-alert': 'warn',

            // Style rules
            semi: ['error', 'always'],
            quotes: [
                'error',
                'single',
                {
                    allowTemplateLiterals: true,
                    avoidEscape: true
                }
            ],
            indent: [
                'error',
                4,
                {
                    SwitchCase: 1
                }
            ],
            'comma-dangle': ['error', 'never'],
            'object-curly-spacing': ['error', 'always'],
            'array-bracket-spacing': ['error', 'never'],

            // Best practices
            eqeqeq: ['error', 'always'],
            curly: ['error', 'all'],
            'brace-style': ['error', '1tbs'],
            'prefer-const': 'error',
            'no-var': 'error',

            // Error prevention
            'no-undef': 'error',
            'no-unused-expressions': 'warn',
            'no-implicit-globals': 'error',
            strict: ['error', 'never'] // Not needed in modules
        }
    }
];
