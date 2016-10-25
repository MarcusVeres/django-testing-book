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
    env.site_name = DEFAULT_SITE_NAME

    # env.user is what you used to log into the server 
    # env.host is provided when you run the fab command from your CLI

    # define vars 
    site_folder = '/home/%s/sites/www/%s' % ( env.user , env.site_name )
    source_folder = site_folder + '/source' 

    # execute deploy functions 
    _describe_self( site_folder ) 
    _get_system_information() 
    _create_main_folder_if_necessary( site_folder )
    _get_latest_source( site_folder , source_folder ) 
    _create_directory_structure_if_necessary( site_folder )
    _update_settings( source_folder , env.site_name )
    return
    _update_virtualenv( source_folder ) 
    _update_static_files( source_folder ) 
    _update_database( source_folder ) 


def _describe_self( site_folder ) : 
    print "This script will deploy: %s \n hosted on %s \n as %s \n to %s\n" % ( env.site_name , REPO_URL , env.user , site_folder )


def _get_system_information():
    run( "uname -a" )
    run( "whoami" )


def _create_main_folder_if_necessary( site_folder ) : 
    run ( 'mkdir -p %s' % ( site_folder ) )


def _get_latest_source( site_folder , source_folder ) : 

    # check if the git repo already exists 
    if exists( site_folder + '/.git' ) : 
        print "A Git repo for this project already exists. Fetching..." 
        run( 'cd %s && git fetch' % ( source_folder ) ) 

    else : 
        print "Did not find a Git repo at this location. Cloning..."
        run( 'git clone %s %s' % ( REPO_URL , site_folder ) )
        #run( 'mv %s/superlists %s/source' % ( site_folder , site_folder ) ) << not necessary because it was renamed in the repo

    # grab the git log hash from the LOCAL (dev) machine 
    current_commit = local( "git log -n 1 --format=%H" , capture = True )

    # hard reset to the current_commit, which will wipe away any current changes to the server's code
    run( 'cd %s && git reset --hard %s' % ( source_folder , current_commit ) )


def _create_directory_structure_if_necessary( site_folder ) : 
    for subfolder in ( 'database' , 'static' , 'venv' ) : 
        run( 'mkdir -p %s/%s' % ( site_folder , subfolder ) ) 


def _update_settings( source_folder , site_name ) :
    # set the ALLOWED_HOSTS and DEBUG, and create a new secret key

    settings_file = source_folder + '/superlists/settings.py'

    # find and replace the line with the DEBUG setting 
    print "\nDisabling DEBUG mode..."
    sed( settings_file , 'DEBUG = True' , 'DEBUG = False' )

    # find the ALLOWED_HOSTS line, and add our site name to the list of allowed hosts
    print "\nAdding %s to ALLOWED_HOSTS..." % ( site_name )
    sed( settings_file , 
        'ALLOWED_HOSTS = .+$' , 
        'ALLOWED_HOSTS = ["%s"]' % ( site_name )
        )

    # generate a secret key
    character_pool = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    new_key = '' . join( random.SystemRandom().choice( character_pool ) for _ in range( 50 ) ) 

    # find and replace the secret key line
    print "\nUpdating secret key..."
    sed( settings_file , 'SECRET_KEY = .+$' , 'SECRET_KEY = "%s"' % ( new_key ) )


# syntax : fab function_name:host=hostname.com
# example : fab deploy:host=dummy.com

