class ClassementUtilisateurs:

    def __init__(self, collection):
        self.collection = collection

    #Retourne les écoutes de tous les utilisateurs pour la période sélectionnée.
    def ecoutes_periode(self, annee, mois=None):

        ecoutes = []

        #Parcourt toutes les écoutes de la collection.
        for ecoute in self.collection.ecoutes:

            #Vérifie si l'écoute appartient à l'année sélectionnée.
            if ecoute.date_heure.year == annee:

                #Vérifie le mois ou conserve toute l'année si mois est None:
                if mois is None or ecoute.date_heure.month == mois:
                    ecoutes.append(ecoute)

        return ecoutes

    #Retourne la position de l'utilisateur dans le classement fait avec les méthodes classement.
    def calculer_position(self, utilisateur, compteurs):

        #Vérifie si l'utilisateur est présent dans le classement.
        if utilisateur not in compteurs:
            return None

        #Récupère le nombre d'écoute ou la durée de l'utilisateur.
        valeur = compteurs[utilisateur]

        position = 1

        #Parcourt les utilisateurs du classement.
        for autre_utilisateur in compteurs:

            #Augmente la position si un utilisateur possède une valeur supérieure.
            if compteurs[autre_utilisateur] > valeur:
                position += 1

        #Compte le nombre d'utilisateurs dans le classement.
        total = len(compteurs)

        #Calcule le pourcentage correspondant à la position.
        pourcentage = round(position * 100 / total, 1)

        #Retourne les résultats du classement dans un dictionnaire.
        return {"position": position, "total": total, "pourcentage": pourcentage }

    #Crée un dictionnaire avec tous les utilisateurs qui ont écouté
    #la chanson et le nombre d'écoutes de chacun.
    #Transmet ce dictionnaire à calculer_position() pour obtenir
    #la position et le pourcentage de l'utilisateur sélectionné.
    def classement_chanson(self, utilisateur, chanson, annee, mois=None):

        #Crée un dictionnaire pour compter les écoutes par utilisateur.
        compteurs = {}

        #Récupère les écoutes de tous les utilisateurs pour la période.
        ecoutes = self.ecoutes_periode(annee, mois)

        #Parcourt les écoutes de la période.
        for ecoute in ecoutes:

            #Vérifie si l'écoute correspond à la chanson sélectionnée.
            if ecoute.chanson == chanson:

                #Initialise le compteur si l'utilisateur n'est pas ds le compteur.
                if ecoute.utilisateur not in compteurs:
                    compteurs[ecoute.utilisateur] = 0

                    #Ajoute une écoute à l'utilisateur.
                compteurs[ecoute.utilisateur] += 1

        #retourne la position parmi les autilisateurs qui ont écoutés la chanson.
        return self.calculer_position(utilisateur, compteurs)

    #Crée un dictionnaire avec tous les utilisateurs qui ont écouté
    #l'artiste et le nombre d'écoutes de chacun.
    #Transmet ce dictionnaire à calculer_position() pour obtenir
    #la position et le pourcentage de l'utilisateur sélectionné.
    def classement_artiste(self, utilisateur, artiste, annee, mois=None):

        #Crée un dictionnaire pour compter les écoutes par utilisateur.
        compteurs = {}

        #Récupère les écoutes de la période.
        ecoutes = self.ecoutes_periode(annee, mois)

        #Parcourt les écoutes de la période.
        for ecoute in ecoutes:

            #Vérifie si la chanson écouté appartient à cet artiste.
            if ecoute.chanson.artiste == artiste:

                #Initialise le compteur si l'utilisateur n'est pas ds le compteur.
                if ecoute.utilisateur not in compteurs:
                    compteurs[ecoute.utilisateur] = 0

                    #Ajoute une écoute à l'utilisateur.
                compteurs[ecoute.utilisateur] += 1

        #retourne la position parmi les autilisateurs qui ont écoutés l'artiste.
        return self.calculer_position(utilisateur, compteurs)

    #Crée un dictionnaire avec tous les utilisateurs et le nombre d'écoutes de chacun.
    #Transmet ce dictionnaire à calculer_position() pour obtenir
    #la position et le pourcentage de l'utilisateur sélectionné.
    def classement_minutes(self, utilisateur, annee, mois=None):

        #Crée un dictionnaire pour enregistrer les durées par utilisateur.
        durees = {}

        #Initialise le compteur de chaque utilisateur à 0.
        for autre_utilisateur in self.collection.utilisateurs.values():
            durees[autre_utilisateur] = 0

        #Récupère les écoutes de la période.
        ecoutes = self.ecoutes_periode(annee, mois)

        #Compte les écoutes.
        nombre_durees = 0

        #Parcourt toutes les écoutes de la période.
        for ecoute in ecoutes:

            #Vérifie si la durée de la chanson est disponible.
            if ecoute.chanson.duree is not None:

                #Additionne la durée à celle du user.
                durees[ecoute.utilisateur] += ecoute.chanson.duree

                nombre_durees += 1

        #Ne calcul pas de classement si aucune durée n'est dispo.
        if nombre_durees == 0:
            return None

        #Retourne la position de l'utilisateur selon ses minutes d'écoute.
        return self.calculer_position(utilisateur, durees)
