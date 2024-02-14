import sqlite3,cgi
base=sqlite3.connect("database.db")
inter=base.cursor()
form=cgi.FieldStorage()
Msg=""

if 'Pseudo' in form and 'Mdp' in form:
    P = form.getvalue("Pseudo")
    M = form.getvalue("Mdp")
    inter.execute("""SELECT Pseudo FROM Login""")
    Ps = inter.fetchone()
    if Ps == None:
        inter.execute("""INSERT INTO Login Values (?,?,?,?)""",(None,P,M,1000))
        Msg = "<p>Login enregistré !</p>"
        inter.execute(f"""SELECT ID FROM Login WHERE Pseudo LIKE '{P}'""")
        Test = inter.fetchone()
        inter.execute(f"""CREATE TABLE "{Test[0]}" ("ID" INTEGER,"Nom" TEXT,"Nombre" INTEGER,"Type" TEXT,"Marque" TEXT,PRIMARY KEY("ID" AUTOINCREMENT));""")
    elif not(P in Ps):
        inter.execute("""INSERT INTO Login Values (?,?,?,?)""",(None,P,M,1000))
        Msg = "<p>Login enregistré !</p>"
        inter.execute(f"""SELECT ID FROM Login WHERE Pseudo LIKE '{P}'""")
        Test = inter.fetchone()
        inter.execute(f"""CREATE TABLE "{Test[0]}" ("ID" INTEGER,"Nom" TEXT,"Nombre" INTEGER,"Type" TEXT,"Marque" TEXT,PRIMARY KEY("ID" AUTOINCREMENT));""")
    else:
        Msg = "<p>Il y a déjà quelqu'un ayant ce pseudo !</p>"

result=inter.execute("""Select * FROM Login""")
listeM=""
for messageTuple in result:
    listeM+="<p>"+str(messageTuple)+"</p>"

base.commit()
base.close()

html=f"""Content-type:text/html

<html>
<head>
<title>Register</title>
</head>
<body>
<p>
<form method="POST">
<label for="Pseudo"> Pseudo </label>
<input type="text" name="Pseudo"> <br>
<label for="Mdp"> Mdp  </label>
<input type="text" name="Mdp"> <br>
<input type="submit" name="Register" value="Register"> <br>
</form>
{Msg}
<form action="login.py" method="POST">
<input type="submit" name="Back" value="Back">
</form>
</p>
</body>
</html>"""

print(html)