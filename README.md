# DS_To_YoloV8
Allows a user to input a unlabeled dataset and create a YoloV8 trained model for Object Detection. Currently the following features are WIP:
- Implement split-by-user choice (Drop a ton of images into raw_dataset, through prompts automatically split those images up per user requirements)\
- Multi-subject ontology for the Autodistill step (Currently you must enter a single ontology for each class at the beginning of each Autodistill run.
- Allow for ontology repitition/memory per user requirements

This is a work in progress!

HOW TO USE
1. Ensure that you are running CUDA and the corresponding CuDNN for that CUDA toolkit, as well as OpenCV+Torch versions that are compatible with that CUDA/CuDNN configuration
2. Drop your target YoloV8 models (downloaded from https://github.com/ultralytics/ultralytics) into the model/ folder
3. Drop a dataset split into folders (classA, classB, classC,...) into the ds/split_dataset file
4. Run dm_to_model.py and decline dataset splitting
5. Proceed through all remaining steps
-->Note that during the AutoDistill step, you must enter an ontology for each class folder once a folder has been labeled!
