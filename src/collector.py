#!/usr/bin/env python3
import requests
import pika
import json
import os
import time
from datetime import datetime

def fetch_market_data():
    url = "https://dummyjson.com/products/category/smartphones"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("products", [])
    else:
        print("Failed to fetch data from API.")
        return []

if __name__ == "__main__":
    while True:
        print("Fetching market data...")
        devices = fetch_market_data()

        if devices:
            print(f"Found {len(devices)} devices. Publishing to RabbitMQ...")
            rabbitmq_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            channel = connection.channel()
            channel.queue_declare(queue='raw_device_data')

            for item in devices:
                payload = {
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "timestamp": datetime.utcnow().isoformat()
                }
                channel.basic_publish(exchange='',
                                      routing_key='raw_device_data',
                                      body=json.dumps(payload))
                print(f"Published: {payload['title']}")
            
            connection.close()
            print("Success! Data has been published!")
        else:
            print("No data to store.")
        
        # Sleep for 5 minutes before next run
        time.sleep(300)