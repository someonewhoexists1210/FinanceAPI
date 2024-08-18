# Finance Manager Website

## Overview

The Finance Manager Website is a Django-based application that provides easy managing for your finance

## Features

- **Budgeting**: Implement budgets for specific categories
- **Transaction**: Record transactions.
- **Financial Goals**: Allocate money towards specific goals with due dates
- **Recurring Transactions**: Automatically add recurring transactions(Work in progress)
- **User Accounts**: Secure login and account management.

## Technologies

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite

## Usage

1. **Recording Transactions**
   - Visit the transaction page to see transaction history.
   - You can also make a transaction yourself
  
2. **Managing Budgets**
   - Visit budget page to enter limits for spending
   - On the transaction page, you can bind each transaction to a specific budget
  
3. **Goals**
   - Visit the Finance page to make different finance goals
   - You can visit the save page to contribute to those goals

## Deployment

The project is deployed at tbd.com

## Contributing
Contributions are welcome! If you'd like to set up the project locally, follow these steps:

1. Clone the Repository
```bash
  git clone https://github.com/someonewhoexists1210/FinanceAPI.git
  cd WeatherAPI
```
2. Create a Virtual Environment

```bash

  python -m venv venv
  Activate the Virtual Environment
```

### On Windows
```bash
venv\Scripts\activate
```

### On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run Migrations

```bash
python manage.py migrate
```


5. Run the Development Server
```bash   
python manage.py runserver
```

Access the website at http://127.0.0.1:8000/.
Please ensure that your code adheres to the project's coding standards and includes appropriate tests before submitting a pull request.

## Contact
For any questions or issues, please contact [darshdiv20@gmail.com] (mailto:darshdiv20@gmail.com)
