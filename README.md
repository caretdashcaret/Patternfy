Patternfy
============

Transformation of textures from one OBJ to another, given two OBJs with the same vertexes and faces, but different UVs

Credits
-------------

Code by Jenny [CaretDashCaret](http://caretdashcaret.wordpress.com/)


License
-------------

Code is under MIT License 2013

	A copy of the license can be found at http://opensource.org/licenses/mit-license.php

To Run
-------------
Enter in path/name to the original model, texture, and new model in run.py

The final texture scale (compared with the original) needs to be changed in transform.py

Caveats / Future To-Dos
-------------
Incorrect textures will be produced if the vertexes and faces of the two objects are no in identical order. Reordering may occur from some OBJ exports.