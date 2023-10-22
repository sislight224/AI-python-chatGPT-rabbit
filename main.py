import multiprocessing
from queue import Empty
from TikTokLive import TikTokLiveClient
from script_generator import *
import asyncio

NUM_WORKERS = 5

# Shared queues between TikTokLiveClient and worker tasks
task_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()

def worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def async_worker():
        while True:
            try:
                topic = task_queue.get(timeout=1)  # This is blocking but for 1 second only
                if topic:
                    print(f"Worker found topic: {topic}")
                    output = await get_dialogue(prompt=topic)
                    output_queue.put(output)  # Put the result in the output_queue
            except Empty:  # Using the Empty exception here
                time.sleep(5)
            except Exception as e:
                print(f"Error in worker: {e}")

    loop.run_until_complete(async_worker())

def tt_client_process():
    tt_client = TikTokLiveClient(unique_id="@fashion.lady02")

    @tt_client.on("comment")
    async def on_comment(event):
        if event.comment.startswith("!topic"):
            topic = event.comment[len("!topic"):].strip()
            print(f"Topic found: {topic}")
            task_queue.put(topic)

def main():
    # Start worker processes
    worker_processes = [multiprocessing.Process(target=worker) for _ in range(NUM_WORKERS)]
    for process in worker_processes:
        process.start()

    # Start TikTokLiveClient in a separate process
    client_process = multiprocessing.Process(target=tt_client_process)
    client_process.start()

    # This part is optional. It keeps the main process alive until manually terminated.
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Terminating processes...")
        for process in worker_processes:
            process.terminate()
        client_process.terminate()

if __name__ == "__main__":
    # Run the main function
    main()
