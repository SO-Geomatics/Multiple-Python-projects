"""
Copyright (c) 2025 [SO-Geomatics, Simeon Oppliger]

Permission is hereby granted, free of charge, to any person obtaining a copy...

French: ce script lit tous les fichiers [mp3] situés dans le répertoire et tous les sous-répertoires,
puis crée un affichage graphique qui permet la lecture de votre musique
"""

from tkinter import Tk, Frame, Label, Button, YES
import pygame.mixer as pgMix
import random
import time
import threading
import os
import sys

def list_all_mp3(directory):
    # Lister tous les fichiers .mp3 dans ce répertoire
    from pathlib import Path

    repertoire = Path(directory)

    files = repertoire.rglob("*.mp3", )

    lst_files_path = []
    for f in files:

        f = str(f).replace("\\", "/")

        lst_files_path.append(f)

    return lst_files_path

def launch_play_thread(ordered = False, prev = False):
    # thread pour continuer la lecture à la fin de la musique
    global thread
    thread = threading.Thread(target=play_musique_aleatoire, kwargs={'prev':prev})
    thread.start()

# Création de la fonction qui va lire la musique
def play_musique_aleatoire(ordered = False, prev = False):
    global son, titre, pgMix

    pgMix.init()
    print(stop_thread.is_set())
    while not stop_thread.is_set():
        print(stop_thread.is_set())
        # Choix d'un morceau du répertoire, enlever dans liste de lecture, ajout dans historique
        if not prev:
            titre =  random.choice(modifiable_list_mp3_sounds)
            modifiable_list_mp3_sounds.remove(titre)
            history_list_mp3_sounds.append(titre)
        else:
            if len(history_list_mp3_sounds) < 1:
                pass
            else:
                modifiable_list_mp3_sounds.append(titre)
                titre = history_list_mp3_sounds[-1]
                history_list_mp3_sounds.remove(titre)

        try:
            short_titre = " ".join(titre.split('/')[-1].split(' ')[1:])
        except:
            short_titre = " ".join(titre.split('/')[-1])

        print(f"Le titre lu est: {short_titre}")
        label_title2.config(text = short_titre)

        # Initialisation de la musique et play
        son = pgMix.Sound(titre)
        son.play()

        while pgMix.get_busy():
            print('en lecture...)')
            time.sleep(2.0)

        try:
            son.stop()
            pgMix.stop()
        except:
            pass

def play_selector():
    """Lance la lecture de la musique"""


    # Si une musique est déjà en lecture
    if 'son' in globals():
        pgMix.unpause()

    # Si aucune musique n'est encore en lecture
    else:
        # Initialisation liste de sons
        global modifiable_list_mp3_sounds, history_list_mp3_sounds
        modifiable_list_mp3_sounds = list_mp3_sounds
        history_list_mp3_sounds = []

        # lancement fonction lecture
        launch_play_thread()

def pause_musique():
    pgMix.pause()

def next_sound():
    stop_threading()
    unstop_threading()
    launch_play_thread()

def previous_sound():
    stop_threading()
    unstop_threading()
    launch_play_thread(prev = True)


def stop_everything_reset():

    pgMix.quit()
    stop_threading()
    unstop_threading()

    try:
        # Supprime les variables dans globals
        globals().pop('son')
    except KeyError:
        pass

    try:
        # Supprime les variables dans globals
        globals().pop('modifiable_list_mp3_sounds')
    except KeyError:
        pass

    try:
        # Supprime les variables dans globals
        globals().pop('history_list_mp3_sounds')
    except KeyError:
        pass

    print("Réinitialisé !")


def Tk_Window():
    global label_title2
    back_color = "#C4AFAC"

    # Créer une fenêtre
    window = Tk()

    # Personnaliser la fenêtre
    window.title("Lire un mp3")
    window.geometry("600x590")
    # window.minsize(480, 240)
    
    # window.iconbitmap("Logo.ico") # Impossible à faire fonctionner...
    window.config(background=back_color)

    # Création d'un cadre
    frame = Frame(window, bg=back_color)   # , bd= 1, relief=SUNKEN

    # Ajout de Widgets
    label_title1 = Label(frame, text="Cliquez pour écouter ...", font=("arial", 23), bg=back_color, fg="white")
    label_title1.pack()

    label_title2 = Label(frame, text="", font=("arial", 18), bg=back_color, fg="black")
    label_title2.pack()

    # Ajout d'un bouton play
    play_button = Button(frame,
                        text="PLAY",
                        font=("arial", 18),
                        bg="white",
                        fg="black",
                        command=play_selector
                        )
    play_button.pack(pady=20)

    # Ajout d'un bouton pause
    pause_button = Button(frame,
                        text="PAUSE",
                        font=("arial", 18),
                        bg="white",
                        fg="black",
                        command=pause_musique
                        )
    pause_button.pack(pady=20)

    # Ajout d'un bouton stop
    stop_button = Button(frame,
                        text="STOP",
                        font=("arial", 18),
                        bg="white",
                        fg="black",
                        command=stop_everything_reset
                        )
    stop_button.pack(pady=20)

    # Ajout d'un bouton next
    next_button = Button(frame,
                        text="NEXT",
                        font=("arial", 18),
                        bg="white",
                        fg="black",
                        command=next_sound
                        )
    next_button.pack(pady=20)

    # Ajout d'un bouton previous
    previous_button = Button(frame,
                        text="PREVIOUS",
                        font=("arial", 18),
                        bg="white",
                        fg="black",
                        command=previous_sound
                        )
    previous_button.pack(pady=20)

    # Affichage du cadre
    frame.pack(expand=YES)

    # En cas de fermeture de la fenêtre, pgMix est quitté aussi !
    def close_window():
        # Arrête la musique en arrière-plan
        pgMix.quit()
        # Ferme la fenetre tkinter
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_window)

    # Afficher la fenêtre
    window.mainloop()

def stop_threading():
    pgMix.stop()
    stop_thread.set()

def unstop_threading():
    stop_thread.clear()

if __name__ == "__main__":


    if getattr(sys, 'frozen', False):
        # Exécuté via PyInstaller
        current_dir = os.path.dirname(sys.executable)
    else:
        # Exécuté comme script Python
        current_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(current_dir)
    print(current_dir)

    global stop_thread
    stop_thread = threading.Event()

    # Listage de tous les morceaux du répertoire
    global list_mp3_sounds
    list_mp3_sounds = list_all_mp3(current_dir)

    # Lancement de la fenêtre Tkinter
    Tk_Window()