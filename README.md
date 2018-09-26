# WallGen

Generates HQ poly wallpapers

## Installation 

`pip install --editable .`

## Usage

### `wallgen`

```
Usage: wallgen [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  pattern  Generate a HQ image of a beautiful pattern
  poly     Generates a HQ low poly image
```

### `wallgen poly --help`

```
Usage: wallgen poly [OPTIONS] SIDE

  Generates a HQ low poly image

Options:
  --colors TEXT...  use custom gradient, e.g --colors #ff0000 #0000ff
  --np INTEGER      number of points to use, default = 100
  --show            open the image
  --help            Show this message and exit.
```

### `wallgen pattern --help`


```
Usage: wallgen pattern [OPTIONS] SIDE

  Generate a HQ image of a beautiful pattern

Options:
  --sq              use squares instead of rhombus
  --colors TEXT...  use custom gradient, e.g --colors #ff0000 #0000ff
  --show            open the image
  --help            Show this message and exit.
```

## Examples

## `wallgen poly 2000 --colors #dd0000 #4455ff`

![](./images/demo1.png)

## `wallgen poly 2000`

![](./images/demo2.png)

## `wallgen pattern 2000 --sq --colors #dd0000 #4455ff`

![](./images/demo3.png)
