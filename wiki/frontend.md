# Frontend

## Structure

The structure of the frontend is as follows:
* Config files at the top level ([package.json](../frontend/package.json), [tsconfig.json](../frontend/tsconfig.json), [vite.config.json](../frontend/vite.config.ts), etc.)
* In the `src` directory we have: 
    - **API:** Glue code for communicating with the backend through Fetch requests
    - **Components:** Reusable components used throughout the project
    - **Contexts:** React contexts holding information for the logged in state and pdf renderer
    - **Pages:** Main pages of the webpages, each with its own folder for better clarity
    - **Tests:** Folder for tests.
    - **Utils:** Common functions in order to not have duplicated code or to not pollute other source files with unnecesary implementation details.

## Development & Build

### Development

In order to work on the frontend, assuming `conda` is installed, everything that needs to be done in order for the app to work is:
* In order to have a working backend, make sure the `.env` file in the `backend` folder is set up
* To run the project, use `make frontend` which automatically installs npm dependencies and runs the project in dev mode.

### Build

For making an optimized build for production, simply use the command:

`
    npx vite build
`

It will generate the output in the `dist` directory.

## Testing

For running the tests, run either:
* `yarn test`
* `npx react-scripts test [--watchAll=false]`
