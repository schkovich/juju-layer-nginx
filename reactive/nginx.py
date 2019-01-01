from charms.reactive import (
    set_state,
    when_not,
    when
)

from charms.layer import status

from charms.layer.nginx import remove_default_site

# Handlers --------------------------------------------------------------------
@when_not('apt.installed.nginx-common')
def install_nginx():
    nginx_flavor = layer.options.get('nginx', 'nginx_flavor'):
    charms.apt.queue_install([nginx_flavor])

@when('apt.installed.nginx-common')
@when_not('nginx.available')
def nginx_ready():
    remove_default_site()
    status.active('NGINX is ready.');
    set_state('nginx.available')

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
