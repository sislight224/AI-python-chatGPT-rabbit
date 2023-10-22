import pika
from TikTokLive import TikTokLiveClient
import os
print("TikTok Script Started")
# RabbitMQ setup
connection_parameters = pika.ConnectionParameters(
    host='rabbitmq',
    heartbeat=600  # Set heartbeat to 10 minutes (600 seconds)
)
connection = pika.BlockingConnection(connection_parameters)  # use the service name you gave to RabbitMQ in docker-compose.yml
channel = connection.channel()
channel.queue_declare(queue='tiktok_queue')


tt_client = TikTokLiveClient(unique_id=os.environ.get('TIK_TOK_ID'))

@tt_client.on("comment")
async def on_comment(event):
    # print(event.comment)
    if event.comment.startswith("!topic"):
        topic = event.comment[len("!topic"):].strip()
        print(f"Topic found: {topic}")

        # Send the topic to the RabbitMQ queue
        channel.basic_publish(exchange='', routing_key='tiktok_queue', body=topic)


if __name__ == "__main__":
    print("Starting TikTok")
    tt_client.run()
