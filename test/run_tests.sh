#! /bin/sh

if [[ "${TRAVIS_PYTHON_VERSION}" == "pypy" ]]; then
    PYENV_ROOT="${HOME}/.pyenv"
    PATH="${PYENV_ROOT}/bin:${PATH}"
    eval "$(pyenv init -)"
    pyenv global pypy-2.6.0
fi

python -V

cd test
pip freeze  # so to help eventual debug: know what exact versions are in use can be rather useful.

nosetests -xv --process-restartworker --processes=1 --process-timeout=300  --with-coverage --cover-package=alignak

coverage combine

cd .. && pep8 --max-line-length=100 --exclude='*.pyc' alignak/*

pylint --rcfile=.pylintrc --disable=all --enable=C0111 --enable=W0403 --enable=W0106 --enable=W1401 --enable=W0614 --enable=W0107 --enable=C0204 --enable=W0109  --enable=W0223  --enable=W0311  --enable=W0404  --enable=W0623  --enable=W0633 --enable=W0640  --enable=W0105 --enable=W0141 --enable=C0325 --enable=W1201 --enable=W0231 --enable=W0611 --enable=C0326 --enable=W0122 --enable=E0102 --enable=W0401 --enable=W0622 -r no alignak/*

pep257 --select=D300 alignak

cd test && (pkill -6 -f "alignak_-" || :) && python full_tst.py && cd ..

if [[ $TRAVIS_PYTHON_VERSION == '2.7' ]]
then
    ./test/test_all_setup.sh
fi
