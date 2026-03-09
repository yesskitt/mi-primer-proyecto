## sistema de gestion de prestamos
import json

prestamos = []

#---------Funciones------------
def registrar_prestamo():
    try: 
         datos_deudor = pedir_datos('deudor')
         if any(p['deudor']['cc'] == datos_deudor['cc'] and p['estado'] == "pendiente" for p in prestamos):
              print("Lo siento, ya existe un prestamo pendiente con ese numero de cedula")
              return
         
         opcion_fiador = input("Desea ingresar un fiador (Si / No):").strip().lower()
         datos_fiador = None
         if opcion_fiador == "si":
              datos_fiador = pedir_datos('fiador')

         monto = round(float(input("Ingresa el monto del prestamo: ")),2)

         if monto <= 0:
              raise ValueError("No puedes prestar $ 0.")
         
         prestamo = {
              "deudor": datos_deudor,
              "fiador": datos_fiador,
              "saldo_inicial": monto,
              "saldo_restante": monto,
              "estado": "pendiente"
         }
         prestamos.append(prestamo)
         guardar_datos()

         print(f"Se registró el préstamo exitosamente para {datos_deudor['nombre']}")
         
    except ValueError as e:
         print("Error",e)

                 
         
def ver_prestamos_estado(prestamos, estado):
     filtrados = [p for p in prestamos if p['estado'].lower() == estado.lower()]

     if not filtrados:
          print(f"\nNo hay prestamos {estado}")
     else: 
          print("-" * 40)
          print(f"        prestamos {estado}")
          print("-" * 40)
          for p in filtrados:
               print(f"CC: {p['deudor']['cc']} | Deudor: {p['deudor']['nombre']} | monto: ${p['saldo_inicial']:.2f}")
          print("-" * 40)
    
     
def marcar_prestamos():
     try: 
          cc_buscar = input("Ingresa la CC del deudor que abona dinero: ").strip()
          abono = round(float(input("Ingresa el monto del abono: ")),2)

          if abono <= 0:
               raise ValueError("Lo siento, no puedes abonar $ 0.")
          
          
          prestamo_encontrado = None

          # Buscar solo el prestamo pendiente
          for p in prestamos:
               if p['deudor']['cc'] == cc_buscar and p['estado']=="pendiente":
                    prestamo_encontrado = p
                    break
          
          if prestamo_encontrado is None:
               print("No hay ningun prestamo pendiente con esa cedula")
               return
          
          if abono > prestamo_encontrado['saldo_restante']:
               print("Lo siento, no puedes abonar mas dinero del saldo actual.")
               return
          
          prestamo_encontrado['saldo_restante'] = round(prestamo_encontrado['saldo_restante'] - abono ,2)

          if prestamo_encontrado['saldo_restante'] <= 0:
               prestamo_encontrado['saldo_restante'] = 0
               prestamo_encontrado['estado'] = "pagado"

          guardar_datos()
          print("El abono se realizo correctamente")

     except ValueError as e :
          print("Error:",e)
          

def guardar_datos():
     with open("prestamos.json", "w", encoding= "utf-8") as archivo:
          json.dump(prestamos,archivo,indent=4)
    
def cargar_datos():
       global prestamos
       try:
            with open("prestamos.json", "r", encoding="utf-8") as archivo:
                 prestamos = json.load(archivo)

       except FileNotFoundError:
            prestamos = []

def id_consultar():
     nombre = input("Ingresa el nombre del deudor para consultar su CC:").strip().lower()
     resultados = []
     
     for p in prestamos: 
          if nombre in p['deudor']['nombre'].strip().lower():
               resultados.append(p)    

     if not resultados:
          print("Lo siento, no se encontro ese nombre")
     else:
          print("\nResultados encontrados:\n")
          for i,r in enumerate(resultados, start=1):
               print(
                    f"{i}.Nombre: {r['deudor'] ['nombre']} | "
                    f"CC: {r['deudor']['cc']} "   
               )

def saldo_consultar():
     cc_buscar = input("Ingresa la CC del deudor para consultar su saldo: ").strip()

     for i in prestamos:
          if i['deudor']['cc'] == cc_buscar:
               print(
                    f"Deudor: {i['deudor']['nombre']}  | "
                    f"Saldo inicial: ${i['saldo_inicial']:.2f}  | "
                    f"Saldo restante: ${i['saldo_restante']:.2f}  | "
                    f"Estado: {i['estado']}"
               )
               return

     print("No se encontro ese numero de cedula.")

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
          raise ValueError("hay datos vacios,por favor completar")
     
     if not cc.isdigit():
          raise ValueError("lo siento, la cedula debe ser numerica.")
     if not cel.isdigit():
          raise ValueError("lo siento, el telefono solo debe ser numerico")
     
     return datos

     
#----------Programa principal--------------
def main():
    cargar_datos()
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




# permitir un nuevo prestamo sin repetir datos: si la cedula  no existe pide todos los datos, si existe  y el saldo esta pagado, pedir solo el monto
#si existe y el saldo es mayor a 0 bloquear

#mensajes de prestamos cancelados: cuando llegue a 0 mostrar prestamo cancelado y dejar listo para pedir otro


         
