; Auto-generated. Do not edit!


(cl:in-package keenon_vslam_msgs-srv)


;//! \htmlinclude VSLAMMapping-request.msg.html

(cl:defclass <VSLAMMapping-request> (roslisp-msg-protocol:ros-message)
  ((option
    :reader option
    :initarg :option
    :type cl:fixnum
    :initform 0))
)

(cl:defclass VSLAMMapping-request (<VSLAMMapping-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <VSLAMMapping-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'VSLAMMapping-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name keenon_vslam_msgs-srv:<VSLAMMapping-request> is deprecated: use keenon_vslam_msgs-srv:VSLAMMapping-request instead.")))

(cl:ensure-generic-function 'option-val :lambda-list '(m))
(cl:defmethod option-val ((m <VSLAMMapping-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:option-val is deprecated.  Use keenon_vslam_msgs-srv:option instead.")
  (option m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <VSLAMMapping-request>) ostream)
  "Serializes a message object of type '<VSLAMMapping-request>"
  (cl:let* ((signed (cl:slot-value msg 'option)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <VSLAMMapping-request>) istream)
  "Deserializes a message object of type '<VSLAMMapping-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'option) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<VSLAMMapping-request>)))
  "Returns string type for a service object of type '<VSLAMMapping-request>"
  "keenon_vslam_msgs/VSLAMMappingRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'VSLAMMapping-request)))
  "Returns string type for a service object of type 'VSLAMMapping-request"
  "keenon_vslam_msgs/VSLAMMappingRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<VSLAMMapping-request>)))
  "Returns md5sum for a message object of type '<VSLAMMapping-request>"
  "1bd103c1c478d6c9ac445349ec564625")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'VSLAMMapping-request)))
  "Returns md5sum for a message object of type 'VSLAMMapping-request"
  "1bd103c1c478d6c9ac445349ec564625")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<VSLAMMapping-request>)))
  "Returns full string definition for message of type '<VSLAMMapping-request>"
  (cl:format cl:nil "~%~%int16 option~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'VSLAMMapping-request)))
  "Returns full string definition for message of type 'VSLAMMapping-request"
  (cl:format cl:nil "~%~%int16 option~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <VSLAMMapping-request>))
  (cl:+ 0
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <VSLAMMapping-request>))
  "Converts a ROS message object to a list"
  (cl:list 'VSLAMMapping-request
    (cl:cons ':option (option msg))
))
;//! \htmlinclude VSLAMMapping-response.msg.html

(cl:defclass <VSLAMMapping-response> (roslisp-msg-protocol:ros-message)
  ((stamp
    :reader stamp
    :initarg :stamp
    :type cl:real
    :initform 0)
   (floor
    :reader floor
    :initarg :floor
    :type cl:fixnum
    :initform 0)
   (db_key_sn
    :reader db_key_sn
    :initarg :db_key_sn
    :type cl:string
    :initform "")
   (db_key_time
    :reader db_key_time
    :initarg :db_key_time
    :type cl:string
    :initform "")
   (db_key_sub_db_desc
    :reader db_key_sub_db_desc
    :initarg :db_key_sub_db_desc
    :type cl:string
    :initform "")
   (option_result
    :reader option_result
    :initarg :option_result
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass VSLAMMapping-response (<VSLAMMapping-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <VSLAMMapping-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'VSLAMMapping-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name keenon_vslam_msgs-srv:<VSLAMMapping-response> is deprecated: use keenon_vslam_msgs-srv:VSLAMMapping-response instead.")))

(cl:ensure-generic-function 'stamp-val :lambda-list '(m))
(cl:defmethod stamp-val ((m <VSLAMMapping-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:stamp-val is deprecated.  Use keenon_vslam_msgs-srv:stamp instead.")
  (stamp m))

(cl:ensure-generic-function 'floor-val :lambda-list '(m))
(cl:defmethod floor-val ((m <VSLAMMapping-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:floor-val is deprecated.  Use keenon_vslam_msgs-srv:floor instead.")
  (floor m))

(cl:ensure-generic-function 'db_key_sn-val :lambda-list '(m))
(cl:defmethod db_key_sn-val ((m <VSLAMMapping-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:db_key_sn-val is deprecated.  Use keenon_vslam_msgs-srv:db_key_sn instead.")
  (db_key_sn m))

(cl:ensure-generic-function 'db_key_time-val :lambda-list '(m))
(cl:defmethod db_key_time-val ((m <VSLAMMapping-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:db_key_time-val is deprecated.  Use keenon_vslam_msgs-srv:db_key_time instead.")
  (db_key_time m))

(cl:ensure-generic-function 'db_key_sub_db_desc-val :lambda-list '(m))
(cl:defmethod db_key_sub_db_desc-val ((m <VSLAMMapping-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:db_key_sub_db_desc-val is deprecated.  Use keenon_vslam_msgs-srv:db_key_sub_db_desc instead.")
  (db_key_sub_db_desc m))

(cl:ensure-generic-function 'option_result-val :lambda-list '(m))
(cl:defmethod option_result-val ((m <VSLAMMapping-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader keenon_vslam_msgs-srv:option_result-val is deprecated.  Use keenon_vslam_msgs-srv:option_result instead.")
  (option_result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <VSLAMMapping-response>) ostream)
  "Serializes a message object of type '<VSLAMMapping-response>"
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'stamp)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'stamp) (cl:floor (cl:slot-value msg 'stamp)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
  (cl:let* ((signed (cl:slot-value msg 'floor)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'db_key_sn))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'db_key_sn))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'db_key_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'db_key_time))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'db_key_sub_db_desc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'db_key_sub_db_desc))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'option_result) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <VSLAMMapping-response>) istream)
  "Deserializes a message object of type '<VSLAMMapping-response>"
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'stamp) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'floor) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'db_key_sn) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'db_key_sn) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'db_key_time) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'db_key_time) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'db_key_sub_db_desc) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'db_key_sub_db_desc) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:slot-value msg 'option_result) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<VSLAMMapping-response>)))
  "Returns string type for a service object of type '<VSLAMMapping-response>"
  "keenon_vslam_msgs/VSLAMMappingResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'VSLAMMapping-response)))
  "Returns string type for a service object of type 'VSLAMMapping-response"
  "keenon_vslam_msgs/VSLAMMappingResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<VSLAMMapping-response>)))
  "Returns md5sum for a message object of type '<VSLAMMapping-response>"
  "1bd103c1c478d6c9ac445349ec564625")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'VSLAMMapping-response)))
  "Returns md5sum for a message object of type 'VSLAMMapping-response"
  "1bd103c1c478d6c9ac445349ec564625")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<VSLAMMapping-response>)))
  "Returns full string definition for message of type '<VSLAMMapping-response>"
  (cl:format cl:nil "~%time stamp~%int16 floor~%string db_key_sn~%string db_key_time~%string db_key_sub_db_desc~%bool option_result~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'VSLAMMapping-response)))
  "Returns full string definition for message of type 'VSLAMMapping-response"
  (cl:format cl:nil "~%time stamp~%int16 floor~%string db_key_sn~%string db_key_time~%string db_key_sub_db_desc~%bool option_result~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <VSLAMMapping-response>))
  (cl:+ 0
     8
     2
     4 (cl:length (cl:slot-value msg 'db_key_sn))
     4 (cl:length (cl:slot-value msg 'db_key_time))
     4 (cl:length (cl:slot-value msg 'db_key_sub_db_desc))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <VSLAMMapping-response>))
  "Converts a ROS message object to a list"
  (cl:list 'VSLAMMapping-response
    (cl:cons ':stamp (stamp msg))
    (cl:cons ':floor (floor msg))
    (cl:cons ':db_key_sn (db_key_sn msg))
    (cl:cons ':db_key_time (db_key_time msg))
    (cl:cons ':db_key_sub_db_desc (db_key_sub_db_desc msg))
    (cl:cons ':option_result (option_result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'VSLAMMapping)))
  'VSLAMMapping-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'VSLAMMapping)))
  'VSLAMMapping-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'VSLAMMapping)))
  "Returns string type for a service object of type '<VSLAMMapping>"
  "keenon_vslam_msgs/VSLAMMapping")