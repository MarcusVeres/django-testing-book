from fabric.contrib.files import append , exists , sed
from fabric.api import task , env , local , run
import random

# variable setup 
REPO_URL = 'https://github.com/MarcusVeres/django-testing-book.git'
LOCAL_HOST = [ 'localhost' ]
REMOTE_HOST = [ 'do-sandbox-learner' ]
DEFAULT_SITE_NAME = 'mysite'

# environment setup methods 
# run these with : "fab localhost install" or "fab remote install"
@task
def localhost() :
    env.run = local
    env.hosts = LOCAL_HOST

@task
def remote() :
    # allow fabric to use my ssh config file
    env.use_ssh_config = True

    env.run = run
    env.hosts = REMOTE_HOST

@task
def deploy() :
    env.sitename = DEFAULT_SITE_NAME

    # env.user is what you used to log into the server 
    # env.host is provided when you run the fab command from your CLI

    # define vars 
    site_folder = '/home/%s/sites/www/%s' % ( env.user , env.sitename )
    source_folder = site_folder + '/source' 

    # execute deploy functions 
    _describe_self( site_folder ) 
    _get_system_information() 
    _create_directory_structure_if_necessary( site_folder )
    return
    _get_latest_source( source_folder ) 
    _update_settings( source_folder , env.host ) 
    _update_virtualenv( source_folder ) 
    _update_static_files( source_folder ) 
    _update_database( source_folder ) 


def _describe_self( site_folder ) : 
    print "This script will deploy: %s \n hosted on %s \n as %s \n to %s\n" % ( env.sitename , REPO_URL , env.user , site_folder )


def _get_system_information():
    run( "uname -a" )
    run( "whoami" )


def _create_directory_structure_if_necessary( site_folder ) : 
    for subfolder in ( 'database' , 'static' , 'venv' , 'source' ) : 
        run( 'mkdir -p %s/%s' % ( site_folder , subfolder ) ) 


#def _get_latest_source( source_folder ) : 
#
#    # check if the git repo already exists 
#    if exists( site_folder + '/.git' ) : 
#        run( 'cd %s && git fetch' % ( source_folder ) ) 
#
#    else : 
#        run( 'git clone %s %s' % ( REPO_URL , site_folder ) 
#
#    # remember: your shit is a bit different than what he's done
#    # chdir to site_folder 
#    # run git pull into site_folder  
#    # rename superlists folder to "source" 


# syntax : fab function_name:host=hostname.com
# example : fab deploy:host=dummy.com
