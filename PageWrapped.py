import customtkinter as ctk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from BilanMusical import BilanMusical
from GestionnaireCSV import GestionnaireCSV

#Hérite de CTkFrame pour que PageWrapped soit directement un cadre graphique.
#Cela permet d'utiliser les méthodes de CTkFrame sans devoir créer
#un cadre supplémentaire comme attribut de la classe.
class PageWrapped(ctk.CTkFrame):

    #Initialise la page Wrapped
    def __init__(self, parent, collection, graphiques):

        #Initialise le cadre graphique de la page Wrapped dans
        #le cadre parent de l'app qui est déja fait.
        ctk.CTkFrame.__init__(self, parent)

        #Conserve une référence à l'objet GestionnaireGraphiques
        #pour utiliser ses méthodes de création de graphiques.
        self.graphiques = graphiques

        #Conserve une référence à l'objet CollectionMusicale
        #pour accéder aux données musicales et à ses méthodes.
        self.collection = collection

        #Crée un objet BilanMusical pour utiliser ses méthodes
        #de calcul des statistiques du Wrapped. 
        self.bilan = BilanMusical(collection)

        self.utilisateur = None
        self.annee = None
        self.mois = None
        self.type_bilan = "Mensuel"
        self.ecoutes = []
        self.creer_interface()

    #Crée une case pour afficher le titre et la valeur d'une stats.
    def creer_case_statistiques(self, titre, ligne , colonne):

        #Crée le cadre de la stats.
        cadre = ctk.CTkFrame(self.cadre_statistiques)
        cadre.grid(row=ligne, column=colonne, padx=10, pady=10, sticky="nsew")

        #Affiche le titre de la statistique.
        label_titre = ctk.CTkLabel(cadre, text=titre)
        label_titre.pack(pady=(10, 0))

        #Crée une étiquette pour afficher la valeur de la statistique.
        #Son texte sera modifié plus tard dans afficher_bilan() avec configure().
        label_valeur = ctk.CTkLabel(cadre, text="-", font=("Arial", 30, "bold"))
        label_valeur.pack(pady=10)

        #Retourne l'étiquette pour pouboir modifier la valeur.
        return label_valeur

    #Calcul et affcihe les stats de la période sélectionné.
    def afficher_bilan(self):

        #Vérifie si un user est sélectionné.
        if self.utilisateur is None:
            return

        #Récupère les écoutes de la période sélectionné.
        self.ecoutes = self.bilan.filtrer_ecoutes(self.utilisateur, self.annee, self.mois)

        #Récupère le dictionnaire des stats.
        statistiques = self.bilan.calculer_statistiques(self.ecoutes)

        #Affiche le nombre d'écoutes.
        self.label_ecoutes.configure(text=str(statistiques["nombre_ecoutes"]))

        #Affiche le nom de l'utilisateur dans le titre.
        self.titre.configure(text="MusicStats Wrapped de " + self.utilisateur.nom)

        #Affiche le nombre de minutes avec 2 décimales.
        self.label_minutes.configure(text=str(round(statistiques["nombre_minutes"], 2)))

        #Affiche le nombre d'artistes différents.
        self.label_artistes.configure(text=str(statistiques["nombre_artistes"]))
        
        #Affiche les nombre de chansons différentes.
        self.label_chansons.configure(text=str(statistiques["nombre_chansons"]))

        #Met à jour les graph de la période.
        self.afficher_graphiques()

        #Active le bouton pour exporter si la période contient des écoutes.
        if len(self.ecoutes) > 0:
            self.bouton_export.configure(state="normal")
        else:
            self.bouton_export.configure(state="disabled")

    #Met à jour le bilan quand le user change de mois.
    def changer_mois(self, mois):

        #Change le mois sélevtionné en un nombre entier pour
        # pouvoir l'utiliser dans les calculs.
        self.mois = int(mois)

        #Met à jour les stats.
        self.afficher_bilan()

    #Met à jour les mois disponibles pour l'année sélectionné.
    def changer_annee(self, annee):

        #Change l'année sélectionné en nombre entier.
        self.annee = int(annee)

        #Récupère les mois disponibles pour cette année.
        mois = self.bilan.mois_disponibles(self.utilisateur, self.annee)

        valeurs = []

        #Convertit les numéros de mois en chaine de catactères.
        for numero in mois:
            valeurs.append(str(numero))

        #Met à jour le menu des mois.
        self.menu_mois.configure(values=valeurs, state="normal")

        #Sélectionne le premier mois dispo.
        self.menu_mois.set(valeurs[0])

        #Met à jour le bilan.
        self.changer_mois(valeurs[0])

    #Réinitialise les sélections et stats afficher.
    def mettre_a_jour_bilan(self):

        self.utilisateur = None
        self.annee = None
        self.mois = None
        self.ecoutes = []

        #Réinitialise le menu de années.
        self.menu_annee.configure(values=["-"], state="disabled")
        self.menu_annee.set("-")

        #Réinitialise le menu des mois.
        self.menu_mois.configure(values=["-"], state="disabled")
        self.menu_mois.set("-")

        #Réinitialise le titre.
        self.titre.configure(text="MusicStats Wrapped")

        #Efface les stats afficher.
        self.label_ecoutes.configure(text="-")
        self.label_minutes.configure(text="-")
        self.label_artistes.configure(text="-")
        self.label_chansons.configure(text="-")

        # winfo_children() retourne la liste des éléments contenus dans le cadre.
        # Parcourt cette liste et supprime chaque élément avec destroy(). 
        for graph in self.cadre_graph_artistes.winfo_children():
            graph.destroy()

        for graph in self.cadre_graph_chansons.winfo_children():
            graph.destroy()

        #Désactive le bouton pour exporter quand on réinitialise le bilan.
        self.bouton_export.configure(state="disabled")

    #Rechercher un utilisateur et préparation de ses périodes dispo.
    def rechercher_utilisateur(self):

        #Récupère le nom écrit dans le champ de recherche.
        nom = self.champ_recherche.get().strip() #strip() retire les espaces au début et à la fin du nom.

        #Réinitialise le bilan.
        self.mettre_a_jour_bilan()

        #Recherche l'utilisateur sans tenir compte des majuscules.
        for utilisateur in self.collection.utilisateurs.values():
            if utilisateur.nom.lower() == nom.lower():
                self.utilisateur = utilisateur
                break

        #Vérifie si un utilisateur a été trouvé.
        if self.utilisateur is None:
            self.label_message.configure(text="Utilisateur introuvable.", text_color="red")
            return

        #Récupère les années dispo.
        annees = self.bilan.annees_disponibles(self.utilisateur)

        if len(annees) == 0:
            self.label_message.configure(text="Aucune écoute disponible pour cet utilisateur.", text_color="red")
            return

        valeurs = []

        #Convertit les années en chaine de caracteres.
        for annee in annees:
            valeurs.append(str(annee))

        #Met à jour le menu des années.
        self.menu_annee.configure(values=valeurs, state="normal")

        #Sélectionne la première année dispo.
        self.menu_annee.set(valeurs[0])

        #Efface le message d'erreur.
        self.label_message.configure(text="", text_color="black")

        #Affiche le bilan de la première période dispo.
        self.changer_annee(valeurs[0])

    #Crée les éléments visuels de la page Wrapped.
    def creer_interface(self):

        #Crée une zone scrolable.
        self.zone = ctk.CTkScrollableFrame(self) 
        self.zone.pack(fill="both", expand=True)

        #Crée le titre de la page.
        self.titre = ctk.CTkLabel(self.zone, text="MusicStats Wrapped", font=("Arial", 30, "bold"))
        self.titre.pack(pady=20)

        #Crée un cadre pour placer tous les boutons sur la meme ligne.
        self.cadre_boutons = ctk.CTkFrame(self.zone)
        self.cadre_boutons.pack(fill="x", padx=20, pady=10)

        #Crée un bouton pour exporter les stats du Wrapped.
        self.bouton_export = ctk.CTkButton(self.cadre_boutons, text="Exporter les stats", width=170, height=45, command=self.exporter_csv, state="disabled")
        self.bouton_export.pack(side="right", padx=10, pady=10)

        #Crée le cadre de recherche.
        self.cadre_recherche = ctk.CTkFrame(self.cadre_boutons, fg_color="transparent") #fg_color transparent pour que le cadre ne soit pas visible.
        self.cadre_recherche.pack(side="left", pady=10, padx=5)

        #Crée le champ de recherche.
        self.champ_recherche = ctk.CTkEntry(self.cadre_recherche, placeholder_text="Nom de l'utilisateur", width=200, height=45)
        self.champ_recherche.pack(side="left", padx=5)

        #Crée le bouton de recherche.
        self.bouton_recherche = ctk.CTkButton(self.cadre_recherche, text="Rechercher", width=140, height = 45, command=self.rechercher_utilisateur)
        self.bouton_recherche.pack(side="left", padx=5)

        #Crée une étiquette pour les messages d'erreurs de recherche.
        self.label_message = ctk.CTkLabel(self.zone, text="")
        self.label_message.pack()

        #Crée le cadre des sélecteurs de la période.
        self.cadre_periode = ctk.CTkFrame(self.cadre_boutons, fg_color="transparent") #fg_color transparent pour que le cadre ne soit pas visible.
        self.cadre_periode.pack(side="left", pady=10, padx=5) #Fill"x" etire horizontalement.
        
        #Affiche le titre du sélecteur d'année.
        label_annee = ctk.CTkLabel(self.cadre_periode, text="Année :")
        label_annee.pack(side="left", padx=5, pady=10)

        #Crée le menu déroulant des années.
        self.menu_annee = ctk.CTkOptionMenu(self.cadre_periode, values=["-"], width=130, height=45, state="disabled", command=self.changer_annee)
        self.menu_annee.pack(side="left", padx=5)

        #Affiche le titre du sélecteur de mois.
        label_mois = ctk.CTkLabel(self.cadre_periode, text="Mois :")
        label_mois.pack(side="left", padx=5)

        #Crée le menu déroulant des mois.
        self.menu_mois = ctk.CTkOptionMenu(self.cadre_periode, values=["-"], width=130, height=45, state="disabled", command=self.changer_mois)
        self.menu_mois.pack(side="left", padx=5)

        #Crée le cadre contenant les 4 cases de stats.
        self.cadre_statistiques = ctk.CTkFrame(self.zone, fg_color="transparent")
        self.cadre_statistiques.pack(pady=10, padx=20, fill="x")

        #Permet aux 2 colonne d'avoir meme largeur.
        self.cadre_statistiques.grid_columnconfigure(0, weight=1)
        self.cadre_statistiques.grid_columnconfigure(1, weight=1)

        #Crée la case du nb écoutes.
        self.label_ecoutes = self.creer_case_statistiques("Nombre d'écoutes", 0, 0)

        #Crée la case du nb minutes.
        self.label_minutes = self.creer_case_statistiques("Nombre de minutes", 0, 1)

        #Crée la case du nb artistes.
        self.label_artistes = self.creer_case_statistiques("Nombre d'artistes différents", 1, 0)

        #Crée la case du nb chansons.
        self.label_chansons = self.creer_case_statistiques("Nombre de chansons différentes", 1, 1)

        #Crée un cadre dans la zone scrolable pour afficher les
        #2 graphs de Wrapped.
        self.cadre_graphiques = ctk.CTkFrame(self.zone, fg_color="transparent") #fg_color transparent pour que le cadre ne soit pas visible.
        self.cadre_graphiques.pack(pady=10, padx=10, fill="x")

        #Permet aux 2 colonnes des graph d'avoir meme largeur.
        self.cadre_graphiques.grid_columnconfigure(0, weight=1)
        self.cadre_graphiques.grid_columnconfigure(1, weight=1)

        #Crée le cadre du graph des artistes à gauche.
        self.cadre_graph_artistes = ctk.CTkFrame(self.cadre_graphiques, fg_color="transparent") #fg_color transparent pour que le cadre ne soit pas visible.
        self.cadre_graph_artistes.grid(row=0, column=0, padx=5, pady=10, sticky="nsew") #sticky="nsew" permet au cadre de s'étirer dans les 4 directions pour remplir sa case.

        #Crée le cadre du graph des chansons à droite.
        self.cadre_graph_chansons = ctk.CTkFrame(self.cadre_graphiques, fg_color="transparent") #fg_color transparent pour que le cadre ne soit pas visible.
        self.cadre_graph_chansons.grid(row=0, column=1, padx=5, pady=10, sticky="nsew") #sticky="nsew" permet au cadre de s'étirer dans les 4 directions pour remplir sa case.

    #Affiche les graphiques des artistes et chansons préférés.
    def afficher_graphiques(self):

        #Suprime les anciens graph qui sont ds le cadre.
        for graph in self.cadre_graph_artistes.winfo_children(): # winfo_children() retourne la liste des éléments contenus dans le cadre.
            graph.destroy()

        for graph in self.cadre_graph_chansons.winfo_children(): # winfo_children() retourne la liste des éléments contenus dans le cadre.
            graph.destroy()

        #Vérifie si la période contient des écoutes.
        if len(self.ecoutes) == 0:

            message = ctk.CTkLabel(self.cadre_graph_artistes, text="Aucune écoute disponible pour cette période.")
            message.pack(pady=20)
            return

        #Récupère les données de répartition des artistes.
        repartition = self.bilan.repartition_artistes(self.ecoutes)

        #Crée le graph circulaire des artistes.
        graph_artistes = self.graphiques.graphique_repartition_artistes_wrapped(repartition)

        #Met le graph ds le cadre de Wrapped.
        self.canvas_artistes = FigureCanvasTkAgg(graph_artistes, master=self.cadre_graph_artistes)

        #Dessine et affiche le graph.
        self.canvas_artistes.draw()
        self.canvas_artistes.get_tk_widget().pack(pady=10) # get_tk_widget() récupère le widget Tkinter associé au graphique pour pouvoir l'afficher dans le cadre avec pack().

        #Ferme la figure Matplotlib.
        plt.close(graph_artistes)

        #Récupère le top 5 des chansons de la période.
        classement = self.bilan.top_chansons(self.ecoutes)

        #Crée le graph des chansons à barre.
        graph_chansons = self.graphiques.graphique_top_chansons_wrapped(classement)

        #Met le graph ds le cadre de Wrapped.
        self.canvas_chansons = FigureCanvasTkAgg(graph_chansons, master=self.cadre_graph_chansons)

        #Dessine et affiche le graph.
        self.canvas_chansons.draw()
        self.canvas_chansons.get_tk_widget().pack(pady=10)

        #Ferme la figure Matplotlib.
        plt.close(graph_chansons)

    #Prépare les stats et les classements du Wrapped pour le CSV.
    def preparer_donnees_export(self):

        #Crée une liste pour enregistrer chaque ligne du CSV.
        lignes = []

        #Récupère les 4 stats de la période.
        statistiques = self.bilan.calculer_statistiques(self.ecoutes)

        #Regroupe les noms et les valeurs stats.
        donnees = [
            ("Nombre d'écoutes", statistiques["nombre_ecoutes"]),
            ("Minutes", round(statistiques["nombre_minutes"], 2)),
            ("Artistes différents", statistiques["nombre_artistes"]),
            ("Chansons différentes", statistiques["nombre_chansons"])
        ]

        #Ajoute les stats générales.
        for nom, valeur in donnees:

            lignes.append({
                "utilisateur": self.utilisateur.nom,
                "annee": self.annee,
                "mois": self.mois,
                "catégorie": "Statistiques",
                "nom": nom,
                "valeur": valeur
            })

        #Récupère le top 5 des artistes.
        classement_artistes = self.bilan.top_artistes(self.ecoutes)

        position = 1

        #Ajoute chaque artistes et son nombre d'écoutes.
        for artiste, nombre in classement_artistes:

            lignes.append({
                "utilisateur": self.utilisateur.nom,
                "annee": self.annee,
                "mois": self.mois,
                "catégorie": "Top Artistes",
                "nom": artiste.nom,
                "valeur": nombre,
                "position": position
            })

            position += 1

        #Récupère le top 5 des chansons.
        classement_chansons = self.bilan.top_chansons(self.ecoutes)

        position = 1

        #Ajoute chaque chanson et son nombre d'écoutes.
        for chanson, nombre in classement_chansons:

            lignes.append({
                "utilisateur": self.utilisateur.nom,
                "annee": self.annee,
                "mois": self.mois,
                "catégorie": "Top Chansons",
                "nom": chanson.titre + " - " + chanson.artiste.nom, #pour eviter de se melanger entre 2 chansons du meme titre.
                "valeur": nombre,
                "position": position
            })

            position += 1

        #Retourne les lignes qui seront enregistrés ds le CSV.
        return lignes

    #Exporte automatiquement le Wrapped dans un CSV enregistré
    #dans le meme dossier que le programme.
    def exporter_csv(self):

        #Vérifie si un utilisateur est sélectionné.
        if self.utilisateur is None:
            return

        #Crée le nom du fichier CSV.
        nom_fichier = ("wrapped_" + self.utilisateur.nom + "_" + str(self.annee) + "_" + str(self.mois) + ".csv")

        #Prépare les données à exporter.
        donnees = self.preparer_donnees_export()

        #Enregistre le fichier CSV.
        gestionnaire = GestionnaireCSV()
        reussi = gestionnaire.exporter_statistiques(nom_fichier, donnees)

        #Affiche un message selon resultat.
        if reussi:
            self.label_message.configure(text="Stats exportées dans " + nom_fichier, text_color="green")
        else:
            self.label_message.configure(text="Erreur lors de l'exportation.", text_color="red")