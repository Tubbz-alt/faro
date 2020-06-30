<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: faro/proto/face_service.proto

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>DetectRequest</code>
 */
class DetectRequest extends \Google\Protobuf\Internal\Message
{
    /**
     * Generated from protobuf field <code>.Image image = 1;</code>
     */
    private $image = null;
    /**
     * Generated from protobuf field <code>string source = 2;</code>
     */
    private $source = '';
    /**
     * Generated from protobuf field <code>int64 frame = 3;</code>
     */
    private $frame = 0;
    /**
     * Generated from protobuf field <code>string subject_id = 4;</code>
     */
    private $subject_id = '';
    /**
     * Generated from protobuf field <code>string subject_name = 5;</code>
     */
    private $subject_name = '';
    /**
     * Generated from protobuf field <code>.DetectionOptions detect_options = 8;</code>
     */
    private $detect_options = null;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type \Image $image
     *     @type string $source
     *     @type int|string $frame
     *     @type string $subject_id
     *     @type string $subject_name
     *     @type \DetectionOptions $detect_options
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Faro\Proto\FaceService::initOnce();
        parent::__construct($data);
    }

    /**
     * Generated from protobuf field <code>.Image image = 1;</code>
     * @return \Image
     */
    public function getImage()
    {
        return $this->image;
    }

    /**
     * Generated from protobuf field <code>.Image image = 1;</code>
     * @param \Image $var
     * @return $this
     */
    public function setImage($var)
    {
        GPBUtil::checkMessage($var, \Image::class);
        $this->image = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string source = 2;</code>
     * @return string
     */
    public function getSource()
    {
        return $this->source;
    }

    /**
     * Generated from protobuf field <code>string source = 2;</code>
     * @param string $var
     * @return $this
     */
    public function setSource($var)
    {
        GPBUtil::checkString($var, True);
        $this->source = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>int64 frame = 3;</code>
     * @return int|string
     */
    public function getFrame()
    {
        return $this->frame;
    }

    /**
     * Generated from protobuf field <code>int64 frame = 3;</code>
     * @param int|string $var
     * @return $this
     */
    public function setFrame($var)
    {
        GPBUtil::checkInt64($var);
        $this->frame = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string subject_id = 4;</code>
     * @return string
     */
    public function getSubjectId()
    {
        return $this->subject_id;
    }

    /**
     * Generated from protobuf field <code>string subject_id = 4;</code>
     * @param string $var
     * @return $this
     */
    public function setSubjectId($var)
    {
        GPBUtil::checkString($var, True);
        $this->subject_id = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string subject_name = 5;</code>
     * @return string
     */
    public function getSubjectName()
    {
        return $this->subject_name;
    }

    /**
     * Generated from protobuf field <code>string subject_name = 5;</code>
     * @param string $var
     * @return $this
     */
    public function setSubjectName($var)
    {
        GPBUtil::checkString($var, True);
        $this->subject_name = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>.DetectionOptions detect_options = 8;</code>
     * @return \DetectionOptions
     */
    public function getDetectOptions()
    {
        return $this->detect_options;
    }

    /**
     * Generated from protobuf field <code>.DetectionOptions detect_options = 8;</code>
     * @param \DetectionOptions $var
     * @return $this
     */
    public function setDetectOptions($var)
    {
        GPBUtil::checkMessage($var, \DetectionOptions::class);
        $this->detect_options = $var;

        return $this;
    }

}
