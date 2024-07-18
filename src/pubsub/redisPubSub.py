import redis
"""
The above code snippet is a simple example of how to use Redis Pub/Sub in Python.
"""
class RedisPubSub:
  def __init__(self, channel) -> None:
    """
    Initializes the RedisPubSub class.
    """
    self.channel = channel
  def publish(self, message: str) -> None:
    """
    Publishes a message to a specified channel.

    Parameters:
        channel (str): The channel to publish the message to.
        message (str): The message to publish.
    """
    r = redis.Redis()
    r.publish(self.channel, message)

  def subscribe(self) -> None:
    """
    Subscribes to a specified channel and prints received messages.

    Parameters:
        channel (str): The channel to subscribe to.
    """
    print(f"Subscribed to channel: {self.channel}")
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe(self.channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received: {message['data']}")