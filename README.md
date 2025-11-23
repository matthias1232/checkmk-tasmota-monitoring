# Checkmk Tasmota Monitoring

This plugin enables comprehensive monitoring of Tasmota devices in Checkmk. It uses a special agent to query status information and sensor data directly from the device via the HTTP interface.

## Features

The plugin offers a wide range of monitoring options for your Tasmota devices:

### 1. Firmware & System
*   **Firmware Version:** Monitors the installed Tasmota version.
*   **Update Check:** Automatically compares the installed version with the latest release on GitHub and warns if the firmware is outdated (configurable).
*   **Build Info:** Displays the build date and OTA URL.
*   **Uptime:** Monitors the device uptime.

### 2. Power Monitoring
For devices with energy monitoring capabilities (e.g., Gosund SP111, Sonoff POW):
*   **Current Power:** Watt (W).
*   **Voltage & Current:** Volt (V) and Ampere (A).
*   **Energy Consumption:**
    *   Today (kWh)
    *   Yesterday (kWh)
    *   Total (kWh)
*   **Additional Metrics:** Apparent Power (VA), Reactive Power (VAr), and Power Factor.
*   **Thresholds:** Warning and critical thresholds for power are configurable.

### 3. Power State
*   Monitors the current status of the relay (ON/OFF).
*   **Configurable Expected State:** You can define whether the device should be permanently switched on (e.g., for fridges or servers) and trigger an alarm if it is switched off.

### 4. Environmental Sensors
Support for connected sensors (e.g., via I2C):
*   **SI7021 & SHT3x:**
    *   Temperature (°C)
    *   Humidity (% RH)
    *   Dew Point (°C)
*   Uses standard Checkmk rulesets for temperature and humidity (allowing configurable thresholds).

## Installation

1.  Package the plugin as MKP or download the ready-made file.
2.  Install the package on your Checkmk instance:
    ```bash
    mkp install tasmota_monitoring-1.0.mkp
    ```
    *(Note: The filename may vary depending on the version)*

## Configuration

1.  **Create Host:**
    *   Create a new host in Checkmk for the Tasmota device.
    *   Under **Checkmk Agent / API Integrations**, select **"Configured API integrations, no Checkmk agent"**.

2.  **Create Rule:**
    *   Go to **Setup > Agents > VM, Cloud, Container > Tasmota Special Agent**.
    *   Create a new rule.
    *   **Hostname:** Enter the IP address or DNS name of the Tasmota device.
    *   **Password:** (Optional) If you have set a web password on the Tasmota device, enter it here.

3.  **Service Discovery:**
    *   Perform a service discovery for the host. The available services (Firmware, Wattage, Sensors, etc.) should now be detected automatically.

## Requirements

*   **Checkmk Version:** 2.x (Tested with Checkmk 2.3)
*   **Network:** The Checkmk server must be able to reach the Tasmota device via HTTP (Port 80).
*   **Tasmota:** The device must be flashed with Tasmota firmware and support JSON status queries.
