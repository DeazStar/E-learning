import pika
import json
from ..utils import send_password_reset_email, send_prompotional_mail

def process_message(ch, method, properties, body):
    """
    Processes incoming RabbitMQ messages and sends a password reset email.
    """
    try:
        data = json.loads(body)
        email = data.get('email')
        otp = data.get('otp')
        if email and otp:
            send_password_reset_email(email, otp)
            print(f"Password reset email sent to {email}")
        else:
            print("Invalid data: Missing email or reset link")
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")

def send(ch, method, properties, body):
    try:
        data = json.loads(body)
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        send_prompotional_mail(email, subject, message)
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")

def start_consumer():
    """
    Starts the RabbitMQ consumer to listen for messages.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Ensure the queue exists
    channel.queue_declare(queue='password_reset')
    channel.queue_declare(queue='email')

    # Set up the consumer
    channel.basic_consume(queue='password_reset', on_message_callback=process_message, auto_ack=True)
    channel.basic_consume(queue='email', on_message_callback=send, auto_ack=True)
    print("RabbitMQ Consumer is running. Press CTRL+C to exit.")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
