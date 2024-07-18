import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from pubsub.redisPubSub import RedisPubSub
"""
This module defines a Watcher class that extends the FileSystemEventHandler class from the watchdog library to monitor changes in a directory.
"""

class Watcher(FileSystemEventHandler):
    """
    Watcher monitors changes in a specified directory.

    Attributes:
        path (str): The path to the directory to watch.
        partial_file_identifier (str): Identifier for partial files to be ignored.
    """

    partial_file_identifier = ".part"

    def __init__(self, path: str) -> None:
        """
        Initializes the Watcher with a specified path.

        Parameters:
            path (str): The path to the directory to watch.
        """
        self.path = path
        self.pubsub = RedisPubSub("file modified channel")

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handles the modified event: ignores the event if it's from a file that should be ignored.

        Parameters:
            event (FileSystemEvent): The event to handle.
        """
        if self.ignoreFile(event.src_path):
            return
        

        self.pubsub.publish(f"Modified: {event.src_path}, event_type: {event.event_type}")

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handles the created event: prints the path and event type of the created file.

        Parameters:
            event (FileSystemEvent): The event to handle.
        """
        print(f"Created: {event.src_path}, event_type: {event.event_type}")
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        Handles the deleted event: prints the path and event type of the deleted file.

        Parameters:
            event (FileSystemEvent): The event to handle.
        """
        print(f"Deleted: {event.src_path}, event_type: {event.event_type}")

    def ignoreFile(self, file: str) -> bool:
        """
        Determines if a file should be ignored based on its name or if it's a directory.
        
        Parameters:
            file (str): The file path to check.

        Returns:
            bool: True if the file should be ignored, False otherwise.
        """
        is_partial_file = self.partial_file_identifier in file
        is_directory = os.path.isdir(file)
        return is_partial_file or is_directory
    
    def start(self) -> None:
        """
        Starts the observer to watch the specified directory.
        """
        observer = Observer()
        observer.schedule(self, self.path, recursive=False)
        observer.start()
        try:
            while True:
                print("Watching...")
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
        finally:
            observer.join()