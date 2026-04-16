## sistema de gestion de prestamos
import json
prestamos = []

#---------Funciones------------
def registrar_prestamo(prestamos): 
    try: 
        cedula_buscar,datos_fiador,monto,porcentaje = pedir_datos_prestamo()

        prestamo_activo = buscar_prestamo_cc(prestamos, cedula_buscar,"pendiente")
      
        if prestamo_activo:
             raise ValueError("Ya existe un prestamo activo con esa cedula.")
             
             
        datos_deudor = obtener_o_crear_deudor(prestamos,cedula_buscar)
             

        prestamo = crear_prestamo_logica(
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
        print(f"\nNo hay préstamos en estado: {estado}")
        return
    
    titulo = estado.capitalize()
    print("-" * 50)
    print(f"        Préstamos {titulo}")
    print("-" * 50)

    for p in filtrados:
        print(formatear_prestamo(p))

    print("-" * 50)
    

def marcar_prestamos(prestamos):
        cc_buscar = input("Ingresa la cedula del deudor que va a abonar: ").strip()

        #  VALIDAR ABONo
        while True:
             try:
                  abono = round(float(input("Ingresa el monto del abono:")),2)
                  if abono > 0:
                       break
                  else:
                       raise ValueError("El abono debe ser mayor a $0.")
             except ValueError as e:
                  print(f"Error: {e}")
                  
        try:
          prestamo = abonar_prestamo(prestamos, cc_buscar, abono)
          if prestamo.get('estado', '')== "pagado":
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
       except json.JSONDecodeError:
            raise ValueError("Error: el archivo de datos esta dañado. No se cargaran los datos")
       



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

    while True:
        nombre = input(f"Ingresa el nombre del {tipo}: ").strip()
        if nombre == "":
            print("Error: el nombre no puede estar vacío.")
        else:
            break

    while True:
        cc = input(f"Comfirma el número de cédula del {tipo}: ").strip()
        if not cc.isdigit():
            print("Error: la cédula debe ser numérica.")
        else:
            break

    while True:
        cel = input(f"Ingresa número de teléfono del {tipo}: ").strip()
        if not cel.isdigit():
            print("Error: el teléfono debe ser numérico.")
        else:
            break

    while True:
        direccion = input(f"Ingresa la dirección del {tipo}: ").strip()
        if direccion == "":
            print("Error: la dirección no puede estar vacía.")
        else:
            break

    return {
        "nombre": nombre,
        "cc": cc,
        "telefono": cel,
        "direccion": direccion
    }

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
    return prestamo 

def abonar_prestamo(prestamos, cc, abono):
     prestamo = buscar_prestamo_cc(prestamos, cc, "pendiente") 

     if not prestamo:
          raise ValueError("No se encontró un préstamo pendiente para esa cédula.")
     
     if abono > prestamo['saldo_restante']:
          raise ValueError("No puedes abonar mas del saldo actual.")
     
     #actualizar resultados
     prestamo['abonado'] += abono
     prestamo['saldo_restante'] = round(prestamo['saldo_restante'] - abono,2)
                
                 # validar cuando el saldo sea pagado
     if prestamo['saldo_restante'] == 0 :
          prestamo['estado'] = "pagado"
                     
     return prestamo
     

def obtener_saldo(prestamos,cc):
     prestamo = buscar_prestamo_cc(prestamos, cc) 

     if not prestamo:
          raise ValueError("No se encontró ese número de cédula.")
     
     return prestamo

def buscar_por_nombre(prestamos, nombre):
     nombre_buscar = nombre.strip().lower()
     if not nombre_buscar:
          raise ValueError("Debe ingresar un nombre valido.")

     resultado = [b for b in prestamos if nombre_buscar in b.get('deudor',{}).get('nombre',"").strip().lower()]

     if not resultado:
          raise ValueError("No se encontraron prestamos con ese nombre.")

     return resultado

def obtener_prestamos_estado(prestamos,estado):
     return [p for p in prestamos if p.get('estado', '').lower()== estado.lower()] 

def formatear_prestamo(p):
     fiador = "No tiene"
     if isinstance(p.get('fiador'), dict): 
          fiador = p['fiador'].get('nombre', "No tiene") 

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

def buscar_prestamo_cc(prestamos, cc, estado= None): 
     for p in prestamos:
          if p['deudor']['cc']== cc:
               if estado and p['estado'] != estado:
                    continue
               return p
     return None

def crear_prestamo_logica(prestamos,datos_deudor,datos_fiador,monto,porcentaje):
     prestamo = crear_prestamo(
          prestamos,
          datos_deudor,
          datos_fiador,
          monto,
          porcentaje

     )

     return prestamo


def pedir_datos_prestamo():
     while True:
          cedula_buscar = input("Ingresa el numero de cedula del deudor: ").strip()
          if not cedula_buscar.isdigit():
               print("Error: la cedula debe ser numerica.")
          else:
               break
     datos_fiador = None
     while True:
          opcion_fiador = input("Deseas ingresar un fiador (Si / No): ").strip().lower()

          if opcion_fiador in ["si", "sí", "s"]:
               datos_fiador = pedir_datos("fiador")
               break
          elif opcion_fiador in ["no", "n"]:
               break
          else:
               print("Error: responde solo 'Si' o 'No'.")
               
     while True:
          try:
               monto =round(float(input("ingresa el monto del prestamo:")),2)
               if monto > 0 :
                    break
               else: 
                    raise ValueError("El monto debe ser mayor a $0")
          except ValueError as e:
               print(f"Error: {e}")
     
     while True:
          try:
               porcentaje = int(input("Ingresa el porcentaje de interes (1% - 50%):").strip())
               if 1 <= porcentaje <= 50:
                    break
               else:
                    raise ValueError("El porcentaje debe estar entre 1 - 50.")

          except ValueError as e:
               print(f"Error: {e}")

     return cedula_buscar,datos_fiador,monto,porcentaje

def obtener_o_crear_deudor(prestamos,cc):
     prestamo_existente = buscar_prestamo_cc(prestamos,cc)
     
     if prestamo_existente :
          return prestamo_existente['deudor']
     
     return pedir_datos('deudor')

          
  
#----------Programa principal--------------
def main():
    try:
         prestamos = cargar_datos()
    except ValueError as e:
         print(f"Error: {e}")
         return
    
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






         


