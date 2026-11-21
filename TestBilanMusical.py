from GestionnaireCSV import GestionnaireCSV
from BilanMusical import BilanMusical

gestionnaire = GestionnaireCSV()
collection = gestionnaire.lire_fichier("donnees.csv")

utilisateur = collection.trouver_utilisateur("user_000001")

bilan = BilanMusical(collection)

#test annees dispo
print("Annees:", bilan.annees_disponibles(utilisateur))

#test mois dispo
print("Mois:", bilan.mois_disponibles(utilisateur, 2008))

#filtre pour mars 2008(valeur aleatoire)
ecoutes = bilan.filtrer_ecoutes(utilisateur, 2008, 3)

#test stats
print("Nombre ecoutes:", bilan.nombre_ecoutes(ecoutes))
print("Nombre minutes:", bilan.nombre_minutes(ecoutes))
print("Nombre artistes:", bilan.nombre_artistes(ecoutes))
print("Nombre chansons:", bilan.nombre_chansons(ecoutes))

#Test pour top 5 artistes et top 5 chansons
print("Top 5 des artistes :")

for artiste, nombre in bilan.top_artistes(ecoutes):
    print(artiste.nom, nombre)

print("Top 5 des chansons :")

for chanson, nombre in bilan.top_chansons(ecoutes):
    print(chanson.titre, chanson.artiste.nom, nombre)

#Test pour la répartition des artistes.
print("Repartition des artistes :")
print(bilan.repartition_artistes(ecoutes))

ecoutes_avril = bilan.filtrer_ecoutes(utilisateur, 2008, 4)

print(bilan.repartition_artistes(ecoutes_avril))

print(bilan.calculer_statistiques(ecoutes))
