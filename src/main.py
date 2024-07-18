from watcher.fileSystemWatcher import Watcher
from pubsub.redisPubSub import RedisPubSub
import threading

def main():
    """
    The main function of the program.
    """
    watcher = Watcher("/Users/varunkumar/Downloads")
    watcher.start()

if __name__ == "__main__":
    subscriber = RedisPubSub("file modified channel")
    try:
        threading.Thread(target=subscriber.subscribe).start()
        main()
    except KeyboardInterrupt:
        threading.Thread(target=subscriber.subscribe)