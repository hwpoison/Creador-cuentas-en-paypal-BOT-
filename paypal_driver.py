#!/usr/bin/env Python 3.6
#Codigo by sRBill96 para netixzen.blogspot.com.ar
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class PaypalBot():
	def __init__(self):
		self.driver_name = "chromedriver.exe"
		self.driver = None
		self.error = {
			1:"El navegador aun no ah sido iniciado.",
			2:"El navegador o el elemento no estan disponibles."
		}
		self.elementos_paypal = {
			#Nombres de elementos y alternativos (debido a la dinamica de la pagina en cada carga
			"firtsName":["firstName","paypalAccountData_firstName","/paypalAccountData/firstName",],
			"lastName":["lastName","/paypalAccountData/lastName","paypalAccountData_lastName"],
			"address":["address1","paypalAccountData_address1","/paypalAccountData/address/address1"],
			"city":["city","paypalAccountData_city","/paypalAccountData/address/city"],
			"postal":["postalCode","paypalAccountData_zip","/paypalAccountData/address/zip"],
			"phoneNumber":["phoneNumber","/paypalAccountData/phoneNumber","paypalAccountData_phone"],
			
			"email":["email","paypalAccountData_email"],
			"password":["password","paypalAccountData_password"],
			"cpassword":["confirmPassword","paypalAccountData_confirmPassword"],
			"seguir_logeado":["stayLoggedIn","paypalAccountData_oneTouchCheckbox"],
			"next_primero":["_eventId_personal","/appData/action"],
			"state":["paypalAccountData_state","state","/paypalAccountData/address/state"],
			"terminos":["termsAgree","paypalAccountData_tcpa","terms","marketingOptIn","terms_checkbox","terms_checkbox"],
			"crear":["submitBtn","_eventId_continue","/appData/action"],
			"asociar":["_eventId_continue","submitBtn","/appData/action"],
			"ocupacion":["occupation"],
			"numero_tarjeta":["cardNumber","cardData_cardNumber","/cardData/cardNumber"],
			"expiracion":["expiryDate","cardData_expiryDate","/cardData/expiryDate"],
			"cseguridad":["csc","cardData_csc","/cardData/csc"],
			"saltar_promocion":["exploreBenefits","skipPromoteCredit"],
			"ir_a_nuevacuenta":["myaccountLink","exploreBenefits"]
		}
		#Url comunes de la pagina y registro
		self.url_paypal = {
			"usa":{
				"home":"https://www.paypal.com/myaccount/home",
				"registro":"https://www.paypal.com/us/signup/account?Z3JncnB0=",
				"formulario_registro":"https://www.paypal.com/signup/create",
				"aniadir_tarjeta":"https://www.paypal.com/signup/addCard",
				"promocion":"https://www.paypal.com/signup/promoteCredit",
				"success":"https://www.paypal.com/signup/success"
			},
			"ca":{
				"home":"https://www.paypal.com/myaccount/home",
				"registro":"https://www.paypal.com/ca/signup/account?Z3JncnB0=",
				"formulario_registro":"https://www.paypal.com/signup/create?Z3JncnB0=",
				"aniadir_tarjeta":"https://www.paypal.com/signup/addCard",
				"promocion":"https://www.paypal.com/signup/promoteCredit",
				"success":"https://www.paypal.com/signup/success"
			}
		}

	
	def Verificar(self, element=True):#Verificar elemento y driver encendido
		if(self.driver == None):
			self.pError(2)
			return False
		elif(element == None or element == False):
			self.pError(2)
			return False
		else:
			return True
			
	def pError(self,error_id=None):#Lanzar algun error
		if error_id in self.error:
			print(self.error[error_id])
		else:
			print("Error desconocido.")
			
	def Iniciar(self):#Inicializacion de driver
		print("Iniciando Chrome..")

		options1 = Options()
		options1.add_argument("start-maximized");
		#options1.binary_location = "C:\\Program Files\\Hola\\app\\chromium\\"
		self.driver = webdriver.Chrome(self.driver_name,chrome_options=options1)

	def cerrar(self):
		print("Saliendo de Google Chrome")
		self.driver.quit()
		
	def Ir(self, pagina="google.com"):#Redirigir a una pagina
		if self.driver != None:
			print("Dirigiendose a %s"%(pagina))
			self.driver.get(pagina)
		else:
			self.pError(1)
			return False
			
	def irAtras(self):
		if(Verificar):
			self.driver.back()
	
	def irAdelante(self):
		if(Verificar):
			self.driver.forward()
			#Busca elementos en la pagina

	def Buscar_Elemento(self,nombre,tipo="id"):#Buscar elemento 
			""" Si no encuentra un elemento por id busca otro
				Esta funcion cubre la dinamica del sitio de paypal
				a la hora de renombrar elementos.
			"""
			elemento = None
			if(nombre in self.elementos_paypal):
				for i in self.elementos_paypal[nombre]:
					elemento = self.bElemento(i, tipo)
					if(elemento != False):
						print("  [v]Se localizo el elemento %s correctamente."%nombre)
						return elemento
					time.sleep(2)
			tipos_ = ["name","id"]
			print("[+]Buscando elemento:\"%s\" por todos los tipos.."%(nombre))
			for tipo in tipos_:
				elemento = self.bElemento(nombre, tipo)
				if(elemento):
					return elemento
			print("  [x]No se encontro el elemento \"%s\""%nombre)
			return elemento
	
	def bElemento(self,name,Type="id"):#Buscar elemento por tipo especifico
		print("[+]Buscando elemento:\"%s\" por %s"%(name,Type))
		try:
			if(Type == "id"):
				return self.driver.find_element_by_id(name)
			elif(Type == "name"):
				return self.driver.find_element_by_name(name)
			elif(Type == "link"):
				return self.driver.find_element_by_link_text(name)
			elif(Type == "xlink"):
				return self.driver.find_element_by_partial_link_text(name)
			elif(Type == "class"):
				return self.driver_find_element_by_class_name(name)
			elif(Type == "tag"):
				return self.driver_find_element_by_tag_name(name)
			else:
				return self.driver.find_element_xpath("//input[@id='%s']"%name)
		except:
			return False
		
	def cClear(self, element):#Vaciar caja o elemento
		if(self.Verificar(element)):
			try:
				element.clear()
				print("Elemento vaciado.")
			except:
				print("Error al borrar el elemento.")
	
	def tKey(self, element, text):#Tipea texto sobre elemento
		if(self.Verificar(element) and text != None):
			element.clear()
			element.send_keys(text)
			print("Se ah completado el campo %s con:\"%s\""%(str(element.get_attribute("name")),str(text[0:8])));
	
	def tKey2(self, element, text):#Tipea texto sobre elemento pero no borra(para listabox)
		if(self.Verificar(element) and text != None):
			element.send_keys(text)
			print("Se ah completado el campo %s con:\"%s\""%(str(element.get_attribute("name")),str(text[0:8])));
	
	def kEnter(self, element):
		if(self.Verificar(element)):
			print("Apretando enter..")
			element.send_keys(Keys.ENTER)
			
	def sKey(self, KEY, element):
		if(self.Verificar(element)):
			print("Presionando ",KEY)
			element.send_keys(KEY)
			
	def Salir(self):
		print("Cerrando..")
		self.driver.close()
		
	def aClic(self, element):#Hacer click sobre elemento
		try:
			if(self.Verificar(element)):
				element.click()
		except:
			print("Error al clicker :(")
			print("Corrige el error manualmente..")
			return False
			
	def tEspera(self, segs=10):#Tiempo de espera en navegador
		if(self.Verificar()):
			print("Tiempo de espera re estrablecido a %s segundos"%segs)
			self.driver.implicitly_wait(segs)
		
	def Pausa(self, segs=5):
		print("Esperando %s segundos en el script."%segs)
		time.sleep(5)
		
	def tEsperar(self, nombre_elemento, tipo="name",tiempo=100):#Esperar x tiempo hasta que se encuentre el elemento
		if(self.Verificar()):
			print("Esperando a que el elemento \"%s\" sea cargado"%nombre_elemento)
			WebDriverWait(self.driver, tiempo).until(lambda driver:self.bElemento(tipo,nombre_elemento))
	
	def tMouse(self, element):
		if(self.Verificar()):
			print("Moviendo mouse sobre el elemento \"%s\""%element.get_attribute("name"))
			ActionChains(self.driver).move_to_element(element)
	
	def sSeleccionarElemento(self, element):#Seleccionar item en caja opciones
		if(self.Verificar(element)):
			ActionChains(self.driver).move_to_element(element).click(element).perform()

	def buscarEnCodigoFuente(self,strings):
		if type(strings) == list:
			for i in strings:
				if i in str(self.driver.page_source):
					return True
		if type(strings) == str:
			if i in str(self.driver.page_source):
				return True
		
		return False
				
	
	def crear_cuenta(self, datos_usuario):	
		input("Presionar enter para comenzar la creacion")
		archivo_cuentas = None
		nombre_archivo = "cuenta_creadas.txt"
		archivo_cuentas = open("cuenta_creadas.txt", "a+") 
		if(datos_usuario == None):
			print("Introduzca los datos de usuario.")
			return False

		"""Se inicia la automatizacion"""
		self.Iniciar()
		pais = datos_usuario["paypal_loc"]
		self.Ir(self.url_paypal[pais]["registro"])
		
		def primero():
			#1 Elementos formulario inicial
			caja_email 				=	self.Buscar_Elemento("email")
			caja_password 			= 	self.Buscar_Elemento("password")
			caja_confirm_password	=   self.Buscar_Elemento("cpassword")
			check_staylogin 		=	self.Buscar_Elemento("seguir_logeado")
			self.tKey(caja_email, datos_usuario["email"])
			self.tKey(caja_password, datos_usuario["passw"])
			self.tKey(caja_confirm_password, datos_usuario["passw"])
			self.sSeleccionarElemento(check_staylogin)
			boton_next_primero		=	self.Buscar_Elemento("next_primero")
			nextt = self.aClic(boton_next_primero)
	

		def segundo():
			#2 Elementos formulario personal
			print("[+]Pasando al formulario de datos..\n\n")
			primer_nombre			= 	self.Buscar_Elemento("firtsName")
			self.tKey(primer_nombre, datos_usuario["firtsName"])
			segundo_nombre 			= 	self.Buscar_Elemento("lastName")
			self.tKey(segundo_nombre, datos_usuario["lastName"])
			calle 					=	self.Buscar_Elemento("address")
			self.tKey(calle,datos_usuario["address"])
			ciudad 					=	self.Buscar_Elemento("city")
			self.tKey(ciudad,datos_usuario["city"])
			postal 					= 	self.Buscar_Elemento("postal")
			self.tKey(postal,datos_usuario["postalCode"])
			telefono				=	self.Buscar_Elemento("phoneNumber")
			self.tKey(telefono,datos_usuario["phoneNumber"])
			#seleccionar estado
			estado 	=	self.Buscar_Elemento("state")
			self.sSeleccionarElemento(estado)
			print("Aceptando terminos..")
			self.tKey2(estado, datos_usuario["state"])
			self.sKey(Keys.RETURN, estado)
			#aceptar terminos
			terminos = self.Buscar_Elemento("terminos")
			self.sSeleccionarElemento(terminos)
			boton_aceptar = 		self.Buscar_Elemento("crear")
			crear = self.aClic(boton_aceptar)
		
		def tercero():		
			#3 Elementos eleccion tarjeta
			print("[+]Pasando a pagina de registro de tarjeta..\n")
			numero_tarjeta  		=  	self.Buscar_Elemento("numero_tarjeta","name")
			expiracion 				= 	self.Buscar_Elemento("expiracion")
			codigo_seg  			= 	self.Buscar_Elemento("cseguridad")
			boton_asociar			= 	self.Buscar_Elemento("asociar")
			self.tKey(numero_tarjeta, datos_usuario["tarjeta"]["numero"])
			self.tKey(expiracion, datos_usuario["tarjeta"]["fecha"]["fecha_acortada"])
			self.tKey(codigo_seg, datos_usuario["tarjeta"]["codigo_seg"])
			self.aClic(boton_asociar)
		
		def cuarto():
			print("[+]Salteando promocion.")
			boton_saltar = self.Buscar_Elemento("saltar_promocion","name")
			self.aClic(boton_saltar)
		
		def quinto():
			print("[+]LLendo a nueva cuenta")
			boton_ir = self.Buscar_Elemento("ir_a_nuevacuenta", "name")
			self.aClic(boton_ir)
			
		iniciado = True
		p1 = False
		p2 = False
		p3 = False
		p4 = False
		p5 = False
		while(iniciado):
			if(p5 is True):
				iniciado = False
			if(p1 is False):
				primero()
				#if(self.buscarEnCodigoFuente("
				p1 = True
			elif(p2 is False):
				textos_pagina_formulario = ["Complete la siguiente","Just a few more "]
				if(self.buscarEnCodigoFuente(textos_pagina_formulario) == False):
						p2 = True
				else:
					segundo()
			elif(p3 is False):
				textos_pagina_tarjeta = ["Asocie una tarjeta","Link a debit"]
				if(self.buscarEnCodigoFuente(textos_pagina_tarjeta) == False):
						p3 = True
				else:
					tercero()
			elif(p4 is False):
				textos_pagina_sucess = ["Viva el presente","Live in the"]
				if(self.buscarEnCodigoFuente(textos_pagina_sucess) == False):
						p4 = True
				else:
					cuarto()
			elif(p5 is False):
				textos_pagina_explorar_ofertas = ["Explorar ofertas","Realice compras","Explore"]
				if(self.buscarEnCodigoFuente(textos_pagina_explorar_ofertas) == False  ):
						p5 = True
				else:
					quinto()

		print("Cuenta creada:")
		
		cuenta = {
				"email":datos_usuario["email"],
				"pass":datos_usuario["passw"]
		}
		self.Salir()
		print("Cuenta creada:",cuenta)
		archivo_cuentas.writelines("%s:%s\n"%(cuenta["email"], cuenta["pass"]))
		return cuenta
