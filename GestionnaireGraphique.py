import matplotlib.pyplot as plt
import AnalyseurStatistique
class GestionnaireGraphiques:

     #Enregistre l'objet analyseur dans self.analyseur pour pouvoir
     #utiliser ses fonctions de calcul de statistiques musicales.
    def __init__(self, analyseur):
        self.analyseur = analyseur
    
    #Crée une courbe du nombre d'utilisateurs actifs pour chaque semaine
    #de la période demandée et retourne la figure Matplotlib.
    def graphique_utilisateur_actifs(self, semaines=4):

        #Récupère le nombre d'utilisateurs actifs pour chaque semaine.
        donnees = self.analyseur.utilisateur_actifs_par_semaine(semaines)

        #Trie les dates des semaines dans l'ordre chronologique.
        dates = list(donnees)
        dates.sort()

        #Crée deux listes pour les valeurs et les dates du graphique.
        valeurs = []
        etiquettes = []

        #Ajoute chaque date et son nombre d'utilisateurs actifs aux listes.
        for date in dates:
            
            etiquettes.append(str(date))
            valeurs.append(donnees[date])

        #Crée les positions des semaines sur l'axe horizontal.
        positions = list(range(len(etiquettes)))

        #Crée la figure qui va contenir le graphique.
        figure = plt.figure(figsize=(9, 5))

        #Trace la courbe et affiche les dates sur l'axe horizontal.
        plt.plot(positions, valeurs, marker='o')
        plt.xticks(positions, etiquettes)
        plt.title("Evolution des utilisateurs actifs")
        plt.xlabel("Semaine")
        plt.ylabel("Nombre d'utilisateurs actifs")

        return figure
    
    #Prend les n artistes les plus écoutés et crée un diagramme
    #à barres qui présente le nombre d'écoutes de chaque artiste.
    #Retourne la figure Matplotlib.
    def graphique_top_artistes(self, n = 5):

        #Récupère le classement des artistes.
        classement = self.analyseur.top_artistes(n)

        #Crée les listes pour les artistes et leur nombre d'écoutes.
        artistes = []
        ecoutes = []

        #Sépare les artistes et leur nombre d'écoutes.
        for artiste,nombre in classement:
            artistes.append(artiste.nom)
            ecoutes.append(nombre)

        #Crée la figure et trace le diagramme à barres.
        figure = plt.figure(figsize=(9, 5))

        plt.bar(artistes, ecoutes)
        plt.title("Artistes les plus écoutés")
        plt.xlabel("Artistes")
        plt.ylabel("Nombre d'écoutes")

        return figure

    #Prend les n chansons les plus écoutés et crée un diagramme
    #à barres présantant le nobre d'écoutes de chaque morceau.
    #Retourne la figure Matplotlib.
    def graphique_top_chansons(self, n = 5):

        #Récupère le classement des chansons.
        classement = self.analyseur.top_chansons(n)

        #Crée les listes pour les chansons et leur nombre d'écoutes.
        chansons = []
        ecoutes = []

        #Sépare les chansons et leur nombre d'éçoute.
        for chanson, nombre in classement:
            chansons.append(chanson.titre + " - " + chanson.artiste.nom) #pour eviter de se melanger entre 2 chansons du meme titre.
            ecoutes.append(nombre)

        #Crée la figure et trace le diagramme à barres.
        figure = plt.figure(figsize=(9, 5))

        plt.bar(chansons, ecoutes)
        plt.title("Chansons les plus écoutées")
        plt.xlabel("Chansons")
        plt.ylabel("Nombre d'écoutes")

        return figure

    def graphique_jours(self):
        """Cela retourne un diagramme circulaire des ecoutes par jour"""
        jours = ["Lundi", "Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
        ecoutes = self.analyseur.ecoutes_par_jour()   #Myke a mis attribut analyseur
        jours_graph = []    #sans cela, les jours sans ecoutes s'empilent et cest laid
        ecoutes_graph = []
        for jour in range(7):
            if ecoutes[jour] > 0:
                ecoutes_graph.append(ecoutes[jour])
                jours_graph.append(jours[jour])

        fig = plt.figure() #Cest sur elle que le graphique sera cree
        plt.pie(ecoutes_graph, labels= jours_graph, autopct="%1.0f%%")
        plt.title("La répartition des écoutes par jour de la semaine ")
        plt.legend(jours_graph)
        return fig
    
    def graphique_heures(self):
         """Cela retourne un diagramme a barres des ecoutes par heure"""
         heures = [i for i in range(24)]
         ecoutes = self.analyseur.ecoutes_par_heure() #Myke a mis attribut analyseur
        
         fig = plt.figure()
         plt.bar(heures, ecoutes,
                 width=0.8,
                 color= "green")
         plt.title("Le nombre d'écoutes par heure de la journée")
         plt.xlabel("Heures")
         plt.ylabel("Nombre d'écoutes")
         plt.grid(False)
         return fig

    #Crée un diagramme circulaire de la répartition des écoutes
    #entre les artistes préférés et Autres.
    def graphique_repartition_artistes_wrapped(self, donnees):

        #Récupère les noms et les nombres d'écoutes.
        artistes = donnees["artistes"]
        ecoutes = donnees["ecoutes"]

        #Raccourcit les noms des artistes pour pas avoir chevauchement.
        nom_courts = []

        for artiste in artistes:
            nom_courts.append(artiste[:12])

        #Crée la figure du graphique.
        figure = plt.figure(figsize=(5.5, 3.5))

        #Crée le graph sans les noms diretement dessus.
        parties, textes, pourcentages = plt.pie(ecoutes, autopct="%1.0f%%")

        #Affiche les noms des artistes dans une légende à droite.
        plt.legend(parties, artistes, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)

        #Laisse de la place pour la légende.
        plt.subplots_adjust(right=0.55)

        #Affiche le titre et conserve proportion du cercle.
        plt.title("Répartition des artistes")
        plt.axis("equal")

        return figure

    #Crée un graphique à barres des 5 chansons les plus 
    #écoutées pendant la période sélectionné.
    def graphique_top_chansons_wrapped(self, classement):

        #Crée les listes nécessaires au graph.
        legendes = []
        nombres = []
        positions = []

        position = 1

        #Parcourt les chansons du top 5.
        for chanson, nombre in classement:

            #Enregistre la position, le titre et le nombre d'écoutes.
            positions.append(position)
            legendes.append(str(position) + ". " + chanson.titre) #pour eviter de se melanger entre 2 chansons du meme titre.
            nombres.append(nombre)

            position += 1


        #Crée la figure.
        figure = plt.figure(figsize=(6.2, 4))

        #Donne des couleurs différentes à chaque bar.
        couleurs = ["blue", "orange", "green", "red", "purple"]

        #Crée les barres et les étiquettes.
        barres = plt.bar(positions, nombres, color=couleurs)

        #Affiche seulement les numéros 1 à 5.
        plt.xticks(positions)

        #Affiche la légende des chansons à droite.
        plt.legend(barres, legendes, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)

        #Laisse de la place pour la légende.
        plt.subplots_adjust(left=0.12,right=0.45, bottom=0.22)

        #Ajoute les infos du graph.
        plt.title("Top 5 des chansons")
        plt.xlabel("Chansons")
        plt.ylabel("Nombre d'écoutes")

        return figure
