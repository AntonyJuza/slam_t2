-- Copyright 2016 The Cartographer Authors
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

TRAJECTORY_BUILDER_2D = {
  use_imu_data = true,
  min_range = 0.,
  max_range = 30.,
  sum_scan_numbers = 300,
  min_z = -0.8,
  max_z = 2.,
  missing_data_ray_length = 5.,
  num_accumulated_range_data = 1,--积累到这个数量的点云信息后，执行一次匹配scan_match，将有效点云插入局部地图InsertIntoSubmap().
  voxel_filter_size = 0.025,--此值越小，得到的数据越稠密，但是计算量越高；此值越大，丢失数据越多，但计算更快。

  adaptive_voxel_filter = {
    max_length = 0.5,
    min_num_points = 200,
    max_range = 30.,
  },

  loop_closure_adaptive_voxel_filter = {
    max_length = 0.9,
    min_num_points = 200,
    max_range = 50.,
  },

  use_online_correlative_scan_matching = false,
  real_time_correlative_scan_matcher = { --用于传感器质量较差场合,在闭环中对submap进行匹配，而不是与当前的submap相匹配,最好的匹配用作CeresScanMatcher的先验
    linear_search_window = 0.05,
    angular_search_window = math.rad(2.),
    translation_delta_cost_weight = 1e-1,
    rotation_delta_cost_weight = 3e-1,
  },

  ceres_scan_matcher = {--用于高质量的传感器场合
    occupied_space_weight = 1.,--占用空间（扫描点）
    translation_weight = 10.,
    rotation_weight = 40.,--PoseExtrapolator或者RealTimeCorrelativeScanMatcher的权重
    ceres_solver_options = {--Ceres匹配算法收敛速度配置
      use_nonmonotonic_steps = false,--bool量，启动非单调置信区域
      max_num_iterations = 20,--最大迭代步数
      num_threads = 1,--线程数
    },
  },

  motion_filter = {
    max_time_seconds = 5,
    max_distance_meters = 0.05,
    max_angle_radians = math.rad(1.),
  },

  imu_gravity_time_constant = 10.,
  max_pitch = 0.1,--0.06
  use_imu_filter = false;
  support_vslam = true;

  submaps = {
    num_range_data = 90,
    grid_options_2d = {
      grid_type = "PROBABILITY_GRID",
      resolution = 0.05,
    },
    range_data_inserter = {
      range_data_inserter_type = "PROBABILITY_GRID_INSERTER_2D",
      probability_grid_range_data_inserter = {
        insert_free_space = true,
        hit_probability = 0.55,
        miss_probability = 0.49,
      },
    },
  },
}
