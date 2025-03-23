# Overview
Apply yolo11n model on rasberry pi for capturing train timetable between Manchester Piccadility station and Oxford station. Based on the captured img, generating a xlsx file for clear displaying the train information.

# Example output
The example output of a captured train screen shoot looks as below. Notice, it is not used for the dataset. Feel free to change the save function position for getting the two example outputs.
[example_1](./Example_1.png)
[example_2](./Example_2.jpg)
The code is below:
[Train_capture_Code](./Yolo_Rasberry_TrainRecording.py)

# Time Table output Example
After capturing all the images for the trains, I upload a code to generate a xlsx file for clearly displaying the image time relationship.
[Time Table Example](./TimeTable_Example.png)
The code is below:
[Time_Table_Code](./sort_timetable.py)

# Model Explain
The default yolo model is based on pytorch. For application on Rasbeery pi with arm strcutre, please refer to the below article
[convert pytorch to ncnn format](https://docs.ultralytics.com/integrations/ncnn/)

# Limitation 
The model only works for the day time, during night, due to the limit of default pi camera, RGB values are zero making model not working.

# [Other Project](../../project.md)


