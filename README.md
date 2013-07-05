# Sciparse

## Organization
* util: Assorted utility files
* sources: Publisher-specific parsers and validators

## Install
* python setup.py install

## Testing

* Run python -m sciparse.tests.test_parse
* Or run nosetests

## Documentation

* sphinx-apidoc . -o doc -F
* cd doc
* Add the following to conf.py:
    * sys.path.insert(0, os.path.abspath(os.path.pardir))
* make html
