import customtkinter as ctk
from BilanMusical import BilanMusical

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

        #Affiche le nom du user.
        self.label_profil.configure(text=self.utilisateur.nom)

        #Affiche le nombre d'écoutes.
        self.label_ecoutes.configure(text=str(statistiques["nombre_ecoutes"]))

        #Affiche le nombre de minutes avec 2 décimales.
        self.label_minutes.configure(text=str(round(statistiques["nombre_minutes"], 2)))

        #Affiche le nombre d'artistes différents.
        self.label_artistes.configure(text=str(statistiques["nombre_artistes"]))
        
        #Affiche les nombre de chansons différentes.
        self.label_chansons.configure(text=str(statistiques["nombre_chansons"]))

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

        #Réinitialise le nom de l'utilisateur.
        self.label_profil.configure(text="Aucun utilisateur sélectionné")

        #Efface les stats afficher.
        self.label_ecoutes.configure(text="-")
        self.label_minutes.configure(text="-")
        self.label_artistes.configure(text="-")
        self.label_chansons.configure(text="-")

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

        #Crée le cadre de recherche.
        self.cadre_recherche = ctk.CTkFrame(self.zone)
        self.cadre_recherche.pack(fill="x", pady=10, padx=20)

        #Crée le champ de recherche.
        self.champ_recherche = ctk.CTkEntry(self.cadre_recherche, placeholder_text="Nom de l'utilisateur", width=200)
        self.champ_recherche.pack(side="left", padx=(10, 15))

        #Crée le bouton de recherche.
        self.bouton_recherche = ctk.CTkButton(self.cadre_recherche, text="Rechercher", command=self.rechercher_utilisateur)
        self.bouton_recherche.pack(side="left", padx=10)

        #Crée une étiquette pour les messages d'erreurs de recherche.
        self.label_message = ctk.CTkLabel(self.zone, text="")
        self.label_message.pack()

        #Crée le cadre des sélecteurs de la période.
        self.cadre_periode = ctk.CTkFrame(self.zone)
        self.cadre_periode.pack(fill="x", pady=20, padx=10) #Fill"x" etire horizontalement.
        
        #Affiche le titre du sélecteur d'année.
        label_annee = ctk.CTkLabel(self.cadre_periode, text="Année :")
        label_annee.pack(side="left", padx=10, pady=15)

        #Crée le menu déroulant des années.
        self.menu_annee = ctk.CTkOptionMenu(self.cadre_periode, values=["-"], state="disabled", command=self.changer_annee)
        self.menu_annee.pack(side="left", padx=10)

        #Affiche le titre du sélecteur de mois.
        label_mois = ctk.CTkLabel(self.cadre_periode, text="Mois :")
        label_mois.pack(side="left", padx=10)

        #Crée le menu déroulant des mois.
        self.menu_mois = ctk.CTkOptionMenu(self.cadre_periode, values=["-"], state="disabled", command=self.changer_mois)
        self.menu_mois.pack(side="left", padx=10)

        #Crée une étiquette pour le nom du profil sélectionné.
        self.label_profil = ctk.CTkLabel(self.zone, text="Aucun utilisateur sélectionné", font=("Arial", 20, "bold"))
        self.label_profil.pack(pady=15)

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
