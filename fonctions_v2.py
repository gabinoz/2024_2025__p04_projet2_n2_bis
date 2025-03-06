import random
import tkinter as tk

def trouver_gagnant(joueurs):
    max_score = max(joueurs.values(), key=lambda joueur: joueur['score'])['score']
    gagnants = [joueur for joueur in joueurs if joueurs[joueur]['score'] == max_score]
    return gagnants


def Verif_param_nombre(text):
    for char in text:
        if char.isdigit():
            return True
        else:
            return False



def feliciter_gagnant(nom_gagnant):
    # Création de la fenêtre
    root = tk.Tk()
    root.title("Félicitations !")
    root.geometry("500x300")
    root.configure(bg="black")

    # Création du label avec le nom du gagnant
    label = tk.Label(root, text=f"Félicitations {nom_gagnant} ! 🎉", 
                     font=("Arial", 24, "bold"), fg="white", bg="black")
    label.pack(expand=True)

    # Liste de couleurs pour l'animation
    couleurs = ["red", "yellow", "green", "blue", "purple", "orange", "white"]

    def changer_couleur():
        """Change la couleur du texte aléatoirement."""
        label.config(fg=random.choice(couleurs))
        root.after(300, changer_couleur)  # Relancer après 300ms

    # Lancer l'animation
    changer_couleur()

    # Afficher la fenêtre
    root.mainloop()






def recuperer_nombre(entry):
    if Verif_param_nombre(entry.get()) == True:
        nombre = entry.get()
        return int(nombre)
    return False


def ajouter_nom_joueur_dans_liste(entry, liste):
    nom_du_joueur = entry.get()
    liste.append(nom_du_joueur)


import copy

def generer_la_combinaison_aleatoire(liste_des_joueurs):
    nouvelle_liste = copy.deepcopy(liste_des_joueurs)  # Copie profonde pour éviter toute modification
    print("Avant shuffle :", nouvelle_liste)  # Debug
    
    if len(nouvelle_liste) % 2 != 0:
        nouvelle_liste.append("joueur_fictif")
    
    random.shuffle(nouvelle_liste)  # Mélange la copie, pas l'originale
    print("Après shuffle :", nouvelle_liste)  # Debug

    return nouvelle_liste


def creer_le_dictionnaire_joueurs(liste_des_joueurs):
    dictionnaire_joueurs = {}
    for joueur in liste_des_joueurs :
        dictionnaire_joueurs[joueur] = {"score": 0, "joueurs_affrontés" : [], "joueur_fictif_affronté" : False}  # Tu peux ajouter d'autres informations ici
    print(dictionnaire_joueurs)
    return dictionnaire_joueurs











# les deux suivantes sont bizarres

def recuperer_les_scores(dictionnaire_joueurs, liste_de_joueurs):
    liste_scores_joueurs = []
    for i in range(len(liste_de_joueurs)):
        liste_scores_joueurs.append(dictionnaire_joueurs[joueurs[i]]["score"], dictionnaire_joueurs[joueurs[i]])
    print(liste_scores_joueurs)



def recuperer_indice_score_max(dictionnaire_joueurs, liste_de_joueurs):
    valeur_max = 0
    indice_valeur_max = 0
    for joueur in liste_de_joueurs:
        if dictionnaire_joueurs[liste_de_joueurs[i]]["sccore"]  > valeur_max:
            valeur_max = dictionnaire_joueurs[liste_de_joueurs[i]]["sccore"] 
            indice_valeur_max = i
    return indice_valeur_max



