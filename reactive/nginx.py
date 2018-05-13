from charms.reactive import (
    set_state,
    when_not,
    when
)
from charms.layer import status

from charms.layer import nginx

from charmhelpers.core import hookenv

config = hookenv.config()

# Handlers --------------------------------------------------------------------
@when('apt.installed.nginx')
@when_not('nginx.available')
def nginx_ready():
    nginx.remove_default_site()
    hookenv.status_set('active', 'NGINX is ready')
    set_state('nginx.started')

# Example website.available reaction ------------------------------------------
"""
This example reaction for an application layer which consumes this nginx layer.
If left here then this reaction may overwrite your top-level reaction depending
on service names, ie., both nginx and ghost have the same reaction method,
however, nginx will execute since it's a higher precedence.

@when('nginx.available', 'website.available')
def configure_website(website):
    website.configure(port=config['port'])

"""
