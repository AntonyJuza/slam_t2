; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-srv)


;//! \htmlinclude SetFilterMode-request.msg.html

(cl:defclass <SetFilterMode-request> (roslisp-msg-protocol:ros-message)
  ((open_filter
    :reader open_filter
    :initarg :open_filter
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass SetFilterMode-request (<SetFilterMode-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetFilterMode-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetFilterMode-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<SetFilterMode-request> is deprecated: use cartographer_ros_msgs-srv:SetFilterMode-request instead.")))

(cl:ensure-generic-function 'open_filter-val :lambda-list '(m))
(cl:defmethod open_filter-val ((m <SetFilterMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:open_filter-val is deprecated.  Use cartographer_ros_msgs-srv:open_filter instead.")
  (open_filter m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetFilterMode-request>) ostream)
  "Serializes a message object of type '<SetFilterMode-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'open_filter) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetFilterMode-request>) istream)
  "Deserializes a message object of type '<SetFilterMode-request>"
    (cl:setf (cl:slot-value msg 'open_filter) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetFilterMode-request>)))
  "Returns string type for a service object of type '<SetFilterMode-request>"
  "cartographer_ros_msgs/SetFilterModeRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetFilterMode-request)))
  "Returns string type for a service object of type 'SetFilterMode-request"
  "cartographer_ros_msgs/SetFilterModeRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetFilterMode-request>)))
  "Returns md5sum for a message object of type '<SetFilterMode-request>"
  "d4bf3ba13370f4cc90a0b1718b13ecd4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetFilterMode-request)))
  "Returns md5sum for a message object of type 'SetFilterMode-request"
  "d4bf3ba13370f4cc90a0b1718b13ecd4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetFilterMode-request>)))
  "Returns full string definition for message of type '<SetFilterMode-request>"
  (cl:format cl:nil "bool open_filter~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetFilterMode-request)))
  "Returns full string definition for message of type 'SetFilterMode-request"
  (cl:format cl:nil "bool open_filter~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetFilterMode-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetFilterMode-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetFilterMode-request
    (cl:cons ':open_filter (open_filter msg))
))
;//! \htmlinclude SetFilterMode-response.msg.html

(cl:defclass <SetFilterMode-response> (roslisp-msg-protocol:ros-message)
  ((res
    :reader res
    :initarg :res
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass SetFilterMode-response (<SetFilterMode-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetFilterMode-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetFilterMode-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<SetFilterMode-response> is deprecated: use cartographer_ros_msgs-srv:SetFilterMode-response instead.")))

(cl:ensure-generic-function 'res-val :lambda-list '(m))
(cl:defmethod res-val ((m <SetFilterMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:res-val is deprecated.  Use cartographer_ros_msgs-srv:res instead.")
  (res m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetFilterMode-response>) ostream)
  "Serializes a message object of type '<SetFilterMode-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'res) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetFilterMode-response>) istream)
  "Deserializes a message object of type '<SetFilterMode-response>"
    (cl:setf (cl:slot-value msg 'res) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetFilterMode-response>)))
  "Returns string type for a service object of type '<SetFilterMode-response>"
  "cartographer_ros_msgs/SetFilterModeResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetFilterMode-response)))
  "Returns string type for a service object of type 'SetFilterMode-response"
  "cartographer_ros_msgs/SetFilterModeResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetFilterMode-response>)))
  "Returns md5sum for a message object of type '<SetFilterMode-response>"
  "d4bf3ba13370f4cc90a0b1718b13ecd4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetFilterMode-response)))
  "Returns md5sum for a message object of type 'SetFilterMode-response"
  "d4bf3ba13370f4cc90a0b1718b13ecd4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetFilterMode-response>)))
  "Returns full string definition for message of type '<SetFilterMode-response>"
  (cl:format cl:nil "bool res~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetFilterMode-response)))
  "Returns full string definition for message of type 'SetFilterMode-response"
  (cl:format cl:nil "bool res~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetFilterMode-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetFilterMode-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetFilterMode-response
    (cl:cons ':res (res msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetFilterMode)))
  'SetFilterMode-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetFilterMode)))
  'SetFilterMode-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetFilterMode)))
  "Returns string type for a service object of type '<SetFilterMode>"
  "cartographer_ros_msgs/SetFilterMode")