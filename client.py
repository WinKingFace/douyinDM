import asyncio
import websockets


async def receive_messages():
    async with websockets.connect('ws://localhost:2333/room_id=2222') as websocket:
        async for message in websocket:
            # 处理服务端发来的消息
            print(f'Received message: {message}')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(receive_messages())
