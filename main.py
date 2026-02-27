## sistema de gestion de prestamos
import uuid
import json

prestamos = []

#---------Funciones------------
def registrar_prestamo():
    try:
        nombre = input("Ingresa el nombre completo del deudor: ").strip()
        monto = round(float(input("Ingresa el monto del prestamo: ")),2)

        if monto <= 0:
            raise ValueError("el monto debe ser mayor a 0")
        
        prestamo = { 
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "monto": monto,
            "saldo_restante" : monto,
            "estado": "pendiente"
        }
        prestamos.append(prestamo)
        guardar_datos()
        print(f"prestamo registrado con ID: {prestamo['id']}  |  Monto: ${prestamo['monto']:.2f}")
        
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
               print(f"ID: {p['id']} | Deudor: {p['nombre']} | monto: ${p['monto']:.2f}")
          print("-" * 40)
    
     
def marcar_prestamos():
     try: 
          id_buscar = input("Ingresa el ID del deudor que abona dinero: ").strip().lower()
          abono = round(float(input("Ingresa el monto del abono: ")),2)

          if abono <= 0:
               print("No puedes abonar 0 pesos.")
               return
          
          for p in prestamos:
               if p['id'].lower() == id_buscar:

                    if p['estado'] == 'pagado':
                         print("No puedes abonar a un prestamo pagado.")
                         return
                    if abono > p['saldo_restante']:
                         print("No puedes abonar mas dinero del saldo actual")
                         return
                    
                    p['saldo_restante'] = round(p['saldo_restante'] - abono,2)
                    if p['saldo_restante'] <= 0:
                         p['saldo_restante'] = 0
                         p['estado'] = 'pagado'
                    
                    guardar_datos()
                    print("El abono se realizo correctamente")
                    return

          print("No se encontro prestamo con ese ID.")
          
     except ValueError:
          print("Ingrresa un monto valido")
                    

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
     nombre = input("ingresa el nombre del deudor para consultar ID:").strip().lower()
     resultados = []
     
     for p in prestamos: 
          if nombre in p['nombre'].strip().lower():
               resultados.append(p)    

     if not resultados:
          print("No se encontro ese nombre")
     else:
          print("\nResultados encontrados:\n")
          for i,r in enumerate(resultados, start=1):
               print(
                    f"{i}.Nombre: {r['nombre']} | "
                    f"ID: {r['id']} "   
               )

def saldo_consultar():
     id_buscar = input("Ingresa el id del deudor para consultar su saldo: ").strip().lower()

     for i in prestamos:
          if i['id'].lower() == id_buscar:
               print(
                    f"Deudor: {i['nombre']}  | "
                    f"Saldo inicial: ${i['monto']:.2f}  | "
                    f"Saldo restante: ${i['saldo_restante']:.2f}"
               )
               return

     print("No se encontro ese id.")

     
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
                   print("\n1- Consultar ID.")
                   print("2- Ver prestamos pagados.")
                   print("3- Ver prestamos pendientes.")
                   print("4- Consultar saldo / estado.")
                   print("5- Volver al menu principal.")

                   sub_opcion = input("\nIngresa la opcion: ").strip().lower()
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

# crear otra funcion para la opcion 4








  