# Overview  
Apply the YOLOv11n model on a Raspberry Pi to capture the train timetable between Manchester Piccadilly Station and Oxford Station. Based on the captured images, generate an Excel (.xlsx) file to display the train information clearly.

# Example Output  
The example output of a captured train screenshot looks as follows. Please note, this is not part of the dataset. Feel free to adjust the save function position for generating the two example outputs.

[example_1](./Example_1.png)  
[example_2](./Example_2.jpg)

The code is as follows:  
[Train_capture_Code](./Yolo_Rasberry_TrainRecording.py)

# Time Table Output Example  
After capturing all the images for the trains, I use the following code to generate an Excel (.xlsx) file to clearly display the image and time relationship.  
[Time Table Example](./TimeTable_Example.png)

The code is as follows:  
[Time_Table_Code](./sort_timetable.py)

# Model Explanation  
The default YOLO model is based on PyTorch. To deploy it on a Raspberry Pi with an ARM architecture, please refer to the article below:  
[Convert PyTorch to NCNN format](https://docs.ultralytics.com/integrations/ncnn/)

# Limitations  
The model only works during the day. At night, due to limitations of the default Pi camera, RGB values are zero, which causes the model to stop working.

# [Other Project](../../project.md)
