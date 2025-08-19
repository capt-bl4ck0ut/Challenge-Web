# Chat Application

This is a simple chat application built using Flask. The application allows users to send messages, and if a message contains a URL to an image, it will display the embedded image in the chat interface.

## Project Structure

```
chat-app
├── app.py               # Main application file
├── static
│   └── style.css        # CSS styles for the chat application
├── templates
│   └── index.html       # HTML template for the chat interface
├── requirements.txt      # List of dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chat-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000` to access the chat application.

## Usage Guidelines

- Enter your message in the input field and press "Send".
- If your message contains a URL to an image, it will be displayed as an embedded image in the chat.
- Enjoy chatting!