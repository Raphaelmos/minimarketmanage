import sqlite3,cgi
base=sqlite3.connect("database.db")
inter=base.cursor()
form=cgi.FieldStorage()

user = form.getvalue("id")
inter.execute(f"""SELECT Pseudo, Money FROM Login WHERE ID LIKE '{user}'""")
Info = inter.fetchone()
Name = Info[0]
Money = Info[1]

if 'Nom' in form:
    Nom = form.getvalue("Nom")
    Nmb = form.getvalue("Nombre")
    Typ = form.getvalue("Type")
    Mar = form.getvalue("Marque")
    inter.execute(f"""INSERT INTO '{user}' Values (?,?,?,?,?)""",(None,Nom,Nmb,Typ,Mar))

if 'ID' in form:
    id = form.getvalue("ID")
    prix = form.getvalue("Prix")
    nmb = int(form.getvalue("Quantite"))
    inter.execute(f"""SELECT * FROM '{user}' WHERE ID is (?)""",(id,))
    X = inter.fetchone()
    if X != None:
        if nmb < X[2]:
            inter.execute(f"""INSERT INTO Market Values (?,?,?,?,?,?,?,?)""",(None,id,Name,X[1],prix,nmb,X[3],X[4]))
            inter.execute(f"""UPDATE '{user}' SET Nombre = {X[2]-nmb} WHERE ID is (?)""",(id,))
        else:
            inter.execute(f"""INSERT INTO Market Values (?,?,?,?,?,?,?,?)""",(None,id,Name,X[1],prix,X[2],X[3],X[4]))
            inter.execute(f"""DELETE FROM '{user}' WHERE ID is (?)""",(id,))

Produits=""
inter.execute(f"""SELECT * FROM '{user}'""")
Pro = inter.fetchall()

if Pro != None:
    for i in Pro:
        Produits+=f"ID {i[0]} | {i[1]} | Stock : {i[2]} | Type : {i[3]} | Marque : {i[4]}<br>"


base.commit()
base.close()

html=f"""Content-type:text/html

<html>
<head>
<title>{Name}</title>
</head>
<body>
<p>
User : {Name} <br>
Money : {Money} <br>
</p>
<form action="login.py" method="POST">
<input type="submit" name="Logout" value="Logout">
</form>
<hr>
<p>
Inventaire : <br>
{Produits}
<form method="POST">
<label for="Nom"> Nom </label>
<input type="text" name="Nom">
<label for="Nombre"> Nombre </label>
<input type="number" name="Nombre">
<label for="Type"> Type </label>
<input type="text" name="Type">
<label for="Marque"> Marque </label>
<input type="text" name="Marque">
<input type="submit" name="Ajout" value="Ajout de produit">
</form>
</p>
<hr>
<p>
<form method="POST">
<label for="ID"> ID (du produit) </label>
<input type="number" name="ID">
<label for="Prix"> Prix </label>
<input type="number" name="Prix">
<label for="Quantite"> Quantité </label>
<input type="number" name="Quantite">
<input type="submit" name="Vente" value="Vendre un produit">
</form>
</p>
<hr>
<p>
<form action="market.py?id={user}" method="POST">
<input type="submit" name="Marché" value="Acheter un produit (Espace de Vente)">
</form>
</p>
</body>
</html>"""

print(html)