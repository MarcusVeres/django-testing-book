
### Testing 

Run all tests
    cd superlists && python manage.py test

Run unit tests
    cd superlists && python manage.py test lists

Run functional tests    
    cd superlists && python manage.py test functional_tests/

-----

### Live Testing 

Run functional tests 
    python manage.py test functional_tests/ --liveserver=pybook-staging.lazerstorm.com

