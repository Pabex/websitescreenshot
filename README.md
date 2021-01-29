# Simple Website Screenshot

It's a simple server that expose an endpoint for download a preview image of any website.
Uses selenium with chrome driver for capture the screenshot.

## Use
In the root of the project execute `docker-compose up`, then with the browser, curl or whatever you want,
make a GET request to `http://localhost:5010/?url=https://pabex.com.ar`.
Change the query param **url** for you needs.

![Website Screenshot Gif](./ws.gif?raw=true "Website Screenshot")
