#!/usr/bin/python

### ---                              VERSIONS                              ---
# V1.0.0    29.11.2022             
#   - Installation für VPN Client implementiert
# V1.0.1    02.12.2022
#   - Funktion zum Flashen des Mikrocontrollers ergänzt
#   - Funktion zum Anlegen von Dateien überarbeitet
# V1.0.2    14.12.2022
#   - DNS Update für VPN ergänzt
### --------------------------------------------------------------------------

__author__      = "Manuel Zimmermann"
__copyright__   = "Copyright 2022, Team Gruen WST Kurs 2022"
__credits__     = []
#__license__     = ""
__version__     = "1.0.2"
__maintainer__  = "Manuel Zimmermann"
__email__       = "m.zimmermann1@oth-aw.de"
__status__      = "Developement"



import sys, os, re, argparse, apt
from pathlib import Path
from getpass import getpass
from datetime import datetime



### CONSTANTS / CONFIGURATION ###

OVPN_CONFIG = """
remote 8a770854cc89.sn.mynetname.net 443   # VPN Server-Verbindung

script-security 2
setenv PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
up /usr/bin/update-systemd-resolved
up-restart
down /usr/bin/update-systemd-resolved
down-pre

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
v28L8UheAFTYfBMnCrRRdE4HCg==
-----END ENCRYPTED PRIVATE KEY-----
"""

CLIENT_CRT = """
-----BEGIN CERTIFICATE-----
MIIF0DCCA7igAwIBAgIIFwg+Wbu2fBkwDQYJKoZIhvcNAQELBQAwajELMAkGA1UE
BhMCREUxDzANBgNVBAgMBkJheWVybjEPMA0GA1UEBwwGQW1iZXJnMQ8wDQYDVQQK
DAZQcml2YXQxDzANBgNVBAsMBlByaXZhdDEXMBUGA1UEAwwOc2Vuc29ybmV0endl
cmswHhcNMjIxMTI2MTQyNjU4WhcNMzIxMTIzMTQyNjU4WjBnMQswCQYDVQQGEwJE
RTEPMA0GA1UECAwGQmF5ZXJuMQ8wDQYDVQQHDAZBbWJlcmcxDzANBgNVBAoMBlBy
aXZhdDEPMA0GA1UECwwGUHJpdmF0MRQwEgYDVQQDDAtvcGN1YWNsaWVudDCCAiIw
DQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBALQR+FJBqSdya6g3wNFjRDh2kXKW
enkq3Gexw6FOi5r0D4dHSMkwwlLsGZceC4cO35L7uPACd9Nq14WAI5kpcLup2sxb
imbETI/VjNCyOZhpPXXUvL8QUTU/sqKqUKCeaXCocB9tIwrIRGRUQ+c51CUaoi+y
p/SAaLkatEccSiZORzncj1PShzOXZrkdxAXJhsBCxAn1H9h5ZnSV8MtEHr0ME5DT
B6CWW3O4AbXwPCaje8VL3Tby8pGeFgWDSTy2/TvxapjvneFnJ8PE1FyWO/x/aagy
VlPwY9X49/Ggb6PEh3X2CWbEb1Ev183EdLPEiPYRoCzpGJgYGpoazCutB2iuBjVA
OP7DdIo1XcjDL/W8aFoaa78mw4gisvz/p3byhUeJlRYyl5e24tw/MhzkSyJbdJUI
oyW8R68PEa3yoFHJfDCocXhivdQoe04okfOvG4jtnECikjtjZVkFZvSDXbg22s1F
1Cfb5NPPxMskrI0LD99rdNCQ2RjD4W0dFIMVPrUOSwLx/K+vi1GjfIwP1KP3pI0N
fzFZkEEEZocAHtAFjBtVNDREe1lsplPGyyus+49Zurj8qsuPeeS+BPjwThdfbunG
LpSnnq7HOJUXtr2VQnvzxwSPXVa7y8L7xFsjFwoM8D+sQIEnQyNVYowEbzWAtaqI
tAGNug2x2Ly4Yl79AgMBAAGjfTB7MBMGA1UdJQQMMAoGCCsGAQUFBwMCMB0GA1Ud
DgQWBBRXB6M7EvdPMPEUt6QGAgn6VKRwLDAfBgNVHSMEGDAWgBRpOiRJ0vhJG+sf
nGO0xaTZRn6ryzAkBglghkgBhvhCAQ0EFxYVR2VuZXJhdGVkIGJ5IFJvdXRlck9T
MA0GCSqGSIb3DQEBCwUAA4ICAQCFvqHP8jzMIfOoXccxAfxSm/JAB0wHixbBz8q/
SWZVgOB3VB3ucwC/LwegxWr/Q0sRmqG8/h9zGVvvyjyPjeWLzkzA95FYekhtZsWa
NwmMNNtPyerETT/Q0Twxy9lx5kMgF3SaZYZ8nv+QtLWzQPOxyV6qFRCJDd29aBet
CjXMMaDjE6Iz0nNwGxoRE9GkBQcyQ85Poew8ppnNYt8likzzztXM3TFT3qJQ4tkO
L6QsTI65dD8fgDr0YK1wGwTi6sOLDERsd5nGsmK7VFmdcS6CnjFWeUmIOK642NrI
xBM1+pOPut9xeCZ7bfuXXeD6SwB6BKKKLYd7hd9ZMxZJ4iR2oBvvcwr6uR0vqqTH
F8KtmOFbLQZl4g4Z3YwMkLrdv1wJRO9tx8gk/sJWBkcCkH+Yu/wL1e+HfGtqGDZW
hXNdCjSpnn0tJSC8iAd6v1YZAVfdc1VcMMF7HYKy8jeMo+unbJ5+L6mTt6SFiaC0
nLZui5kolIONvYBq51Zj4nX4Sx304+tRCOrAbIp8R48P4KTmdbdXzJf8/S6lUDFr
9AqBLZeymLItqE3gRfxQkO7I/I+BZ97H/HUoFdI8FGs4TfcARckD7z0w1fdqtAl2
+J9qOGH4YUGl7AMwC0pHQZ0OdEl6KvCpN6l2ptLh2cUyqroVTfh8MTlLNPP85Blk
kBgMCA==
-----END CERTIFICATE-----
"""

AVR_CONF = """

programmer
  id    = "pi_extension";
  desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
  type  = "linuxgpio";
  reset = 10;
  sck   = 3;
  mosi  = 2;
  miso  = 22;
;
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
def create_file(file, txt, override=False, perm=None, user=None):
    if file.is_file() and not override: raise Exception(f"Datei '{file}' existiert bereits")
    
    with file.open("w") as fh: fh.write(txt)
    if perm: os.chmod(file, perm)
    if user: os.chown(file, user, user)
    
    return file

# Öffnet eine Datei und führt darin einen REGEX-SUB aus, um den Inhalt nach einer gewissen Form anzupassen
def replace_in_file(file, rgx, replacement=""):
    with file.open("r") as fh: txt = fh.read()
    txt = rgx.sub(replacement, txt)
    with file.open("w") as fh: fh.write(txt)

# Fügt einen Text am Ende der Datei an
def append_in_file(file, txt):
    with file.open("a") as fh: fh.write(txt)

# Installiert neue Linux Packages
cache = None
def apt_install(package):
    global cache
    if cache is None:
        cache = apt.cache.Cache()
        cache.update()
        cache.open()
    
    pkg = cache[package]
    if not pkg.is_installed:
        log(f"Installiere Paket '{package}'")
        pkg.mark_install()
        cache.commit()

### END GENERAL FUNCTIONS ###



### INSTALLATION FUNCTIONS ###

def install_vpn():
    log("VPN Einrichtung gestartet")
        
    assert_is_admin() # Installation und Konfiguration benötigt Admin-Rechte (Dateien werden als Root angelegt und Permissions gesetzt)

    # systemd-resolved updater installieren
    log("Installiere Update-Resolver")
    cmd("git clone https://github.com/jonathanio/update-systemd-resolved.git")
    cmd("(cd update-systemd-resolved && make)")
    cmd("rm -r update-systemd-resolved")
    cmd("systemctl enable systemd-resolved.service") # Service autostart

    # resolvectl nutzen. Alte resolv.conf als Fallback (wenn VPN nicht connected)
    replace_in_file(Path("/etc/nsswitch.conf"), re.compile(r'(^#?hosts:.*?$)', re.M), r"hosts:          files resolve dns myhostname")
    cmd("ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf") # Neuen Dienst als DNS nutzen
    
    replace_in_file(Path("/etc/systemd/resolved.conf"), re.compile(r'(^#?Domains=.*?$)', re.M), r"Domains=sn.local")
    replace_in_file(Path("/etc/systemd/resolved.conf"), re.compile(r'(^#?DNSStubListener=.*?$)', re.M), r"DNSStubListener=no")

    log("Update-Resolver installiert")

    ### OpenVPN installieren ###
    log("Prüfe OpenVPN Installation")
    openvpn_path = Path("/etc/openvpn")
    if not openvpn_path.is_dir(): # Paket "openvpn" noch nicht installiert? -> Installieren
        log("Installiere benötigte Pakete")
        apt_install("openvpn")
        if not openvpn_path.is_dir(): raise Exception(f"VPN Einrichtung fehlgeschlagen, da OpenVPN Konfigurationsordner '{openvpn_path}' fehlt. Wurde OpenVPN richtig installiert?")
    
    ### PKI installieren ###
    log("Installiere PKI")
    ca_file     = create_file(openvpn_path.joinpath("sensornetzwerk_ca.crt"),     SERVER_CA,   True, 0o400) # Erstelle Server-CA File und setze Berechtigung
    crt_file    = create_file(openvpn_path.joinpath("sensornetzwerk_client.crt"), CLIENT_CRT,  True, 0o400) # Erstelle Client-Cert File und setze Berechtigung
    key_file    = create_file(openvpn_path.joinpath("sensornetzwerk_client.key"), CLIENT_KEY,  True, 0o400) # Erstelle Client-Key File
    decrypt_key_if_encrypted(key_file)                                                                      # Keyfile noch verschlüsselt? -> entschlüsseln

    ### Zugangsdaten einrichten ###
    log("Richte OpenVPN Zugang ein")
    vpn_user    =   input(s("VPN Benutzername:", "white", "blue")+ " ")                       
    vpn_pass    = getpass(s("VPN Passwort    :", "white", "blue")+ " ")
    secret_file = create_file(openvpn_path.joinpath(".secret"), f"{vpn_user}\n{vpn_pass}",     True, 0o400)
    cfg_file    = create_file(openvpn_path.joinpath("client.conf"),               OVPN_CONFIG, True, 0o400) # VPN Konfigurations-Datei erstellen

    ### Autostart aktivieren ###
    log("Konfiguriere Autostart")
    replace_in_file(Path("/etc/default/openvpn"), re.compile(r'#?(AUTOSTART="all")', re.M), r"\g<1>") # Autostart aktivieren
    cmd("systemctl enable openvpn@client.service")                                                    # Autostart-Service aktivieren
    cmd("systemctl daemon-reload")
    cmd("service openvpn@client start")

    log("VPN Einrichtung abgeschlossen")
    
    
    
def flash_microcontroller(hex_file):
    log("Flashen des Mikrocontrollers gestartet")
    
    assert_is_admin() # Installation und Konfiguration benötigt Admin-Rechte

    hex_file = Path(hex_file)
    if not hex_file.is_file(): raise Exception(f"Flash-Datei '{hex_file}' nicht gefunden")

    apt_install("avrdude")
    
    avr_conf_file = hex_file.parent.joinpath("avr.conf")
    if not avr_conf_file.is_file():
        log(f"Erstelle Konfigurations-Datei '{avr_conf_file}'")
        cmd(f"cp /etc/avrdude.conf '{avr_conf_file}'")
        avr_conf_file = Path(avr_conf_file)
        
        append_in_file(avr_conf_file, AVR_CONF)
        
    cmd(f"avrdude -p attiny84 -C '{avr_conf_file}' -c pi_extension -v -U '{hex_file}'")
        
        
        
        

### END INSTALLATION FUNCTIONS ###



### MAIN ###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=Path(__file__).name, description="Installationsscript zum Einrichten des Sensorknotens")
    
    parser.add_argument("-a", "--all",   action='store_true', help="Alle Pakete installieren")
    parser.add_argument("-v", "--vpn",   action='store_true', help="Installiert und Konfiguriert den VPN-Zugang")
    parser.add_argument("-f", "--flash", nargs=1,             help="Flasht eine neue Software auf den Mikrocontroller")

    args = vars(parser.parse_args())
    
    try:
        if not any(args.values()):
            parser.print_help()
            raise Exception(f"Kein Argument angegeben")
        
        # Config
        if args["flash"]: flash_microcontroller(args["flash"][0])
            
        # Installer
        if args["all"] or args["vpn"]: install_vpn()
    
    except Exception as ex: log(ex, True)
    
### END MAIN ###