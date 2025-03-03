# Bitcoin Wallet Tracker

This app allows you to manage Bitcoin addresses, sync wallet transactions, and view balances and transaction history.

## Features

- **Add/Remove Bitcoin Addresses**: Manage Bitcoin addresses with optional labels.
- **Synchronize Transactions**: Fetch the latest transactions for Bitcoin addresses using the Blockchair API.
- **View Balances and History**: See current balances and detailed transaction history.
- **Asynchronous Processing**: Background processing of Bitcoin address synchronization using Celery and Redis.

## Getting Started (macOS)

### Setting Up Your Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/bitcoin_wallet_tracker.git
   cd bitcoin_wallet_tracker
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

### Starting the Server

1. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
   The application will be available at http://127.0.0.1:8000/

2. **Start the Celery worker** (in a separate terminal):
   ```bash
   # Make sure to activate the virtual environment first
   source .venv/bin/activate
   
   # Then start the Celery worker
   celery -A config.celery_app worker -l info
   ```

### API Usage

The application uses the Blockchain.com API as the data source for Bitcoin address information and transactions.

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Redis Setup

This application uses Redis as a message broker for Celery tasks. You need to install and run Redis before starting the Celery worker.

#### Installing Redis on macOS

```bash
# Install Redis using Homebrew
brew install redis

# Start Redis as a background service
brew services start redis

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

### Celery

This app comes with Celery for asynchronous task processing, such as Bitcoin address synchronization.

**Important**: Make sure Redis is installed and running before starting Celery (see [Redis Setup](#redis-setup) section).

To run a celery worker:

```bash
cd bitcoin_wallet_tracker
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd bitcoin_wallet_tracker
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd bitcoin_wallet_tracker
celery -A config.celery_app worker -B -l info
```

