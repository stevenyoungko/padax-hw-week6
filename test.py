import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="website"
)


mycursor = mydb.cursor(dictionary=True)
mycursor.execute("SELECT * FROM user WHERE username = 'ply' AND passward = 'ply'")
myresult = mycursor.fetchone()
print(myresult)