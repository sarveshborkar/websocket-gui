import asyncio
import websockets
import random
import logging
import signal
import sys

# Configure logging to log only the message content to the log file
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(message)s")

# Counter to keep track of the total messages received
message_count = 0

async def handle_message(websocket, path):
    global message_count
    try:
        async for message in websocket:
            # Increment the message count
            message_count += 1
            
            # Log only the received message content
            logging.info(message)
            
            # Append a random number to the message and send it back
            random_number = random.randint(1, 100)
            response_message = f"{message} {random_number}"
            await websocket.send(response_message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Handle graceful shutdown on exit
def on_exit(signal_received, frame):
    print(f"\nTotal messages received: {message_count}")
    # Log the total message count on shutdown without logging to the file
    sys.exit(0)

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)

if __name__ == "__main__":
    asyncio.run(main())