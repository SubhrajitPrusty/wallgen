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
  pattern  Generate a HQ image of a beautiful pattern
  poly     Generates a HQ low poly image
  slants   Generates slanting lines of various colors
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
  --help                Show this message and exit.
```

### `wallgen pattern --help`


```
Usage: wallgen pattern [OPTIONS] SIDE

  Generate a HQ image of a beautiful pattern

Options:
  -sq, --squares     use squares instead of rhombus
  -hx, --hexagons    use Hexagons instead of rhombus (Experimental)
  -c, --colors TEXT  use many colors custom gradient, e.g -c #ff0000 -c
                     #000000 -c #0000ff
  -s, --show         open the image
  --help             Show this message and exit.
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

### `wallgen poly 2000 --colors "#dc2221" --colors "#35d7d6"`

Fixed color/gradient

<img src="./images/demo2.png" width="50%">

### `wallgen poly 2000 -c "#dd0000" -c "#4455ff" --points 50`

Fixed no. of points

<img src="./images/demo9.png" width="50%">

### `wallgen poly 2000 -c "#dd0000" -c "#4455ff" -p 500`

Fixed no. of points

<img src="./images/demo8.png" width="50%">

### `wallgen poly 2000 -c "#ff0000" -c "#000000" -c "#0000ff"`

More than 2 colours

<img src="./images/demo3.png" width="50%">

### `wallgen pattern 2000 --squares -c "#dd0000" -c "#4455ff"`

Square pattern

<img src="./images/demo4.png" width="50%">

### `wallgen pattern 2000 --hexagons -c "#ff0000" -c "#0000ff"`

Hexagon pattern

<img src="./images/demo5.png" width="50%">

### `wallgen pattern 2000 -hx -c "#ff0000" -c "#000000" -c "#00ff00" -c "#00ffff" -c "#0000ff"`

Multicoloured gradient, hexagon pattern

<img src="./images/demo7.png" width="50%">

### `wallgen slants 2000`

Slants pattern

<img src="./images/demo6.png" width="50%">


## Screenshots

### `Homepage`

![homepage](./images/homepage.png)

### `Poly_Demo`

![image11](https://user-images.githubusercontent.com/35899910/46815367-664f5b80-cd98-11e8-9247-1e96dac8b8e1.png)

### `Wallgen1`

![image12](https://user-images.githubusercontent.com/35899910/46815734-22108b00-cd99-11e8-9ec5-006118b87532.png)

### `Square_Demo`

![image21](https://user-images.githubusercontent.com/35899910/46815830-53895680-cd99-11e8-8795-fa8f6731e153.png)

### `Wallgen2`

![image22](https://user-images.githubusercontent.com/35899910/46815900-76b40600-cd99-11e8-8123-966446e9c0b7.png)
