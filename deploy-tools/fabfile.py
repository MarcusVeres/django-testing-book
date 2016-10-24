from fabric.contrib.files import append , exists , sed
from fabric.api import env , local , run
import random

REPO_URL = 'https://github.com/MarcusVeres/django-testing-book.git'

def deploy() : 

    # env.user is what you used to log into the server 
    # env.host is provided when you run the fab command from your CLI

    # define vars 
    site_folder = '/home/%s/sites/%s' % ( env.user , env.host )
    source_folder = site_folder + '/source' 

    # execute deploy functions 
    _describe_self( site_folder ) 

    return
    _create_directory_structure_if_necessary( site_folder )
    _get_latest_source( source_folder ) 
    _update_settings( source_folder , env.host ) 
    _update_virtualenv( source_folder ) 
    _update_static_files( source_folder ) 
    _update_database( source_folder ) 


def _describe_self( site_folder ) : 
    print "This script will deploy: %s \n hosted on %s \n as %s \n to %s" % ( env.host , REPO_URL , env.user , site_folder )


#def _create_directory_structure_if_necessary( site_folder ) : 
#
#    for subfolder in ( 'database' , 'static' , 'venv' , 'source' ) : 
#        run( 'mkdir -p %s/%s' % ( site_folder , subfolder ) 
#
#
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

    
