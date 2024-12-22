import threading
from django.apps import AppConfig
from .consumer.rabbitmq_consumer import start_consumer

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        print("Starting RabbitMQ consumer...")
        """
        Starts the RabbitMQ consumer when the app is ready.
        """
        # Start the consumer in a separate thread to avoid blocking the app
        threading.Thread(target=start_consumer, daemon=True).start()
