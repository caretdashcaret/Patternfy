Patternfy
============

Transformation of textures from one OBJ to another, given two OBJs with the same vertexes and faces, but different UVs.

Credits
-------------

Code by Jenny [CaretDashCaret](http://caretdashcaret.wordpress.com/)

License
-------------

Code is under MIT License 2013.

A copy of the license can be found at [http://opensource.org/licenses/mit-license.php](http://opensource.org/licenses/mit-license.php).

To Run
-------------

Requires Python 2.7, [PIL](http://www.pythonware.com/products/pil/), and [numpy](http://www.numpy.org/)

Pass the appropriate arguments into `run()`

```python
texture = "babyroshtext.png"
original = "babyrosh.obj"
modified = "modrosh.obj"
save_as = "output.png"

run(texture, original, modified, save_as)
```

* `texture` is a png of the original texture of the 3D model
* `original` is the original 3D obj model
* `modified` is the 3D obj model with modified UVs
* `save_as` is the output name of the image

Caveats / Future To-Dos
-------------

Incorrect textures will be produced if the vertexes and faces of the two objects are not in identical order. Reordering may occur from some OBJ exports.
