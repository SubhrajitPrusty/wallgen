# Examples


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
