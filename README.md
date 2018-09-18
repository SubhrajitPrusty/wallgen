# WallGen

Generates HQ poly wallpapers

## Installation 

`pip install --editable .`

## Usage

```
Usage: wallgen [OPTIONS] SIDE

  Generates a side X side HQ low poly image of random gradient

Options:
  --colors TEXT...  use color1 --> color2 gradient, e.g #ff0000 #0000ff
  --np INTEGER      number of points to use, default = 100
  --radius INTEGER  radius, within which no other point is generated,
                    default=200
  --show            open the image
  --help            Show this message and exit.
```

## Examples

![](./images/demo1.png)
![](./images/demo2.png)
![](./images/demo3.png)
