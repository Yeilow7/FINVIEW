### Project Description
## Personal Finances
This is a web application that simulates a simple stock trading platform. Users can register, log in, and manage their virtual portfolios by buying and selling stocks. The application interacts with the Yahoo Finance API to retrieve real-time stock data, allowing users to see current stock prices and track their investments.

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

## Usage

1. **Register:** Create a new account.
2. **Log in:** Use your credentials to log in.
3. **Get a Quote:** Use the "Quote" option to check the price of any stock.
4. **Buy Stock:** Purchase stocks by providing a valid stock symbol and the amount you want to buy.
5. **Sell Stock:** Sell any stock in your portfolio.
6. **View Portfolio:** See a summary of your holdings and their total value.
7. **Transaction History:** View your past transactions and clear them if necessary.
8. **Add/Withdraw Cash:** Manage your account balance by adding or withdrawing cash.

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and use a feature branch. Pull requests are gladly accepted.

1. Fork the project.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.


## Acknowledgments

- [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2021/) - The inspiration for this project.
- [Yahoo Finance API](https://www.yahoofinanceapi.com/) - For providing the stock data.

## How to View the Page

The website is hosted on GitHub Pages and can be visited at the following URL:
https://yeilow7.github.io/FINVIEW/

