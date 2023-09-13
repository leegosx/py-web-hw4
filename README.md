# Web Application Homework 4

This project demonstrates the creation of a simple web application with routing for two HTML pages (`index.html` and `message.html`), static resource handling, form data processing, and a Socket server for data persistence.

## Features

1. Routing for two HTML pages: `index.html` and `message.html`.
2. Static resource handling for `style.css` and `logo.png`.
3. Form processing from `message.html`.
4. A custom 404 error page (`error.html`) for "Not Found" errors.
5. Web application running on port 3000.
6. A Socket server (UDP protocol) running on port 5000.
7. Data from the form is sent to the Socket server and persisted in a `data.json` file inside a `storage` folder.

## Data Persistence

Form data is saved with a timestamp key in the `data.json` file. The format is:

```json
{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  },
  "2022-10-29 20:21:11.812177": {
    "username": "Krabat",
    "message": "Second message"
  }
}
```
## Usage
  1. Run the application:
      python main.py

  2. Open a web browser and navigate to http://localhost:3000 to access the web application.

  3. Submit data via the form on the message.html page to see it persisted in the data.json file.

## Additional Task (Optional)
  This project also includes a Docker setup:

 1. Build docker image:
    docker build -t webapp-hw4 .
 2. Run the application as a Docker container. Use volumes to persist storage/data.json outside the container:
    docker run -p 3000:3000 -v /path/to/your/storage:/app/storage webapp-hw4

## Contributors
  [Dmytro Klymenko]
