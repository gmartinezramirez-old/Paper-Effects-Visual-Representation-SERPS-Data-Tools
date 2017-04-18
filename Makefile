clean-pyc:
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +
    find . -name '*~' -exec rm --force  {} +

clean-build:
    rm --force --recursive build/
    rm --force --recursive dist/
    rm --force --recursive *.egg-info

help:
    @echo "    clean-pyc"
    @echo "        Remove python artifacts."
    @echo "    clean-build"
    @echo "        Remove build artifacts."
    @echo "    isort"
    @echo "        Sort import statements."
    @echo "    lint"
    @echo "        Check style with flake8."
    @echo "    test"
    @echo "        Run py.test"
    @echo '    run'
    @echo '        Run the `my_project` service on your local machine.'
    @echo '    docker-run'
    @echo '        Build and run the `my_project` service in a Docker container.'