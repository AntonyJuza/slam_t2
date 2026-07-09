/*
 * Copyright 2016 The Cartographer Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef CARTOGRAPHER_MAPPING_2D_PROBABILITY_GRID_H_
#define CARTOGRAPHER_MAPPING_2D_PROBABILITY_GRID_H_

#include <vector>
#include<stack>
#include<algorithm>
#include<set>
#include "cartographer/common/port.h"
#include "cartographer/mapping/2d/grid_2d.h"
#include "cartographer/mapping/2d/map_limits.h"
#include "cartographer/mapping/2d/xy_index.h"
#include "cartographer/mapping/2d/leastSquare.h"



namespace cartographer {
namespace mapping {
using namespace leastSquare;
using namespace PointAndLine;
struct TwoInt {
  int x;
  int y;
  TwoInt(const int gx,const int gy) : x(gx), y(gy) {}
  bool operator==(const TwoInt& other) const {
    return std::forward_as_tuple(x, y) == std::forward_as_tuple(other.x, other.y);
  }

  bool operator!=(const TwoInt& other) const { return !operator==(other); }

  bool operator<(const TwoInt& other) const {
    return std::forward_as_tuple(x, y) <
           std::forward_as_tuple(other.x, other.y);
  }
};
// Represents a 2D grid of probabilities.
class ProbabilityGrid : public Grid2D {
 public:
  explicit ProbabilityGrid(const MapLimits& limits);
  explicit ProbabilityGrid(const proto::Grid2D& proto);

  // Sets the probability of the cell at 'cell_index' to the given
  // 'probability'. Only allowed if the cell was unknown before.
  void SetProbability(const Eigen::Array2i& cell_index,
                      const float probability);

  // Applies the 'odds' specified when calling ComputeLookupTableToApplyOdds()
  // to the probability of the cell at 'cell_index' if the cell has not already
  // been updated. Multiple updates of the same cell will be ignored until
  // FinishUpdate() is called. Returns true if the cell was updated.
  //
  // If this is the first call to ApplyOdds() for the specified cell, its value
  // will be set to probability corresponding to 'odds'.
  bool ApplyLookupTable(const Eigen::Array2i& cell_index,
                        const std::vector<uint16>& table);
  bool ApplyHitTableWithCheck(const Eigen::Array2i& cell_index,
                        const std::vector<uint16>& table);
  bool ApplyMissTableWithCheck(const Eigen::Array2i& cell_index,
                        const std::vector<uint16>& table);

  // Returns the probability of the cell with 'cell_index'.
  float GetProbability(const Eigen::Array2i& cell_index) const;
  uint16 GetValue(const Eigen::Array2i& cell_index) const;
  void SetUnknownValue(const Eigen::Array2i& cell_index, int &hit_count,
                                                    std::vector<std::pair<Eigen::Array2i,uint16>> &raw_value);
  void SetEliminateValue(
  const Eigen::Array2i& cell_index, int &hit_count,
  std::vector<std::pair<Eigen::Array2i,uint16>> &raw_value);
  void SetValue(const Eigen::Array2i& cell_index, const uint16 &value);
  void EdgeFill(const std::vector<Eigen::Array2i> &forward_pix,const int &min_hit_index,const std::vector<std::pair<Line,std::vector<int>>> &line_indexs, const int &data_index);
  bool EdgeEliminate(const std::vector<Eigen::Array2i> &forward_pix,const int &min_hit_index,const std::vector<std::pair<Line,std::vector<int>>> &line_indexs, const int &data_index);
  void SetMinProb(const Eigen::Array2i& cell_index,const float probability);
  void AddFitPoints(const std::pair<Eigen::Vector2f,Eigen::Vector2f> pts)
  {
    fit_lines_.emplace_back(pts);
  }
  void ClearPoints()
  {
    fit_lines_.clear();
    fill_points_.clear();
    eli_points_.clear();
    fit_points_.clear();
  }
  void AddFitPts(const Eigen::Vector2f &center)
  {
    fit_points_.emplace_back(center);
  }
  void AddFillPts(const Eigen::Vector2f &center)
  {
    fill_points_.emplace_back(center);
  }
  void AddEliPts(const Eigen::Vector2f &center)
  {
    eli_points_.emplace_back(center);
  }
  void ClearHitIndexs()
  {
    //hit_queue_.emplace_back(hit_indexs_);
    hit_indexs_.clear();
    //if(hit_queue_.size()>2) hit_queue_.pop_front();
  }
  void ClearLastspIndexs()
  {
    last_sp_indexs_.clear();
  }
  void AddLastspIndexs(const std::set<int> &indexs)
  {
    last_sp_indexs_ = indexs;
  }
  std::set<int> GetLastspIndexs()
  {
    return last_sp_indexs_;
  }
  void CombineHitIndexs()
  {
    // all_hit_indexs_.clear();
    // for(const auto &indexs :  hit_queue_)
    // {
    //   for(const auto &index : indexs)
    //   {
    //     all_hit_indexs_.insert(index);
    //   }   
    // }
  }
  std::vector<std::pair<Eigen::Vector2f,Eigen::Vector2f>> GetFitLine() const override
  {
    return fit_lines_;
  }
  std::vector<Eigen::Vector2f> GetFillPts() const override
  {
    return fill_points_;
  }
  std::vector<Eigen::Vector2f> GetFitPts() const override
  {
    std::vector<Eigen::Vector2f> hit_pts;
    // hit_pts.reserve(hit_indexs_.size());
    // for (const auto &index: hit_indexs_)
    // {
    //   hit_pts.emplace_back(limits().GetCellCenter(Eigen::Array2i(index.x,index.y)));
    // }
    return hit_pts;
  }
  std::vector<Eigen::Vector2f> GetEliPts() const override
  {
    return eli_points_;
  }

  virtual proto::Grid2D ToProto() const override;
  virtual std::unique_ptr<Grid2D> ComputeCroppedGrid() const override;
  virtual bool DrawToSubmapTexture(
      proto::SubmapQuery::Response::SubmapTexture* const texture,
      transform::Rigid3d local_pose) const override;
  private:
    std::vector<std::pair<Eigen::Vector2f,Eigen::Vector2f>> fit_lines_;
    std::vector<Eigen::Vector2f> fill_points_;
    std::vector<Eigen::Vector2f> eli_points_;
    std::vector<Eigen::Vector2f> fit_points_;
    std::vector<int> hit_indexs_;
    std::set<int> last_sp_indexs_;
    //std::deque<std::set<TwoInt>> hit_queue_;
    //std::set<TwoInt> all_hit_indexs_;
    
};

}  // namespace mapping
}  // namespace cartographer

#endif  // CARTOGRAPHER_MAPPING_2D_PROBABILITY_GRID_H_
