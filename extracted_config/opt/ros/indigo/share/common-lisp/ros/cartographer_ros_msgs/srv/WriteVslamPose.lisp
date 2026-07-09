; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-srv)


;//! \htmlinclude WriteVslamPose-request.msg.html

(cl:defclass <WriteVslamPose-request> (roslisp-msg-protocol:ros-message)
  ((filepath
    :reader filepath
    :initarg :filepath
    :type cl:string
    :initform ""))
)

(cl:defclass WriteVslamPose-request (<WriteVslamPose-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WriteVslamPose-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WriteVslamPose-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<WriteVslamPose-request> is deprecated: use cartographer_ros_msgs-srv:WriteVslamPose-request instead.")))

(cl:ensure-generic-function 'filepath-val :lambda-list '(m))
(cl:defmethod filepath-val ((m <WriteVslamPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:filepath-val is deprecated.  Use cartographer_ros_msgs-srv:filepath instead.")
  (filepath m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WriteVslamPose-request>) ostream)
  "Serializes a message object of type '<WriteVslamPose-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'filepath))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'filepath))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WriteVslamPose-request>) istream)
  "Deserializes a message object of type '<WriteVslamPose-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'filepath) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'filepath) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WriteVslamPose-request>)))
  "Returns string type for a service object of type '<WriteVslamPose-request>"
  "cartographer_ros_msgs/WriteVslamPoseRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WriteVslamPose-request)))
  "Returns string type for a service object of type 'WriteVslamPose-request"
  "cartographer_ros_msgs/WriteVslamPoseRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WriteVslamPose-request>)))
  "Returns md5sum for a message object of type '<WriteVslamPose-request>"
  "c4b744c4e970327c482e45a815076dee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WriteVslamPose-request)))
  "Returns md5sum for a message object of type 'WriteVslamPose-request"
  "c4b744c4e970327c482e45a815076dee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WriteVslamPose-request>)))
  "Returns full string definition for message of type '<WriteVslamPose-request>"
  (cl:format cl:nil "~%~%~%~%~%~%~%~%~%~%~%~%~%string filepath~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WriteVslamPose-request)))
  "Returns full string definition for message of type 'WriteVslamPose-request"
  (cl:format cl:nil "~%~%~%~%~%~%~%~%~%~%~%~%~%string filepath~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WriteVslamPose-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'filepath))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WriteVslamPose-request>))
  "Converts a ROS message object to a list"
  (cl:list 'WriteVslamPose-request
    (cl:cons ':filepath (filepath msg))
))
;//! \htmlinclude WriteVslamPose-response.msg.html

(cl:defclass <WriteVslamPose-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:boolean
    :initform cl:nil)
   (msg
    :reader msg
    :initarg :msg
    :type cl:string
    :initform ""))
)

(cl:defclass WriteVslamPose-response (<WriteVslamPose-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WriteVslamPose-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WriteVslamPose-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<WriteVslamPose-response> is deprecated: use cartographer_ros_msgs-srv:WriteVslamPose-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <WriteVslamPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:result-val is deprecated.  Use cartographer_ros_msgs-srv:result instead.")
  (result m))

(cl:ensure-generic-function 'msg-val :lambda-list '(m))
(cl:defmethod msg-val ((m <WriteVslamPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:msg-val is deprecated.  Use cartographer_ros_msgs-srv:msg instead.")
  (msg m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WriteVslamPose-response>) ostream)
  "Serializes a message object of type '<WriteVslamPose-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'msg))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'msg))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WriteVslamPose-response>) istream)
  "Deserializes a message object of type '<WriteVslamPose-response>"
    (cl:setf (cl:slot-value msg 'result) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'msg) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'msg) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WriteVslamPose-response>)))
  "Returns string type for a service object of type '<WriteVslamPose-response>"
  "cartographer_ros_msgs/WriteVslamPoseResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WriteVslamPose-response)))
  "Returns string type for a service object of type 'WriteVslamPose-response"
  "cartographer_ros_msgs/WriteVslamPoseResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WriteVslamPose-response>)))
  "Returns md5sum for a message object of type '<WriteVslamPose-response>"
  "c4b744c4e970327c482e45a815076dee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WriteVslamPose-response)))
  "Returns md5sum for a message object of type 'WriteVslamPose-response"
  "c4b744c4e970327c482e45a815076dee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WriteVslamPose-response>)))
  "Returns full string definition for message of type '<WriteVslamPose-response>"
  (cl:format cl:nil "bool result~%string msg~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WriteVslamPose-response)))
  "Returns full string definition for message of type 'WriteVslamPose-response"
  (cl:format cl:nil "bool result~%string msg~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WriteVslamPose-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'msg))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WriteVslamPose-response>))
  "Converts a ROS message object to a list"
  (cl:list 'WriteVslamPose-response
    (cl:cons ':result (result msg))
    (cl:cons ':msg (msg msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'WriteVslamPose)))
  'WriteVslamPose-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'WriteVslamPose)))
  'WriteVslamPose-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WriteVslamPose)))
  "Returns string type for a service object of type '<WriteVslamPose>"
  "cartographer_ros_msgs/WriteVslamPose")