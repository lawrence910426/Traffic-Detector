from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Parameter(_message.Message):
    __slots__ = ["A", "B", "Input_Video_Path", "Log_Path", "Output_Video_Path", "Stabilization_Period", "T", "Traffic_Mode", "X", "Y", "Z"]
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Detector_Line(_message.Message):
        __slots__ = ["x1", "x2", "y1", "y2"]
        X1_FIELD_NUMBER: _ClassVar[int]
        X2_FIELD_NUMBER: _ClassVar[int]
        Y1_FIELD_NUMBER: _ClassVar[int]
        Y2_FIELD_NUMBER: _ClassVar[int]
        x1: int
        x2: int
        y1: int
        y2: int
        def __init__(self, x1: _Optional[int] = ..., y1: _Optional[int] = ..., x2: _Optional[int] = ..., y2: _Optional[int] = ...) -> None: ...
    A: Parameter.Detector_Line
    A_FIELD_NUMBER: _ClassVar[int]
    B: Parameter.Detector_Line
    B_FIELD_NUMBER: _ClassVar[int]
    CROSS_INTERSECTION: Parameter.Mode
    INPUT_VIDEO_PATH_FIELD_NUMBER: _ClassVar[int]
    Input_Video_Path: str
    LOG_PATH_FIELD_NUMBER: _ClassVar[int]
    Log_Path: str
    OUTPUT_VIDEO_PATH_FIELD_NUMBER: _ClassVar[int]
    Output_Video_Path: str
    STABILIZATION_PERIOD_FIELD_NUMBER: _ClassVar[int]
    STRAIGHT: Parameter.Mode
    Stabilization_Period: int
    T: Parameter.Detector_Line
    TRAFFIC_MODE_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    T_INTERSECTION: Parameter.Mode
    Traffic_Mode: Parameter.Mode
    X: Parameter.Detector_Line
    X_FIELD_NUMBER: _ClassVar[int]
    Y: Parameter.Detector_Line
    Y_FIELD_NUMBER: _ClassVar[int]
    Z: Parameter.Detector_Line
    Z_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, Traffic_Mode: _Optional[_Union[Parameter.Mode, str]] = ..., X: _Optional[_Union[Parameter.Detector_Line, _Mapping]] = ..., Y: _Optional[_Union[Parameter.Detector_Line, _Mapping]] = ..., Z: _Optional[_Union[Parameter.Detector_Line, _Mapping]] = ..., T: _Optional[_Union[Parameter.Detector_Line, _Mapping]] = ..., A: _Optional[_Union[Parameter.Detector_Line, _Mapping]] = ..., B: _Optional[_Union[Parameter.Detector_Line, _Mapping]] = ..., Stabilization_Period: _Optional[int] = ..., Input_Video_Path: _Optional[str] = ..., Output_Video_Path: _Optional[str] = ..., Log_Path: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["JsonFlow", "Output_Video_Path", "Progress"]
    JSONFLOW_FIELD_NUMBER: _ClassVar[int]
    JsonFlow: str
    OUTPUT_VIDEO_PATH_FIELD_NUMBER: _ClassVar[int]
    Output_Video_Path: str
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    Progress: float
    def __init__(self, JsonFlow: _Optional[str] = ..., Progress: _Optional[float] = ..., Output_Video_Path: _Optional[str] = ...) -> None: ...
