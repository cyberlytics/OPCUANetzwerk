#!/usr/bin/python

__author__      = "Manuel Zimmermann"
__copyright__   = "Copyright 2022, Team Gruen WST Kurs 2022"
__credits__     = []
#__license__     = ""
__version__     = "1.0.0"
__maintainer__  = "Manuel Zimmermann"
__email__       = "m.zimmermann1@oth-aw.de"
__status__      = "Developement"

import sys, os, re, argparse
from pathlib import Path
from getpass import getpass
from datetime import datetime

### CONSTANTS / CONFIGURATION ###

OVPN_CONFIG = """
remote 8a770854cc89.sn.mynetname.net 443   # VPN Server-Verbindung

proto tcp-client                           # TCP Protokoll
dev tun                                    # Layer 3 OSI Netzwerk
nobind                                     # Dynamischer Lokaler Port

resolv-retry infinite                      # Wenn Netzwerkverbindung verloren geht -> Dauerhaft versuchen neu zu verbinden
persist-key                                # Bei Neustart versuchen, Key und Adapter beizubehalten
persist-tun 

tls-client                                 # SSL Verschlüsselte Verbindung
ca "sensornetzwerk_ca.crt"                 # Zertifikat CA
cert "sensornetzwerk_client.crt"           # Client Public Key 
key "sensornetzwerk_client.key"            # Client Private Key
remote-cert-tls server                     # Server-Zertifikat prüfen
auth-user-pass .secret                     # Zusätzliche Authentifizierung Via Username/Passwort
auth SHA512                                # Authentifizierung via SHA1

cipher AES-256-CBC                         # AES256 CBC Verschlüsselung benutzen
pull                                       

ping 10                                    # Verbindung alle 10 Sek via Ping prüfen
verb 3                                     # Loglevel 3
"""

SERVER_CA = """
-----BEGIN CERTIFICATE-----
MIIFvjCCA6agAwIBAgIIWjQgT74eMDAwDQYJKoZIhvcNAQELBQAwajELMAkGA1UE
BhMCREUxDzANBgNVBAgMBkJheWVybjEPMA0GA1UEBwwGQW1iZXJnMQ8wDQYDVQQK
DAZQcml2YXQxDzANBgNVBAsMBlByaXZhdDEXMBUGA1UEAwwOc2Vuc29ybmV0endl
cmswHhcNMjIxMTI2MTMwMTM3WhcNMzIxMTIzMTMwMTM3WjBqMQswCQYDVQQGEwJE
RTEPMA0GA1UECAwGQmF5ZXJuMQ8wDQYDVQQHDAZBbWJlcmcxDzANBgNVBAoMBlBy
aXZhdDEPMA0GA1UECwwGUHJpdmF0MRcwFQYDVQQDDA5zZW5zb3JuZXR6d2VyazCC
AiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBANctwgiN0lotiGMvC7KAvKYd
OPl3Ea73K7VAi3BpGfMnAhlCaEr+/KuVOIt6mVf1JM/gBa+uuB3RhyT/yepJ0EYm
HTmysIz2jLhPRuwpOb4X6LgQ1GYix85tzPqnFqA6HfVlp6iSjW0E1nvscNdNLLnL
alSltHnN/aNIw2awucvS5eXrbY9wpMp+laWXqcxO6Vr2SK1omn2NIibYgBKfw25t
/s8pP45DjE6wc2TB3k1rdBHoGMWglfJbJERtZxzbW2nPj1raRVHpxI5PPlPECwqG
1IttIxH7pB8l1cWtZiaiqx0idistlNAK15FEbxRnbdIxUDsjKEmXc7qHI10HtJ/1
teWkXD5qbRzX48KnuTrCtheocM9HPYF5Rl/IBJHcvB69DbumiXJ9ASEvqwXwilxC
Nia2t/dHrKbzRsa4VbV8YUJZgX4kXmb/cUQikJsfjK1yYMntWfNukQRQOWOd07IX
8sq663EqIW5EeuxpyUGGGmmFjwtrFKk9uRoI7yAUjXuYos2G2et0Z9kRsVHGKzqy
AMaGIHPSfkh3DBCS4pwqKJ6/Cf2zJsC5aAyVKUjq2ysSJKK3kTTFzfvNDUhJW4li
k74iB7IXdb0ysiTC+1AAaMrRblTgErDtRhmDjeT9TsIEidQIGGQUsSbzTdwJ/c4o
/UV1TabKrmfUOv/NJlB/AgMBAAGjaDBmMA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0P
AQH/BAQDAgEGMB0GA1UdDgQWBBRpOiRJ0vhJG+sfnGO0xaTZRn6ryzAkBglghkgB
hvhCAQ0EFxYVR2VuZXJhdGVkIGJ5IFJvdXRlck9TMA0GCSqGSIb3DQEBCwUAA4IC
AQAxrf96Ny17uDtKoD/oNpKO+dt2DiO5HcscjmpdDG7F11wfC1zMo+nFesUAffgz
0275m3SA2FZIoqAjzlSmDigg9cYPh0mQ5EIVwx7A99CIB7v32mggzV2+gFuWA/e2
sH7DXCToDHAZNj5KUGuDbp648Io9yt5Z50tf/wdGrcnYFj1lje6leMJhaXKxpyHF
zsxmdNsVdqzmxuwjw16UMJrzDe3i/H662FpoIAFjSU2S5qDU78/e5CFTY+qLnIif
r4y8qh2JDKiCuxzrXo4O2fX5k/NseJYbrkELCJDZyyIv4H8pDBKC4KO+Qp5gYUFp
IWmNZ4qHtlFE0O5DiqWa5/nTdSeYIkMf4YQNind6dBoH//zQARxdEFyqNuVtXzcV
J0PkRf7LXFhrFXb1qjhyJrlK53CmNBovHIYGLQZlTeYIOvm0DChHnrrE35I8Z8hm
5zbfO7+sUeLlMDSM7iH2s2XbIuOc4B3wdPc1053E3Uld+00MbmUr9/0H3zByEixS
+v1o0z5I9Emg/zjNgcKLeBlpRb0ZDLVTwA38BfCiM8TtrUhzAyCoIU+siCmaSd9a
8azYG19YTXfqlsySYSeD00UZaI2HKHUBdY90PgaqenyfjikVP19zsC+/qF5zSMK6
EVDNNmIIf7gb6vzxQZiAWo8+fV80hZROHoYAo8vPJLkYpA==
-----END CERTIFICATE-----
"""

CLIENT_KEY = """
-----BEGIN ENCRYPTED PRIVATE KEY-----
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
iczf/vSzc6mb3yA8LqyvUju5jw==
-----END ENCRYPTED PRIVATE KEY-----
"""

CLIENT_CRT = """
-----BEGIN CERTIFICATE-----
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
gA==
-----END CERTIFICATE-----
"""

### END CONSTANTS / CONFIGURATION ###



### GENERAL FUNCTIONS ###

# Fancy Textausgabe auf der Konsole
def s(txt, fg="default", bg="default", style="default"):
    fg_colors = { "black" : 30, "red" : 31, "green" : 32, "yellow" : 33, "blue" : 34, "magenta" : 35, "cyan" : 36, "white" : 37, "default" : 39 }    
    if fg not in fg_colors: raise Exception(f"Unbekannte Vordergrundfarbe: '{fg}'. Verfügbar: {list(fg_colors.keys())}")
    fg = fg_colors[fg]
    
    bg_colors = { "black" : 40, "red" : 41, "green" : 42, "yellow" : 43, "blue" : 44, "magenta" : 45, "cyan" : 46, "white" : 47, "default" : 49 }    
    if bg not in bg_colors: raise Exception(f"Unbekannte Hintergrundfarbe: '{bg}'. Verfügbar: {list(bg_colors.keys())}")
    bg = bg_colors[bg]
    
    styles = { "bold" : 1, "underline" : 4, "blink" : 5, "inverse" : 7, "default" : 0 }    
    if style not in styles: raise Exception(f"Unbekannter Style: '{style}'. Verfügbar: {list(styles.keys())}")
    style = styles[style]

    return f"\033[{style};{fg};{bg}m{txt}\033[m"

# Zeigt eine formatierte Lognachricht auf der Konsole an
def log(txt, is_error=False):
    if is_error: sys.stderr.write(f">>> [{datetime.now():%H:%M:%S}] " + s("Fehler:", "white", "red", "bold") + " " + s(txt, "red", style="bold") + "\n")
    else: print(f">>> [{datetime.now():%H:%M:%S}]: {txt}")

# Führt einen Shell-Befehl aus. Wenn [error] == True, wird der Rückgabewert des Befehls geprüft. Ist dieser nicht OK, wird ein Fehler geworfen
def cmd(c, error=True):
    ret = os.system(c)
    if error and ret != 0: raise Exception(f"Befehl '{c}' konnte nicht ausgeführt werden. Fehler: {ret}")
    return ret

# Prüft, ob die aktuelle Instanz als Admin ausgeführt wird. Wirft alternativ einen Fehler
def assert_is_admin():
    if os.geteuid() != 0: raise Exception(f"Script muss mit Root-Rechten ausgeführt werden")
    
# Prüft, ob ein Private-Key verschlüsselt ist
def check_if_encrypted(file):
    with file.open("r") as fh: return "BEGIN ENCRYPTED PRIVATE KEY" in fh.read() 

# Prüft, ob ein Privat-Key verschlüsselt ist. Falls Ja, wird der User mit einer Prompt informiert und eine Passwortabfrage gestartet.
# Es wird [retries] Mal versucht, die Datei zu entschlüsseln. Alternativ wird ein Fehler geworfen
def decrypt_key_if_encrypted(key_file, retries=3):
    is_encrypted = check_if_encrypted(key_file)
    if not is_encrypted: return;
    
    log(f"Private-Key ist verschlüsselt '{key_file}'")
    
    for i in range(retries):
        keyfile_pass = getpass(s(f"Schlüssel      :", "white", "blue")+ " ")
        cmd(f"openssl rsa -in '{key_file}' -passin pass:'{keyfile_pass}' -out '{key_file}'", error=False)
        is_encrypted = check_if_encrypted(key_file)
        if not is_encrypted: break
        
    if is_encrypted: raise Exception(f"'{key_file}' konnte nicht entschlüsselt werden")
    else: log(f"Private-Key erfolgreich entschlüsselt")

# Erstellt eine Datei [file] und fügt den Inhalt [txt] ein. Existiert diese bereits und wurde keine Überschreibungsberechtigung [override] gesetzt,
# wird ein Fehler geworfen. Zusätzlich wird die Berechtigung [perm] gesetzt
def create_file(file, txt, override=False, perm="400"):
    if file.is_file() and not override: raise Exception(f"Datei '{file}' existiert bereits")
    
    with file.open("w") as fh: fh.write(txt)
    cmd(f"chmod {perm} '{file}'")
    return file

# Öffnet eine Datei und führt darin einen REGEX-SUB aus, um den Inhalt nach einer gewissen Form anzupassen
def replace_in_file(file, rgx, replacement=""):
    with file.open("r") as fh: txt = fh.read()
    txt = rgx.sub(r"\g<1>", txt)
    with file.open("w") as fh: fh.write(txt)

### END GENERAL FUNCTIONS ###



### INSTALLATION FUNCTIONS ###

def install_vpn():
    log("VPN Einrichtung gestartet")
        
    assert_is_admin() # Installation und Konfiguration benötigt Admin-Rechte (Dateien werden als Root angelegt und Permissions gesetzt)

    ### OpenVPN installieren ###
    log("Prüfe OpenVPN Installation")
    openvpn_path = Path("/etc/openvpn")
    if not openvpn_path.is_dir(): # Paket "openvpn" noch nicht installiert? -> Installieren
        log("Installiere benötigte Pakete")
        cmd(f"apt-get install openvpn -y")
        if not openvpn_path.is_dir(): raise Exception(f"VPN Einrichtung fehlgeschlagen, da OpenVPN Konfigurationsordner '{openvpn_path}' fehlt. Wurde OpenVPN richtig installiert?")
    
    ### PKI installieren ###
    log("Installiere PKI")
    ca_file     = create_file(openvpn_path.joinpath("sensornetzwerk_ca.crt"),     SERVER_CA,   True, "400") # Erstelle Server-CA File und setze Berechtigung
    crt_file    = create_file(openvpn_path.joinpath("sensornetzwerk_client.crt"), CLIENT_CRT,  True, "400") # Erstelle Client-Cert File und setze Berechtigung
    key_file    = create_file(openvpn_path.joinpath("sensornetzwerk_client.key"), CLIENT_KEY,  True, "400") # Erstelle Client-Key File
    decrypt_key_if_encrypted(key_file)                                                                      # Keyfile noch verschlüsselt? -> entschlüsseln

    ### Zugangsdaten einrichten ###
    log("Richte OpenVPN Zugang ein")
    vpn_user    =   input(s("VPN Benutzername:", "white", "blue")+ " ")                       
    vpn_pass    = getpass(s("VPN Passwort    :", "white", "blue")+ " ")
    secret_file = create_file(openvpn_path.joinpath(".secret"), f"{vpn_user}\n{vpn_pass}",     True, "400")
    cfg_file    = create_file(openvpn_path.joinpath("client.conf"),               OVPN_CONFIG, True, "400") # VPN Konfigurations-Datei erstellen

    ### Autostart aktivieren ###
    log("Konfiguriere Autostart")
    replace_in_file(Path("/etc/default/openvpn"), re.compile(r'#?(AUTOSTART="all")', re.M), r"\g<1>") # Autostart aktivieren
    cmd("systemctl enable openvpn@client.service")                                              # Autostart-Service aktivieren
    cmd("systemctl daemon-reload")
    cmd("service openvpn@client start")

    log("VPN Einrichtung abgeschlossen")

### END INSTALLATION FUNCTIONS ###



### MAIN ###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=Path(__file__).name, description="Installationsscript zum Einrichten des Servers")
    
    parser.add_argument("-a", "--all", action='store_true', help="Alle Pakete installieren")
    parser.add_argument("-v", "--vpn", action='store_true', help="Installiert und Konfiguriert den VPN-Zugang")

    args = vars(parser.parse_args())
    
    try:
        if not any(args.values()):
            parser.print_help()
            raise Exception(f"Kein Argument angegeben")
            
        if args["all"] or args["vpn"]: install_vpn()
    
    except Exception as ex: log(ex, True)
    
### END MAIN ###