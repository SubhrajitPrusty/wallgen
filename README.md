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

`docker build -t wallgen-doc:latest .`

`docker run -d -p 5000:5000 wallgen-doc`

Run `docker ps` to check if container is running.

Goto [localhost:5000](http://localhost:5000) to check out the website.

----

## Examples


`wallgen poly 2000`

Random Gradient

<img src="./images/demo1.png" width="50%">

---

`wallgen poly 2000 --use-nn --points 5000`

NbyNGradient method

<img src="./images/nngradient.png" width="50%">

---

`wallgen poly 1000 --colors "#ff0000" --colors "#00ddff"`

Fixed color/gradient

<img src="./images/poly.png" width="50%">

---

`wallgen poly 2000 -c "#ff0000" -c "#00ddff" --points 2000 --swirl`

Swirl

<img src="./images/poly_swirl.png" width="50%">

---

`wallgen poly 2000 --points 2000 -un --swirl`

NbyN and swirl

<img src="./images/nn_swirl.png" width="50%">

---

`wallgen poly 2000 -c "#ff0000" -c "#000000" -c "#0000ff"`

More than 2 colours

<img src="./images/demo3.png" width="50%">

---

`wallgen poly 1000 -c "#ff0000" -c "#00ddff" -o "#2c2c2c"`

With outline

<img src="./images/poly-outline.png" width="50%">

---

`wallgen shape 2000 -t square -c "#ff0099" -c "#00ddff"`

Square pattern

<img src="./images/square.png" width="50%">

---

`wallgen shape 2000 -t square -c "#ff0099" -c "#00ddff" -o "#2c2c2c"`

Square pattern with Outline

<img src="./images/square-outline.png" width="50%">

---

`wallgen shape 2000 -t square -c "#ff0099" -c "#00ddff" --swirl`

Square with swirl

<img src="./images/sq_swirl.png" width="50%">

---

`wallgen shape 2000 -t hex -c "#ff0099" -c "#00ddff"`

Hexagon pattern

<img src="./images/hex.png" width="50%">

---

`wallgen shape 2000 -t diamond -c "#ff0099" -c "#00ddff"`

Diamond pattern

<img src="./images/diamond.png" width="50%">

---

`wallgen shape 2000 -t triangle -c "#ff0099" -c "#00ddff"`

Triangle pattern

<img src="./images/triangle.png" width="50%">

---

`wallgen slants 2000`

Slants pattern

<img src="./images/slants.png" width="50%">

---

`wallgen slants 2000 --swirl`

Slants with swirl

<img src="./images/slants_swirl.png" width="50%">

---

Polygonizing a picture

1

`wallgen pic poly bonfire.jpg -p 50000`

<img src="./images/bonfire.jpg" width="50%">
<img src="./images/bonfire-poly.png" width="50%">

2

`wallgen pic poly anime.png -p 50000`

<img src="./images/anime.png" width="50%">
<img src="./images/anime-poly.png" width="50%">

3

`wallgen pic poly clouds.jpg -p 50000`

<img src="./images/clouds.jpg" width="50%">
<img src="./images/clouds-poly.png" width="50%">

---

Using a picture with Smart edges

`wallgen pic poly art.jpg --smart`

<img src="./images/art.jpg" width="50%">
<img src="./images/art-smart.png" width="50%">

---
