class BilanMusical:

    #Initialise le bilan musical avec la collection musicale
    def __init__(self, collection):
        self.collection = collection

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

    