import glob
import os
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

import random
import time
import numpy as np

IM_WIDTH = 512
IM_HEIGHT = 512
RGB = 'rgb'
SEG = 'semantic_segmentation'


actor_list = []
try:
    ## making a connection to the server, its a localhost
    client = carla.Client('localhost', 2000)
    ## make sure you give enough time to connect, for me it takes 3.5 sec so I gave 5 sec it depends on your system 
    client.set_timeout(5.0)

    ## now setting up the environment
    world = client.get_world()

    bpl = world.get_blueprint_library()
        
    car_blueprint = bpl.filter('model3')[0]
    print(car_blueprint)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(car_blueprint, spawn_point)
    #vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    vehicle.set_autopilot(True) 

    actor_list.append(vehicle)
    

    def camera_bpl(val):

        ## https://carla.readthedocs.io/en/latest/cameras_and_sensors
        ## get the blueprint for any type of camera, I'm using for semantic segmentation
        camera_blueprint = bpl.find('sensor.camera.'+val)
        # changing the dimensions of the image
        camera_blueprint.set_attribute('image_size_x', f'{IM_WIDTH}')
        camera_blueprint.set_attribute('image_size_y', f'{IM_HEIGHT}')
        camera_blueprint.set_attribute('fov', '90')
        camera_blueprint.set_attribute('sensor_tick', '3.0')
        # Adjust camera relative to vehicle
        # spawn the camera and attach to vehicle.
        camera_spawn_point = carla.Transform(carla.Location(x=2.5, z=1))
        camera = world.spawn_actor(camera_blueprint,camera_spawn_point,attach_to = vehicle)
        return camera


    
    
    # creating two different cameras - rgb, segmentation    
    camera_rgb = camera_bpl(RGB)
    camera_seg = camera_bpl(SEG)

    # add sensor to list of actors
    actor_list.append(camera_seg)
    actor_list.append(camera_rgb)
    
    # creating an instance of the color map for segmentaions
    cc = carla.ColorConverter.CityScapesPalette
    # getting the image and saving to a local disk
    camera_rgb.listen(lambda image: image.save_to_disk('output/rgb/%06d.png' % image.timestamp))
    camera_seg.listen(lambda image: image.save_to_disk('output/seg/%06d.png' % image.timestamp, cc))
    # makes the before instruction run for given seconds, so here the sensor takes input for 1000 sec and since we sampled for 1 sec we get 1000 frames
    time.sleep(1200)

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')
