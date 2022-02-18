# Wiki

## Deployment

Currently, we can deploy by pushing the `main` branch to the production server.
The production remote can be found at address `smartforms.ml`, same with the application.

### Prerequisites
A one time setup is needed to  configure the remote branch

1. Add the production git remote with the command:
    ```bash
    git remote add production ssh://deployer@smartforms.ml:22/home/deployer/Production/SmartForms-GitBare/smart-forms.git
    ```

### Deploying
To manually deploy just do the following steps:

1. Checkout to the `main` branch
    ```bash
    git checkout main    
    ```

2. Push to the production remote
    ```bash
    git push production main
    ```

### Notes
If you manually deploy, then if you did not setup a ssh key to be recognized, you will have to enter the password for user `deployer`
