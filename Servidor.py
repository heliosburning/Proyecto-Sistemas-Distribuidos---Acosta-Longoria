import asyncio
import websockets
import json

# Almacena todas las conexiones de clientes.
clientes = set()

async def chat(websocket, path):
    # Agrega el nuevo cliente a la lista de clientes.
    clientes.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            nombre = data["nombre"]
            mensaje = data["mensaje"]
            # Transmite el mensaje a todos los clientes conectados.
            for cliente in clientes:
                await cliente.send(json.dumps({"nombre": nombre, "mensaje": mensaje}))
    finally:
        # Cuando el cliente se desconecta, lo eliminamos de la lista.
        clientes.remove(websocket)

start_server = websockets.serve(chat, "192.168.0.16", 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()