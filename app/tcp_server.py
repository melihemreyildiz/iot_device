import asyncio
import aio_pika
from config import settings
import json
from celery import Celery
import logging

celery = Celery(__name__, broker=settings.rabbitmq_url)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    logger.info(f"Received {message} from {addr}")

    celery.send_task('app.tasks.process_location', args=[message])

    logger.info(f"Sent {message} to the queue")

    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8888)

    addr = server.sockets[0].getsockname()
    logger.info(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    logger.info("Starting TCP server")
    asyncio.run(main())
