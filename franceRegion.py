def regionFRA(var):
    try:
        if var == "Bourg-en-Bresse":
            deptFR = "Ain"
        if var == "Laon":
            deptFR = "Aisne"
        if var == "Moulins":
            deptFR = "Allier"
        if var == "Digne-les-Bains":
            deptFR = "Alpes-de-Haute-Provence"
        if var == "Gap":
            deptFR = "Hautes-Alpes"
        if var == "Nice":
            deptFR = "Alpes-Maritimes"
        if var == "Privas":
            deptFR = "Ardèche"
        if var == "Charleville-Mézières":
            deptFR = "Ardennes"
        if var == "Foix":
            deptFR = "Ariège"
        if var == "Troyes":
            deptFR = "Aube"
        if var == "Carcassonne":
            deptFR = "Aude"
        if var == "Rodez":
            deptFR = "Aveyron"
        if var == "Marseille":
            deptFR = "Bouches-du-Rhône"
        if var == "Caen":
            deptFR = "Calvados"#from here
        if var == "Aurillac":
            deptFR = "Cantal"
        if var == "Angoulême":
            deptFR = "Charente"
        if var == "La Rochelle":
            deptFR = "Charente-Maritime"
        if var == "Bourges":
            deptFR = "Cher"
        if var == "Tulle":
            deptFR = "Corrèze"
        if var == "Ajaccio":
            deptFR = "Corse-du-Sud"
        if var == "Bastia":
            deptFR = "Haute-Corse"
        if var == "Dijon":
            deptFR = "Côte-d'Or"
        if var == "Saint-Brieuc":
            deptFR = "Côtes d'Armor"
        if var == "Guéret":
            deptFR = "Creuse"
        if var == "Périgueux":
            deptFR = "Dordogne"
        if var == "Besançon":
            deptFR = "Doubs"
        if var == "Valence":
            deptFR = "Drôme"
        if var == "Évreux":
            deptFR = "Eure"
        if var == "Chartres":
            deptFR = "Eure-et-Loir"
        if var == "Quimper":
            deptFR = "Finistère"
        if var == "Nîmes":
            deptFR = "Gard"
        if var == "Toulouse":
            deptFR = "Haute-Garonne"
        if var == "Auch":
            deptFR = "Gers"
        if var == "Bordeaux":
            deptFR = "Gironde"
        if var == "Montpellier":
            deptFR = "Hérault"
        if var == "Rennes":
            deptFR = "Ille-et-Vilaine"
        if var == "Châteauroux":
            deptFR = "Indre"
        if var == "Tours":
            deptFR = "Indre-et-Loire"
        if var == "Grenoble":
            deptFR = "Isère"
        if var == "Lons-le-Saunier":
            deptFR = "Jura"
        if var == "Mont-de-Marsan":
            deptFR = "Landes"
        if var == "Blois":
            deptFR = "Loir-et-Cher"
        if var == "Saint-Étienne":
            deptFR = "Loire"
        if var == "Le Puy-en-Velay":
            deptFR = "Haute-Loire"
        if var == "Nantes":
            deptFR = "Loire-Atlantique"
        if var == "Orléans":
            deptFR = "Loiret"
        if var == "Cahors":
            deptFR = "Lot"
        if var == "Agen":
            deptFR = "Lot-et-Garonne"
        if var == "Mende":
            deptFR = "Lozère"
        if var == "Angers":
            deptFR = "Maine-et-Loire"
        if var == "Saint-Lô":
            deptFR = "Manche"
        if var == "Châlons-en-Champagne":
            deptFR = "Marne"
        if var == "Chaumont":
            deptFR = "Haute-Marne"
        if var == "Laval":
            deptFR = "Mayenne"
        if var == "Nancy":
            deptFR = "Meurthe-et-Moselle"
        if var == "Bar-le-Duc":
            deptFR = "Meuse" #from here nOw
        if var == "Vannes":
            deptFR = "Morbihan"
        if var == "Metz":
            deptFR = "Moselle"
        if var == "Nevers":
            deptFR = "Nièvre"
        if var == "Lille":
            deptFR = "Nord"
        if var == "Beauvais":
            deptFR = "Oise"
        if var == "Alençon":
            deptFR = "Orne"
        if var == "Arras":
            deptFR = "Pas-de-Calais"
        if var == "Clermont-Ferrand":
            deptFR = "Puy-de-Dôme"
        if var == "Pau":
            deptFR = "Pyrénées-Atlantiques"
        if var == "Tarbes":
            deptFR = "Hautes-Pyrénées"
        if var == "Perpignan":
            deptFR = "Pyrénées-Orientales"
        if var == "Strasbourg":
            deptFR = "Bas-Rhin"
        if var == "Colmar":
            deptFR = "Haut-Rhin"
        if var == "Lyon":
            deptFR = "Rhône"#from here
        if var == "Vesoul":
            deptFR = "Haute-Saône"
        if var == "Mâcon":
            deptFR = "Saône-et-Loire"
        if var == "Le Mans":
            deptFR = "Sarthe"
        if var == "Chambéry":
            deptFR = "Savoie"
        if var == "Annecy":
            deptFR = "Haute-Savoie"
        if var == "Paris":
            deptFR = "Paris"
        if var == "Rouen":
            deptFR = "Seine-Maritime"
        if var == "Melun":
            deptFR = "Seine-et-Marne"
        if var == "Versailles":
            deptFR = "Yvelines"
        if var == "Niort":
            deptFR = "Deux-Sèvres"
        if var == "Amiens":
            deptFR = "Somme"
        if var == "Albi":
            deptFR = "Tarn"
        if var == "Montauban":
            deptFR = "Tarn-et-Garonne"
        if var == "Toulon":
            deptFR = "Var"
        if var == "Avignon":
            deptFR = "Vaucluse"
        if var == "La Roche-sur-Yon":
            deptFR = "Vendée"
        if var == "Poitiers":
            deptFR = "Vienne"
        if var == "Limoges":
            deptFR = "Haute-Vienne"
        if var == "Épinal":
            deptFR = "Vosges"
        if var == "Auxerre":
            deptFR = "Yonne"
        if var == "Belfort":
            deptFR = "Territoire-de-Belfort"
        if var == "Évry":
            deptFR = "Essonne"
        if var == "Nanterre":
            deptFR = "Hauts-de-Seine"
        if var == "Bobigny":
            deptFR = "Seine-Saint-Denis"
        if var == "Créteil":
            deptFR = "Val-de-Marne"
        if var == "Pontoise":
            deptFR = "Val-D'Oise"
        if var == "Basse-Terre":
            deptFR = "Guadeloupe"
        if var == "Fort-de-France":
            deptFR = "Martinique"
        if var == "Cayenne":
            deptFR = "Guyane"
        if var == "Saint-Denis":
            deptFR = "La Réunion"
        if var == "Dzaoudzi":
            deptFR = "Mayotte"
    except:
        var = deptFR
    
    return deptFR
