//#include <unordered_map>
//#include <geometry_msgs/Pose.h>
//#include <visualization_msgs/Marker.h>
//#include <cartographer_ros/msg_conversion.h>
//#include <cartographer/mapping/map_builder.h>
//#include <cartographer_ros_msgs/SubmapList.h>
//#include <boost/serialization/serialization.hpp>
//#include <boost/serialization/vector.hpp>
//// #include <boost/serialization/unordered_map.hpp>

//namespace cartographer_ros {
//namespace {
//class TopoMapVertex
//{
//public:
//  /**
//   * Type definition for list of vertices
//   */
//  struct Vertex {
//    int id;
//    double pose_x;
//    double pose_y;

//    friend class boost::serialization::access;
//    template<class Archive>
//    void serialize(Archive& ar, long unsigned int const& version)
//    {
//      ar& id;
//      ar& pose_x;
//      ar& pose_y;
//    }
//  };

//// typedef std::unordered_map<int, Vertex> VertexList;

//public:
//  /**
//   * Default constructor
//   */
//  TopoMapVertex(cartographer_ros_msgs::SubmapList submaps)
//  {
//    for (const auto& submap :
//         submaps.submap)
//    {
//      Vertex tmp_vertex;
//      tmp_vertex.id   = submap.submap_index;
//      tmp_vertex.pose_x = submap.pose.position.x;
//      tmp_vertex.pose_y = submap.pose.position.y;
//      vertices_.push_back(tmp_vertex);
//    }
//  }

//  /**
//   * Destructor
//   */
//  virtual ~TopoMapVertex()
//  {
//  }

//protected:
//  /**
//   * Map of names to vector of vertices
//   */
//  std::vector<Vertex> vertices_;
//protected:
//  friend class boost::serialization::access;
//  template<class Archive>
//  void serialize(Archive& ar, long unsigned int const& version)
//  {
//    ar& vertices_;
//  }
//};   // Graph<T>
//}
//}
