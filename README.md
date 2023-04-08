# Ground Truth Data Generation Toolkit
Using data sources from the games static files we have developed a series of generators for common machine learning vision tasks.
In `generate_data.py` the `MultiprocessDataGenerator` class can be configured to iterate over samples in a folder made by the interfaces recording harness.
For each frame, or a sub sampling of frames, it can generate semantic segmentation maps, normal maps and depth maps from the perspective of the car when a sample was recorded.
To add a new type of data inherit from `generator/base.py` and register the generator in `DATA_GENERATORS` in `generator/generator.py`.
To modify how data is generated you can make changes to the respective `DataGenerator`.

![semantics](../../../imgs/semantic-maps.gif)
![depth](../../../imgs/depth-maps.gif)
![normals](../../../imgs/normal-maps.gif)

Each track needs to be manually inspected and a file with associated constants created prior to being able to use the generator, see `tracks/monza.py` and register the `TrackData` object in `tracks/tracks.py`.
Introduction of a new map requires each vertex groups semantic label to be decided on, any vertex groups that should be removed and any that require their materials to be modified so they are distinguishable from an important class.
We usually open the mesh in blender to inspect any classes that are ambiguous and progressively refine them based on visualisation of the coded rules.
Similarly car specific camera positioning data needs to be registered in the `cars/` folder.
The details for camera offset and pitch can be found in the game files for each car.
Specifically, each car has a `car.ini` file inside a `data.acd` archive that you need to unpack with content manager to access.
It can be helpful to assemble the data into a video with the raw capture on the left and the generated data on the right using `src/analysis/test_video.py` script.

## Editing Tracks In Blender
After parsing game kn5 files to a `.obj` file you may need to inspect and adjust certain objects that are semantically different but are textured using the same material.
First import `<track_name>.obj` into blender.
![Blender Import Obj](../../../imgs/blender-import-obj.png)

After making any changes to mesh export it using the following settings:
![Blender Export Obj](../../../imgs/blender-export-obj.png)
Then open up the exported `.obj` in a text editor and use `Find and replace` to change all the occurrences of `o ` to `g `. 
(*Note:* This is a bug in blender as vertex groups in obj should have a g prefix)