from telethon import TelegramClient
from typing import List, Dict, Any


class Client:
    def __init__(self, clients_dto: List[Dict[str, Any]]) -> None:
        # Store the client details received as input
        self.clients_dto = clients_dto
        self.telegram_clients = []

    async def initialize_clients(self) -> None:
        # Iterate through each client data and initialize the Telegram client
        for client_data in self.clients_dto:
            client = TelegramClient(
                session=f"Extraction{client_data['session_name']}",
                api_id=client_data['api_id'],
                api_hash=client_data['api_hash'],
            )
            # Connect to Telegram servers
            await client.connect()

            # Check if the user is authorized
            if not await client.is_user_authorized():
                # If the user is not authorized, request the authentication code
                await client.send_code_request(client_data['phone_number'])
                # Sign in the user by providing the authentication code
                await client.sign_in(client_data['phone_number'], input('Enter the code: '))

            # Store the phone number with the client
            client.phone_number = client_data['phone_number']

            # Add the client to the list of Telegram clients
            self.telegram_clients.append(client)

    def get_clients(self) -> List[TelegramClient]:
        # Return the list of initialized Telegram clients
        return self.telegram_clients
