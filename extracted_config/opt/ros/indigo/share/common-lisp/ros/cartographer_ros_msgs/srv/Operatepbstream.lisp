; Auto-generated. Do not edit!


(cl:in-package cartographer_ros_msgs-srv)


;//! \htmlinclude Operatepbstream-request.msg.html

(cl:defclass <Operatepbstream-request> (roslisp-msg-protocol:ros-message)
  ((option
    :reader option
    :initarg :option
    :type cl:string
    :initform "")
   (floor
    :reader floor
    :initarg :floor
    :type cl:fixnum
    :initform 0)
   (md5
    :reader md5
    :initarg :md5
    :type cl:string
    :initform "")
   (data
    :reader data
    :initarg :data
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass Operatepbstream-request (<Operatepbstream-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Operatepbstream-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Operatepbstream-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<Operatepbstream-request> is deprecated: use cartographer_ros_msgs-srv:Operatepbstream-request instead.")))

(cl:ensure-generic-function 'option-val :lambda-list '(m))
(cl:defmethod option-val ((m <Operatepbstream-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:option-val is deprecated.  Use cartographer_ros_msgs-srv:option instead.")
  (option m))

(cl:ensure-generic-function 'floor-val :lambda-list '(m))
(cl:defmethod floor-val ((m <Operatepbstream-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:floor-val is deprecated.  Use cartographer_ros_msgs-srv:floor instead.")
  (floor m))

(cl:ensure-generic-function 'md5-val :lambda-list '(m))
(cl:defmethod md5-val ((m <Operatepbstream-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:md5-val is deprecated.  Use cartographer_ros_msgs-srv:md5 instead.")
  (md5 m))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <Operatepbstream-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:data-val is deprecated.  Use cartographer_ros_msgs-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Operatepbstream-request>) ostream)
  "Serializes a message object of type '<Operatepbstream-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'option))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'option))
  (cl:let* ((signed (cl:slot-value msg 'floor)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'md5))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'md5))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream))
   (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Operatepbstream-request>) istream)
  "Deserializes a message object of type '<Operatepbstream-request>"
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
      (cl:setf (cl:slot-value msg 'floor) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'md5) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'md5) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'data) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'data)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Operatepbstream-request>)))
  "Returns string type for a service object of type '<Operatepbstream-request>"
  "cartographer_ros_msgs/OperatepbstreamRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Operatepbstream-request)))
  "Returns string type for a service object of type 'Operatepbstream-request"
  "cartographer_ros_msgs/OperatepbstreamRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Operatepbstream-request>)))
  "Returns md5sum for a message object of type '<Operatepbstream-request>"
  "95103b6286636b56ab523be0c9f38932")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Operatepbstream-request)))
  "Returns md5sum for a message object of type 'Operatepbstream-request"
  "95103b6286636b56ab523be0c9f38932")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Operatepbstream-request>)))
  "Returns full string definition for message of type '<Operatepbstream-request>"
  (cl:format cl:nil "string option~%int8 floor~%string md5~%char[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Operatepbstream-request)))
  "Returns full string definition for message of type 'Operatepbstream-request"
  (cl:format cl:nil "string option~%int8 floor~%string md5~%char[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Operatepbstream-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'option))
     1
     4 (cl:length (cl:slot-value msg 'md5))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'data) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Operatepbstream-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Operatepbstream-request
    (cl:cons ':option (option msg))
    (cl:cons ':floor (floor msg))
    (cl:cons ':md5 (md5 msg))
    (cl:cons ':data (data msg))
))
;//! \htmlinclude Operatepbstream-response.msg.html

(cl:defclass <Operatepbstream-response> (roslisp-msg-protocol:ros-message)
  ((msg
    :reader msg
    :initarg :msg
    :type cl:string
    :initform "")
   (result
    :reader result
    :initarg :result
    :type cl:integer
    :initform 0)
   (data
    :reader data
    :initarg :data
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass Operatepbstream-response (<Operatepbstream-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Operatepbstream-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Operatepbstream-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name cartographer_ros_msgs-srv:<Operatepbstream-response> is deprecated: use cartographer_ros_msgs-srv:Operatepbstream-response instead.")))

(cl:ensure-generic-function 'msg-val :lambda-list '(m))
(cl:defmethod msg-val ((m <Operatepbstream-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:msg-val is deprecated.  Use cartographer_ros_msgs-srv:msg instead.")
  (msg m))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <Operatepbstream-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:result-val is deprecated.  Use cartographer_ros_msgs-srv:result instead.")
  (result m))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <Operatepbstream-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader cartographer_ros_msgs-srv:data-val is deprecated.  Use cartographer_ros_msgs-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Operatepbstream-response>) ostream)
  "Serializes a message object of type '<Operatepbstream-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'msg))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'msg))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'result)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'result)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'result)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'result)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream))
   (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Operatepbstream-response>) istream)
  "Deserializes a message object of type '<Operatepbstream-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'msg) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'msg) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'result)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'result)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'result)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'result)) (cl:read-byte istream))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'data) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'data)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Operatepbstream-response>)))
  "Returns string type for a service object of type '<Operatepbstream-response>"
  "cartographer_ros_msgs/OperatepbstreamResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Operatepbstream-response)))
  "Returns string type for a service object of type 'Operatepbstream-response"
  "cartographer_ros_msgs/OperatepbstreamResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Operatepbstream-response>)))
  "Returns md5sum for a message object of type '<Operatepbstream-response>"
  "95103b6286636b56ab523be0c9f38932")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Operatepbstream-response)))
  "Returns md5sum for a message object of type 'Operatepbstream-response"
  "95103b6286636b56ab523be0c9f38932")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Operatepbstream-response>)))
  "Returns full string definition for message of type '<Operatepbstream-response>"
  (cl:format cl:nil "string msg~%uint32 result~%char[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Operatepbstream-response)))
  "Returns full string definition for message of type 'Operatepbstream-response"
  (cl:format cl:nil "string msg~%uint32 result~%char[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Operatepbstream-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'msg))
     4
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'data) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Operatepbstream-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Operatepbstream-response
    (cl:cons ':msg (msg msg))
    (cl:cons ':result (result msg))
    (cl:cons ':data (data msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Operatepbstream)))
  'Operatepbstream-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Operatepbstream)))
  'Operatepbstream-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Operatepbstream)))
  "Returns string type for a service object of type '<Operatepbstream>"
  "cartographer_ros_msgs/Operatepbstream")