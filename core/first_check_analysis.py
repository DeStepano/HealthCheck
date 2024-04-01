import json
import pika
import time
import asyncio

from config import config

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host))

channel = connection.channel()

channel.queue_declare(queue=config.first_check_queue)

def first_check_analysis(data):
    time.sleep(2)
    return 12345

def on_request(ch, method, props, body):
    body = json.loads(body)
    response = json.dumps(first_check_analysis(body))
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.first_check_queue, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()