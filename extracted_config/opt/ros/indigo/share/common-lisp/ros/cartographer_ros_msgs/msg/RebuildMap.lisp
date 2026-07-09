; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-msg)


;//! \htmlinclude RebuildMap.msg.html

(cl:defclass <RebuildMap> (roslisp-msg-protocol:ros-message)
  ((hit_prob
    :reader hit_prob
    :initarg :hit_prob
    :type cl:float
    :initform 0.0)
   (miss_prob
    :reader miss_prob
    :initarg :miss_prob
    :type cl:float
    :initform 0.0)
   (dis
    :reader dis
    :initarg :dis
    :type cl:float
    :initform 0.0)
   (theta
    :reader theta
    :initarg :theta
    :type cl:float
    :initform 0.0))
)

(cl:defclass RebuildMap (<RebuildMap>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RebuildMap>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RebuildMap)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-msg:<RebuildMap> is deprecated: use cartographer_ros_msgs-msg:RebuildMap instead.")))

(cl:ensure-generic-function 'hit_prob-val :lambda-list '(m))
(cl:defmethod hit_prob-val ((m <RebuildMap>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-msg:hit_prob-val is deprecated.  Use cartographer_ros_msgs-msg:hit_prob instead.")
  (hit_prob m))

(cl:ensure-generic-function 'miss_prob-val :lambda-list '(m))
(cl:defmethod miss_prob-val ((m <RebuildMap>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-msg:miss_prob-val is deprecated.  Use cartographer_ros_msgs-msg:miss_prob instead.")
  (miss_prob m))

(cl:ensure-generic-function 'dis-val :lambda-list '(m))
(cl:defmethod dis-val ((m <RebuildMap>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-msg:dis-val is deprecated.  Use cartographer_ros_msgs-msg:dis instead.")
  (dis m))

(cl:ensure-generic-function 'theta-val :lambda-list '(m))
(cl:defmethod theta-val ((m <RebuildMap>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-msg:theta-val is deprecated.  Use cartographer_ros_msgs-msg:theta instead.")
  (theta m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RebuildMap>) ostream)
  "Serializes a message object of type '<RebuildMap>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'hit_prob))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'miss_prob))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'dis))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'theta))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RebuildMap>) istream)
  "Deserializes a message object of type '<RebuildMap>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'hit_prob) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'miss_prob) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'dis) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'theta) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RebuildMap>)))
  "Returns string type for a message object of type '<RebuildMap>"
  "cartographer_ros_msgs/RebuildMap")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RebuildMap)))
  "Returns string type for a message object of type 'RebuildMap"
  "cartographer_ros_msgs/RebuildMap")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RebuildMap>)))
  "Returns md5sum for a message object of type '<RebuildMap>"
  "34262ddb2e3ed671445a8c1fe1329a99")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RebuildMap)))
  "Returns md5sum for a message object of type 'RebuildMap"
  "34262ddb2e3ed671445a8c1fe1329a99")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RebuildMap>)))
  "Returns full string definition for message of type '<RebuildMap>"
  (cl:format cl:nil "float32 hit_prob~%float32 miss_prob~%float32 dis~%float32 theta~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RebuildMap)))
  "Returns full string definition for message of type 'RebuildMap"
  (cl:format cl:nil "float32 hit_prob~%float32 miss_prob~%float32 dis~%float32 theta~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RebuildMap>))
  (cl:+ 0
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RebuildMap>))
  "Converts a ROS message object to a list"
  (cl:list 'RebuildMap
    (cl:cons ':hit_prob (hit_prob msg))
    (cl:cons ':miss_prob (miss_prob msg))
    (cl:cons ':dis (dis msg))
    (cl:cons ':theta (theta msg))
))
