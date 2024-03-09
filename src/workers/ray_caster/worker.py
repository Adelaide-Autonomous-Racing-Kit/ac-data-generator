import multiprocessing as mp
from typing import Dict

import numpy as np

from src.utils.load import load_game_state
from src.workers.base import BaseWorker
from src.workers.ray_caster.utils import (
    calculate_horizontal_fov,
    convert_scene_to_collision_mesh,
    get_camera_location,
    get_camera_rotation,
)


class RayCastingWorker(BaseWorker):
    """
    Process responsible for calculating collisions via casting camera rays out
        into a scene. This class receives work from a MultiprocessDataGenerator
        and posts work to DataGenerationWorkers via two multiprocessing queues.

    :param configuration: A dictionary containing the configuration for the
        workers.
    :type configuration: Dict
    :param shared_state: An object containing the shared state between all
        workers in the MultiprocessDataGenerator.
    :type shared_state: WorkerSharedState
    """

    def _is_work_complete(self) -> bool:
        """
        Check if all the jobs are done.

        :return: True if the job queue is empty, False otherwise.
        :rtype: bool
        """
        return self._job_queue.empty()

    def _do_work(self):
        """
        Perform ray casting and submit a generation job.
        """
        self._cast_rays()
        self._submit_generation_job()

    def _cast_rays(self):
        """
        Adjust the camera's pose and update the ray intersections.
        """
        self._adjust_camera()
        self._update_ray_intersections()

    def _adjust_camera(self):
        """
        Adjust the camera's pose in the scene.
        """
        state_path = self.recording_path.joinpath(self._record_number + ".bin")
        state = load_game_state(state_path)
        self._scene.set_camera(
            angles=get_camera_rotation(state, self.car_name),
            center=get_camera_location(state, self.car_name),
            resolution=self.image_size,
            distance=0.0,
            fov=self.fov,
        )
        self._set_camera_rays()

    def _set_camera_rays(self):
        """
        Set the rays for each pixel in the current camera to the object
        """
        # (origin, direction unit vector, pixel each ray belongs to)
        self._camera_rays = self._scene.camera_rays()

    def _update_ray_intersections(self):
        """
        Run ray casting for the current camera and update the object.
        """
        self._ray_intersections = self._cast_camera_rays()
        if self._is_generating_depth:
            self._pixels_to_rays = self._pixels[self._i_rays]

    def _cast_camera_rays(self):
        """
        Cast camera rays and get ray intersections.

        :return: list of ray intersections.
        :rtype: list
        """
        origins, directions = self._ray_origins, self._ray_directions
        if not self._is_generating_depth:
            return self._mesh.intersects_first(origins, directions)
        return self._mesh.intersects_location(origins, directions, False)

    def _submit_generation_job(self):
        """
        Submit a data generation job to the GenerationWorker queue.
        """
        generation_job = self._create_generation_job()
        self.generation_queue.put(generation_job)

    def _create_generation_job(self) -> Dict:
        """
        Packs information required by the DataGenerationWorker to create data
            from triangle intersections into a dictionary.
        """
        generation_job = {
            "record_number": self._record_number,
            "i_triangles": self._i_triangles,
        }
        self._maybe_add_depth_generation_information(generation_job)
        return generation_job

    def _maybe_add_depth_generation_information(self, generation_job: Dict):
        """
        If the data generation worker need to generate depth maps, ensure the
            extra information required to do so is present in the job.

        :param generation_job: A dictionary containing ray casting information
            required for downstream workers
        :type generation_job: Dict
        """
        if self._is_generating_depth:
            self._add_depth_generation_information(generation_job)

    def _add_depth_generation_information(self, generation_job: Dict):
        """
        Update the information contained in the generation job to include ray
            hit locations (locations), the camera origin (origin), a
            pixel to ray index mapping (pixels_to_rays), ray direction vectors
            (ray_directions) and the index of each ray (i_rays).

        :param generation_job: A dictionary containing ray casting information
            required for downstream workers
        :type generation_job: Dict
        """
        additional_information_for_depth_calculations = {
            "locations": self._locations,
            "origin": self._ray_origins[0],
            "pixels_to_rays": self._pixels_to_rays,
            "ray_directions": self._ray_directions,
            "i_rays": self._i_rays,
        }
        generation_job.update(additional_information_for_depth_calculations)

    @property
    def _record_number(self) -> str:
        """
        ID number of the sample in a recording to be processed
        """
        return self._work

    @property
    def _job_queue(self) -> mp.Queue:
        """
        Multiprocessing queue that the ray caster receives work from
        """
        return self.ray_cast_queue

    @property
    def _i_rays(self) -> np.array:
        """
        Index for each ray cast by camera pixels
        """
        return self._ray_intersections[1]

    @property
    def _i_triangles(self) -> np.array:
        """
        Index of each triangle hit by a given ray
        """
        if self._is_generating_depth:
            return self._ray_intersections[2]
        return self._ray_intersections

    @property
    def _locations(self) -> np.array:
        """
        3D points where rays hit a triangle
        """
        return self._ray_intersections[0]

    @property
    def _pixels(self) -> np.array:
        """
        Mapping from image coordinates to rays
        """
        return self._camera_rays[2]

    @property
    def _ray_origins(self) -> np.array:
        """
        Origin of camera ray for each pixel
        """
        return self._camera_rays[0]

    @property
    def _ray_directions(self) -> np.array:
        """
        Direction of camera ray for each pixel
        """
        return self._camera_rays[1]

    def _setup(self):
        """
        Setup steps specific to the RayCastingWorker
        """
        self._set_depth_generation_flag()
        self._setup_field_of_view()
        self._setup_scene()
        self._setup_collision_mesh()
        self.set_as_ready()

    def _set_depth_generation_flag(self):
        """
        Set whether depth maps are being generated by the down stream workers.
        """
        self._is_generating_depth = "depth" in self._config["generate"]

    def _setup_collision_mesh(self):
        """
        Create the collision mesh to run ray casting on
        """
        self._mesh = convert_scene_to_collision_mesh(self._scene)

    def _setup_field_of_view(self):
        """
        Set the field of view for the camera.
        """
        v_fov = self._config["vertical_fov"]
        width, height = self.image_size
        h_fov = calculate_horizontal_fov(v_fov, width, height)
        self.fov = (h_fov, v_fov)
