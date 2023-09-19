# Link Shortener Service

This service uses a Flask backend, a React web client, and a Postgres database. I could have simplified the setup a bit by using a simple HTML page, and perhaps a SQLite database, but decided to use a more complex setup for demonstrative purposes.

Developing a link-shortening service is pretty straightforward conceptually. The idea is to take the original link, generate a shorter link from it using the domain of the service, save it in the database, and when a request is made to the shorter link, fetch it from the database and redirect the user to the original link. To make the link as short as possible, it's ideal to have a short domain, e.g. "bit.ly". For the purposes of this challenge, the localhost domain sufficed.

I took a number of shortcuts for the sake of time:

- In a production application, you would inject secrets rather than hardcoding them in the docker-compose file
- In a production environment, the React client would typically be hosted on a CDN rather than served from a development node server. If SSR was needed, the client may be served from a node server, but would use something like Express/Next.js instead of the CRA dev server.
- The Flask service is also being run with a development server. Typically you'd use a WSGI server in front of Flask, e.g. Gunicorn.
- In a production environment, a Postgres database typically wouldn't be containerized.

There is certainly more I could mention, but these are some of the main things.

Some assumptions I made included:

- I assumed this service can be hosted for less than $10k/month. This would depend largely on the expected load on the service, which would dictate the amount of infrastructure needed to run it. I assumed that a single Flask server could handle all of the traffic, however if this wasn't the case, I'd want to consider using something like Kubernetes to auto-scale the Flask services and load balance between them.
- I assumed a short code of 6 characters was sufficient. Depending on the expected load, this may not be enough. The more shortened links generated, the higher probability of a collision (i.e. the same shortened link pointing to two different original links). However, practically speaking there are ways to keep a short code while sufficiently addressing/avoiding collisions. For example, we can check the database for a collision before saving the short URL. If there is a collision, we can attempt to generate another short URL ad infinitum until there is no collision. We can also define a duration that we agree to store the link, and recycle links when they expire.

---

To run the service, you can run `docker-compose up --build`. Once running, you can go to `localhost:3000`, and enter a URL, and then click the generated link and you should be redirected to the original URL entered.
