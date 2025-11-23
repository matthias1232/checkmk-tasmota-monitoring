# Checkmk Tasmota Monitoring
<img width="1158" height="263" alt="image" src="https://github.com/user-attachments/assets/4035d1f2-2c66-43d4-b79b-7bef55f720d7" />

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

### 4. Supported Sensors

The following sensors and metrics are currently supported:

| Sensor Name | Monitored Metrics |
| :--- | :--- |
| **SI7021** | Temperature (°C), Humidity (% RH), Dew Point (°C) |
| **SHT3x** | Temperature (°C), Humidity (% RH), Dew Point (°C) |
| **Energy Monitor** | Power (W), Current (A), Energy Today (kWh), Energy Yesterday (kWh), Energy Total (kWh), Apparent Power (VA), Reactive Power (VAr), Power Factor |

*Note: Standard Checkmk rulesets for temperature and humidity are used, allowing for configurable thresholds.*

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
    *   Go to **Setup > Agents > Other integrations > Tasmota Special Agent**.
    *   Create a new rule.
    *   **Password:** (Optional) If you have set a web password on the Tasmota device, enter it here.

3.  **Service Discovery:**
    *   Perform a service discovery for the host. The available services (Firmware, Wattage, Sensors, etc.) should now be detected automatically.

## Requirements

*   **Checkmk Version:** 2.4 (Tested with Checkmk 2.4)
*   **Network:** The Checkmk server must be able to reach the Tasmota device via HTTP (Port 80).
*   **Tasmota:** The device must be flashed with Tasmota firmware and support JSON status queries.



## Screenshots Gui

<img width="1158" height="244" alt="image" src="https://github.com/user-attachments/assets/479ebb82-99f0-468c-be3a-3a1814330469" />
<img width="1385" height="295" alt="image" src="https://github.com/user-attachments/assets/82fb58a4-d470-48fb-878b-adec2910bd96" />
<img width="597" height="156" alt="image" src="https://github.com/user-attachments/assets/ccfc3287-8ae9-479c-9110-4920f778f5e2" />
<img width="345" height="138" alt="image" src="https://github.com/user-attachments/assets/f85decbd-ad2b-4e3f-9235-b88e9e27a2c2" />
<img width="1148" height="292" alt="image" src="https://github.com/user-attachments/assets/b8ae0e11-e8f3-41d9-956a-c7bd67551922" />
<img width="1158" height="263" alt="image" src="https://github.com/user-attachments/assets/c37decbb-82f6-45b2-bf53-898908eae55c" />
<img width="1037" height="319" alt="image" src="https://github.com/user-attachments/assets/d1a71472-c6dc-4303-a811-1f0e266efa88" />

## Screenshots Wato Config

<img width="821" height="458" alt="image" src="https://github.com/user-attachments/assets/72fc9cdb-1ed8-4d2c-8479-3aa48ff956fc" />
<img width="878" height="562" alt="image" src="https://github.com/user-attachments/assets/1ca208f0-373b-499e-b4b4-566a4795e0fb" />
<img width="843" height="545" alt="image" src="https://github.com/user-attachments/assets/01f3cb06-0276-4b02-b333-bec3b3431585" />
<img width="833" height="791" alt="image" src="https://github.com/user-attachments/assets/2289bcd7-04c0-4f11-b2be-76bff82691ea" />
<img width="858" height="867" alt="image" src="https://github.com/user-attachments/assets/27fcb208-cc8e-4fc7-ac34-69615f3279e6" />
<img width="879" height="595" alt="image" src="https://github.com/user-attachments/assets/a30336da-a6f4-4c10-a553-a40998e89a0b" />
<img width="865" height="676" alt="image" src="https://github.com/user-attachments/assets/0b3b3881-fe51-4029-9245-e923f97eb84d" />



