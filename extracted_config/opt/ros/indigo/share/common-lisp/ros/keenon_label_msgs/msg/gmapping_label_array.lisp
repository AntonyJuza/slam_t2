; Auto-generated. Do not edit!


(cl:in-package keenon_label_msgs-msg)


;//! \htmlinclude gmapping_label_array.msg.html

(cl:defclass <gmapping_label_array> (roslisp-msg-protocol:ros-message)
  ((label
    :reader label
    :initarg :label
    :type (cl:vector keenon_label_msgs-msg:gmapping_label)
   :initform (cl:make-array 0 :element-type 'keenon_label_msgs-msg:gmapping_label :initial-element (cl:make-instance 'keenon_label_msgs-msg:gmapping_label)))
   (show
    :reader show
    :initarg :show
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass gmapping_label_array (<gmapping_label_array>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <gmapping_label_array>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'gmapping_label_array)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name keenon_label_msgs-msg:<gmapping_label_array> is deprecated: use keenon_label_msgs-msg:gmapping_label_array instead.")))

(cl:ensure-generic-function 'label-val :lambda-list '(m))
(cl:defmethod label-val ((m <gmapping_label_array>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_label_msgs-msg:label-val is deprecated.  Use keenon_label_msgs-msg:label instead.")
  (label m))

(cl:ensure-generic-function 'show-val :lambda-list '(m))
(cl:defmethod show-val ((m <gmapping_label_array>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_label_msgs-msg:show-val is deprecated.  Use keenon_label_msgs-msg:show instead.")
  (show m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <gmapping_label_array>) ostream)
  "Serializes a message object of type '<gmapping_label_array>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'label))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'label))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'show) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <gmapping_label_array>) istream)
  "Deserializes a message object of type '<gmapping_label_array>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'label) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'label)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'keenon_label_msgs-msg:gmapping_label))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:setf (cl:slot-value msg 'show) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<gmapping_label_array>)))
  "Returns string type for a message object of type '<gmapping_label_array>"
  "keenon_label_msgs/gmapping_label_array")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'gmapping_label_array)))
  "Returns string type for a message object of type 'gmapping_label_array"
  "keenon_label_msgs/gmapping_label_array")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<gmapping_label_array>)))
  "Returns md5sum for a message object of type '<gmapping_label_array>"
  "b5fbe04a6b16bde66803610d7bbf55d6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'gmapping_label_array)))
  "Returns md5sum for a message object of type 'gmapping_label_array"
  "b5fbe04a6b16bde66803610d7bbf55d6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<gmapping_label_array>)))
  "Returns full string definition for message of type '<gmapping_label_array>"
  (cl:format cl:nil "keenon_label_msgs/gmapping_label[] label~%bool show~%================================================================================~%MSG: keenon_label_msgs/gmapping_label~%float64 x~%float64 y~%float64 z~%float64 yaw~%float64 roll~%float64 pitch~%int64 id~%int64 floor_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'gmapping_label_array)))
  "Returns full string definition for message of type 'gmapping_label_array"
  (cl:format cl:nil "keenon_label_msgs/gmapping_label[] label~%bool show~%================================================================================~%MSG: keenon_label_msgs/gmapping_label~%float64 x~%float64 y~%float64 z~%float64 yaw~%float64 roll~%float64 pitch~%int64 id~%int64 floor_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <gmapping_label_array>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'label) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <gmapping_label_array>))
  "Converts a ROS message object to a list"
  (cl:list 'gmapping_label_array
    (cl:cons ':label (label msg))
    (cl:cons ':show (show msg))
))
