import json
import pika
import time
import asyncio
from PIL import Image
import io
import base64
from config import config

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host))

channel = connection.channel()

channel.queue_declare(queue=config.brain_analysis_queue)

def brain_analysis(image):
    time.sleep(3)
    return 123456

def on_request(ch, method, props, body):
    body = body[2:-1]
    decoded_data = base64.b64decode(body)
    image = Image.open(io.BytesIO(decoded_data))
    response = json.dumps(brain_analysis(image))
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.brain_analysis_queue, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()