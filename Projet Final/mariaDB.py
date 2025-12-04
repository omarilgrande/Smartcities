from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from TablesMariaDB import Image, Battrie, Wifi, CamParametre
import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as client
from datetime import datetime
import time
import os
import base64

print(">>> Classe Image chargee depuis :", Image.__module__)
print(">>> Colonnes :", [c.key for c in Image.__table__.columns])

engine = create_engine("mariadb+mariadbconnector://martin:1234@192.168.2.58:3306/RPG", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
id_bat = session.query(Battrie.id).order_by(Battrie.id.desc()).first()
session.close()
update=False

# Variables pour la reconstruction d'image
image_chunks = []          
dernier_wifi = {}
dernier_cam = {}
nom_image_courante = None
image_en_reception = False   

def envoyerParametresVersESP32():
    global dernier_wifi, dernier_cam
    session = Session()

    # RÃ©cupÃ©rer les derniers paramÃ¨tres Wi-Fi
    wifi = session.query(Wifi).order_by(Wifi.id.desc()).first()
    if wifi:
        data_wifi = {
            "ssid": wifi.ssid,
            "password": wifi.pasword
        }
        if data_wifi != dernier_wifi:
            print("Envoi des paramÃ¨tres Wi-Fi :")
            cli.publish("B3/MartinOmar/parametre/wifi/ssid", str(wifi.ssid))
            print(f"ssid = {wifi.ssid}")
            cli.publish("B3/MartinOmar/parametre/wifi/password", str(wifi.pasword))
            print(f"password = {wifi.pasword}")
            dernier_wifi = data_wifi.copy()
    else:
        print("Aucun paramÃ¨tre Wi-Fi trouvÃ© en base.")

    # RÃ©cupÃ©rer les derniers paramÃ¨tres camÃ©ra
    cam = session.query(CamParametre).order_by(CamParametre.id.desc()).first()
    if cam:
        data_cam = {
            "resolution": cam.resolution,
            "brightness": cam.brightness,
            "contrast": cam.contrast,
            "saturation": cam.saturation,
            "quality": cam.quality,
            "mirror": cam.mirror,
            "flip": cam.flip
        }
        if data_cam != dernier_cam:
            print("\nEnvoi des paramÃ¨tres camÃ©ra :")
            cli.publish("B3/MartinOmar/parametre/camera/resolution", str(cam.resolution))
            cli.publish("B3/MartinOmar/parametre/camera/brightness", str(cam.brightness))
            cli.publish("B3/MartinOmar/parametre/camera/contrast", str(cam.contrast))
            cli.publish("B3/MartinOmar/parametre/camera/saturation", str(cam.saturation))
            cli.publish("B3/MartinOmar/parametre/camera/quality", str(cam.quality))
            cli.publish("B3/MartinOmar/parametre/camera/mirror", str(cam.mirror))
            cli.publish("B3/MartinOmar/parametre/camera/flip", str(cam.flip))
            print("ParamÃ¨tres camÃ©ra envoyÃ©s.")
            dernier_cam = data_cam.copy()
    else:
        print("Aucun paramÃ¨tre camÃ©ra trouvÃ© en base.")

    session.close()

# Callbacks MQTT
def fctTopicBattrie(ud, c, m):
    global id_bat
    id_bat = request.form.get("id_im", 0)  # valeur par defaut 0
    try:
        id_bat = int(id_bat)
    except ValueError:
        id_bat = 0  # securite si la valeur n'est pas un nombre
    id_bat += 1
    pourc = m.payload.decode()
    date_reception = datetime.now()

    session = Session()
    maBattrie = Battrie(idb=id_bat, poucentage=pourc, date=date_reception)
    session.add(maBattrie)
    session.commit()
    session.close()

    print(f"Batterie: {m.payload.decode()}")


def fctTopicImage(ud, c, m):
    global id_im, image_chunks, nom_image_courante, image_en_reception

    topic = m.topic
    payload = m.payload

    if topic == "B3/MartinOmar/image/start":
        nom_image_courante = payload.decode().strip()
        image_chunks = []
        image_en_reception = True
        print(f"Debut reception de {nom_image_courante}")

    elif topic == "B3/MartinOmar/image/data":
        try:
            image_chunks.append(payload.decode())
            print(f"Morceau recu ({len(payload)} octets)")
        except Exception as e:
            print("Erreur lors du traitement d'un morceau :", e)

    elif topic == "B3/MartinOmar/image/end" and image_en_reception:
        session = Session()
        last = session.query(Image.idi).order_by(Image.idi.desc()).first()
        id_im = (last[0] if last else 0) + 1

        dossier_destination = r"/home/martin/Desktop/smartcities/static/images"
        os.makedirs(dossier_destination, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        nom_fichier_unique = f"image_{timestamp}.jpg"
        chemin_complet = os.path.join(dossier_destination, nom_fichier_unique)

        try:
            image_finale = base64.b64decode("".join(image_chunks))
            with open(chemin_complet, "wb") as f:
                f.write(image_finale)

            print(f"Image terminee : {chemin_complet} ({len(image_finale)} octets)")

            monImage = Image(
                idi=id_im,
                path=chemin_complet,
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            session.add(monImage)
            session.commit()

        except Exception as e:
            print("Erreur lors de la reconstruction :", e)
        finally:
            session.close()
            image_chunks = []
            nom_image_courante = None
            image_en_reception = False

    else:
        print("Paquet recu hors contexte image.")

        
def fctTopicUpdate(ud, c, m):
    global update

    topic = m.topic
    payload = m.payload
    if topic == "B3/MartinOmar/parametre/camera/update":update=True



# Connexion MQTT
cli = client.Client()
cli.connect("192.168.2.58", 1883)

cli.subscribe("B3/MartinOmar/parametre/battrie")
cli.subscribe("B3/MartinOmar/image/start")
cli.subscribe("B3/MartinOmar/image/data", qos=1)  # QoS 1 : garantit la rÃ©ception
cli.subscribe("B3/MartinOmar/image/end")

cli.message_callback_add("B3/MartinOmar/parametre/battrie", fctTopicBattrie)
cli.message_callback_add("B3/MartinOmar/image/start", fctTopicImage)
cli.message_callback_add("B3/MartinOmar/image/data", fctTopicImage)
cli.message_callback_add("B3/MartinOmar/image/end", fctTopicImage)
cli.message_callback_add("B3/MartinOmar/parametre/camera/update", fctTopicUpdate)


cli.loop_start()

while True:
    print("Je suis dans ma boucle")
    if update==True:
        envoyerParametresVersESP32()
        update=False
    time.sleep(5)

cli.loop_stop()

