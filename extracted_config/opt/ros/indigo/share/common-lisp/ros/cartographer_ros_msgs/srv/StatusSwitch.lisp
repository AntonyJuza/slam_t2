; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-srv)


;//! \htmlinclude StatusSwitch-request.msg.html

(cl:defclass <StatusSwitch-request> (roslisp-msg-protocol:ros-message)
  ((mode
    :reader mode
    :initarg :mode
    :type cl:integer
    :initform 0)
   (file_path
    :reader file_path
    :initarg :file_path
    :type cl:string
    :initform ""))
)

(cl:defclass StatusSwitch-request (<StatusSwitch-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StatusSwitch-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StatusSwitch-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<StatusSwitch-request> is deprecated: use cartographer_ros_msgs-srv:StatusSwitch-request instead.")))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <StatusSwitch-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:mode-val is deprecated.  Use cartographer_ros_msgs-srv:mode instead.")
  (mode m))

(cl:ensure-generic-function 'file_path-val :lambda-list '(m))
(cl:defmethod file_path-val ((m <StatusSwitch-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:file_path-val is deprecated.  Use cartographer_ros_msgs-srv:file_path instead.")
  (file_path m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StatusSwitch-request>) ostream)
  "Serializes a message object of type '<StatusSwitch-request>"
  (cl:let* ((signed (cl:slot-value msg 'mode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'file_path))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'file_path))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StatusSwitch-request>) istream)
  "Deserializes a message object of type '<StatusSwitch-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mode) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'file_path) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'file_path) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StatusSwitch-request>)))
  "Returns string type for a service object of type '<StatusSwitch-request>"
  "cartographer_ros_msgs/StatusSwitchRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StatusSwitch-request)))
  "Returns string type for a service object of type 'StatusSwitch-request"
  "cartographer_ros_msgs/StatusSwitchRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StatusSwitch-request>)))
  "Returns md5sum for a message object of type '<StatusSwitch-request>"
  "e91527c3b01a6f0efe28aadb6967cb6d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StatusSwitch-request)))
  "Returns md5sum for a message object of type 'StatusSwitch-request"
  "e91527c3b01a6f0efe28aadb6967cb6d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StatusSwitch-request>)))
  "Returns full string definition for message of type '<StatusSwitch-request>"
  (cl:format cl:nil "~%~%~%~%~%~%~%~%~%~%~%~%~%~%int32 mode~%string file_path~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StatusSwitch-request)))
  "Returns full string definition for message of type 'StatusSwitch-request"
  (cl:format cl:nil "~%~%~%~%~%~%~%~%~%~%~%~%~%~%int32 mode~%string file_path~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StatusSwitch-request>))
  (cl:+ 0
     4
     4 (cl:length (cl:slot-value msg 'file_path))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StatusSwitch-request>))
  "Converts a ROS message object to a list"
  (cl:list 'StatusSwitch-request
    (cl:cons ':mode (mode msg))
    (cl:cons ':file_path (file_path msg))
))
;//! \htmlinclude StatusSwitch-response.msg.html

(cl:defclass <StatusSwitch-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass StatusSwitch-response (<StatusSwitch-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StatusSwitch-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StatusSwitch-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<StatusSwitch-response> is deprecated: use cartographer_ros_msgs-srv:StatusSwitch-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <StatusSwitch-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:result-val is deprecated.  Use cartographer_ros_msgs-srv:result instead.")
  (result m))

(cl:ensure-generic-function 'msg-val :lambda-list '(m))
(cl:defmethod msg-val ((m <StatusSwitch-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:msg-val is deprecated.  Use cartographer_ros_msgs-srv:msg instead.")
  (msg m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StatusSwitch-response>) ostream)
  "Serializes a message object of type '<StatusSwitch-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'msg))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'msg))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StatusSwitch-response>) istream)
  "Deserializes a message object of type '<StatusSwitch-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StatusSwitch-response>)))
  "Returns string type for a service object of type '<StatusSwitch-response>"
  "cartographer_ros_msgs/StatusSwitchResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StatusSwitch-response)))
  "Returns string type for a service object of type 'StatusSwitch-response"
  "cartographer_ros_msgs/StatusSwitchResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StatusSwitch-response>)))
  "Returns md5sum for a message object of type '<StatusSwitch-response>"
  "e91527c3b01a6f0efe28aadb6967cb6d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StatusSwitch-response)))
  "Returns md5sum for a message object of type 'StatusSwitch-response"
  "e91527c3b01a6f0efe28aadb6967cb6d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StatusSwitch-response>)))
  "Returns full string definition for message of type '<StatusSwitch-response>"
  (cl:format cl:nil "bool result~%string msg~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StatusSwitch-response)))
  "Returns full string definition for message of type 'StatusSwitch-response"
  (cl:format cl:nil "bool result~%string msg~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StatusSwitch-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'msg))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StatusSwitch-response>))
  "Converts a ROS message object to a list"
  (cl:list 'StatusSwitch-response
    (cl:cons ':result (result msg))
    (cl:cons ':msg (msg msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'StatusSwitch)))
  'StatusSwitch-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'StatusSwitch)))
  'StatusSwitch-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StatusSwitch)))
  "Returns string type for a service object of type '<StatusSwitch>"
  "cartographer_ros_msgs/StatusSwitch")