# BINOME :  LAGHROUCHE Samir, CARBONNEAUX Jules

#!/usr/bin/python

import sqlite3
from sqlite3 import Error
 
def creer_connexion(db_file):
    """ cree une connexion a la base de donnees SQLite
        specifiee par db_file
    :param db_file: fichier BD
    :return: objet connexion ou None
    """
    try:
        conn = sqlite3.connect(db_file)
		#On active les foreign keys
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except Error as e:
        print(e)
 
    return None

def afficher(titre, cur):
    # Récup les données et les noms des colonnes
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    # Largeur de chaque colonne à 40 (pour les grands noms..., et séparateur (+---+---+---+))
    L = 40
    sep = "+" + ("-" * (L + 2) + "+") * len(cols)

    #Affichage des titres de colonnes alignés à gauche
    print(f"\n{sep}\n  {titre}\n{sep}")
    print("| " + " | ".join(f"{c:<{L}}" for c in cols) + " |")
    print(sep)

    if rows:
        for row in rows:
            ligne_aff = []
            for v in row:
                # on met les espaces pour les milliers et on aligne à droite sur 15 caractères pour avoir l'espace pour les grandes primes (et les "0" du fond soient tous l'un sous l'autre)
                if type(v) == int or type(v) == float:
                    s = f"{v:,}".replace(",", " ")
                    s = f"{s:>15}" 
                else:
                    #si c'est du texte, on le laisse tel que
                    s = str(v)

                ligne_aff.append(s)
            
            # Affichage de la ligne, avec les valeurs alignées à gauche et séparées par " | "
            print("| " + " | ".join(f"{val:<{L}}" for val in ligne_aff) + " |")

    # Affiche nbre total de lignes
    print(f"{sep}\n  {len(rows)} ligne(s)\n\n")



# ========================================#

# 1 - Lister les pirates dont la prime dépasse un seuil donné.

# On peut changer la prime
def select_pirates_superieur_prime(conn):
    """
    :param conn: objet connexion
    :return:
    """
    n=int(input("Prime minimale (ex: 1 000 000 000 - tout collé) : "))
    cur = conn.cursor()
    cur.execute(
    "select nomP, prime " \
    "from LesPirates " \
    "where prime>?", (n,)
    )
 
    afficher("Pirates avec prime > " + str(n), cur)

# 2 - fficher les pirates ayant un rôle donné.

# On peut changer le role
def select_pirates_role(conn):
    """
    :param conn: objet connexion
    :return:
    """
    roles = (
        "\nROLES DISPONIBLES : \n"
        "------------------------------------------------------------------\n"
        "Capitaine, Bras droit, Premier Maitre, Commandant, Officier, \n"
        "Commandant 1re Division (jusqu'a 16e), Ministre de la Farine (et autres ministres)\n"
        "Navigatrice, Tireur elite, Cuisinier, Medecin, Archeologue, Charpentier, \n"
        "Musicien, Timonier, Navigateur, Scientifique, Hypnotiste, Messager\n"
        "Membre, Membre Honoraire, Apprenti, Allie, Calamite, Tobi Roppo, \n"
        "Zombie, Zombie Geant, Unite speciale, Dompteur, Acrobate, Conseiller\n"
        "------------------------------------------------------------------\n"
        "\nROLE VOULU : "
    )

    role = input(roles)    
    cur = conn.cursor()
    cur.execute(
    "select p.nomP, e.nomE, r.role " \
    "from LesPirates p join LesRoles r on(p.nomP = r.nomP) " \
        "join LesEquipages e on(r.id_equipage = e.id_equipage) " \
        "where r.role = ?", (role,)
    )
 
    afficher("Pirates avec role : " + role, cur)


# 3 - Afficher tous les marines triés par prime croissante avec leur grade.

def select_ordre_marine_grade_prime(conn):
    """
    :param conn: objet connexion
    :return:
    """
    cur = conn.cursor()
    cur.execute(
    "select nomM, Grade, prime " \
    "from LaMarine " \
    "order by prime" \
    )

    afficher("Marines triés par prime", cur)


#4 - Trouver la prime maximale dans une région donnée et le pirate associé.

# On peut changer la region
def select_max_prime_par_region(conn):
    """
    :param conn: objet connexion
    :return:
    """
    regions = (
        "\nREGIONS DISPONIBLES : \n"
        "------------------------------------------------------------------\n"
        "MERS/ARCHIPELS : East Blue, Sabaody Archipelago, Archipel Sabaody, \n"
        "                 Archipel Totto Land, mer, Fish-Man Island\n"
        "PAYS/ROYAUMES :  Arabasta, Alabasta, Wano, Pays des Wa, Royaume de Goa, \n"
        "                 Royaume de Flevance, Royaume de Sorbet, Dressrosa, \n"
        "                 Pays des Fleurs, Royaume de Drum, Drum Island\n"
        "VILLES/VILLAGES: Fuschia, Syrup Village, Syrup, Cocoyasi Village, \n"
        "                 Village de Kokoyashi, Water Seven, Water 7, \n"
        "                 Shells Town, Loguetown, Whiskey Peak\n"
        "ILES/LIEUX :     Whole Cake Island, Kuraigana, Ile de Dawn, Ohara, \n"
        "                 Thriller Bark, God Valley, Spider Miles, Skypiea, \n"
        "                 Amazon Lily, Little Garden, Jaya, Enies Lobby, \n"
        "                 Punk Hazard, Zo, Laugh Tale, Erbaf, Baltigo\n"
        "BASES/PRISONS :  Marineford, LaMarine Ford, Impel Down, Enies Lobby\n"
        "------------------------------------------------------------------\n"
        "\nREGION VOULUE : "
    )
    region=input(regions)
    cur = conn.cursor()
    cur.execute(
    "select max(p.prime), p.nomP " \
    "from LesPirates p join LesRegions r on(p.id_region = r.id_region) " \
    "where r.nomR = ?", (region,)
    )
 
    afficher("Prime max dans la region : " + region, cur)


# 5 - Compter le nombre de marines et de fruits du démon par région

def select_nb_marine_par_region(conn):
    """
    :param conn: objet connexion
    :return:
    """
    cur = conn.cursor()
    cur.execute(
    "select r.nomR, count(m.nomM), count(m.nomF) " \
    "from LaMarine m join LesRegions r on(m.id_region = r.id_region) " \
        "group by r.id_region"
    )
 
    afficher("Nombre de marines et fruits par region", cur)


#6 - Lister les pirates d'une région ayant une prime au moins égale à celle d'un pirate donné .

# On peut changer la region et/ou le pirate
def select_region_prime_superieur_pirate(conn):
    """
    :param conn: objet connexion
    :return:
    """
    region=input("Nom de region (ex: East Blue, Wano, Whole Cake Island) : ")
    pirate=input("Pirate (ex: Monkey D. Luffy, Yamato, Tony Tony Chopper, Usopp) : ")
    cur = conn.cursor()
    cur.execute(
    "select p.nomP, p.prime " \
    "from LesPirates p join LesRegions r on(p.id_region = r.id_region) " \
    "where r.nomR = ? and p.prime >= (select prime " \
                                                "from LesPirates " \
                                                "where nomP = ?)", (region, pirate,)
    )
 
    afficher("Pirates dans " + region + " avec prime >= " + pirate, cur)


# 7 - Lister les pirates ayant un rôle mais ne possédant pas de fruit du démon.

def select_role_pirates_sans_fruit(conn):
    """
    :param conn: objet connexion
    :return:
    """
    cur = conn.cursor()
    cur.execute(
    "select p.nomP, r.role, p.prime " \
    "from LesPirates p join LesRoles r on(p.nomP = r.nomP) " \
    
        "except " \
        "select p.nomP, r.role, p.prime " \
        "from LesPirates p join LesRoles r on(p.nomP = r.nomP) " \
            "join LesFruits f on(p.nomF = f.nomF)"
    )
 
    afficher("Pirates sans fruit et leur role dans leur equipage respectif", cur)

# 8 - Afficher la somme des primes et le nombre de pirates par équipage.

def select_prime_par_equipage(conn):
    """
    :param conn: objet connexion
    :return:
    """
    cur = conn.cursor()
    cur.execute(
    "select e.nomE, count(p.nomP), sum(p.prime) " \
    "from LesEquipages e join LesRoles r on(e.id_equipage = r.id_equipage) " \
        "join LesPirates p on(r.nomP = p.nomP) " \
        "group by e.id_equipage " \
        "order by count(p.nomP)"
    )
 
    afficher("Prime totale par equipage (avec leur nombre total de pirate)", cur)

# 9 - Lister les fruits du démon non consommés par un pirate ou un marine.

def select_fruit_non_manger(conn):
    """
    :param conn: objet connexion
    :return:
    """
    cur = conn.cursor()
    cur.execute(
    "select nomF, type, pouvoir " \
    "from LesFruits " \
        
        "except " \
        "select nomF, type, pouvoir " \
        "from (" \
            "select m.nomF, f.type, f.pouvoir " \
            "from LaMarine m join LesFruits f on(m.nomF = f.nomF) " \
                
                "union " \
                "select p.nomF, f.type, f.pouvoir " \
                "from LesPirates p join LesFruits f on(p.nomF = f.nomF))"
    )
 
    afficher("Fruit pas encore mange par une personne", cur)

# ========================================#

def majBD(conn, file):

    # Lecture du fichier et placement des requetes dans un tableau
    createFile = open(file, 'r')
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Execution de toutes les requetes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        cursor.execute(query)

        
def main():
    database = "OnePiece.db"

    # creer une connexion a la BD
    conn = creer_connexion(database)
    
    # remplir la BD 
    print("On cree et on initialise les tables.")
    majBD(conn, "OnePiece.sql")

    print("==========================================================================================")
    print("1 - Lister les pirates dont la prime dépasse un seuil donné")
    print("2 - Afficher les pirates ayant un rôle donné")
    print("3 - Afficher tous les marines triés par prime croissante avec leur grade")
    print("4 - Trouver la prime maximale dans une région donnée et le pirate associé")
    print("5 - Compter le nombre de marines et de fruits du démon par région")
    print("6 - Lister les pirates d'une région ayant une prime au moins égale à celle d'un pirate donné")
    print("7 - Lister les pirates ayant un rôle mais ne possédant pas de fruit du démon")
    print("8 - Afficher la somme des primes et le nombre de pirates par équipage")
    print("9 - Lister les fruits du démon non consommés par un pirate ou un marine")
    print("0 - Quitter")
    print("==========================================================================================\n")
    
    # lire la BD
    while(True):
        res = int(input("-> "))

        match res:
            case 0: break
            case 1: 
                select_pirates_superieur_prime(conn)
                print("Pirate, prime")
                print("\n 10 - pour voir le menu\n")
            case 2: 
                select_pirates_role(conn)
                print("Pirate, equipage, role")
                print("\n 10 - pour voir le menu\n")
            case 3: 
                select_ordre_marine_grade_prime(conn)
                print("Marine, grade, prime")
                print("\n 10 - pour voir le menu\n")
            case 4: 
                select_max_prime_par_region(conn)
                print("prime, Pirate")
                print("\n 10 - pour voir le menu\n")
            case 5: 
                select_nb_marine_par_region(conn)
                print("Region, nb marine, nb fruit")
                print("\n 10 - pour voir le menu\n")
            case 6: 
                select_region_prime_superieur_pirate(conn)
                print("Pirate, prime")
                print("\n 10 - pour voir le menu\n")
            case 7: 
                select_role_pirates_sans_fruit(conn)
                print("Pirate, role, prime")
                print("\n 10 - pour voir le menu\n")
            case 8: 
                select_prime_par_equipage(conn)
                print("Equipage, nb pirate, somme prime")
                print("\n 10 - pour voir le menu\n")
            case 9: 
                select_fruit_non_manger(conn)
                print("Fruit, type, pouvoir")
                print("\n 10 - pour voir le menu\n")
            case 10:
                print("\n==========================================================================================")
                print("1 - Lister les pirates dont la prime dépasse un seuil donné")
                print("2 - Afficher les pirates ayant un rôle donné")
                print("3 - Afficher tous les marines triés par prime croissante avec leur grade")
                print("4 - Trouver la prime maximale dans une région donnée et le pirate associé")
                print("5 - Compter le nombre de marines et de fruits du démon par région")
                print("6 - Lister les pirates d'une région ayant une prime au moins égale à celle d'un pirate donné")
                print("7 - Lister les pirates ayant un rôle mais ne possédant pas de fruit du démon")
                print("8 - Afficher la somme des primes et le nombre de pirates par équipage")
                print("9 - Lister les fruits du démon non consommés par un pirate ou un marine")
                print("0 - Quitter")
                print("==========================================================================================\n")


if __name__ == "__main__":
    main()
