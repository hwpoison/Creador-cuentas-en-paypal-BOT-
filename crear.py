from generador_datos import Generador_datos
from paypal_driver import PaypalBot


datos = {
		"BIN":			"541301xxxxxxxxxx",
		"address":		"405x Havanna Street",
		"city":			"New York",
		"postalCode":	"10080",
		"phoneNumber":	"336364xxxx",
		"passw":		"netflixxxx",
		"state":		"NY",
		"paypal_loc":	"usa"
}


#Se generan los datos
datos = Generador_datos(datos).datos

#Se inicializa el bot
paypal_bot = PaypalBot()

#Se procede a la creacion
paypal_bot.crear_cuenta(datos)
