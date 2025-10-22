from machine import Pin, ADC
from ws2812 import WS2812
import utime, random

# --- Couleurs ---
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN  = (0, 255, 0)
CYAN   = (0, 255, 255)
BLUE   = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE  = (255, 255, 255)
COLORS = (WHITE, PURPLE, BLUE, CYAN, GREEN, YELLOW, RED)

# --- Capteurs et LED ---
SOUND_SENSOR = ADC(1)
led = WS2812(18, 1)

# --- Paramètres ---
DELAY_MS = 150
THRESHOLD = 4         # plus sensible (valeur typique : 4 à 8)
ALPHA = 0.05             # moins de lissage = plus réactif
LOG_INTERVAL_MS = 60000  # 1 minute
MIN_BEAT_INTERVAL = 500  # 0.25 s = 240 BPM max

last_time = utime.ticks_ms()
prev_noise = SOUND_SENSOR.read_u16() / 256
last_beat_time = None

# --- Suivi BPM ---
bpm_values = []
last_log_time = utime.ticks_ms()

# --- Lissage ---
def smooth(value, prev, alpha):
    return prev * (1 - alpha) + value * alpha

while True:
    raw = SOUND_SENSOR.read_u16() / 256
    noise = smooth(raw, prev_noise, ALPHA)
    diff = abs(noise - prev_noise)
    prev_noise = noise

    # --- Détection d'un pic sonore ---
    if diff > THRESHOLD:
        now = utime.ticks_ms()
        interval_since_last = utime.ticks_diff(now, last_beat_time) if last_beat_time else 9999

        # On valide un battement seulement si suffisamment espacé
        if interval_since_last > MIN_BEAT_INTERVAL and utime.ticks_diff(now, last_time) > DELAY_MS:
            if last_beat_time is not None:
                interval = utime.ticks_diff(now, last_beat_time)
                if interval > 0:
                    bpm = 60000 / interval
                    bpm_values.append(bpm)
                    print(f"BPM détecté : {bpm:.1f}")
            last_beat_time = now

            # Changement de couleur
            color = random.choice(COLORS)
            led.pixels_fill(color)
            led.pixels_show()
            print("Changement de couleur 🎵")

            last_time = now

    # --- Toutes les minutes, calculer et enregistrer la moyenne ---
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_log_time) >= LOG_INTERVAL_MS:
        if bpm_values:
            avg_bpm = sum(bpm_values) / len(bpm_values)
            print(f"Moyenne BPM (1 min) : {avg_bpm:.1f}")
            try:
                with open("bpm_log.txt", "a") as f:
                    f.write(f"{utime.localtime()}: {avg_bpm:.1f} BPM\n")
                print("Valeur enregistrée dans bpm_log.txt ✅")
            except Exception as e:
                print("Erreur d’écriture dans le fichier :", e)
            bpm_values = []  # reset pour la prochaine minute
        last_log_time = now

