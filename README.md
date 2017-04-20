pyns
====

A frontend written in Flask to update `bind` DNS zones via the `nsupdate` tool.

To set up, [generate your zone keys](http://linux.yyz.us/nsupdate/) and then fill out `config.example.py` and save as `config.py`.

Point your favorite web server to serve WSGI/FastCGI requests to `app.wsgi`.

Why?
====

I made this for my [Introduction to Servers workshop](https://serv-wksp.lolhax.io) in Spring 2017 with [Hackers@Berkeley](https://hackersatberkeley.com)..
