# exit when any command fails
set -e
echo wallgen --help
wallgen --help || exit
echo wallgen poly --help
wallgen poly --help || exit
echo wallgen shape --help
wallgen shape --help || exit
echo wallgen slants --help
wallgen slants --help || exit
echo wallgen pic --help
wallgen pic --help || exi