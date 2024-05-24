import csv
from faker import Faker
from datetime import datetime, timedelta
import random

def generate_log_entry(fake):
    timestamp = fake.date_time_between(start_date="-10d", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
    ip_address = fake.ipv4()
    request_method = random.choice(["GET", "POST"])
    sport = random.choice(["football", "basketball", "swimming", "gymnastics", "archery", "badminton", "boxing", "cycling", "table_tennis", "wrestling", "weightlifting", "tennis", "100m", "200m", "400m", "800m", "high_jump", "long_jump", "pole_vault", "triple_jump" ])  # Add more sports as needed
    endpoint = random.choice([f"/{sport}.html", f"/images/{sport}.jpg", "/index.html", "/searchsports.php"])
    status_code = random.choice([200, 304, 404])
    return (ip_address, timestamp, endpoint, request_method, status_code)

def generate_log_file(num_entries=10000):
    fake = Faker()
    with open("web_server_log.csv", "w", newline="") as csvfile:
        fieldnames = ['IP', 'Time', 'Resource', 'Request Method', 'Status Code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(num_entries):
            log_entry = generate_log_entry(fake)
            writer.writerow({'IP': log_entry[0], 'Time': log_entry[1], 'Resource': log_entry[2], 'Request Method': log_entry[3], 'Status Code': log_entry[4]})

if __name__ == "__main__":
    generate_log_file()
