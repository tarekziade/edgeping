edgeping
========

Implementation of https://docs.telemetry.mozilla.org/concepts/pipeline/http_edge_spec.html
for testing purpose.

The server will collect pings in memory, and you can call:

- **GET /pings** to get all the collected pings in a JSON payload
- **DELETE /pings** to delete the collected pings

Step-by-step
============

1. Run the service::

    % python3  -m venv  .
    % bin/pip install edgeping
    % bin/edgeping
    Running. Set 'toolkit.telemetry.server' value to http://localhost:7777

2. Run firefox with the right config

3. Grab the pings  with a  GET  /pings call::

    % curl http://localhost:7777/pings

