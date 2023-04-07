[![ZCS Azzurro](https://img.shields.io/github/v/release/aturri/ha-zcsazzurro)](https://github.com/aturri/ha-zcsazzurro/releases/latest) [![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration) ![Validate with hassfest](https://github.com/aturri/ha-zcsazzurro/workflows/Validate%20with%20hassfest/badge.svg) ![Maintenance](https://img.shields.io/maintenance/yes/2023.svg) [![ZCSAzzurro_downloads](https://img.shields.io/github/downloads/aturri/ha-zcsazzurro/total)](https://github.com/aturri/ha-zcsazzurro) [![ZCSAzzurro_downloads](https://img.shields.io/github/downloads/aturri/ha-zcsazzurro/latest/total)](https://github.com/aturri/ha-zcsazzurro)

# ZCS Azzurro Integration for Home Assistant


...

## Installation

...

### Preferred download method

- Use HACS, search for ZCS Azzurro integration and download it.
- Restart Home Assistant

### Manual download method

- Copy all files from custom_components/zcsazzurro in this repo to your config custom_components/zcsazzurro
- Restart Home Assistant

### Setup

Goto `Integrations` > `Add Integration` and select `ZCS Azzurro`. Sometimes you must refresh the browser cache to find the integration.

...

### Wiki - Documentation

Documentation (at least some...) can be found in the [wiki](https://github.com/aturri/ha-zcsazzurro/wiki)

### Development

There are many ways to setup a development environment.

#### Dev Container
One option is to use the VS Code Dev Container. You need to have Docker installed.

1. Clone repository

    ```console
    $ git clone https://github.com/{your_user}/ha-zcsazzurro
    ```
1. Open the repository in VS Code

    ```console
    $ code ha-zcsazzurro # or code-insiders ha-zcsazzurro
    ```
1. VS Code will ask to reopen the folder in a container
    - If not, press `Cmd`+`Shift`+`P` and select `Dev Containers: Reopen in Dev Container`.
1. Wait for the container to be built.
1. Press `Cmd`+`Shift`+`P` and select `Tasks: Run Task` > `Run Home Assistant on port 9123`.
1. Wait for Home Assistant to start and go to http://localhost:9123/.
1. Walk through the Home Assistant first-launch UI.
1. Go to http://localhost:9123/config/integrations, click `Add Integration` and add the `ZCS Azzurro` integration.
1. To debug, press `F5` to attach to the Home Assistant running in the container.
1. You can enable a persistent (survives rebuild of container) config directory for Home Assistant by uncommenting the mounts statement in devcontainer.json and rebuild the container.

#### Without a Dev Container
Alternatively, you can run Home Assistant directly on your machine. The following procedure works fine in the hands of the maintainer developing with VS Code on macOS.

- Make sure you have at least python3.9 installed.
- Create a fork on github

```
$ git clone https://github.com/{your_user}/ha-zcsazzurro
$ cd ha-zcsazzurro
$ make install_dev
```

Home Assistant has defined a code style. Run `make lint` before pushing your changes to align with the peferred style.

There are many ways to test the integration, three examples are:

- run Home Assistant in the development container as described above

- copy all files in `custom_comonents/ha-zcsazzurro` to `custom_components/ha-zcsazzurro` in your HA configuration directory
- mount `custom_components/ha-zcsazzurro` into a HA development container

### Debugging and filing issues

If you find bugs or other issues please download diagnostic information from the ZCS Azzurro integration card or from the device page and attach the file to your issue report.


## Disclaimer

The package and its author are not affiliated with ZCS Azzurro. Use at your own risk.

## License

The package is released under the MIT license.
