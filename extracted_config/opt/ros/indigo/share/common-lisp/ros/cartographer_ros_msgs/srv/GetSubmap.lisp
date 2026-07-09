; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-srv)


;//! \htmlinclude GetSubmap-request.msg.html

(cl:defclass <GetSubmap-request> (roslisp-msg-protocol:ros-message)
  ((submap_index
    :reader submap_index
    :initarg :submap_index
    :type cl:integer
    :initform 0)
   (write_map
    :reader write_map
    :initarg :write_map
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass GetSubmap-request (<GetSubmap-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetSubmap-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetSubmap-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<GetSubmap-request> is deprecated: use cartographer_ros_msgs-srv:GetSubmap-request instead.")))

(cl:ensure-generic-function 'submap_index-val :lambda-list '(m))
(cl:defmethod submap_index-val ((m <GetSubmap-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:submap_index-val is deprecated.  Use cartographer_ros_msgs-srv:submap_index instead.")
  (submap_index m))

(cl:ensure-generic-function 'write_map-val :lambda-list '(m))
(cl:defmethod write_map-val ((m <GetSubmap-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:write_map-val is deprecated.  Use cartographer_ros_msgs-srv:write_map instead.")
  (write_map m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetSubmap-request>) ostream)
  "Serializes a message object of type '<GetSubmap-request>"
  (cl:let* ((signed (cl:slot-value msg 'submap_index)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'write_map) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetSubmap-request>) istream)
  "Deserializes a message object of type '<GetSubmap-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'submap_index) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:setf (cl:slot-value msg 'write_map) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetSubmap-request>)))
  "Returns string type for a service object of type '<GetSubmap-request>"
  "cartographer_ros_msgs/GetSubmapRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetSubmap-request)))
  "Returns string type for a service object of type 'GetSubmap-request"
  "cartographer_ros_msgs/GetSubmapRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetSubmap-request>)))
  "Returns md5sum for a message object of type '<GetSubmap-request>"
  "d186db8adc3c0aec02e182098a6cf86e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetSubmap-request)))
  "Returns md5sum for a message object of type 'GetSubmap-request"
  "d186db8adc3c0aec02e182098a6cf86e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetSubmap-request>)))
  "Returns full string definition for message of type '<GetSubmap-request>"
  (cl:format cl:nil "~%int32 submap_index~%bool write_map~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetSubmap-request)))
  "Returns full string definition for message of type 'GetSubmap-request"
  (cl:format cl:nil "~%int32 submap_index~%bool write_map~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetSubmap-request>))
  (cl:+ 0
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetSubmap-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetSubmap-request
    (cl:cons ':submap_index (submap_index msg))
    (cl:cons ':write_map (write_map msg))
))
;//! \htmlinclude GetSubmap-response.msg.html

(cl:defclass <GetSubmap-response> (roslisp-msg-protocol:ros-message)
  ((map
    :reader map
    :initarg :map
    :type nav_msgs-msg:OccupancyGrid
    :initform (cl:make-instance 'nav_msgs-msg:OccupancyGrid)))
)

(cl:defclass GetSubmap-response (<GetSubmap-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetSubmap-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetSubmap-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<GetSubmap-response> is deprecated: use cartographer_ros_msgs-srv:GetSubmap-response instead.")))

(cl:ensure-generic-function 'map-val :lambda-list '(m))
(cl:defmethod map-val ((m <GetSubmap-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:map-val is deprecated.  Use cartographer_ros_msgs-srv:map instead.")
  (map m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetSubmap-response>) ostream)
  "Serializes a message object of type '<GetSubmap-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'map) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetSubmap-response>) istream)
  "Deserializes a message object of type '<GetSubmap-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'map) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetSubmap-response>)))
  "Returns string type for a service object of type '<GetSubmap-response>"
  "cartographer_ros_msgs/GetSubmapResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetSubmap-response)))
  "Returns string type for a service object of type 'GetSubmap-response"
  "cartographer_ros_msgs/GetSubmapResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetSubmap-response>)))
  "Returns md5sum for a message object of type '<GetSubmap-response>"
  "d186db8adc3c0aec02e182098a6cf86e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetSubmap-response)))
  "Returns md5sum for a message object of type 'GetSubmap-response"
  "d186db8adc3c0aec02e182098a6cf86e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetSubmap-response>)))
  "Returns full string definition for message of type '<GetSubmap-response>"
  (cl:format cl:nil "nav_msgs/OccupancyGrid map~%~%~%================================================================================~%MSG: nav_msgs/OccupancyGrid~%# This represents a 2-D grid map, in which each cell represents the probability of~%# occupancy.~%~%Header header ~%~%#MetaData for the map~%MapMetaData info~%~%# The map data, in row-major order, starting with (0,0).  Occupancy~%# probabilities are in the range [0,100].  Unknown is -1.~%int8[] data~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: nav_msgs/MapMetaData~%# This hold basic information about the characterists of the OccupancyGrid~%~%# The time at which the map was loaded~%time map_load_time~%# The map resolution [m/cell]~%float32 resolution~%# Map width [cells]~%uint32 width~%# Map height [cells]~%uint32 height~%# The origin of the map [m, m, rad].  This is the real-world pose of the~%# cell (0,0) in the map.~%geometry_msgs/Pose origin~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of postion and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetSubmap-response)))
  "Returns full string definition for message of type 'GetSubmap-response"
  (cl:format cl:nil "nav_msgs/OccupancyGrid map~%~%~%================================================================================~%MSG: nav_msgs/OccupancyGrid~%# This represents a 2-D grid map, in which each cell represents the probability of~%# occupancy.~%~%Header header ~%~%#MetaData for the map~%MapMetaData info~%~%# The map data, in row-major order, starting with (0,0).  Occupancy~%# probabilities are in the range [0,100].  Unknown is -1.~%int8[] data~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: nav_msgs/MapMetaData~%# This hold basic information about the characterists of the OccupancyGrid~%~%# The time at which the map was loaded~%time map_load_time~%# The map resolution [m/cell]~%float32 resolution~%# Map width [cells]~%uint32 width~%# Map height [cells]~%uint32 height~%# The origin of the map [m, m, rad].  This is the real-world pose of the~%# cell (0,0) in the map.~%geometry_msgs/Pose origin~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of postion and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetSubmap-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'map))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetSubmap-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetSubmap-response
    (cl:cons ':map (map msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetSubmap)))
  'GetSubmap-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetSubmap)))
  'GetSubmap-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetSubmap)))
  "Returns string type for a service object of type '<GetSubmap>"
  "cartographer_ros_msgs/GetSubmap")