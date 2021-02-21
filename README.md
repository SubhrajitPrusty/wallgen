<img src="./images/logo.png" width="40%" alt="logo">

# WallGen
![](https://img.shields.io/badge/Python-3-blue.svg?style=for-the-badge&logo=python)
----
[![](https://img.shields.io/badge/Website-blue.svg?style=for-the-badge)](http://wallgen.subhrajitpy.me/)
[![Gitter](https://img.shields.io/gitter/room/:user/:repo.svg?style=for-the-badge&colorB=00ddff)](https://gitter.im/wallgen/Lobby)

Generates HQ poly wallpapers

- Make poly wallpapers over a gradient with random colors, or using custom colors
- Choose different shapes like hexagons, squares, and diamonds apart from triangles
- Apply polygons over a picture
- Make a [video](https://gist.github.com/SubhrajitPrusty/5f303202c615e42e12b1a640322f9fec) with polygonized style
- Make a gradient creation [video](https://gist.github.com/SubhrajitPrusty/e994ce8f3b643382328c1c779893a721)
- Make a cool polygonal [video](https://gist.github.com/SubhrajitPrusty/37cf527ca4d92ed4a19af91099984b51)
- Dont have `Python`? Use the [website](http://wallgen.subhrajitpy.me) (Limited capabilites)

## Installation

**Requires Python 3**

Via pip

```pip
pip install -e git+https://github.com/SubhrajitPrusty/wallgen#egg=wallgen
```


Clone the repository

```
git clone https://github.com/SubhrajitPrusty/wallgen.git

cd wallgen

pip install --editable .
```

## Usage

`wallgen`

```
Usage: wallgen [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  pic     Use a picture instead of a gradient
  poly    Generates a HQ low poly image using a gradient
  shape   Generates a HQ image of a beautiful shapes
  slants  Generates slanting lines of various colors

```

----

## Usage Docker for hosting the website

Inside the folder

docker run -d -p 5000:5000 subhrajitprusty/wallgen

Run `docker ps` to check if container is running.

Goto [localhost:5000](http://localhost:5000) to check out the website.

## Examples

[Here](./examples.md)