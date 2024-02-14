import sqlite3,cgi
base=sqlite3.connect("database.db")
inter=base.cursor()
form=cgi.FieldStorage()

user = form.getvalue("id")
inter.execute(f"""SELECT Pseudo, Money FROM Login WHERE ID LIKE '{user}'""")
Info = inter.fetchone()
Name = Info[0]
Money = Info[1]
Msg=""
if 'ID' in form:
    id = form.getvalue("ID")
    nmb = int(form.getvalue("Quantite"))
    inter.execute(f"""SELECT * FROM Market WHERE N is (?)""",(id,))
    X = inter.fetchone()
    if X != None:
        if nmb < X[5]:
            if Money > X[4]*nmb :
                inter.execute(f"""UPDATE Login SET Money = {Money-X[4]*nmb} WHERE ID = {user}""")
                inter.execute(f"""SELECT Money FROM Login WHERE Pseudo is '{X[2]}'""")
                m = inter.fetchone()
                m = m[0]
                if Name != X[2]:
                    Money -= X[4]*X[5]
                inter.execute(f"""UPDATE Login SET Money = {m+X[4]*nmb} WHERE Pseudo is '{X[2]}'""")
                inter.execute(f"""INSERT INTO '{user}' Values (?,?,?,?,?)""",(None,X[3],nmb,X[6],X[7]))
                inter.execute(f"""UPDATE Market SET Nombre = {X[5]-nmb} WHERE N is (?)""",(id,))
            else:
                Msg = "Pas assez d'argent !"
        else:
            if Money > X[4]*X[5] :
                inter.execute(f"""UPDATE Login SET Money = {Money-X[4]*X[5]} WHERE ID = {user}""")
                inter.execute(f"""SELECT Money FROM Login WHERE Pseudo is '{X[2]}'""")
                m = inter.fetchone()
                m = m[0]
                if Name != X[2]:
                    Money -= X[4]*X[5]
                inter.execute(f"""UPDATE Login SET Money = {m+X[4]*X[5]} WHERE Pseudo is '{X[2]}'""")
                inter.execute(f"""INSERT INTO '{user}' Values (?,?,?,?,?)""",(None,X[3],X[5],X[6],X[7]))
                inter.execute(f"""DELETE FROM Market WHERE N is (?)""",(id,))
            else:
                Msg = "Pas assez d'argent !"

Produits=""
inter.execute(f"""SELECT * FROM Market""")
Pro = inter.fetchall()

if Pro != None:
    for i in Pro:
        Produits+=f"ID {i[0]} | Vendeur : {i[2]} | {i[3]} | Prix : {i[4]} | Stock : {i[5]} | Type : {i[6]} | Marque : {i[7]}<br>"




base.commit()
base.close()

html=f"""Content-type:text/html

<html>
<head>
<title>Market</title>
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
Produits : <br>
{Produits}
<form action="market.py?id={user}" method="POST">
<label for="ID"> ID (du produit) </label>
<input type="number" name="ID">
<label for="Quantite"> Quantité </label>
<input type="number" name="Quantite">
<input type="submit" name="Acheter" value="Acheter">
</form>
{Msg}
</p>
<hr>
<p>
<form action="user.py?id={user}" method="POST">
<input type="submit" name="Back" value="Back">
</form>
</p>
</body>
</html>"""

print(html)