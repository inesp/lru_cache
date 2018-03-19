# lru_cache
Very simple LRU cache with the added benefit of a timeout setting


## Set up



## Thought process

### How to install Pylint

Run:
```bash
pip install pylint
```

Pylint has a few depencencies, which will all install with it.

After the installation you need to create a .pylintrc file, which holds
the cpylint configuration. It appears that a default .pylintrc can be created
by running
```bash
pylint --generate-rcfile > .pylintrc
```

Now check the configuration by running pylint on a .py file
```bash
pylint file_dir/file_name.py
```

You'll get way too many errors, thus it is time to change a few settings in 
the configuration.
