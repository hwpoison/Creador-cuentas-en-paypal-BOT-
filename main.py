#import paypal_driver
import os
import json
import sqlite3
import random
from paypal_driver import PaypalBot
from generador_tarjetas import Generar_tarjeta


class Generador_datos():
	def __init__(self, BIN):
		self.pass_defecto = "holasoyun"+str(random.randint(100,300))
		self.datos = {
					"""Se pueden dejar en None para que se generen automaticamente
					o añadir un dato por defecto, puede contener "x" para ser reemplazadas
					por numero aleatorios en casos de direcciones o telefonos
					"""
					"firtsName":None,
					"lastName":None,
					"address":"405x Havanna Street",
					"city":"New York",
					"postalCode":"10080",
					"phoneNumber":"336364xxxx",
					"email":None,
					"passw":None,
					"state":"NY",
					"tarjeta":Generar_tarjeta(BIN,1).dic_tarjetas[0],
					"ocupacion":None,
					"paypal_loc":"usa"
		}
		self.generar_datos()
	
	def reemplazar_x(self, dic):
		nueva = ""
		for i in dic:
			if(i == "x"):
				nueva += str(random.randint(0,9))
			else:
				nueva +=i
		return nueva
	
	def generar_datos(self):
		p = self.persona_azar()
		
		primer_nombre = self.datos["firtsName"]
		if primer_nombre == None:
			self.datos["firtsName"] = p[1]
		if self.datos["lastName"]  == None:
			self.datos["lastName"]  = p[2]
		
		if self.datos["address"]  == None:
			self.datos["address"]  = p[3]
		else:
			#reemplazar x por numero aleatorios
			self.datos["address"] = self.reemplazar_x(self.datos["address"])
								
		if self.datos["city"] == None:
			self.datos["city"] = p[6]

		if self.datos["postalCode"] == None:
			self.datos["postalCode"] = p[8]

		if self.datos["phoneNumber"] == None:
			self.datos["phoneNumber"] = p[5]
		else:
			self.datos["phoneNumber"] = self.reemplazar_x(self.datos["phoneNumber"])

		if self.datos["email"] == None:
			arroba = p[9].index("@")
			self.datos["email"] = p[9][:arroba] + str(random.randint(0,1990)) +  "@gmail.com"

		if self.datos["passw"] == None:
			self.datos["passw"] = self.pass_defecto

		if self.datos["state"] == None:
			self.datos["state"] = "NY"
			
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
			
	def crear_paypal(self):
		input("Presionar enter para comenzar la creacion")
		archivo_cuentas = None
		nombre_archivo = "cuenta_creadas.txt"
		archivo_cuentas = open("cuenta_creadas.txt", "a+") 
		
		cuenta = PaypalBot().crear_cuenta(self.datos)
		print("Cuenta creada:")
		print(cuenta)
		archivo_cuentas.writelines("%s:%s\n"%(cuenta["email"], cuenta["pass"]))
		
BIN = "541301xxxxxxxxxx"
ini = Generador_datos(BIN)
ini.crear_paypal()
