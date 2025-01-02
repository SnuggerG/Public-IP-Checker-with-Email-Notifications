import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import time
import threading

# Load environment variables from .env file
load_dotenv()

# Fetch public IP
def get_public_ip():
    """Fetch the current public IP address."""
    response = requests.get('https://api.ipify.org?format=text')
    return response.text.strip()

# Send the email using Mailtrap
def send_email(new_ip=None):
    """Send an email with the updated IP address (or test email)."""
    sender_email = os.getenv('SENDER_EMAIL')  # Your Mailtrap email
    sender_password = os.getenv('SENDER_PASSWORD')  # Your Mailtrap API Key (used as password)
    receiver_email = os.getenv('RECEIVER_EMAIL')  # The recipient's email address
    smtp_server = os.getenv('SMTP_SERVER')  # Mailtrap SMTP server
    smtp_port = os.getenv('SMTP_PORT')  # SMTP port for Mailtrap

    # Determine subject and body based on IP change or test
    if new_ip:
        subject = "Public IP Address Changed"
        body = f"The server's public IP has changed to: {new_ip}"
    else:
        subject = "Test Email"
        body = f"Hey yes mail, and this is your current IP: {get_public_ip()}"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send the email using Mailtrap's SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Encrypt the connection
            server.login("api", sender_password)  # Login with 'api' as the username and your API key as the password
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
            print(f"Email sent successfully to {receiver_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Check if public IP has changed and send an email if it has
def check_ip_change(ip_file=os.getenv('IP_CHECK_FILE', 'current_ip.txt')):
    """Check if the public IP has changed."""
    current_ip = get_public_ip()
    print(f"Current Public IP: {current_ip}")

    # Ensure the file exists
    if not os.path.exists(ip_file):
        print(f"File '{ip_file}' not found. Creating it...")
        with open(ip_file, 'w') as file:
            file.write("")  # Create an empty file

    # Read the previous IP if available
    with open(ip_file, 'r') as file:
        previous_ip = file.read().strip()

    # Compare and update the file if the IP has changed
    if current_ip != previous_ip:
        with open(ip_file, 'w') as file:
            file.write(current_ip)
        print("Public IP has changed.")
        send_email(current_ip)  # Send email with new IP
    else:
        print("Public IP has not changed.")

# This function will run the IP check loop
def ip_check_loop():
    """Run the IP check loop every 10 seconds."""
    while ip_check_active:
        check_ip_change()  # Check IP and send email if it has changed
        time.sleep(10)  # Wait for 10 seconds before checking again

# Flag to control the loop
ip_check_active = False
ip_check_thread = None

# Main loop to interact with user
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1 - Send Test Email")
        print("2 - Start/Stop IP Check Loop (Every 10 seconds)")
        print("9 - Exit")

        # User input
        choice = input("Enter your choice: ")

        if choice == '1':
            # Send test email
            send_email()
        elif choice == '2':
            # Toggle the IP check loop
            if ip_check_active:
                # Stop the IP check loop
                ip_check_active = False
                if ip_check_thread is not None:
                    ip_check_thread.join()  # Ensure the thread stops
                print("IP check loop stopped. Returning to menu.")
            else:
                # Start the IP check loop
                ip_check_active = True
                ip_check_thread = threading.Thread(target=ip_check_loop)
                ip_check_thread.start()
                print("Starting IP check loop every 10 seconds...")
        elif choice == '9':
            # Exit the program
            print("Exiting program...")
            if ip_check_active:
                ip_check_active = False
                ip_check_thread.join()  # Ensure the thread stops before exiting
            break
        else:
            print("Invalid choice, please enter 1, 2, or 9.")
