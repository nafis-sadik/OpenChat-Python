from fastapi import APIRouter, WebSocket

socket_module = APIRouter(prefix='/sock')


@socket_module.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
