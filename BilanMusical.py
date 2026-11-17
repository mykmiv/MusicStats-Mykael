class BilanMusical:

    def __init__(self, collection):
        self.collection = collection

    def annees_disponibles(self, utilisateur):

        annees = []

        for ecoute in utilisateur.ecoutes:
            annee = ecoute.date_heure.year

            if annee not in annees:
                annees.append(annee)

        return annees

    def mois_disponibles(self, utilisateur, annee):

        mois = []

        for ecoute in utilisateur.ecoutes:

            if ecoute.date_heure.year == annee:
                mois_ecoute = ecoute.date_heure.month

                if mois_ecoute not in mois:
                    mois.append(mois_ecoute)

        return mois

    def filtrer_ecoutes(self, utilisateur, annee, mois):

        ecoutes = []

        for ecoute in utilisateur.ecoutes:

            if ecoute.date_heure.year == annee:
                if ecoute.date_heure.month == mois:
                    ecoutes.append(ecoute)

        return ecoutes

    def nombre_ecoutes(self, ecoutes):
        return len(ecoutes)

    def nombre_minutes(self, ecoutes):

        total_secondes = 0

        for ecoute in ecoutes:

            if ecoute.chanson.duree is not None:
                total_secondes += ecoute.chanson.duree

        return total_secondes / 60

    def nombre_artistes(self,ecoutes):

        artistes = set()

        for ecoute in ecoutes:
            artistes.add(ecoute.chanson.artiste)

        return len(artistes)

    def nombre_chansons(self, ecoutes):

        chansons = set()

        for ecoute in ecoutes:
            chansons.add(ecoute.chanson)

        return len(chansons)

    