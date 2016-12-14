tests="$@"
if [ -z "$tests" ] ; then
    tests=""
fi

docker-compose exec shell bash -c "py.test $tests"