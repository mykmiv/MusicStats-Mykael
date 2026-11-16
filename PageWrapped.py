class PageWrapped:
    def __init__(self, parent, collection, graphiques):
        super().__init__(parent)

        self.graphiques = graphiques
        self.collection = collection
        self.bilan = BilanMusical(collection)
        self.classement = ClassementUtilisateurs(collection)
        self.utilisateur = None
        self.annee = None
        self.mois = None
        self.type_bilan = "Annuel"