import pika
import asyncio
import multiprocessing
from script_generator import *
import threading
import queue  # Import Python's built-in queue
import base64
print("GPT Script Started")
results_queue = queue.Queue()

NUM_WORKERS = 5
connection_parameters = pika.ConnectionParameters(
    host='rabbitmq',
    heartbeat=600  # Set heartbeat to 10 minutes (600 seconds)
)
connection = pika.BlockingConnection(connection_parameters)
ch = connection.channel()
ch.queue_declare(queue='output_queue', durable=True)
ch.confirm_delivery()
async def process_topic_async(topic):
    print(f"Start: {topic}")
    output = await get_dialogue(prompt=topic)
    for i in output:
        try:
            print(f": {i['sound_bytearray'][0]}")
        except Exception as e:
            print(f"Error processing output {e}: .")
    return output

def callback(ch, method, properties, body):
    topic = body.decode()
    print(f"Worker found topic: {topic}")
    threading.Thread(target=run_async_function, args=(process_topic_async, topic)).start()
def convert_to_serializable(obj):
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode('utf-8')  # Convert bytes/bytearray to string
    elif isinstance(obj, dict):
        # Recursively convert values within the dictionary
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        # Recursively convert elements within the list
        return [convert_to_serializable(item) for item in obj]
    elif obj == "":
        return None  # Convert empty string to None
    else:
        return obj  # Return unchanged if it's already serializable
def run_async_function(func, topic):
    global results_queue
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    output = loop.run_until_complete(func(topic))
    for item in output:
        if "sound_bytearray" in item:
            if item["sound_bytearray"] != "":
                if isinstance(item["sound_bytearray"], (bytes, bytearray)):
                    item["sound_bytearray"] = base64.b64encode(item["sound_bytearray"]).decode('utf-8')  # Convert bytes/bytearray to string
    message_body = json.dumps(output)

    try:
        print("Publisher thread started.")  # Confirm the thread is starting

        print(f"Before putting data: Queue size = {results_queue.qsize()}")
        ch.basic_publish(exchange='', routing_key='output_queue', body=message_body)
        print(f"After putting data: Queue size = {results_queue.qsize()}")
    except Exception as e:
        print(f"Queue publishing error: {e}")
    # loop.close()

def publisher_thread():
    global results_queue
    print("Publisher thread started.")  # Confirm the thread is starting
    connection_parameters = pika.ConnectionParameters(
        host='rabbitmq',
        heartbeat=600  # Set heartbeat to 10 minutes (600 seconds)
    )
    connection = pika.BlockingConnection(connection_parameters)
    ch = connection.channel()
    ch.queue_declare(queue='output_queue', durable=True)
    ch.confirm_delivery()

    while True:
        try:

            print(f"Queue size in publisher = {results_queue.qsize()}")
            output = results_queue.get(timeout=10)  # Wait for 10 seconds
            # output = results_queue.get()
            print(f"Output: {output}")
            if output is None:
                print("Terminating publisher thread.")
                connection.close()
                return
            print(f"Attempting to publish: {output}")  # Printing before publishing
            delivery_confirmation, \
                _ = ch.basic_publish(
                exchange='',
                routing_key='output_queue',
                body=str(output),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            if not delivery_confirmation:
                print("Warning: Message was not confirmed by RabbitMQ")
            else:
                print("Message successfully published to RabbitMQ.")
            queue_info = ch.queue_declare(queue='output_queue', passive=True)
            print(f"Current length of output_queue: {queue_info.method.message_count}")
        except queue.Empty:
            print("No data in queue after waiting for 10 seconds.")
        except Exception as e:
            print(f"Error in publisher_thread loop: {e}")

def worker():
    try:
        connection_parameters = pika.ConnectionParameters(
            host='rabbitmq',
            heartbeat=600
        )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        channel.queue_declare(queue='tiktok_queue')
        output_queue_channel = connection.channel()
        output_queue_channel.queue_declare(queue='output_queue', durable=True)
        print(' [*] Worker ready. Waiting for messages.')
        channel.basic_consume(queue='tiktok_queue', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        print(f"Error in worker: {e}")

if __name__ == "__main__":
    print("Starting ChatGPT + Voice script")
    # pub_thread = threading.Thread(target=publisher_thread)
    # pub_thread.start()
    processes = []
    for _ in range(NUM_WORKERS):
        p = multiprocessing.Process(target=worker)
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
