from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from tasks import generate_text

app = FastAPI()

@app.websocket("/generate-text/{model_name}")
async def generate(websocket: WebSocket, model_name: str):
    await websocket.accept()
    try:
        while True:
            prompt = await websocket.receive_text()
            task = generate_text.delay(prompt, model_name)
            while not task.ready():
                await websocket.send_text("Generating...")
            result = task.get()
            await websocket.send_text(result)
    except WebSocketDisconnect:
        # Handle the WebSocket disconnection gracefully
        print("WebSocket disconnected")