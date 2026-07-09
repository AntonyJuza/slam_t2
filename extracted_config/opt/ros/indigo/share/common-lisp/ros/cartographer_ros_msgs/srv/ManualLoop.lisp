; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-srv)


;//! \htmlinclude ManualLoop-request.msg.html

(cl:defclass <ManualLoop-request> (roslisp-msg-protocol:ros-message)
  ((option
    :reader option
    :initarg :option
    :type cl:string
    :initform "")
   (trajectoryid
    :reader trajectoryid
    :initarg :trajectoryid
    :type cl:fixnum
    :initform 0)
   (signal
    :reader signal
    :initarg :signal
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass ManualLoop-request (<ManualLoop-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ManualLoop-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ManualLoop-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<ManualLoop-request> is deprecated: use cartographer_ros_msgs-srv:ManualLoop-request instead.")))

(cl:ensure-generic-function 'option-val :lambda-list '(m))
(cl:defmethod option-val ((m <ManualLoop-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:option-val is deprecated.  Use cartographer_ros_msgs-srv:option instead.")
  (option m))

(cl:ensure-generic-function 'trajectoryid-val :lambda-list '(m))
(cl:defmethod trajectoryid-val ((m <ManualLoop-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:trajectoryid-val is deprecated.  Use cartographer_ros_msgs-srv:trajectoryid instead.")
  (trajectoryid m))

(cl:ensure-generic-function 'signal-val :lambda-list '(m))
(cl:defmethod signal-val ((m <ManualLoop-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:signal-val is deprecated.  Use cartographer_ros_msgs-srv:signal instead.")
  (signal m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ManualLoop-request>) ostream)
  "Serializes a message object of type '<ManualLoop-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'option))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'option))
  (cl:let* ((signed (cl:slot-value msg 'trajectoryid)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'signal) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ManualLoop-request>) istream)
  "Deserializes a message object of type '<ManualLoop-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'option) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'option) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'trajectoryid) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:setf (cl:slot-value msg 'signal) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ManualLoop-request>)))
  "Returns string type for a service object of type '<ManualLoop-request>"
  "cartographer_ros_msgs/ManualLoopRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ManualLoop-request)))
  "Returns string type for a service object of type 'ManualLoop-request"
  "cartographer_ros_msgs/ManualLoopRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ManualLoop-request>)))
  "Returns md5sum for a message object of type '<ManualLoop-request>"
  "1c480aaf8297c71d4cb9e335eba91f51")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ManualLoop-request)))
  "Returns md5sum for a message object of type 'ManualLoop-request"
  "1c480aaf8297c71d4cb9e335eba91f51")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ManualLoop-request>)))
  "Returns full string definition for message of type '<ManualLoop-request>"
  (cl:format cl:nil "~%string option~%int8 trajectoryid~%bool signal~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ManualLoop-request)))
  "Returns full string definition for message of type 'ManualLoop-request"
  (cl:format cl:nil "~%string option~%int8 trajectoryid~%bool signal~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ManualLoop-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'option))
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ManualLoop-request>))
  "Converts a ROS message object to a list"
  (cl:list 'ManualLoop-request
    (cl:cons ':option (option msg))
    (cl:cons ':trajectoryid (trajectoryid msg))
    (cl:cons ':signal (signal msg))
))
;//! \htmlinclude ManualLoop-response.msg.html

(cl:defclass <ManualLoop-response> (roslisp-msg-protocol:ros-message)
  ((msg
    :reader msg
    :initarg :msg
    :type cl:string
    :initform "")
   (code
    :reader code
    :initarg :code
    :type cl:fixnum
    :initform 0))
)

(cl:defclass ManualLoop-response (<ManualLoop-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ManualLoop-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ManualLoop-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<ManualLoop-response> is deprecated: use cartographer_ros_msgs-srv:ManualLoop-response instead.")))

(cl:ensure-generic-function 'msg-val :lambda-list '(m))
(cl:defmethod msg-val ((m <ManualLoop-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:msg-val is deprecated.  Use cartographer_ros_msgs-srv:msg instead.")
  (msg m))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <ManualLoop-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:code-val is deprecated.  Use cartographer_ros_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ManualLoop-response>) ostream)
  "Serializes a message object of type '<ManualLoop-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'msg))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'msg))
  (cl:let* ((signed (cl:slot-value msg 'code)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ManualLoop-response>) istream)
  "Deserializes a message object of type '<ManualLoop-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'msg) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'msg) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'code) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ManualLoop-response>)))
  "Returns string type for a service object of type '<ManualLoop-response>"
  "cartographer_ros_msgs/ManualLoopResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ManualLoop-response)))
  "Returns string type for a service object of type 'ManualLoop-response"
  "cartographer_ros_msgs/ManualLoopResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ManualLoop-response>)))
  "Returns md5sum for a message object of type '<ManualLoop-response>"
  "1c480aaf8297c71d4cb9e335eba91f51")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ManualLoop-response)))
  "Returns md5sum for a message object of type 'ManualLoop-response"
  "1c480aaf8297c71d4cb9e335eba91f51")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ManualLoop-response>)))
  "Returns full string definition for message of type '<ManualLoop-response>"
  (cl:format cl:nil "string msg~%int8 code~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ManualLoop-response)))
  "Returns full string definition for message of type 'ManualLoop-response"
  (cl:format cl:nil "string msg~%int8 code~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ManualLoop-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'msg))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ManualLoop-response>))
  "Converts a ROS message object to a list"
  (cl:list 'ManualLoop-response
    (cl:cons ':msg (msg msg))
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'ManualLoop)))
  'ManualLoop-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'ManualLoop)))
  'ManualLoop-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ManualLoop)))
  "Returns string type for a service object of type '<ManualLoop>"
  "cartographer_ros_msgs/ManualLoop")