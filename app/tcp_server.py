import asyncio
import aio_pika
from config import settings
import json
from celery import Celery

celery = Celery(__name__, broker=settings.rabbitmq_url)


async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message} from {addr}")

    celery.send_task('app.tasks.process_location', args=[message])

    print(f"Sent {message} to the queue")

    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
