# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # Enable NFS access to the disk
  config.vm.synced_folder "..", "/vagrant", :nfs => true

  # Speed up DNS lookups
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "off"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "off"]
  end

  # NFS requires a host-only network
  # This also allows you to test via other devices (e.g. mobiles) on the same
  # network
  config.vm.network :private_network, ip: "10.11.12.13"

  # Django dev server
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  # For accessing via Varnish
  config.vm.network "forwarded_port", guest: 6081, host: 6081
  # For mailcatcher
  config.vm.network "forwarded_port", guest: 1080, host: 1080

  # Give the VM a bit more power to speed things up
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  # Provision the vagrant box
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update

    cd /vagrant/mapit.mysociety.org

    # Install the packages from conf/packages.ubuntu-trusty
    xargs sudo apt-get install -qq -y < conf/packages.ubuntu-trusty
    # Install some of the other things we need that are just for dev
    # ruby-dev for mailcatcher
    # git for installing mapit from the repo directly
    # everything else for building Varnish modules
    sudo apt-get install -qq -y ruby-dev git autotools-dev make automake libtool pkg-config libvarnishapi1 libvarnishapi-dev libpcre3-dev libreadline-dev python-docutils

    # Create a postgresql user
    sudo -u postgres psql -c "CREATE USER mapit SUPERUSER CREATEDB PASSWORD 'mapit'"
    # Create a database
    sudo -u postgres psql -c "CREATE DATABASE mapit"
    # Install the POSTGIS extensions
    sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" -d mapit

    # Install mailcatcher to make dev email development easier
    sudo gem install --no-rdoc --no-ri mailcatcher

    # Copy the example config file into place to get things going
    cp conf/general.yml-example conf/general.yml

    # Run post-deploy actions script to create a virtualenv, install the
    # python packages we need, migrate the db and generate the sass etc
    conf/post_deploy_actions.bash

    # Checkout the varnish-api-key project
    cd /vagrant
    git clone https://github.com/mysociety/varnish-apikey
    sudo cp /vagrant/varnish-apikey/vcl/varnish-apikey.vcl /etc/varnish

    # Install libvmod redis, we need to get and build the Varnish sources
    # for this.
    cd /vagrant
    sudo apt-get source varnish
    cd varnish-3.0.5
    ./autogen.sh
    ./configure
    make

    git clone https://github.com/carlosabalde/libvmod-redis.git
    cd libvmod-redis
    git checkout tags/3.0-0.2.8
    ./autogen.sh
    ./configure VARNISHSRC=/vagrant/varnish-3.0.5
    make && sudo make install

    # Install our own varnish config file
    sudo cp /vagrant/mapit.mysociety.org/conf/varnish.vcl-example /etc/varnish/default.vcl
    sudo service varnish restart
  SHELL

  # Start mailcatcher every time we start the VM
  config.vm.provision "shell", run: "always" do |s|
    s.inline = <<-SHELL
      mailcatcher --http-ip 0.0.0.0
    SHELL
  end
end