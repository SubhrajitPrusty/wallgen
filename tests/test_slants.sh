# exit when any command fails
set -e

echo wallgen slants 1000
wallgen slants 1000
echo wallgen slants 1000 -n test
wallgen slants 1000 -n test
echo wallgen slants 1000 -sw 5
wallgen slants 1000 -sw 5
echo wallgen slants 1000 -g
wallgen slants 1000 -g
echo wallgen slants 1000 -i
wallgen slants 1000 -i
echo wallgen slants 1000 -g -sw 5
wallgen slants 1000 -g -sw 5
echo wallgen slants 1000 -g -i
wallgen slants 1000 -g -i
echo wallgen slants 1000 -i -sw 5
wallgen slants 1000 -i -sw 5
echo wallgen slants 1000 -g -i -sw 5
wallgen slants 1000 -g -i -sw 5