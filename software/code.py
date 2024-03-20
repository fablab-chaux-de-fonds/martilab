# Importation des bibliothèques
import time  # Bibliothèque pour la gestion du temps
import alarm  # Bibliothèque pour la gestion des alarmes
import board  # Bibliothèque pour les broches du microcontrôleur
import busio  # Bibliothèque pour la communication sur le bus I2C
import digitalio  # Bibliothèque pour la gestion des broches numériques
import adafruit_ds1307  # Bibliothèque pour le module RTC DS1307
from DFPlayer import DFPlayer  # Importer la classe DFPlayer depuis un fichier externe

# Définir l'heure après avoir changé la pile.
# Décommentez la ligne suivante et réglez l'heure actuelle
init_time = time.struct_time((2024, 2, 8, 7, 1, 0, 0, -1, -1))

# Volume du lecteur
volume = 40

def log(message):
   try:
       with open("log.txt", "a") as f:
           current_time = rtc.datetime
           log_line = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}: {}\n".format(
               current_time.tm_year,
               current_time.tm_mon,
               current_time.tm_mday,
               current_time.tm_hour,
               current_time.tm_min,
               current_time.tm_sec,
               message
           )
           f.write(log_line)
           f.close()
   except OSError as e:
       print("Error writing to log file:", e, "\n Hints: plug GP0 to ground. More info: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger")

# Initialiser le RTC (Real-Time Clock)
# Configurer le bus IO. Plus d'informations :
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/pinouts
i2c = busio.I2C(scl=board.GP13, sda=board.GP12)

# Initialiser le RTC
rtc = adafruit_ds1307.DS1307(i2c)

# Si 'init_time' est défini, définir l'heure initiale du RTC
if 'init_time' in locals():
    rtc.datetime = init_time

# Vérifier si l'heure actuelle est entre 08:00 et 10:00 ou entre 12:00 et 14:00 ou entre 18:00 et 21:00
if 8 <= rtc.datetime.tm_hour <= 9 or 12 <= rtc.datetime.tm_hour < 14 or 18 <= rtc.datetime.tm_hour < 21:
    # print("Démarrage du lecteur")

    # Initialiser le DFPlayer
    df_player_pin = digitalio.DigitalInOut(board.GP15)  # Broche pour le contrôle du lecteur DFPlayer
    df_player_pin.direction = digitalio.Direction.OUTPUT  # Définir la direction de la broche comme sortie
    df_player_pin.value = False  # Initialiser la valeur de la broche à False
    time.sleep(5)  # Attendre 5 secondes pour laisser le DFPlayer initialiser

    dfplayer = DFPlayer(volume=volume)  # Créer une instance de la classe DFPlayer avec le volume spécifié

    # print('Allumer le lecteur DFPlayer')
    df_player_pin.direction = digitalio.Direction.OUTPUT  # Allumer le lecteur DFPlayer
    time.sleep(1)  # Attendre 1 seconde
    log("Début de la lecture")
    dfplayer.loop()  # Commencer la lecture
    time.sleep(30 * 60 * 2)  # Attendre 2h (durée de lecture du DFPlayer)
    log("Fin de la lecture")

    # print('Éteindre le lecteur DFPlayer')
    df_player_pin.direction = digitalio.Direction.INPUT  # Éteindre le lecteur DFPlayer

    # Dormir pendant 2 heures
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60 * 60 * 2)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)

else:
    # Si l'heure actuelle n'est pas dans la plage spécifiée, attendre 15 minutes
    # print("Attendre 15 minutes")
    log("Attendre 15 minutes")
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 900)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)