## sistema de gestion de prestamos
import json
prestamos = []

#---------Funciones------------
def registrar_prestamo(prestamos): # se implemento lo de la nueva funcion buscar prestamo averiguar como funciona todo
    try: 
        cedula_buscar = input("Por favor, ingresa el numero de cedula del deudor:").strip()

        prestamo_activo = buscar_prestamo_cc(prestamos, cedula_buscar,"pendiente")
        prestamo_existente = buscar_prestamo_cc(prestamos,cedula_buscar)
        if prestamo_activo:
             print("Error: ya existe un prestamo activo con esta cedula.")
             return
        elif prestamo_existente:
             datos_deudor = prestamo_existente['deudor']   
        else :
             datos_deudor = pedir_datos('deudor')
        
        opcion_fiador = input("Deseas ingresar un fiador (Si / No):").strip().lower()
        datos_fiador = None

        if opcion_fiador in ["si", "sí", "s"]:
            datos_fiador = pedir_datos("fiador")

        while True:
             try:
                 monto = round(float(input("Ingresa el monto del prestamo: ")), 2)
                 if monto > 0:
                      break
                 else: 
                      print("Error: el monto debe ser mayor a $0")

             except ValueError:
                  print("Error: ingresa un numero valido.")

        while True:
            try:
                porcentaje = int(input("ingresa el porcentaje de interes (1% - 50%): ").strip())
                if 1 <= porcentaje <= 50:
                    break
                else: 
                    print("error: el porcentaje debe estar entre 1 - 50.")
            except ValueError:
                 print("error: ingresa un numero valido")

        prestamos,prestamo = crear_prestamo(
            prestamos,
            datos_deudor,
            datos_fiador,
            monto,
            porcentaje
        )

        guardar_datos(prestamos)

        print(f"El prestamo se registro exitosamente. Total a pagar: ${prestamo['total_pagar']:.2f}")

    except ValueError as e:
        print(f"Error: {e}")
         
def mostrar_prestamos_estado(prestamos, estado): 
    filtrados = obtener_prestamos_estado(prestamos, estado)

    if not filtrados:
        print(f"\nNo hay préstamos {estado}")
        return
    
    titulo = estado.capitalize()
    print("-" * 50)
    print(f"        Préstamos {titulo}")
    print("-" * 50)

    for p in filtrados:
         print(formatear_prestamo(p))

    print("-" * 50)
    
     
def marcar_prestamos(prestamos):
        cc_buscar = input("Ingresa la Cedula del deudor que abona dinero: ").strip()

        #  VALIDAR ABONo
        while True:
             try:
                  abono = round(float(input("Ingresa el monto del abono:")),2)
                  if abono > 0:
                       break
                  else:
                       print("Error: el abono debe ser mayor a $0. Intentalo nuevamente")
             except ValueError:
                  print("Error: ingresa un numero valido.")
                  
        try:
          prestamo = abonar_prestamo(prestamos, cc_buscar, abono)
          if prestamo['estado']== "pagado":
               print(f"El prestamo de {prestamo['deudor']['nombre']} ha sido pagado completamente.")
          else:
               print(f"Abono realizado exitosamente. Saldo restante: ${prestamo['saldo_restante']:.2f}")

          guardar_datos(prestamos)

        except ValueError as e:
             print(f"Error: {e}")
        
def guardar_datos(prestamos):
     with open("prestamos.json", "w", encoding= "utf-8") as archivo:
          json.dump(prestamos,archivo,indent=4)
    
def cargar_datos():   
       try:
            with open("prestamos.json", "r", encoding="utf-8") as archivo:
                 return json.load(archivo)

       except FileNotFoundError:
            return []
                 
def id_consultar(prestamos):
     nombre = input("Ingresa el nombre del deudor para consultar su numero de cedula:").strip().lower()

     try:
          resultado = buscar_por_nombre(prestamos,nombre)

          print("\nResultados encontrados:\n")
          for i,r in enumerate(resultado, start=1):
               print(
                    f"{i}. Nombre: {r['deudor']['nombre']} | "
                    f"CC: {r['deudor']['cc']} "   
               )
     except ValueError as e:
          print(e)


def saldo_consultar(prestamos):
    cc_buscar = input("Ingresa la cedula del deudor para consultar su saldo: ").strip()

    try :
         prestamo = obtener_saldo(prestamos,cc_buscar)
    
         print(f"""
Deudor: {prestamo['deudor']['nombre']}
CC: {prestamo['deudor']['cc']}
Total a pagar: ${prestamo['total_pagar']:.2f}
Abonado: ${prestamo['abonado']:.2f}
Saldo restante: ${prestamo['saldo_restante']:.2f}
Estado: {prestamo['estado']}
""")
    except ValueError as e:
         print(e)

def pedir_datos(tipo):
     nombre= input(f"Ingresa el nombre del {tipo}: ").strip()
     cc = input(f"ingresa el numero de cedula del {tipo}: ").strip()
     cel = input(f"Ingresa numero de telefono del {tipo}: ").strip()
     direccion = input(f"Ingresa la direccion del {tipo}: ").strip()

     datos = {
          "nombre": nombre,
          "cc": cc,
          "telefono":cel,
          "direccion":direccion
     }
     if any(valor == "" for valor in datos.values()):
          raise ValueError("Hay datos vacios,por favor completar.")
     
     if not cc.isdigit():
          raise ValueError("lo siento, la cedula debe ser numerica.")
     if not cel.isdigit():
          raise ValueError("lo siento, el telefono solo debe ser numerico")
     
     return datos

def calcular_interes(monto,porcentaje):
     interes = monto * (porcentaje / 100)
     total = monto + interes
     return interes, total

def crear_prestamo(prestamos, datos_deudor, datos_fiador, monto, porcentaje):
    # Validar préstamo activo
    for p in prestamos:
        if datos_deudor['cc'] == p['deudor']['cc'] and p['estado'] == "pendiente":
            raise ValueError("Ya existe un préstamo activo para esta cédula")

    interes, total = calcular_interes(monto, porcentaje)

    prestamo = {
        "deudor": datos_deudor,
        "fiador": datos_fiador,
        "monto": monto,
        "porcentaje": porcentaje,
        "interes": interes,
        "total_pagar": total,
        "saldo_restante": total,
        "abonado": 0,
        "estado": "pendiente"
    }

    prestamos.append(prestamo)
    return prestamos,prestamo # entender por que se pone las dos valores y en registrar se llama asi tambien

def abonar_prestamo(prestamos, cc, abono):
     prestamo = buscar_prestamo_cc(prestamos, cc, "pendiente") # esta modificado estudiar como funciona

     if not prestamo:
          raise ValueError("No se encontró un préstamo pendiente para esa cédula.")
     
     if abono > prestamo['saldo_restante']:
          raise ValueError("Lo siento, no puedes abonar mas del saldo actual.")
     
     #actualizar resultados
     prestamo['abonado'] += abono
     prestamo['saldo_restante'] = round(prestamo['saldo_restante'] - abono,2)
                
                 # validar cuando el saldo sea pagado
     if prestamo['saldo_restante'] == 0 :
          prestamo['estado'] = "pagado"
                     
     return prestamo
     

def obtener_saldo(prestamos,cc):
     prestamo = buscar_prestamo_cc(prestamos, cc) # nuevo por que no se usa estado aqui cuando se llama la funcion

     if not prestamo:
          raise ValueError("No se encontró ese número de cédula.")
     
     return prestamo

def buscar_por_nombre(prestamos, nombre):
     resultado = [b for b in prestamos if nombre in b['deudor']['nombre'].strip().lower()]

     if not resultado:
          raise ValueError("Lo siento, no se encontro cedula con ese nombre.")

     return resultado

def obtener_prestamos_estado(prestamos,estado):
     return [p for p in prestamos if p['estado'].lower()== estado.lower()]

def formatear_prestamo(p):
     fiador = "No tiene"
     if isinstance(p.get('fiador'), dict):
          fiador = p['fiador'].get('nombre', "No tiene") # nuevo que hace esto?

     return f"""Deudor: {p['deudor']['nombre']}
CC: {p['deudor']['cc']}
Fiador : {fiador}
Monto: ${p['monto']:.2f}
Interés: ${p['interes']:.2f}
Total a pagar: ${p['total_pagar']:.2f}
Abonado: ${p['abonado']:.2f}
Saldo restante: ${p['saldo_restante']:.2f}
Estado: {p['estado']}
------------------------------"""

def buscar_prestamo_cc(prestamos, cc, estado= None): # nuevo ver como funciona
     for p in prestamos:
          if p['deudor']['cc']== cc:
               if estado and p['estado'] != estado:
                    continue
               return p
     return None
     
  
#----------Programa principal--------------
def main():
    prestamos = cargar_datos()
    while True:
         print("\n-----------menu principal------------")
         print("\n1- Registrar prestamo")
         print("2- Consultar prestamo")
         print("3- abonar prestamo")
         print("4- Salir ")
     
         opcion = input(f"\nIngresa una de las opciones: ")
         
         if opcion == "4":
             guardar_datos(prestamos)
             print("Saliste del menu")
             break
         elif opcion == "1":
              registrar_prestamo(prestamos)
         elif opcion == "2":
              while True:
                   print("\n1- Consultar CC.")
                   print("2- Ver prestamos pagados.")
                   print("3- Ver prestamos pendientes.")
                   print("4- Consultar saldo.")
                   print("5- Volver al menu principal.")

                   sub_opcion = input("\nIngresa la opcion: ").strip()
                   if sub_opcion == "1":
                        id_consultar(prestamos)
                   elif sub_opcion == "2":
                        mostrar_prestamos_estado(prestamos, "pagado")
                   elif sub_opcion == "3":
                        mostrar_prestamos_estado(prestamos, "pendiente")
                   elif sub_opcion == "4":
                        saldo_consultar(prestamos)
                   elif sub_opcion == "5":
                        print("Volviendo al menu principal.")
                        break
                   else:
                        print("Opcion no valida, intentalo nuevamente")
         
         elif opcion == "3":
              marcar_prestamos(prestamos)
         else:
              print("Opcion no valida. intentalo nuevamente")

if __name__ == "__main__":
     main()

## cambiar todas las llamadas a las funciones por que sin global prestamos ya no funciona igual

# por que sin global prestamos toca cambiar como se llaman a las funciones y colocar prestamo como parametro




         


