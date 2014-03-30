Patternfy
============

Patternfy is a script that transforms the textures from one OBJ to another,
given two OBJs with the same vertexes and faces, but different UVs.

It can be used for pattern drafting, (creating printable fabric patterns), if the OBJs represent the final sewed object,
UVs represent the sewing pattern, and the textures represent the fabric print.

I created this script to turn 3D models (extracted from video games) into stuffed animals,
with a procedurally generated sewing pattern that preserves the model's original shape and coloration.

For examples/tutorials see (MAKE magazine Vol 38 - DIY Video Game Plushies from 3D Models)[http://makezine.com/projects/make-38-cameras-and-av/video-game-plushies/].

Credits
-------------

Created by Jenny - [CaretDashCaret](http://caretdashcaret.wordpress.com/)

License
-------------

Patternfy's code is under [GPLv3](http://opensource.org/licenses/gpl-3.0.html).
A copy of GPLv3 can be found at [http://opensource.org/licenses/gpl-3.0.html](http://opensource.org/licenses/gpl-3.0.html).

Patternfy's art assets are under [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/).
A copy of Creative Commons Attribution-ShareAlike 3.0 can be found at [http://creativecommons.org/licenses/by-sa/3.0/](http://creativecommons.org/licenses/by-sa/3.0/).


To Run
-------------

Requires Python 2.7, [PIL](http://www.pythonware.com/products/pil/), and [numpy](http://www.numpy.org/)

Pass the appropriate arguments into `run()`

```python
texture = "original_texture.png"
original = "original.obj"
modified = "modified.obj"
save_as = "output.png"

run(texture, original, modified, save_as)
```

* `texture` is a png of the original texture of the 3D model
* `original` is the original 3D obj model
* `modified` is the 3D obj model with modified UVs
* `save_as` is the output name of the image

Caveats / Future To-Dos
-------------

* Incorrect textures will be produced if the vertexes and faces of the two objects are not in identical order. Reordering may occur from some OBJ exports.
* Maximum number of points per face need to be 4 to correctly generate the texture
