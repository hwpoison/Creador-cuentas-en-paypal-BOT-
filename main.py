import os
import json
import random
import sqlite3
from paypal_driver import PaypalBot
from generador_tarjetas import Generar_tarjeta

class Generador_datos():
	def __init__(self,DATOS):
		self.datos = DATOS
		self.generar_datos()
	
	def remplazar_x(self, dic):
		nueva = ""
		for i in dic:
			if(i == "x"):
				nueva += str(random.randint(0,9))
			else:
				nueva +=i
		return nueva
	
	def generar_datos(self):
		p = self.persona_azar()
		#Generar primer nombre
		if self.datos["firtsName"] == None:
			self.datos["firtsName"] = p[1]
			
		#Generar segundo nombre
		if self.datos["lastName"]  == None:
			self.datos["lastName"]  = p[2]
		
		#Generar direccion calle
		if self.datos["address"]  == None:
			self.datos["address"]  = p[3]
		else:
			self.datos["address"] = self.remplazar_x(self.datos["address"])
		#Generar ciudad				
		if self.datos["city"] == None:
			self.datos["city"] =	 p[6]
		#Generar codigo postal
		if self.datos["postalCode"] == None:
			self.datos["postalCode"] = p[8]
		#Generar numero telefono
		if self.datos["phoneNumber"] == None:
			self.datos["phoneNumber"] = p[5]
		else:
			self.datos["phoneNumber"] = self.remplazar_x(self.datos["phoneNumber"])
		#Generar email
		if self.datos["email"] == None:
			arroba = p[9].index("@")
			self.datos["email"] = p[9][:arroba] + str(random.randint(0,1990)) +  "@gmail.com"
		#Generar contraseña
		if self.datos["passw"] == None:
			self.datos["passw"] = "holasoyun"+str(random.randint(100,300))
		else:
			self.datos["passw"] = self.remplazar_x(self.datos["passw"])
		#Generar estado
		if self.datos["state"] == None:
			self.datos["state"] = "NY"
		#Generar datos tarjeta
		self.datos["tarjeta"] = Generar_tarjeta(self.datos["BIN"],1).dic_tarjetas[0]
		
		print("Datos generado:")
		for i in self.datos:
			print(i,":",self.datos[i])
		print("===============")
		
	def sql_a_sqlite(self, sql, sqlite):
		print("Convirtiendo..")
		db = sqlite3.connect(sqlite)
		cursor = db.cursor()
		try:
			sql = str(open(sql,"r").read())[3:]
		except:
			print("Error con el fichero sql..")
		cursor.executescript(sql)
		db.commit()
		print("Listo..")
		
	def persona_azar(self):
		db = sqlite3.connect("datos_gente.db")
		cur = db.cursor()
		numero_azar = random.randint(1,32979)
		encontrado = False
		while(encontrado == False):
			for e in cur.execute("SELECT * FROM fakenames where number='%s'"%(numero_azar)):
				if(e):
					encontrado = True
			numero_azar+=1
		return e


datos = {
		"BIN":			"541301xxxxxxxxxx",
		"firtsName":	None,
		"lastName":		None,
		"address":		"405x Havanna Street",
		"city":			"New York",
		"postalCode":	"10080",
		"phoneNumber":	"336364xxxx",
		"email":		None,
		"passw":		"netflixxxx",
		"state":		"NY",
		"tarjeta":		None,
		"ocupacion":	None,
		"paypal_loc":	"usa"
}
		
datos = Generador_datos(datos).datos
paypal_bot = PaypalBot().crear_cuenta(datos)
