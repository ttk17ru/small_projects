# Made by ChatGPT

import pywifi
from pywifi import const
import time

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def scan_networks():
    iface.scan()
    time.sleep(2)  # wait for scan to complete
    results = iface.scan_results()
    
    unique_ssids = {}
    for network in results:
        if network.ssid not in unique_ssids and network.ssid != "":
            unique_ssids[network.ssid] = network

    # Sort by signal strength (strongest first)
    sorted_networks = sorted(unique_ssids.values(), key=lambda x: x.signal, reverse=True)

    return sorted_networks

def display_and_connect(networks):
    with open("wifi_scan_results.txt", "w") as log:
        for network in networks:
            ssid = network.ssid
            signal = network.signal
            bssid = network.bssid
            security = "OPEN" if not network.akm else str(network.akm[0])

            log.write(f"SSID: {ssid}, Signal: {signal}, MAC: {bssid}, Security: {security}\n")
            print(f"SSID: {ssid}, Signal: {signal}, MAC: {bssid}, Security: {security}")

            if not network.akm:
                print(f"[+] Attempting to connect to OPEN network: {ssid}")
                profile = pywifi.Profile()
                profile.ssid = ssid
                profile.auth = const.AUTH_ALG_OPEN
                profile.akm.append(const.AKM_TYPE_NONE)
                profile.cipher = const.CIPHER_TYPE_NONE

                iface.remove_all_network_profiles()
                tmp_profile = iface.add_network_profile(profile)

                iface.connect(tmp_profile)
                time.sleep(5)

                if iface.status() == const.IFACE_CONNECTED:
                    print(f"[+] Successfully connected to: {ssid}")
                else:
                    print(f"[-] Failed to connect to: {ssid}")
                iface.disconnect()
                time.sleep(1)

def main():
    print("[*] Scanning for Wi-Fi networks...\n")
    networks = scan_networks()
    display_and_connect(networks)
    print("\n[*] Scan complete. Results saved to wifi_scan_results.txt")

if __name__ == "__main__":
    main()
