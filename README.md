# autonomous-driving
Basic driving assistance based on lane detection using image segmentation

I have uploaded 2 files - spawn_npc.py(existing file made one change) and mydemo.py(own file)

We are using the spawn_npc file to create n number of spectators(I set to 60) in the environment like cars,pedestrians,motorcycles,trucks, etc. This file makes changes in the server side so now the world from server is set up by us and we can make our customized client call through mydemo.py .

I have called the file mydemo.py within spawn_npc.py ,hence running spwan_npc.py file alone is enough.

The output set of images (segmented and its corresponding rgb image) are stored inside 'PythonAPI>examples>output>*'

Default setup : (by me)

* ! No. of frames from sensor per second = 3     
* @ No. of spectators = 60
* @ spawn_point = random

@ --> can change
! --> do not change



Go through the 'detailed explanation.docx for more details( about the scope of this project, model description, etc)
