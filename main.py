## sistema de gestion de prestamos
import uuid
import json
prestamos = []

#---------Funciones------------
def registrar_prestamo():
    try:
        nombre = input("Ingresa tu nombre completo: ")
        monto = float(input("Ingresa el monto del prestamo: "))

        if monto <= 0:
            raise ValueError("el monto debe ser mayor a 0")
        
        prestamo = { 
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "monto": monto,
            "estado": "pendiente"
        }
        prestamos.append(prestamo)
        guardar_datos()
        print("prestamo registrado correctamente")
        
    except ValueError as e:
        print("Error",e)

def mostrar_prestamos():
    if not prestamos:
        print("No hay prestamos registrados")
        return 
    
    for prestamo in prestamos:
        print(
            f"ID:{prestamo['id']} |"
            f"Nombre: {prestamo['nombre']} |"
            f"Monto: {prestamo['monto']} |"
            f"Estado: {prestamo['estado']}"
        )  

def marcar_prestamos():

          id_buscar = input("Ingresa el id a marcar como pagado: ")
          encontrado = False
          
          for p in prestamos:
               if p['id'] == id_buscar:
                    p['estado'] = "pagado"
                    guardar_datos()
                    encontrado = True
                    print("El prestamo ha sido pagado")
                    break
          if not encontrado: 
               print("No se encontro un prestamo con ese ID")  
  

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



#----------Programa principal--------------
def main():
    cargar_datos()
    while True:
         print("\n-----------menu principal------------")
         print("\n1- Registrar prestamo")
         print("2- Ver prestamos")
         print("3- Marcar prestamos como pagados")
         print("4- salir ")
         
         opcion = input(f"\nIngresa una de las opciones: ")
         
         if opcion == "4":
             guardar_datos()
             print("Saliste del menu")
             break
         elif opcion == "1":
              registrar_prestamo()
         elif opcion == "2":
              mostrar_prestamos()
         elif opcion == "3":
              marcar_prestamos()
         else:
              print("Opcion no valida. intentalo nuevamente")

if __name__ == "__main__":
     main()













  