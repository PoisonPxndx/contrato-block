from web3 import Web3
import json
import time

# 🔐 Configuración
private_key = 'c012dc433f9751c7da56dc5e94f1bd5581e0b139ce02b2b685b641f425e11000'
sender_address = '0xE1aF495F286be14fb8EcA35a989088908c2b1444'
contract_address = '0xdB9e58fD7FC671240801B7a59b91A3b805c1CbBc'
rpc_url = 'https://sepolia.infura.io/v3/96b036b5796b478098065135796890fc'


# 🌐 Conexión Web3
w3 = Web3(Web3.HTTPProvider(rpc_url))

# 📦 Cargar ABI
with open('TurtleTracker_abi.json', 'r') as abi_file:
    abi = json.load(abi_file)

contract = w3.eth.contract(address=contract_address, abi=abi)

# 🚀 Enviar transacción
def send_transaction(tx):
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"\n📨 Transacción enviada: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Confirmada en bloque {receipt.blockNumber}")
    return receipt

# 🐢 Crear TurtleBot
def create_bot():
    name = input("Nombre del TurtleBot: ")
    nonce = w3.eth.get_transaction_count(sender_address)
    tx = contract.functions.createBot(name).build_transaction({
        'chainId': 11155111,
        'nonce': nonce,
        'gas': 200000,
        'maxFeePerGas': w3.to_wei('50', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
        'from': sender_address
    })
    send_transaction(tx)

# 🛣️ Crear recorrido
def create_route():
    name = input("Nombre del recorrido: ")
    nonce = w3.eth.get_transaction_count(sender_address)
    tx = contract.functions.createRoute(name).build_transaction({
        'chainId': 11155111,
        'nonce': nonce,
        'gas': 200000,
        'maxFeePerGas': w3.to_wei('50', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
        'from': sender_address
    })
    send_transaction(tx)

def add_position():
    route_id = int(input("ID del recorrido al que quieres agregar posiciones: "))
    try:
        route_name = contract.functions.getRouteName(route_id).call()
        print(f"🛣️ Agregando posiciones a: {route_name} (ID: {route_id})")
    except Exception as e:
        print(f"❌ No se pudo obtener el nombre del recorrido: {e}")
        return

    while True:
        try:
            x = int(input("x: "))
            y = int(input("y: "))
            z = int(input("z: "))
        except ValueError:
            print("❌ Entrada inválida. Debe ser un número entero.")
            continue

        nonce = w3.eth.get_transaction_count(sender_address)
        tx = contract.functions.addPositionToRoute(route_id, x, y, z).build_transaction({
            'chainId': 11155111,
            'nonce': nonce,
            'gas': 200000,
            'maxFeePerGas': w3.to_wei('50', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
            'from': sender_address
        })
        send_transaction(tx)

        seguir = input("¿Quieres agregar otra posición? (s/n): ").strip().lower()
        if seguir != 's':
            print("🔙 Regresando al menú...")
            break

# 🔗 Asignar recorrido a bot
def assign_route():
    bot_id = int(input("ID del bot: "))
    route_id = int(input("ID del recorrido: "))
    nonce = w3.eth.get_transaction_count(sender_address)
    tx = contract.functions.assignRouteToBot(bot_id, route_id).build_transaction({
        'chainId': 11155111,
        'nonce': nonce,
        'gas': 200000,
        'maxFeePerGas': w3.to_wei('50', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
        'from': sender_address
    })
    send_transaction(tx)

# ✏️ Renombrar bot o recorrido
def rename_entity():
    choice = input("¿Renombrar bot (b) o recorrido (r)? ").lower()
    if choice == 'b':
        bot_id = int(input("ID del bot: "))
        new_name = input("Nuevo nombre: ")
        nonce = w3.eth.get_transaction_count(sender_address)
        tx = contract.functions.renameBot(bot_id, new_name).build_transaction({
            'chainId': 11155111,
            'nonce': nonce,
            'gas': 200000,
            'maxFeePerGas': w3.to_wei('50', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
            'from': sender_address
        })
        send_transaction(tx)
    elif choice == 'r':
        route_id = int(input("ID del recorrido: "))
        new_name = input("Nuevo nombre: ")
        nonce = w3.eth.get_transaction_count(sender_address)
        tx = contract.functions.renameRoute(route_id, new_name).build_transaction({
            'chainId': 11155111,
            'nonce': nonce,
            'gas': 200000,
            'maxFeePerGas': w3.to_wei('50', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
            'from': sender_address
        })
        send_transaction(tx)
    else:
        print("❌ Opción inválida.")

# 🔍 Consultar posición
def get_position():
    route_id = int(input("ID del recorrido: "))
    index = int(input("Índice de la posición: "))
    try:
        x, y, z = contract.functions.getPosition(route_id, index).call()
        print(f"📍 Posición #{index} → x: {x}, y: {y}, z: {z}")
    except Exception as e:
        print(f"⚠️ Error al obtener posición: {e}")

# 📏 Ver longitud de recorrido
def get_route_length():
    route_id = int(input("ID del recorrido: "))
    try:
        length = contract.functions.getRouteLength(route_id).call()
        print(f"📏 El recorrido tiene {length} posiciones.")
    except Exception as e:
        print(f"⚠️ Error al obtener longitud: {e}")

def comenzar_recorrido():
    route_id = int(input("ID del recorrido a seguir: "))
    try:
        total = contract.functions.getRouteLength(route_id).call()
        route_name = contract.functions.getRouteName(route_id).call()
        print(f"📍 El recorrido '{route_name}' tiene {total} posiciones.")
    except Exception as e:
        print(f"❌ No se pudo obtener el recorrido: {e}")
        return

    print("🚀 Comenzando recorrido... Ingresa las posiciones cada 3 segundos.")

    i = 0
    while i < total:
        print(f"\n🔄 Posición #{i + 1} de {total}")
        try:
            expected_x, expected_y, expected_z = contract.functions.getPosition(route_id, i).call()
        except Exception as e:
            print(f"⚠️ Error al obtener posición esperada: {e}")
            break

        try:
            x = int(input("x: ").strip())
            y = int(input("y: ").strip())
            z = int(input("z: ").strip())
        except ValueError:
            print("❌ Entrada inválida. Debe ser un número entero.")
            continue

        if x == expected_x and y == expected_y and z == expected_z:
            print("✅ Posición correcta.")
            i += 1
            time.sleep(3)
        else:
            print(f"❌ Posición incorrecta.")
            print(f"   Esperado → x: {expected_x}, y: {expected_y}, z: {expected_z}")
            print(f"   Recibido → x: {x}, y: {y}, z: {z}")
            print("\n⚠️ ¿Qué deseas hacer?")
            print("1. Reiniciar recorrido")
            print("2. Volver al menú")
            opcion = input("Selecciona una opción (1 o 2): ").strip()
            if opcion == '1':
                print("🔁 Reiniciando recorrido desde el inicio...")
                i = 0
            else:
                print("🔙 Regresando al menú...")
                break

    if i == total:
        print("\n🎯 Recorrido completado exitosamente.")


def listar_bots_y_recorridos():
    try:
        total_bots = contract.functions.botCounter().call()
        total_routes = contract.functions.routeCounter().call()
    except Exception as e:
        print(f"❌ Error al obtener contadores: {e}")
        return

    print("\n📋 Lista de TurtleBots y sus recorridos:\n")
    rutas_asociadas = set()

    for bot_id in range(total_bots):
        try:
            bot_name = contract.functions.getBotName(bot_id).call()
            print(f"🐢 {bot_name} (ID: {bot_id})")
            route_ids = contract.functions.getBotRoutes(bot_id).call()
            if not route_ids:
                print("   - (sin recorridos asignados)")
            for route_id in route_ids:
                try:
                    route_name = contract.functions.getRouteName(route_id).call()
                    print(f"   - {route_name} (ID: {route_id})")
                    rutas_asociadas.add(route_id)
                except:
                    print(f"   - Ruta {route_id} (no encontrada)")
        except Exception as e:
            print(f"⚠️ Error al leer bot {bot_id}: {e}")

    print("\n📂 Recorridos no asociados:")
    for route_id in range(total_routes):
        if route_id not in rutas_asociadas:
            try:
                route_name = contract.functions.getRouteName(route_id).call()
                print(f"   - {route_name} (ID: {route_id})")
            except:
                print(f"   - Ruta {route_id} (no encontrada)")

# 🧭 Menú principal
def main():
    while True:
        print("\n📋 Opciones:")
        print("1. Crear TurtleBot")
        print("2. Crear recorrido")
        print("3. Agregar posición a recorrido")
        print("4. Asignar recorrido a bot")
        print("5. Renombrar bot o recorrido")
        print("6. Consultar posición")
        print("7. Ver longitud de recorrido")
        print("8. Comenzar recorrido")
        print("9. Lista bots y recorridos")
        print("10. Salir")

        choice = input("Selecciona una opción (1-10): ")

        if choice == '1':
            create_bot()
        elif choice == '2':
            create_route()
        elif choice == '3':
            add_position()
        elif choice == '4':
            assign_route()
        elif choice == '5':
            rename_entity()
        elif choice == '6':
            get_position()
        elif choice == '7':
            get_route_length()
        elif choice == '8':
            comenzar_recorrido()
        elif choice == '9':
            listar_bots_y_recorridos()
        elif choice == '10':
            print("👋 Saliendo...")

            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
# Verificación directa del nombre del recorrido

if __name__ == "__main__":
    main()
