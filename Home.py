from imaplib import IMAP4_SSL
from telethon import TelegramClient, events

# Replace the values below with your own API ID, API Hash and session file name
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
session_name = 'my_session'

# Replace the values below with your email account credentials and IMAP server details
email_address = 'youremail@example.com'
password = 'yourpassword'
imap_server = 'imap.example.com'

# Create a new Telegram client
client = TelegramClient(session_name, api_id, api_hash)

# Define the event handler for incoming messages
@client.on(events.NewMessage)
async def handle_incoming_message(event):
    if not await client.is_user_authorized() or event.out:
        # User is not currently authorized or message is outgoing, ignore
        return
    
    # Check if the incoming message is a request for new email notifications
    if event.raw_text == '/check_email':
        # Connect to the IMAP server and check for new email messages
        imap_client = IMAP4_SSL(imap_server)
        imap_client.login(email_address, password)
        imap_client.select('INBOX')
        status, messages = imap_client.search(None, 'UNSEEN')
        
        # Send a message to the Telegram bot with details about each new email
        for message_id in messages[0].split():
            _, message_data = imap_client.fetch(message_id, '(RFC822)')
            message_text = message_data[0][1].decode('utf-8')
            await client.send_message(event.chat_id, message_text)
        
        # Close the IMAP client connection
        imap_client.close()
        imap_client.logout()

# Start the client
client.start()

# Run the client until it is disconnected
client.run_until_disconnected()
