from charms.reactive import (
    set_state,
    when_not,
    when_not_all,
    when_any,
    when
)

from charms.layer import status
from charms.layer import options
from charms.layer.nginx import remove_default_site
from charms import apt

from charmhelpers.core.hookenv import log

# Handlers --------------------------------------------------------------------
@when_not_all('apt.installed.nginx-core', "apt.installed.nginx-full", "apt.installed.nginx-light", "apt.installed.nginx-extras")
@when_not('nginx.available')
def install_nginx():
    nginx_flavor = options.get('nginx', 'nginx_flavor')
    log("Installing {}".format(nginx_flavor))
    apt.queue_install([nginx_flavor])

@when_any('apt.installed.nginx-core', "apt.installed.nginx-full", "apt.installed.nginx-light", "apt.installed.nginx-extras")
@when_not('nginx.available')
def nginx_ready():
    log("Remving the default site")
    remove_default_site()
    status.active('NGINX is ready.');
    set_state('nginx.available')

# Example website.available reaction ------------------------------------------

# This example reaction for an application layer which consumes this nginx layer.
# If left here then this reaction may overwrite your top-level reaction depending
# on service names, ie., both nginx and ghost have the same reaction method,
# however, nginx will execute since it's a higher precedence.
#
# @when('nginx.available', 'website.available')
# def configure_website(website):
#    website.configure(port=config['port'])
