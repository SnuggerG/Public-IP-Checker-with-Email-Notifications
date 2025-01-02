# Public-IP-Checker-with-Email-Notifications
This Python application checks if your public IP address has changed, and if so, it sends an email notification with the new IP address. Additionally, the program allows you to send a test email and start/stop the IP checking loop.

## Features
- **Send Test Email**: Send a test email with your current public IP.
- **IP Check Loop**: Periodically checks if the public IP has changed (every 10 seconds) and sends an email with the new IP if it changes.
- **IP File**: Stores the current IP address in a file and compares it with the new one on each check.

## Setup Instructions

### Step 1: Create a Mailtrap Account
1. Go to [Mailtrap](https://mailtrap.io/) and sign up for a free account if you don't have one already.
2. Once signed in, create a new **Transactional Stream** to get your SMTP settings.
3. **Important**: Make sure to use the **SMTP Settings** provided in Mailtrap for sending emails.

### Step 2: Configure Mailtrap
1. After logging into Mailtrap, find the **SMTP Settings** in the Mailtrap dashboard.
2. Copy the **SMTP Server** (e.g., `live.smtp.mailtrap.io`) and **Port** (e.g., `587`).
3. Copy your **API Key** from the **Inboxes** tab.

### Step 3: Configure the `.env` File
1. Create a file named `.env` in the same directory as your Python script (`app.py`).
2. Add the following configurations to your `.env` file:

```env
# Email and SMTP Credentials
SENDER_EMAIL=hello@demomailtrap.com
SENDER_PASSWORD=your_mailtrap_api_key_here  # Replace with your Mailtrap API key
RECEIVER_EMAIL=test@gmail.com  # Replace with your email address

# SMTP Server Configuration
SMTP_SERVER=live.smtp.mailtrap.io
SMTP_PORT=587

# Other Configurations (Optional)
IP_CHECK_FILE=current_ip.txt
```

### Step 4: Install Dependencies
Make sure you have the required dependencies installed. You can do this by running the following command:

```bash
pip install requests python-dotenv
```

The program also uses the `smtplib` module, which is built into Python, so no extra installation is required for that.

### Step 5: Run the Program
1. Once the dependencies are installed, you can run the program with:

   ```bash
   python app.py
   ```

2. You'll be presented with a simple menu:
   - **1**: Send a test email with your current public IP.
   - **2**: Start/Stop the IP check loop (checks every 10 seconds).
   - **9**: Exit the program.

### Example of Running the Program:

```bash
Menu:
1 - Send Test Email
2 - Start/Stop IP Check Loop (Every 10 seconds)
9 - Exit
Enter your choice: 1
Email sent successfully to snuggerg@gmail.com.
```

## How It Works
1. **IP Checking**:
   - The program checks the current public IP by calling the IP service (`https://api.ipify.org?format=text`).
   - It compares the current IP with the saved IP in the file (`current_ip.txt`).
   - If the IP has changed, an email is sent with the new IP.
   
2. **Email Notification**:
   - When an IP change is detected, the program sends an email with the new public IP using your Mailtrap SMTP settings.
   - The test email feature sends a simple email with your current public IP address.

3. **File for Storing IP**:
   - The program creates a file called `current_ip.txt` to store the last known public IP.
   - This file is used to cross-reference the IP on each program startup.

## Code Explanation

The core of the script involves:
- **Fetching Public IP**: Using `requests` to fetch the current public IP from `https://api.ipify.org?format=text`.
- **Sending Email**: Using Python's `smtplib` library to send an email with Mailtrap's SMTP server.
- **Checking IP Changes**: Storing the last known IP address in a file (`current_ip.txt`) and checking if the IP has changed on each run.
- **Menu Options**: You can either send a test email, start the IP check loop, or exit the program.

## License

This project is open-source and available under the [MIT License](LICENSE).
