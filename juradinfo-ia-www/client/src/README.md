# Welcome / ASN-WEBAPP

## Description

Welcome ! asn-webapp is a NLP application to annotate documents, built with `Reactjs` and `NodeJs`.

## Getting started

### Prerequisites

#### IDE

You can choose the IDE you whant, but you need to have some packages installed with it like `ESLint` for the live linter, and some `React` packages to get autocompletion, ...
Here an exemple of the needed packages with Visual Studio Code IDE:

- `Reactjs code snippets`
- `ESLint`

#### Node / Npm / Yarn

Since it's a JS-Based project, due to ReactJs & express you need to install some stuff on your computer:

- macOS:
  Install [Homebrew](https://brew.sh) as package manager and install the following dependencies:

```bash
brew install node
brew install npm
```
---
- Windows:
  Note that you can't run iOS app on windows.
  Install [Chocolatey](https://chocolatey.org) as package manager and install the following dependencies:

```bash
choco install -y nodejs.install python2 jdk8 npm
```
---
- Linux:
  Follow the [install instructions for your linux distribution](https://nodejs.org/en/download/package-manager/) to install Node 8 or newer and npm.
---
- Yarn:
```bash
npm install -g yarn
```

### Install the project

First you need to clone the repository.
  Do not forget to upload your SSH Key into gitlab and having the right access.

```bash
git clone git@gitlab.com:hpringault/asn-webapp.git
```

```bash
cd asn-webapp && yarn
```

### Run it

When everything is installed, if you want to run it, do the following:

server :
```bash
yarn start-app
```

client on linux:
```bash
yarn start
```

client on windows:
```bash
yarn start-on-windows
```
**NOTE :**
```bash
before running the server and the client please make sure to :
1. setup the file "default.json" in 'asn-webapp/config' to point to your local postgresql DB
2. If you want to point to the production DB make sure to have the
   VPNfortiClient connect to the ASN server.

by default the file point to the production DB.
```

### Deployment

Please read [DEPLOYMENT](./docs/DEPLOYMENT.md) for details on our deployment process on the ASN server.


### Test it

when everything is installed and run well, if you want to run every unit tests, do the following:

```bash
yarn test
```

## Documentation

if you want to know everything about the application just run:

```bash
TODO
```

## Contributing

Please read [CONTRIBUTING](./docs/CONTRIBUTING.md) for details on our code of conduct, and the process for pushing new features/patch

## Versioning

```bash
TODO
```

## Authors

* **Junique Virgile** - *Initial contributor* - [Junique Virgile](https://github.com/werayn)
* **Mezrani Amine** - *Initial contributor* - [Mezrani Amine](https://github.com/Amezrani)


## License

This project is completely private.