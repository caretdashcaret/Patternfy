Patternfy
============

[![Video Game Plushie](http://i1115.photobucket.com/albums/k552/caretdashcaret/2014-03/0_zpsd_zps60b0f522.jpg)](http://makezine.com/projects/make-38-cameras-and-av/video-game-plushies/)

Patternfy is a script that transforms the textures from one OBJ to another,
given two OBJs with the same vertexes and faces, but different UVs.

It can be used for pattern drafting, (creating printable fabric patterns), if the OBJs represent the final sewed object,
UVs represent the sewing pattern, and the textures represent the fabric print.

I created this script to turn 3D models (extracted from video games) into stuffed animals,
with a procedurally generated sewing pattern that preserves the model's original shape and coloration.

For examples/tutorials see [MAKE magazine Vol 38 - DIY Video Game Plushies from 3D Models](http://makezine.com/projects/make-38-cameras-and-av/video-game-plushies/).

Credits
-------------

Created by Jenny - [CaretDashCaret](http://caretdashcaret.wordpress.com/)

[![Jenny](http://i1115.photobucket.com/albums/k552/caretdashcaret/2014-03/About5_zps7f79c497.jpg)](http://caretdashcaret.wordpress.com/)

License
-------------

Patternfy's code is under [GPLv3](http://opensource.org/licenses/gpl-3.0.html).
A copy of GPLv3 can be found at [http://opensource.org/licenses/gpl-3.0.html](http://opensource.org/licenses/gpl-3.0.html).

Patternfy's art assets are under [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/).
A copy of the license can be found at [http://creativecommons.org/licenses/by-sa/3.0/](http://creativecommons.org/licenses/by-sa/3.0/).

Development Environment
-------------

It's generally cleaner to set up a development environment. However, you can skip straight to the Run section.
Setting up an environment requires [virtualenv](https://pypi.python.org/pypi/virtualenv). Directories may vary depending on operating system.

```sh
$ virtualenv ~/.virtualenvs/patternfy
$ . ~/.virtualenvs/patternfy/bin/activate
$ pip install -r requirements.txt
```

The requirements.txt contains `numpy` for solving matrices and `nose` for testing.
PIL also needs to be installed, but [`pip install PIL` won't provide support for png](http://jamie.curle.io/blog/webfaction-installing-pil/).
To install PIL with png support, [setup.py needs to be edited](http://stackoverflow.com/questions/4435016/install-pil-on-virtualenv-with-libjpeg).

```sh
$ pip install --no-install PIL
$ cd ~/.virtualenvs/patternfy/build/PIL
```

In `setup.py`, around line 38, change
```sh
JPEG_ROOT = None
ZLIB_ROOT = None
```
to
```sh
JPEG_ROOT = libinclude("/usr/lib")
ZLIB_ROOT = libinclude("/usr/lib")
```

```sh
$ pip install PIL
```

If you get a ```Cannot fetch index base URL http://pypi.python.org/simple/```,
[try using pip version 1.2.1](http://stackoverflow.com/questions/21294997/pip-connection-failure-cannot-fetch-index-base-url-http-pypi-python-org-simpl)

To Run
-------------

Running requires Python 2.7, [PIL](http://www.pythonware.com/products/pil/), and [numpy](http://www.numpy.org/).

Pass the appropriate arguments into run.py from the command line.

```sh
$ python run.py -g "objects/original.obj" -m "objects/modified.obj" -t "objects/original_texture.png" -s "objects/output.png"

$ Patternfy - 2014-03-30 17:13:40,715 - loading texture
$ Patternfy - 2014-03-30 17:13:40,741 - loading original OBJ
$ Patternfy - 2014-03-30 17:13:40,742 - loading modified OBJ
$ Patternfy - 2014-03-30 17:13:40,742 - seam equilizing
$ Patternfy - 2014-03-30 17:13:40,743 - transforming image
$ Patternfy - 2014-03-30 17:13:41,106 - saving
$ Patternfy - 2014-03-30 17:13:41,408 - success
```

* `-g` or `--original` is the original 3D obj model
* `-m` or `--modified` is the 3D obj model with modified UVs
* `-t` or `--texture` is a png of the original texture of the 3D model
* `-s` or `--save` is the name to save the output image as

The `objects/output.png` should be the same as the `objects/expected_output.png`.

Testing
-------------

Running the tests requires [nose](https://nose.readthedocs.org/en/latest/).

```sh
$ nosetests
```

Caveats / Future To-Dos
-------------

* Incorrect textures will be produced if the vertexes and faces of the two objects are not in identical order. Reordering may occur from some OBJ exports.
* Maximum number of points per face need to be 4 to correctly generate the texture
