# WallGen
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)  
[![](https://img.shields.io/badge/Demo-yellow.svg?style=for-the-badge)](http://wallgen.subhrajitpy.me/)


Generates HQ poly wallpapers

## Installation

`pip install --editable .`

## Usage Docker

Inside the folder

`docker build -t wallgen-doc:latest .`

`docker run -d -p 5000:5000 wallgen-doc`

Run `docker ps` to check if container is running.

Goto [localhost:5000](http://localhost:5000) to check out the website.


## Usage

### `wallgen`

```
Usage: wallgen [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  poly    Generates a HQ low poly image
  shape   Generate a HQ image of a beautiful shapes
  slants  Generates slanting lines of various colors

```

### `wallgen poly --help`

```
Usage: wallgen poly [OPTIONS] SIDE

  Generates a HQ low poly image

Options:
  -c, --colors TEXT     use many colors custom gradient, e.g -c #ff0000 -c
                        #000000 -c #0000ff
  -p, --points INTEGER  number of points to use, default = 100
  -s, --show            open the image
  -o, --outline         outline the triangles
  --help                Show this message and exit.

```

### `wallgen shape --help`


```
Usage: wallgen shape [OPTIONS] SIDE

  Generate a HQ image of a beautiful shapes

Options:
  -t, --type [square|hex|diamond] choose which shape to use
                                  
  -c, --colors TEXT               use many colors custom gradient, e.g -c
                                  #ff0000 -c #000000 -c #0000ff
  -s, --show                      open the image
  -o, --outline                   outline the shapes
  --help                          Show this message and exit.

```

### `wallgen slants --help`

```
Usage: wallgen slants [OPTIONS] SIDE

  Generates slanting lines of various colors

Options:
  -s, --show  open the image
  --help      Show this message and exit.

```

## Examples


### `wallgen poly 2000`

Random Gradient

<img src="./images/demo1.png" width="50%">

### `wallgen poly 1000 --colors "#ff0000" --colors "#00ddff"`

Fixed color/gradient

<img src="./images/poly.png" width="50%">

### `wallgen poly 2000 -c "#dd0000" -c "#4455ff" --points 50`

Fixed no. of points

<img src="./images/demo9.png" width="50%">

### `wallgen poly 2000 -c "#dd0000" -c "#4455ff" -p 500`

Fixed no. of points

<img src="./images/demo8.png" width="50%">

### `wallgen poly 2000 -c "#ff0000" -c "#000000" -c "#0000ff"`

More than 2 colours

<img src="./images/demo3.png" width="50%">

### `wallgen poly 1000 -c "#ff0000" -c "#00ddff" -o`

With outline

<img src="./images/poly-outline.png" width="50%">

### `wallgen shape -t square -c "#ff0099" -c "#00ddff"`

Square pattern

<img src="./images/square.png" width="50%">

### `wallgen shape -t square -c "#ff0099" -c "#00ddff" -o`

Square pattern with Outline

<img src="./images/square-outline.png" width="50%">

### `wallgen shape -t hex -c "#ff0099" -c "#00ddff"`

Hexagon pattern

<img src="./images/hex.png" width="50%">

### `wallgen shape -t hexagon -c "#ff0099" -c "#00ddff" -o`

Hexagon pattern with Outline

<img src="./images/hex-outline.png" width="50%">

### `wallgen shape -t diamond -c "#ff0099" -c "#00ddff"`

Diamond pattern

<img src="./images/diamond.png" width="50%">

### `wallgen shape -t square -c "#ff0099" -c "#00ddff" -o`

Diamond pattern with Outline

<img src="./images/diamond-outline.png" width="50%">

### `wallgen slants 2000`

Slants pattern

<img src="./images/demo6.png" width="50%">


## Screenshots

### Homepage

![homepage](./images/web-home.png)

### Poly Page

![Polygon](./images/web-poly.png)

### Shapes Page

![Polygon](./images/web-shape.png)