# Taxi Order Bot

A Telegram bot for ordering taxis using Telegram Stars for payments. Users can purchase orders, view their profile, and place taxi orders through an interactive interface.

## Features

- **Order Purchases**: Buy taxi orders using Telegram Stars (1, 5, or 10 orders at a time).
- **Profile Management**: View user ID and available orders.
- **Taxi Ordering**: Submit a message link to place a taxi order (requires available orders).
- **Clean Interface**: Minimalist design with MarkdownV2 formatting and emoji-based navigation.
- **Payment Handling**: Secure Telegram Stars payment processing with invoice deletion on success or cancellation.
- **Channel Integration**: Posts the main menu to a specified Telegram channel on startup.

## Prerequisites

- Python 3.10+
- A Telegram bot token (obtained from [@BotFather](https://t.me/BotFather))
- A Telegram channel ID (e.g., `@YourChannel` or numeric ID)
- Telegram bot added as an admin in the channel with "Post Messages" and "Delete Messages" permissions

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/taxi-order-bot.git
   cd taxi-order-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Required packages:
   - `aiogram`
   - `aiosqlite`
   - `python-dotenv`

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   BOT_TOKEN=your_bot_token_here
   CHANNEL_ID=@YourChannel
   ```

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py`: Core bot logic, including menu handling, payment processing, and startup.
- `settings/`
  - `config.py`: Configuration for bot token, channel ID, and menu text.
  - `database.py`: SQLite database management for user and order data.
  - `keyboard.py`: Inline keyboard definitions for navigation and payments.

## Usage

1. **Start the Bot**:
   - Use the `/start` command in a private chat to access the main menu.
   - The bot posts the main menu to the configured channel on startup.

2. **Main Menu**:
   - 🛒 **Buy Orders**: Purchase 1, 5, or 10 orders using Telegram Stars.
   - 📦 **Order Taxi**: Submit a message link to place a taxi order (requires available orders).
   - 👤 **Profile**: View your user ID and available orders.

3. **Payment Flow**:
   - Select an order package (1, 5, or 10 orders).
   - Pay using Telegram Stars.
   - On successful payment, the invoice message is deleted, and a confirmation is sent with the main menu.
   - Cancel payments to delete the invoice and return to the main menu.

## Database Schema

The bot uses an SQLite database (`orders.db`) with the following schema:

- **users** table:
  - `user_id` (INTEGER, PRIMARY KEY): Telegram user ID.
  - `num_order` (INTEGER, DEFAULT 0): Number of available orders.

## Notes

- Ensure the bot has appropriate permissions in the Telegram channel for posting and deleting messages.
- Test payments in a private chat, as Telegram Stars payments are processed in private chats.
- MarkdownV2 formatting is used for messages; ensure special characters are escaped correctly to avoid parsing errors.
- Errors (e.g., failed message deletions) are logged to the console for debugging.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.