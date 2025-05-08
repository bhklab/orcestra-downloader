# CHANGELOG


## v0.11.2 (2025-05-08)


## v0.11.1 (2025-05-08)

### Bug Fixes

- Bug that still tried to download dataset if it had a missing link
  ([#6](https://github.com/bhklab/orcestra-downloader/pull/6),
  [`aef881f`](https://github.com/bhklab/orcestra-downloader/commit/aef881f35fe68e9bd5382c824e118ac4c2a7ece9))

* fix: Correct dependency key formatting in pixi.toml

* dont format

- Correct dependency key formatting in pixi.toml
  ([`ed610ec`](https://github.com/bhklab/orcestra-downloader/commit/ed610ecc84f889b8a19ca66cbb8b2d578a39d8f9))

### Chores

- Update pixi lockfile ([#3](https://github.com/bhklab/orcestra-downloader/pull/3),
  [`fddf528`](https://github.com/bhklab/orcestra-downloader/commit/fddf5280d237b26996bf60ed137f0763fd1bc0c2))

Co-authored-by: jjjermiah <44614774+jjjermiah@users.noreply.github.com>


## v0.11.0 (2024-12-13)

### Chores

- Update readme
  ([`44d2f59`](https://github.com/bhklab/orcestra-downloader/commit/44d2f590d26840ac001e04c3cc7cec7b32bbef11))

### Features

- Improve CLI help text and dataset naming conventions
  ([#2](https://github.com/bhklab/orcestra-downloader/pull/2),
  [`4ee9b57`](https://github.com/bhklab/orcestra-downloader/commit/4ee9b57649a9f53f7cbe5dbf2e9b1777f691c893))

* feat: improve help + table naming

* enhancement: enhance CLI help text and add epilog for issue reporting

closes #1


## v0.10.0 (2024-12-11)

### Features

- Add media task command for GIF updates in pixi.toml
  ([`5a99552`](https://github.com/bhklab/orcestra-downloader/commit/5a995525b7a1abd1c448df3a7dcfac090aeb0bc3))

- Add PyPI badges to README for versioning and download statistics
  ([`b28bf5c`](https://github.com/bhklab/orcestra-downloader/commit/b28bf5ccb231f59142d13bb9a5c00351da2a6a8f))

- Add usage examples and GIF to README, and update pixi.toml for media features
  ([`c536650`](https://github.com/bhklab/orcestra-downloader/commit/c536650dba21200658fbd15fe4bd3587306d0725))


## v0.9.0 (2024-12-11)

### Features

- Update command name in CLI for improved clarity
  ([`31f9d98`](https://github.com/bhklab/orcestra-downloader/commit/31f9d988cac74b2b25d16dafc9d3e611804f150b))


## v0.8.0 (2024-12-11)

### Features

- Update Python version support to include 3.10 and 3.11 in workflows and dependencies
  ([`f3fa34b`](https://github.com/bhklab/orcestra-downloader/commit/f3fa34b45c8b076693fda67eba6d7305a0600509))


## v0.7.0 (2024-12-11)

### Chores

- Format
  ([`27ada75`](https://github.com/bhklab/orcestra-downloader/commit/27ada758a5f7aa4c3194c296f68af87ba617fd34))

### Features

- Add support for 'radiomicsets' dataset and enhance dataset download functionality with timeout
  handling
  ([`e5eb513`](https://github.com/bhklab/orcestra-downloader/commit/e5eb513680e62aff652de9da040848d055aa2c86))


## v0.6.0 (2024-12-10)

### Features

- Enhance CLI help formatting for dataset commands
  ([`83e68be`](https://github.com/bhklab/orcestra-downloader/commit/83e68be43575e8bf501849f5c150b94391c8805c))

- Enhance dataset download functionality with support for multiple datasets and default directory
  ([`48ae456`](https://github.com/bhklab/orcestra-downloader/commit/48ae456ce42b9066e67d0df4a9ce696ab255fb49))


## v0.5.0 (2024-12-10)

### Features

- Add RadiomicSet model, and enhance caching functionality
  ([`2340670`](https://github.com/bhklab/orcestra-downloader/commit/2340670fb5f2a64060aa74f9043782edbc129f6c))

- Enhance dataset management commands with optional dataset name and summary printing
  ([`d20afd7`](https://github.com/bhklab/orcestra-downloader/commit/d20afd7d158f82488de8c822e7cd3556da37c060))

- Update cache response handling in tests to include name parameter
  ([`b2f99db`](https://github.com/bhklab/orcestra-downloader/commit/b2f99db22a0e330e2fc61a407e3956a5f6401454))


## v0.4.0 (2024-12-10)

### Features

- Add documentation build and publish workflows with mkdocs
  ([`08b93e9`](https://github.com/bhklab/orcestra-downloader/commit/08b93e9130a4cf84f28ad5a971931b316b18e2d3))

- Add mike dependency for documentation and update CI workflow for quality control
  ([`dff42bd`](https://github.com/bhklab/orcestra-downloader/commit/dff42bd2d4e123b748697a4522ee6982870243bb))


## v0.3.0 (2024-12-10)

### Features

- Scaffold download entry point
  ([`1a0b295`](https://github.com/bhklab/orcestra-downloader/commit/1a0b295515d08349e78f2331bd06ca16676d4e77))


## v0.2.1 (2024-12-10)

### Bug Fixes

- Update CI workflow to use matrix for Python version and environment variable in Publish-To-PyPi
  job
  ([`593cb33`](https://github.com/bhklab/orcestra-downloader/commit/593cb3339b9617e36dd2b3198b82f0035c4c9f55))


## v0.2.0 (2024-12-10)

### Bug Fixes

- Refactor CI workflow to use matrix for environment variable and streamline setup
  ([`09a3944`](https://github.com/bhklab/orcestra-downloader/commit/09a3944904bf542265b69b8cb6dc645a8abd29fc))

- Simplify CI workflow by removing commented-out steps and updating release command in pixi.toml
  ([`8178bca`](https://github.com/bhklab/orcestra-downloader/commit/8178bca3cb5c27546357dac03f3fba53ff280306))

- Update cache response retrieval to include name parameter and adjust CI environment
  ([`e1b5577`](https://github.com/bhklab/orcestra-downloader/commit/e1b5577f6059ab6804b79f782e7dd05c3132c51c))

- Update CI workflow environment to 'quality' and adjust command execution
  ([`1cdcd39`](https://github.com/bhklab/orcestra-downloader/commit/1cdcd39a276ccfb59357b676c93fd0e652bc434e))

- Update CI workflow to use matrix for environment variable and streamline deployment process
  ([`cddbbb4`](https://github.com/bhklab/orcestra-downloader/commit/cddbbb4c3ab7ce4d168a2cd170dd2d09fcdf9ce9))

- Update CI workflow to use Python 3.13 environment
  ([`d99a9d2`](https://github.com/bhklab/orcestra-downloader/commit/d99a9d271d18ffed3d1320da79812638b790aae3))

- Update release command in CI workflow to use matrix environment variable
  ([`e0b0635`](https://github.com/bhklab/orcestra-downloader/commit/e0b063539867f52e0abc38e6e180a63aef82f4cf))

- Update semantic-release commands in pixi.toml to specify configuration file
  ([`23f7b25`](https://github.com/bhklab/orcestra-downloader/commit/23f7b2552a4a524878bad38a8423467c4dff0fe5))

- Update sha256 checksum for orcestra-downloader in pixi.lock
  ([`f259f13`](https://github.com/bhklab/orcestra-downloader/commit/f259f136efe078444d2e7d245517183955021761))

### Features

- Add CI/CD workflow and update development environment features in pixi.toml
  ([`49d0eac`](https://github.com/bhklab/orcestra-downloader/commit/49d0eac80638b5cdc1adc169a4fd38416b9d2d12))

- Add ToxicoSet and XevaSet models with JSON parsing and summary printing
  ([`e780e9d`](https://github.com/bhklab/orcestra-downloader/commit/e780e9da764c5d0ee398626b4ae5d8e8c63286d4))

- Enhance CLI with pretty printing options and improve usage documentation
  ([`b186135`](https://github.com/bhklab/orcestra-downloader/commit/b186135a62bd150116229daf5ed0d4891f1a1894))

- Implement logging configuration and data models for dataset handling
  ([`3e273e9`](https://github.com/bhklab/orcestra-downloader/commit/3e273e94bfa7807da740c517ea8e602be2357298))

- Update CLI structure and add dataset management commands with logging configuration
  ([`6d85aab`](https://github.com/bhklab/orcestra-downloader/commit/6d85aab15f97b7c7345e086a5fcefd479c603197))

### Refactoring

- Clean up code formatting and remove unused main module and tests
  ([`112242b`](https://github.com/bhklab/orcestra-downloader/commit/112242b6e90b918a26e57596f3840d68d41bd402))


## v0.1.0 (2024-12-09)

### Bug Fixes

- Add error handling and logging for PharmacoSet filtering in cli function
  ([`fe9bd24`](https://github.com/bhklab/orcestra-downloader/commit/fe9bd24ab58b4ed0afe15959974ad432d5390d54))

- Update Python version badge URL in README for correct reference
  ([`4cf06d9`](https://github.com/bhklab/orcestra-downloader/commit/4cf06d9ab5e1dff5c3cd300f75cc9d5c5f87920f))

### Chores

- Comment out Python version badge in README and add empty hatch.toml file
  ([`92df07a`](https://github.com/bhklab/orcestra-downloader/commit/92df07a12d1c0da68ef53b3d51483811802cbccd))

- Update repository references from jjjermiah to bhklab in documentation and configuration files
  ([`1df233a`](https://github.com/bhklab/orcestra-downloader/commit/1df233a6ba93751615f2b3f830dd9ebec28a027d))

### Features

- Add initial implementation of PharmacoSet downloader with caching and API integration
  ([`c197552`](https://github.com/bhklab/orcestra-downloader/commit/c1975520a1cfe51c2041950bf6320507aaf8ffd7))

- Enhance PharmacoSet caching and API fetching logic
  ([`ebb679d`](https://github.com/bhklab/orcestra-downloader/commit/ebb679d6e0b4cfc159147ac49632ef5ac13cf657))

- Enhance PharmacoSetManager with filtering and table printing capabilities
  ([`5d1a9f9`](https://github.com/bhklab/orcestra-downloader/commit/5d1a9f9116fe1b59bbda1f18bf625e8bbe3b54c4))

### Refactoring

- Rename package from orcestradownloader to orcestra-downloader for consistency
  ([`debbbf7`](https://github.com/bhklab/orcestra-downloader/commit/debbbf779e63d2d044833cffe02c432647aa766d))
