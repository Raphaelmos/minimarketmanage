import sqlite3,cgi
base=sqlite3.connect("database.db")
inter=base.cursor()
form=cgi.FieldStorage()
condition = "false"
Msg=""
Test = [None]

if 'Pseudo' in form and 'Mdp' in form:
    P = form.getvalue("Pseudo")
    M = form.getvalue("Mdp")
    inter.execute(f"""SELECT ID FROM Login WHERE Pseudo LIKE '{P}' AND Mdp LIKE '{M}'""")
    Test = inter.fetchone()
    if Test != None:
        condition = "true"
    else:
        Msg = "<p>Mauvais identifiants !</p>"

base.commit()
base.close()

js="""
<script>
if ("""+condition+""") {
    window.location = "http://127.0.0.1:2022/cgi-bin/user.py?id="""+str(Test[0])+"""";
}
</script>
"""

html=f"""Content-type:text/html

<html>
<head>
<title>Login</title>
</head>
<body>
{js}
<p>
<form method="POST">
<label for="Pseudo"> Pseudo </label>
<input type="text" name="Pseudo"> <br>
<label for="Mdp"> Mdp  </label>
<input type="text" name="Mdp"> <br>
<input type="submit" name="Login" value="Login"> <br>
</form>
{Msg}
<form action="register.py" method="POST">
<input type="submit" name="Register" value="Register">
</form>
</p>
</body>
</html>"""

print(html)