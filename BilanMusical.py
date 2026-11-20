from AnalyseurStatistique import AnalyseurStatistique


class BilanMusical:

    #Initialise le bilan musical avec la collection musicale
    def __init__(self, collection):
        self.collection = collection
        self.analyseur = AnalyseurStatistique(collection)

    #Retourne les années pendant lesquelles l'utilisateur
    #possède des écoutes.
    def annees_disponibles(self, utilisateur):

        annees = []

        #Parcourt toutes les écoutes de l'utilisateur.
        for ecoute in utilisateur.ecoutes:

            #Récupère l'année de l'écoute.
            annee = ecoute.date_heure.year

            #Ajoute l'année à la liste en évitant les doublons.
            if annee not in annees:
                annees.append(annee)

        return annees

    #Retourne les mois contenant des écoutes pour l'année sélectionné.
    def mois_disponibles(self, utilisateur, annee):

        mois = []

        for ecoute in utilisateur.ecoutes:

            #Vérifie si l'écoute apparrtient à l'année sélectionné.
            if ecoute.date_heure.year == annee:
                mois_ecoute = ecoute.date_heure.month

                #Ajoute le mois à la liste en évitant les doublons.
                if mois_ecoute not in mois:
                    mois.append(mois_ecoute)

        return mois

    #Retourne les écoutes de l'utilisateur pour le mois et l'année sélectionné.
    def filtrer_ecoutes(self, utilisateur, annee, mois):

        ecoutes = []

        for ecoute in utilisateur.ecoutes:

            #Vérifie si l'écoute apparrtient à l'année et au mois sélectionné.
            if ecoute.date_heure.year == annee:
                if ecoute.date_heure.month == mois:
                    ecoutes.append(ecoute)

        return ecoutes

    #Retourne le nombre d'écoute de la période.
    def nombre_ecoutes(self, ecoutes):
        return len(ecoutes)

    #Calcul le nombre total de minute d'écoute.
    def nombre_minutes(self, ecoutes):

        total_secondes = 0

        for ecoute in ecoutes:

            #Additionne la durée des chansons écoutés si la durée existe.
            if ecoute.chanson.duree is not None:
                total_secondes += ecoute.chanson.duree

        #Convertion en minutes.
        return total_secondes / 60

    #Retourne le nombre d'artistes différents écoutés pendant la période sélectionné.
    def nombre_artistes(self,ecoutes):

        #Crée un ensemble pour éviter les doublons.
        artistes = set()

        #Ajoute l'artiste de chaque écoute dans l'ensemble.
        for ecoute in ecoutes:
            artistes.add(ecoute.chanson.artiste)

        return len(artistes)

    #Retourne le nombre de chansons différentes écoutés pendant la période sélectionné.
    def nombre_chansons(self, ecoutes):

        #Crée un ensemble pour éviter les doublons.
        chansons = set()

        #Ajoute la chanson de chaque écoute dans l'ensemble.
        for ecoute in ecoutes:
            chansons.add(ecoute.chanson)

        return len(chansons)

    #Retourne le top 5 des artistes les plus écoutés pendant la période sélectionnée.
    def top_artistes(self, ecoutes, n=5):

        #Reprend la méthode définie dans la classe AnalyseurStatistique pour obtenir le top 5 des artistes les plus écoutés.
        return self.analyseur.top_artistes(n, ecoutes)

    #Retourne le top 5 des chansons les plus écoutés pendant la période sélectionnée.
    def top_chansons(self, ecoutes, n=5):

        #Reprend la méthode définie dans la classe AnalyseurStatistique pour obtenir le top 5 des chansons les plus écoutés.
        return self.analyseur.top_chansons(n, ecoutes)


    def repartition_artistes(self, ecoutes):

        #Récupère le toop 5 des artistes
        classement = self.top_artistes(ecoutes)


        #Crée les listes nécessaires au diagramme circulaire.
        artistes = []
        nombres = []

        #Compteur des écoutes du top 5.
        total_top = 0

        #Parcourt artistes et nb écoutes.
        for artiste, nombre in classement:

            #Ajoute le nom de l'artiste et son nombre d'écoutes.
            artistes.append(artiste.nom)
            nombres.append(nombre)

            #Additionne les écoutes du top 5.
            total_top += nombre

        #Calcule le nombre d'écoutes hors top 5.
        autres = self.nombre_ecoutes(ecoutes) - total_top

        #Ajoute la catégorie Autres si il rest des écoutes.
        if autres > 0:
            artistes.append("Autres")
            nombres.append(autres)

        #Retourne les données nécessaires au diagramme circulaire.
        return {"artistes": artistes, "ecoutes": nombres}

    #Regroupe les stats de base du Wrapped dans un dictionnaire.
    def calculer_statistiques(self, ecoutes):

        statistiques = {
            "nombre_ecoutes": self.nombre_ecoutes(ecoutes),
            "nombre_minutes": self.nombre_minutes(ecoutes),
            "nombre_artistes": self.nombre_artistes(ecoutes),
            "nombre_chansons": self.nombre_chansons(ecoutes),
        }

        return statistiques
