# Daily Expenses Sharing Application

This is a backend application for sharing daily expenses among users. It allows users to add expenses and split them based on three different methods: exact amounts, percentages, and equal splits.

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd expense_sharing_app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

The application will start running on `http://127.0.0.1:5000`.

## API Endpoints

### Create User
- **URL:** `/user`
- **Method:** POST
- **Data Params:** 
  ```json
  {
    "email": "user@example.com",
    "name": "User Name",
    "mobile": "1234567890"
  }
  ```
- **Success Response:** Code 201

### Add Expense
- **URL:** `/expense`
- **Method:** POST
- **Data Params:** 
  ```json
  {
    "amount": 100,
    "description": "Dinner",
    "split_method": "equal",
    "user_id": 1,
    "splits": [
      {"user_id": 1, "amount": 50},
      {"user_id": 2, "amount": 50}
    ]
  }
  ```
- **Success Response:** Code 201

### Get Balance Sheet
- **URL:** `/balance_sheet`
- **Method:** GET
- **Success Response:** Code 200 (Returns a CSV file)

### Get User Balance
- **URL:** `/user_balance/<user_id>`
- **Method:** GET
- **Success Response:** Code 200
  ```json
  {
    "user_id": 1,
    "name": "User Name",
    "balance": 50.00
  }
  ```

## Running Tests

To run the tests, use the following command:

```
pytest test_app.py
```

## Future Improvements

- Implement user authentication
- Add more detailed error messages
- Improve test coverage
- Optimize database queries for better performance