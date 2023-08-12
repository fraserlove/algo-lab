
![alt text](images/fl3d_small.png)
# FL3D - A 3D Rendering Engine
A 3D rendering engine to create, display and transform basic 3D objects. Includes a fully featured GUI, world lighting and object database storage.

![alt text](https://i.ibb.co/84VG3zS/Screenshot-2023-08-12-at-20-23-15.png)

## Installation and Usage

Due to issues and limitations with `pygame` and `tkinter` the engine can only be ran on windows systems. The FL3D engine can be ran from the projects root directory as follows:
```bash
python src/engine_client.py
```

## Implementation Notes
This project was used to further my understanding of 3D graphics and the mathematics behind it. As such, I implemented a custom `matrix_math` module to perform matrix operations to transform. rotate and scale objects in the scene. Note that a more efficient implementation would be to use numpy arrays and use numpys own inbuilt matrix operations.

The included lighting system has a very basic implementation that uses the average y position of the nodes in a surface on the screen to calculate the lighting based on a map between the height of the screen and 0 to 255. This system gives an impression that the light is coming down from the top of the window. The engine also uses insertion sort to order all of the surfaces in the screen by their z position so that the closest surfaces get drawn last. The engines GUI allows for the creation, deletion of objects as well as editing their attributes. A sqlite database implementation is used to store object data so that so called 'world spaces' (all the objects in the scene) can be imported and saved.
