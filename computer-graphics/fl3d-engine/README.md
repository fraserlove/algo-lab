
![alt text](images/FL3D_small.png)
# FL3D - A 3D Rendering Engine
A 3D rendering engine to create, display and transform basic 3D objects. Includes a fully featured GUI, world lighting and object database storage.

![alt text](https://i.ibb.co/84VG3zS/Screenshot-2023-08-12-at-20-23-15.png)

## Installation and Usage

Note that due to limitations with `pygame` and `tkinter` the engine can only be ran on windows systems. FL3D can be ran from the projects root directory as follows:
```bash
python src/engine_client.py
```

## Implementation Notes
Currently the engine only supports Windows however a Linux version may be avaliable soon. For more detail into the design and implementation of the engine see the development report under the docs folder.

I wanted to create my own matrix functions and so I created a matrix class that can use the matrix_math module included to perform matrix operations to transform, rotate and scale the objects in the scene. This project was not meant to be the most efficient engine by using numpy and other libraries, but was instead intended to allow me to get a better understanding of 3d graphics.

The included lighting system has a very basic implementation that uses the average y position of the nodes in a surface on the screen to calculate the lighting based on a map between the height of the screen and 0 to 255. The engine also uses insertion sort to order all of the surfaces in the screen by their z position so that the closest surfaces get drawn last. The engines GUI allows for the creation, deletion of objects as well as editing their attributes. A sqlite database implementation is used to store object data so that so called 'world spaces' (all the objects in the scene) can be imported and saved.
