class transform_config:
    def __init__(self):
        self.degrees_between_dist_sensors = 15.5
        self.pitch_scale_factor = 1/5000
        self.pitch_offset = -0.3
        self.yaw_scale_factor = 1/80
        self.roll_offset = 1.5
        self.projector_resolution_px = (1080, 1920)
        self.throw_ratio = 88/120
        self.input_image_dimension_m = (2.5,2.5)
        self.input_image_dimension_px = (3500,3500)
        self.distance_scale_factor = 1/100
        self.distancee_offset_cm = 5
