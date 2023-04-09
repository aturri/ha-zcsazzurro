[![ZCS Azzurro](https://img.shields.io/github/v/release/aturri/ha-zcsazzurro)](https://github.com/aturri/ha-zcsazzurro/releases/latest) [![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration) ![Validate with hassfest](https://github.com/aturri/ha-zcsazzurro/workflows/Validate%20with%20hassfest/badge.svg) ![Maintenance](https://img.shields.io/maintenance/yes/2023.svg) [![ZCSAzzurro_downloads](https://img.shields.io/github/downloads/aturri/ha-zcsazzurro/total)](https://github.com/aturri/ha-zcsazzurro) [![ZCSAzzurro_downloads](https://img.shields.io/github/downloads/aturri/ha-zcsazzurro/latest/total)](https://github.com/aturri/ha-zcsazzurro)

# ZCS Azzurro Integration for Home Assistant

All supported ZCS Azzurro inverters / energy meters will show a status sensor and sensors represnting generating power/energy. According to device types and installation, there are some other sensors representing the power/energy consuming, auto-consuming, charging, discharging, importing, exporting, as well as batteries charge status. Note that these sensors are disabled by default, they need to be manually enabled on device page.

This integration lets you configure an authentication to ZCS Azzurro portal and then you can add inverters through integration page on frontend.

Read more on design philosophy etc in the [Wiki](https://github.com/aturri/ha-zcsazzurro/wiki).

## Installation

Make sure you have the asked ZCS Azzurro credentials to use this integration. Contact their support and they will give you a client code and an auth key.
If you have an existing integration with the name "zcsazzurro" you are recommended to remove it before attemping to install this one.

### Preferred download method

- Use HACS, search for ZCS Azzurro integration and download it.
- Restart Home Assistant

### Manual download method

- Copy all files from custom_components/zcsazzurro in this repo to your config custom_components/zcsazzurro
- Restart Home Assistant

### Setup

First thing you have to do is to specify in your `configuration.yaml` file the credentials that are required for this integration:
```
zcsazzurro:
  auth_key: xxx
  client_code: xxx
```

After modifying this, restart Home Assistant and go to `Integrations` > `Add Integration` and select `ZCS Azzurro`. Sometimes you must refresh the browser cache to find the integration.

Pick serial number of your inverter / energy meter and insert it to complete the config flow: a new device with serial number inserted will appear. Add a new `ZCS Azzurro` config entry for each device you want to add.

### Wiki - Documentation

Documentation can be found in the [wiki](https://github.com/aturri/ha-zcsazzurro/wiki)

### Development

There are many ways to setup a development environment.

#### Dev Container
Use VS Code Dev Container. You need to have Docker installed.

1. Clone repository

    ```console
    $ git clone https://github.com/{your_user}/ha-zcsazzurro
    ```
2. Open the repository in VS Code

    ```console
    $ code ha-zcsazzurro # or code-insiders ha-zcsazzurro
    ```
3. VS Code will ask to reopen the folder in a container
    - If not, press `Cmd`/`Ctrl`+`Shift`+`P` and select `Dev Containers: Reopen in Dev Container`.
4. Wait for the container to be built.
5. Add a file `secrets.yaml` into folder `.devcontainer` with your credentials:
    ```
    zcs.authkey: xxx
    zcs.clientcode: xxx
    ```
6. Press `Cmd`/`Ctrl`+`Shift`+`P` and select `Tasks: Run Task` > `Run Home Assistant on port 9123`.
7. Wait for Home Assistant to start and go to http://localhost:9123/.
8. Walk through the Home Assistant first-launch UI.
9. Go to http://localhost:9123/config/integrations, click `Add Integration` and add the `ZCS Azzurro` integration.
10. To debug, press `F5` to attach to the Home Assistant running in the container.
11. You can enable a persistent (survives rebuild of container) config directory for Home Assistant by uncommenting the mounts statement in devcontainer.json and rebuild the container.

### Debugging and filing issues

If you find bugs or other issues please download diagnostic information from the ZCS Azzurro integration card or from the device page and attach the file to your issue report.

## Disclaimer

The package and its author are not affiliated with ZCS Azzurro. Use at your own risk.

## License

The package is released under the MIT license.
