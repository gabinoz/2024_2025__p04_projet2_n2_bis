from tkinter import *
import random
from tkinter import ttk
from fonctions import *  
from itertools import permutations
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

liste_des_joueurs = []
liste_des_frames_bloc_fin_match = []
liste_des_boutons_fin_match = []
liste_gagnants = []
liste_joueurs_ayant_fait_match_nul = []
nombre_question_nom = 0
question_widget = {}
round_effectue = 0
question_id = 0
indice_joueur_liste = 0
nombre_de_fin_de_match_validee = 0

window = Tk()
window.title("Gestionnaire de tournoi d'échecs")
window.geometry("900x700")

label_nombre_de_joueurs = ttk.Label(window, text="Combien de joueurs participent au tournoi?", font=("arial", 20))
label_nombre_de_joueurs.pack()

entry_nombre_joueurs = ttk.Entry(window, font=("Ariel", 20), justify="center")
entry_nombre_joueurs.pack(pady=20)

label_nombre_de_round = ttk.Label(window, text="en combien de round?", font=("Ariel", 20))
label_nombre_de_round.pack(pady=20)

entry_nombre_de_round = ttk.Entry(window, font=("Arial", 20))
entry_nombre_de_round.pack(pady=20)

button = Button(window, text="valider", font=("Arial", 20), command=lambda: fonction_bouton_valider_nombre_joueur_et_round(entry_nombre_joueurs, entry_nombre_de_round))
button.pack(pady=20)

# Déclaration globale du label d'erreur
label_erreur = None  

# Déclaration globale du label d'erreur
label_erreur = None  

def fonction_bouton_valider_nombre_joueur_et_round(entry_nombre_joueurs, entry_nombre_de_round):
    global nombre_de_joueurs, nombre_de_round, nombre_de_joueurs_sans_le_joueur_fictif, label_erreur
    if Verif_param_nombre(entry_nombre_joueurs.get()) == True:
        nombre_de_joueurs_recupere = int(entry_nombre_joueurs.get())
    else:
        return
    
    if Verif_param_nombre(entry_nombre_de_round.get()) == True:
        nombre_de_round_recupere = int(entry_nombre_de_round.get())
    else:
        return
    


    message_erreur = ""

    # Vérification du nombre de joueurs
    if nombre_de_joueurs_recupere > 50:
        message_erreur = "Le nombre de joueurs ne peut pas dépasser 40."

    # Vérification du nombre de rounds
    if nombre_de_joueurs_recupere % 2 != 0:
        if nombre_de_round_recupere > nombre_de_joueurs_recupere :
            message_erreur = "Le nombre de rounds ne peut pas être supérieur au nombre de joueurs."
    else:
        if nombre_de_round_recupere >= nombre_de_joueurs_recupere :
            message_erreur = "Le nombre de rounds ne peut pas être supérieur ou égal au nombre de joueurs."


    # Affichage ou suppression du message d'erreur
    if message_erreur:
        # Supprime le message d'erreur précédent s'il existe
        if label_erreur:
            label_erreur.destroy()
        
        # Création d'un nouveau message d'erreur
        label_erreur = ttk.Label(window, text=message_erreur, font=("Ariel", 15), foreground="red")
        label_erreur.pack()
        return  # Arrête la fonction

    # Si tout est valide, on supprime le message d'erreur
    if label_erreur:
        label_erreur.destroy()
        label_erreur = None  

    # Mise à jour des valeurs
    nombre_de_joueurs_sans_le_joueur_fictif = nombre_de_joueurs_recupere

    # Ajout d'un joueur fictif si nécessaire
    if nombre_de_joueurs_sans_le_joueur_fictif % 2 != 0:
        nombre_de_joueurs = nombre_de_joueurs_sans_le_joueur_fictif + 1
    else:
        nombre_de_joueurs = nombre_de_joueurs_sans_le_joueur_fictif

    nombre_de_round = nombre_de_round_recupere

    afficher_nouvelle_page()




def afficher_nouvelle_page():
    global nombre_question_nom 
    for widget in window.winfo_children():
        widget.destroy()

    label = ttk.Label(window, text=f"Quel est le nom du joueur {nombre_question_nom + 1}?", font=('arial', 20))
    label.pack()

    entry_nom_joueur = ttk.Entry(window, font=("Arial", 20))
    entry_nom_joueur.pack(pady=20)

    button = Button(window, font=("Arial", 20), text="valider", command=lambda: fonction_bouton_valider_nom_joueur(entry_nom_joueur))
    button.pack(pady=20)


def fonction_bouton_valider_nom_joueur(entry_nom_joueur): 
    if entry_nom_joueur.get() == "":
        return
    elif entry_nom_joueur.get() not in liste_des_joueurs:
        ajouter_nom_joueur_dans_liste(entry_nom_joueur, liste_des_joueurs)
    else: 
        label_erreur_nom_de_joueur_deja_utilise = ttk.Label(window, text="Nom d'utilisateur déjà utilisé", font=("Ariel", 20), foreground="red")
        label_erreur_nom_de_joueur_deja_utilise.place(x = 270, y=200)
        
        return
    global nombre_question_nom, dictionnaire_joueurs
    nombre_question_nom += 1
    if nombre_question_nom < nombre_de_joueurs_sans_le_joueur_fictif :
        afficher_nouvelle_page()
    else:
        dictionnaire_joueurs = (creer_le_dictionnaire_joueurs(liste_des_joueurs))
        afficher_nouvelle_page_tableau(liste_des_joueurs, nombre_de_joueurs)
        


def afficher_nouvelle_page_tableau(liste_des_joueurs, nombre_de_joueurs):
    global indice_joueur_liste, dictionnaire_joueurs, round_effectue
    for widget in window.winfo_children():
        widget.destroy()

    if round_effectue == 0:
        generer_la_combinaison_aleatoire(liste_des_joueurs)
    else:
        liste_des_joueurs = generate_match_list(liste_des_joueurs)

    ajouter_les_informations_des_joueurs_sauf_score_dans_le_dico(liste_des_joueurs, dictionnaire_joueurs)

    # Calcul du nombre de lignes à afficher
    nombre_de_lignes = len(liste_des_joueurs) // 2

    # Création du tableau avec une hauteur dynamique
    table = ttk.Treeview(window, columns=("joueur1", "joueur2"), show="headings", height=nombre_de_lignes)
    table.heading("joueur1", text="Joueur 1 (blanc)")
    table.heading("joueur2", text="Joueur 2(noir)")

    # Insérer les joueurs par paires
    for i in range(0, len(liste_des_joueurs), 2):
        table.insert(parent="", index="end", values=(liste_des_joueurs[i], liste_des_joueurs[i + 1]))

    table.place(x=10, y=50)
    label_tableau_match = ttk.Label(window, text="Tableau des matchs", font=("arial", 15))
    label_tableau_match.place(x = 100, y = 0)

    label_round = ttk.Label(window, text=f"round n°{round_effectue + 1}", font=("arial", 15))
    label_round.place(x = 300, y = 0)

    frame_fin_round = Frame(window, width=400)
    frame_fin_round.pack(side="right", fill="y")

    creer_un_complexe_question_reponse_fin_round(frame_fin_round, liste_des_joueurs)
    indice_joueur_liste = 0
    round_effectue += 1


def generate_match_list(liste_des_joueurs):
    note_max = 0
    liste_des_joueurs_bien = None  # Initialisation de la variable
    for i in range(1500000):
        # Créer une copie de la liste à chaque itération pour ne pas affecter la liste originale
        copie_liste_joueurs = liste_des_joueurs.copy()  # Ou utilisez list(liste_des_joueurs)
        random.shuffle(copie_liste_joueurs)
        note = noter_la_liste(copie_liste_joueurs)
        
        # Si la note est meilleure, on garde cette permutation
        if note > note_max: 
            note_max = note
            liste_des_joueurs_bien = copie_liste_joueurs

    print("La note max est", note_max)
    return liste_des_joueurs_bien

def noter_la_liste(liste_des_joueurs):
    note = 0
    score_ecart_total = 0
    for i in range(len(liste_des_joueurs)):
        if i % 2 == 0:
            if i < len(liste_des_joueurs) - 1:
                if str(liste_des_joueurs[i + 1]) != "joueur_fictif":
                    if str(liste_des_joueurs[i]) not in dictionnaire_joueurs[liste_des_joueurs[i + 1]]['joueurs_affrontés']:
                        note += 1
                    if str(liste_des_joueurs[i]) != "joueur_fictif":
                        score_ecart_total += abs(dictionnaire_joueurs[liste_des_joueurs[i + 1]]['score'] - dictionnaire_joueurs[liste_des_joueurs[i]]['score'])
                    
        else: 
            if str(liste_des_joueurs[i - 1]) != "joueur_fictif":
                if str(liste_des_joueurs[i]) not in dictionnaire_joueurs[liste_des_joueurs[i - 1]]['joueurs_affrontés']:
                    note += 1
    impact_sur_note_du_score = score_ecart_total / 10
    note -= impact_sur_note_du_score

    return note






def aucun_des_joueurs_n_a_deja_joue_ensemble(liste_des_joueurs):
    global dictionnaire_joueurs
    les_joueurs_ne_se_sont_pas_affrontés = True
    i = 0
    while les_joueurs_ne_se_sont_pas_affrontés and i < len(liste_des_joueurs)-1:
        if liste_des_joueurs[i] != "joueur_fictif":
            
            if i % 2 == 0:
                if liste_des_joueurs[i + 1] in dictionnaire_joueurs[liste_des_joueurs[i]]["joueurs_affrontés"]:
                    les_joueurs_ne_se_sont_pas_affrontés = False
            else: 
                if liste_des_joueurs[i - 1] in dictionnaire_joueurs[liste_des_joueurs[i]]["joueurs_affrontés"]:
                    les_joueurs_ne_se_sont_pas_affrontés = False
        i += 1
    return les_joueurs_ne_se_sont_pas_affrontés


def ajouter_les_informations_des_joueurs_sauf_score_dans_le_dico(liste_des_joueurs, dictionnaire_joueurs):
    print("Liste des joueurs :", liste_des_joueurs)

    i = 0
    while i < len(liste_des_joueurs) - 1:
        joueur1 = liste_des_joueurs[i]
        joueur2 = liste_des_joueurs[i + 1]

        # Si joueur1 ou joueur2 est "joueur_fictif", on le note mais on continue
        if joueur1 == "joueur_fictif":
            if joueur2 in dictionnaire_joueurs:
                dictionnaire_joueurs[joueur2]['joueur_fictif_affronté'] = True
                dictionnaire_joueurs[joueur2]['joueurs_affrontés'].append("joueur_fictif")  # Ajouter joueur_fictif dans les affrontés
            i += 2  # On saute cette paire et continue
            continue

        if joueur2 == "joueur_fictif":
            if joueur1 in dictionnaire_joueurs:
                dictionnaire_joueurs[joueur1]['joueur_fictif_affronté'] = True
                dictionnaire_joueurs[joueur1]['joueurs_affrontés'].append("joueur_fictif")  # Ajouter joueur_fictif dans les affrontés
            i += 2  # On saute cette paire et continue
            continue

        # Ajouter l'adversaire dans le dictionnaire si les joueurs existent
        if joueur1 in dictionnaire_joueurs and joueur2 in dictionnaire_joueurs:
            dictionnaire_joueurs[joueur1]['joueurs_affrontés'].append(joueur2)
            dictionnaire_joueurs[joueur2]['joueurs_affrontés'].append(joueur1)
        else:
            print(f"⚠ Erreur : {joueur1} ou {joueur2} n'existent pas dans le dictionnaire !")

        i += 2  # On passe au prochain duo

    print("Dictionnaire après mise à jour :", dictionnaire_joueurs)






def creer_un_complexe_question_reponse_fin_round(frame_fin_round, liste_des_joueurs):
    global nombre_de_joueurs

    
    for i in range(nombre_de_joueurs // 2):
        global question_id, indice_joueur_liste
        question_id += 1


        frame_bloc_fin_match = Frame(frame_fin_round)
        label = ttk.Label(frame_bloc_fin_match, text=f"match {i + 1} : qui a gagné?", font=("Arial", 20))
        label.pack(pady=20)


        if not (liste_des_joueurs[indice_joueur_liste] == "joueur_fictif" or liste_des_joueurs[indice_joueur_liste + 1] == "joueur_fictif"):
            # Créer un combobox avec les joueurs
            combobox = ttk.Combobox(
                frame_bloc_fin_match, 
                font=("Arial", 20), 
                values=[
                    liste_des_joueurs[indice_joueur_liste], 
                    liste_des_joueurs[indice_joueur_liste + 1], 
                    f"match_nul {liste_des_joueurs[indice_joueur_liste]}, {liste_des_joueurs[indice_joueur_liste + 1]}"
                ], 
                state="readonly"
            )
        else:
            if liste_des_joueurs[indice_joueur_liste] == "joueur_fictif":
                bon_joueur = liste_des_joueurs[indice_joueur_liste + 1]
            else:
                bon_joueur = liste_des_joueurs[indice_joueur_liste]
            # Créer un combobox avec le joueur sans le joueur fictif
            combobox = ttk.Combobox(
                frame_bloc_fin_match, 
                font=("Arial", 20), 
                values=[bon_joueur],
                state="readonly"
            )


        indice_joueur_liste += 2
        combobox.pack()

        button = Button(frame_bloc_fin_match, font=("Arial", 20), text="valider", 
                        command=lambda f=frame_bloc_fin_match, c=combobox: fonction_bouton_valider_fin_match(f, c))
        button.pack()

        frame_bloc_fin_match.pack()
        question_widget[question_id] = frame_bloc_fin_match
        print(liste_gagnants)
    button_valider_tous_scores = Button(
    window,font=("Arial", 20),text="valider tout",
    command=fonction_bouton_valider_tout, bg="green", fg="white")

    button_valider_tous_scores.place(x = 120, y = 550 )


def fonction_bouton_valider_fin_match(frame_bloc_fin_match, combobox):
    global liste_gagnants, liste_joueurs_ayant_fait_match_nul, nombre_de_fin_de_match_validee
    if combobox.get() != "":
        resultat = combobox.get()
        nombre_de_fin_de_match_validee += 1

    else:
        return
    
    if "match_nul" in resultat:
        try:
            _, noms_joueurs = resultat.split("match_nul ", 1)  # Ignorer la première partie
            joueurs = [nom.strip() for nom in noms_joueurs.split(",")]  # Séparer et nettoyer les noms
            
            liste_joueurs_ayant_fait_match_nul.extend(joueurs)  # Ajouter à la liste des matchs nuls
            print("Joueurs ayant fait match nul :", joueurs)
        
        except ValueError:
            print("Erreur de format dans la chaîne du match nul :", resultat)
    
    else:
        liste_gagnants.append(resultat)  # Ajouter le gagnant à la liste des gagnants

    frame_bloc_fin_match.destroy()  # Fermer l'interface après validation


def fonction_bouton_valider_tout():
    global dictionnaire_joueurs, round_effectue, nombre_de_fin_de_match_validee
    if nombre_de_fin_de_match_validee == nombre_de_joueurs // 2:
        nombre_de_fin_de_match_validee = 0
        for i in range(len(liste_gagnants)):
            dictionnaire_joueurs[str(liste_gagnants[i])]["score"] += 1
        for i in range(len(liste_joueurs_ayant_fait_match_nul)):
            dictionnaire_joueurs[liste_joueurs_ayant_fait_match_nul[i]]["score"] += 0.5
        liste_gagnants.clear()  # Au lieu de recréer la liste, on la vide
        liste_joueurs_ayant_fait_match_nul.clear()
        print("le nombre de round est", nombre_de_round)
        print("le nombre de round_effectue est", round_effectue)
        if round_effectue < nombre_de_round:
            afficher_nouvelle_page_tableau(liste_des_joueurs, nombre_de_joueurs)
        else:
            print("le tournoi est fini")
            for widget in window.winfo_children():
                widget.destroy()
            print(dictionnaire_joueurs)
            gagnant = trouver_gagnant(dictionnaire_joueurs)
            if len(gagnant) > 1:
                label_fin = ttk.Label(window, text=f"Les gagnants sont: {gagnant}", font=("Arial", 20))
            else:
                label_fin = ttk.Label(window, text=f"Le gagnant est: {gagnant}", font=("Arial", 20))
            label_fin.pack()
    else:
        return

        


def ajouter_question(frame_fin_round):
    global question_id
    question_id += 1

    frame_bloc_fin_match = Frame(frame_fin_round)
    label = ttk.Label(frame_bloc_fin_match, text=f"match {question_id} : qui a gagné?", font=("Arial", 20))
    label.pack(pady=20)

    # Créer un combobox avec les joueurs
    combobox = ttk.Combobox(frame_bloc_fin_match, font=("Arial", 20), values=liste_des_joueurs, state="readonly")
    combobox.pack()

    button = Button(frame_bloc_fin_match, text="valider", font=("Arial", 20), command=lambda f=frame_bloc_fin_match, c=combobox: fonction_bouton_valider_fin_match(f, c))
    button.pack()

    frame_bloc_fin_match.pack()
    question_widget[question_id] = frame_bloc_fin_match

# def afficher_graphique():
#     """ Affiche un graphique des scores des joueurs """
#     global canvas, fig, ax

#     # Récupérer les noms et scores
#     noms = liste_des_joueurs
#     scores = [dictionnaire_joueurs[nom]["score"] for nom in noms]

#     # Création de la figure
#     fig, ax = plt.subplots(figsize=(8, 6))
    
#     # Couleurs modernes
#     couleurs = ["#FF6F61", "#6B5B95", "#88B04B", "#FFA07A"]
    
#     # Création des barres
#     bars = ax.bar(noms, scores, color=couleurs, width=0.5, edgecolor="black", linewidth=1)

#     # Personnalisation du graphique
#     ax.set_title("Scores du Tournoi", fontsize=18, fontweight="bold", color="#333")
#     ax.set_xlabel("Joueurs", fontsize=14, color="#555")
#     ax.set_ylabel("Score", fontsize=14, color="#555")
#     ax.set_ylim(0, max(scores) + 5)  # Ajuste l'échelle pour plus de lisibilité

#     # Supprimer les bordures inutiles
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)

#     # Ajouter une grille légère
#     ax.grid(axis="y", linestyle="--", alpha=0.6)

#     # Affichage des scores au-dessus des barres
#     for bar, score in zip(bars, scores):
#         ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(score),
#                 ha="center", fontsize=12, fontweight="bold", color="black")

#     # Insérer le graphique dans Tkinter
#     canvas = FigureCanvasTkAgg(fig, master=window)
#     canvas.draw()
#     canvas.get_tk_widget().pack(expand=True, fill="both")



window.mainloop()
