## sistema de gestion de prestamos
import json
prestamos = []

#---------Funciones------------
def registrar_prestamo():
    try: 
         cedula_buscar = input("Por favor, ingresa el numero de cedula del deudor:").strip()
         encontrado = None

         for c in prestamos:
              if cedula_buscar == c['deudor']['cc'] and c['estado']== "pendiente":
               print("Lo siento, ya existe un prestamo activo con este numero de cedula.")
               return

              elif cedula_buscar == c['deudor']['cc'] and c['estado'] == "pagado":
               encontrado = c
               datos_deudor = c['deudor']
               break
          
         if not encontrado:
                    datos_deudor = pedir_datos('deudor')
               
         opcion_fiador = input("Deseas ingresar un fiador (Si / No):").strip().lower()
         datos_fiador = None

         if opcion_fiador == "si":
             datos_fiador = pedir_datos("fiador")

         monto = round(float(input("Ingresa el monto del prestamo: ")),2)
         if monto <= 0:
              raise ValueError("No puedes prestar $0.")
         
         while True:
              try:
                   porcentaje = int(input("ingresa el porcentaje de interes (1% - 50%): ").strip())
                   if 1 <= porcentaje <= 50:
                        break
                   else: 
                        print("Porcentaje invalido, Debe estar entre 1 - 50.")
              except :
                   print("error. ingresa un numero valido")

         interes, total = calcular_interes(monto,porcentaje)
         
         prestamo = {
              "deudor": datos_deudor,
              "fiador": datos_fiador,
              "monto": monto,
              "porcentaje": porcentaje,
              "interes": interes,
              "total_pagar":total,
              "saldo_restante": total,
              "abonado": 0,
              "estado": "pendiente"
         }

         prestamos.append(prestamo)
         guardar_datos()

         print(f"El prestamo se registro exitosamnete. Total a pagar: {total:.2f}")

    except ValueError as e:
         print("Error",e)
         
def ver_prestamos_estado(prestamos, estado):
    filtrados = [p for p in prestamos if p['estado'].lower() == estado.lower()]

    if not filtrados:
        print(f"\nNo hay préstamos {estado}")
        return

    print("-" * 50)
    print(f"        Préstamos {estado.capitalize()}")
    print("-" * 50)

    for p in filtrados:
        print(f"""
Deudor: {p['deudor']['nombre']}
CC: {p['deudor']['cc']}
Monto: ${p['monto']:.2f}
Interés: ${p['interes']:.2f}
Total a pagar: ${p['total_pagar']:.2f}
Abonado: ${p['abonado']:.2f}
Saldo restante: ${p['saldo_restante']:.2f}
Estado: {p['estado']}
------------------------------
""")

    print("-" * 50)
    
     
def marcar_prestamos():
        cc_buscar = input("Ingresa la Cedula del deudor que abona dinero: ").strip()

        #  VALIDAR ABONo
        while True:
             try:
                  abono = round(float(input("Ingresa el monto del abono:")),2)
                  if abono > 0:
                       break
                  else:
                       print("El abono debe ser mayor a $0. Intentalo nuevamente")
             except:
                  print("Lo siento, ingresa un numero valido.")

        #  BUSCAR PRÉSTAMO
        prestamo_encontrado = None

        for p in prestamos:
             if p['deudor']['cc'] == cc_buscar and p['estado']=="pendiente":
                  prestamo_encontrado = p
                  break

        if not prestamo_encontrado:
             print("Lo siento,no se encontro prestamo registrado con ese numero de cedula.")
             return
        #  VALIDAR ABONO VS SALDO
        if abono > prestamo_encontrado['saldo_restante']:
             print("Lo siento, no puedes abonar mas dinero del saldo restante.")
             return
        #  ACTUALIZAR DATOS
        prestamo_encontrado['abonado'] += abono
        prestamo_encontrado['saldo_restante'] = round(prestamo_encontrado['saldo_restante'] - abono,2)
        #  VERIFICAR SI YA PAGÓ
        if prestamo_encontrado['saldo_restante'] == 0:
             prestamo_encontrado['estado']= "pagado"
             print(f"el prestamo de {prestamo_encontrado['deudor']['nombre']} ha sido pagado completamente.")
        else:
             print(f"El abono se realizo exitosamente. saldo restante: {prestamo_encontrado['saldo_restante']:.2f}")

        guardar_datos()
        
def guardar_datos():
     with open("prestamos.json", "w", encoding= "utf-8") as archivo:
          json.dump(prestamos,archivo,indent=4)
    
def cargar_datos():   
       try:
            with open("prestamos.json", "r", encoding="utf-8") as archivo:
                 return json.load(archivo)

       except FileNotFoundError:
            return []
                 
def id_consultar():
     nombre = input("Ingresa el nombre del deudor para consultar su numero de cedula:").strip().lower()

     resultado  =[b for b in prestamos if nombre in b['deudor']['nombre'].strip().lower()]
     
     if not resultado:         
          print("Lo siento, no se encontro cedula con ese nombre")
     else:
          print("\nResultados encontrados:\n")
          for i,r in enumerate(resultado, start=1):
               print(
                    f"{i}.Nombre: {r['deudor']['nombre']} | "
                    f"CC: {r['deudor']['cc']} "   
               )

def saldo_consultar():
    cc_buscar = input("Ingresa la cedula del deudor para consultar su saldo: ").strip()

    for i in prestamos:
        if i['deudor']['cc'] == cc_buscar:
            print(f"""
Deudor: {i['deudor']['nombre']}
CC: {i['deudor']['cc']}
Total a pagar: ${i['total_pagar']:.2f}
Abonado: ${i['abonado']:.2f}
Saldo restante: ${i['saldo_restante']:.2f}
Estado: {i['estado']}
""")
            return 

    print("No se encontró ese número de cédula.")
    
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

      
#----------Programa principal--------------
def main():
    global prestamos
    prestamos = cargar_datos()
    while True:
         print("\n-----------menu principal------------")
         print("\n1- Registrar prestamo")
         print("2- Consultar prestamo")
         print("3- abonar prestamo")
         print("4- Salir ")
     
         opcion = input(f"\nIngresa una de las opciones: ")
         
         if opcion == "4":
             guardar_datos()
             print("Saliste del menu")
             break
         elif opcion == "1":
              registrar_prestamo()
         elif opcion == "2":
              while True:
                   print("\n1- Consultar CC.")
                   print("2- Ver prestamos pagados.")
                   print("3- Ver prestamos pendientes.")
                   print("4- Consultar saldo.")
                   print("5- Volver al menu principal.")

                   sub_opcion = input("\nIngresa la opcion: ").strip()
                   if sub_opcion == "1":
                        id_consultar()
                   elif sub_opcion == "2":
                        ver_prestamos_estado(prestamos, "pagado")
                   elif sub_opcion == "3":
                        ver_prestamos_estado(prestamos, "pendiente")
                   elif sub_opcion == "4":
                        saldo_consultar()
                   elif sub_opcion == "5":
                        print("Volviendo al menu principal.")
                        break
                   else:
                        print("Opcion no valida, intentalo nuevamente")
         
         elif opcion == "3":
              marcar_prestamos()
         else:
              print("Opcion no valida. intentalo nuevamente")

if __name__ == "__main__":
     main()





         


