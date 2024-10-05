# FINVIEW - Personal Finances

## Project Description

FINVIEW is a web application that simulates a simple stock trading platform. Users can register, log in, and manage their virtual portfolios by buying and selling stocks. The application interacts with the Yahoo Finance API to retrieve real-time stock data, allowing users to see current stock prices and track their investments.

## Features

- **User Registration and Login:** Users can create an account, log in, and manage their portfolio.
- **Quote:** Users can search for real-time stock prices.
- **Buy Stocks:** Users can buy stocks in fractional amounts and add them to their portfolio.
- **Sell Stocks:** Users can sell the stocks in their portfolio. The interface automatically groups multiple purchases of the same stock.
- **Portfolio Overview:** Users can view their portfolio, including the number of shares they own, the current price, and the total value.
- **Transaction History:** Users can view their past transactions, including a button to clear the history if desired.
- **Add/Withdraw Cash:** Users can add or withdraw cash from their account. Withdrawals are limited to the available balance.
- **Stock Info:** Users can see detailed information about stocks, including the company name, current price, market capitalization, P/E ratio, 52-week high and low, and daily price change.

## Technologies Used

- **Flask:** A lightweight WSGI web application framework.
- **SQLite:** A lightweight database engine.
- **Yahoo Finance API:** Used to retrieve stock prices and related data.
- **Bootstrap:** Frontend framework for building responsive web interfaces.
- **Python:** Main programming language used for the backend logic.
- **Jinja2:** Templating engine used to dynamically generate HTML content.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository** to your local machine:

    ```bash
    git clone https://github.com/yourusername/finview.git
    cd finview
    ```

2. **Create a virtual environment** and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database**:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. **Configure environment variables**:

    Create a `.env` file in the root directory of the project and add the following variables:

    ```plaintext
    FLASK_APP=app
    FLASK_ENV=development
    SECRET_KEY=<your-secret-key>
    ```

    Replace `<your-secret-key>` with a secure key for your Flask application.

6. **Run the application**:

    Start the Flask development server with the following command:

    ```bash
    flask run
    ```

7. **Access the application**:

    Open your web browser and navigate to:

    ```arduino
    http://127.0.0.1:5000
    ```

    Here you can interact with the FINVIEW application and test all its functionalities.

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork the project.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## Acknowledgments

- [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2021/) - The inspiration for this project.
- [Yahoo Finance API](https://www.yahoofinanceapi.com/) - For providing the stock data.

---

© 2024 Juan Luis Ovalle. All rights reserved.
