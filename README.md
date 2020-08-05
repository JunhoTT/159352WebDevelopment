# PythonServer
--------------------------------
**Part A**
Implement state using cookies.

When the browser sends a GET request to the /welcome URL (e.g. http://localhost:8080/welcome) the server checks for cookie header. In case when there is no cookie header (e.g. new user with empty browser cache) the server should respond with a simple HTML page (index.html) with a single text input box to read the username and a submit button

![](https://github.com/JunhoTT/159352WebDevelopment/blob/master/Screen%20Shot%202020-08-05%20at%2010.28.40%20PM.png)

When the user clicks the submit button, it should send the form data to /submit URL using GET method. The server should serve a simple welcome message with the user’s name on it, and set a cookie to remember the user.

![](https://github.com/JunhoTT/159352WebDevelopment/blob/master/Screen%20Shot%202020-08-05%20at%2010.28.56%20PM.png)

Subsequent visits by the same user to the /welcome URL should display the welcome message with that user’s name

![](https://github.com/JunhoTT/159352WebDevelopment/blob/master/Screen%20Shot%202020-08-05%20at%2010.29.12%20PM.png)

**Part B**
Implement a password protected website using the basic access authentication scheme.

When the browser sends the initial GET request, the server check for authentication credentials in the headers and respond with a suitable HTTP status code requesting for authentication credentials using the basic access authentication.

When the browser sends the authentication credentials, the server checks the headers and serves the requested content if the authentication credentials match. Set the authentication credentials for your website to be your ID number:

![](https://github.com/JunhoTT/159352WebDevelopment/blob/master/Screen%20Shot%202020-08-05%20at%2010.29.24%20PM.png)
