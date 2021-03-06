// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.23.0
// 	protoc        v3.13.0
// source: network_api.proto

package base

import (
	context "context"
	proto "github.com/golang/protobuf/proto"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

// This is a compile-time assertion that a sufficiently up-to-date version
// of the legacy proto package is being used.
const _ = proto.ProtoPackageIsVersion4

type SubscriberConfig struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	ClientId *ClientId  `protobuf:"bytes,1,opt,name=clientId,proto3" json:"clientId,omitempty"`
	Signals  *SignalIds `protobuf:"bytes,2,opt,name=signals,proto3" json:"signals,omitempty"`
	OnChange bool       `protobuf:"varint,3,opt,name=onChange,proto3" json:"onChange,omitempty"`
}

func (x *SubscriberConfig) Reset() {
	*x = SubscriberConfig{}
	if protoimpl.UnsafeEnabled {
		mi := &file_network_api_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SubscriberConfig) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SubscriberConfig) ProtoMessage() {}

func (x *SubscriberConfig) ProtoReflect() protoreflect.Message {
	mi := &file_network_api_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SubscriberConfig.ProtoReflect.Descriptor instead.
func (*SubscriberConfig) Descriptor() ([]byte, []int) {
	return file_network_api_proto_rawDescGZIP(), []int{0}
}

func (x *SubscriberConfig) GetClientId() *ClientId {
	if x != nil {
		return x.ClientId
	}
	return nil
}

func (x *SubscriberConfig) GetSignals() *SignalIds {
	if x != nil {
		return x.Signals
	}
	return nil
}

func (x *SubscriberConfig) GetOnChange() bool {
	if x != nil {
		return x.OnChange
	}
	return false
}

type SignalIds struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	SignalId []*SignalId `protobuf:"bytes,1,rep,name=signalId,proto3" json:"signalId,omitempty"`
}

func (x *SignalIds) Reset() {
	*x = SignalIds{}
	if protoimpl.UnsafeEnabled {
		mi := &file_network_api_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SignalIds) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SignalIds) ProtoMessage() {}

func (x *SignalIds) ProtoReflect() protoreflect.Message {
	mi := &file_network_api_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SignalIds.ProtoReflect.Descriptor instead.
func (*SignalIds) Descriptor() ([]byte, []int) {
	return file_network_api_proto_rawDescGZIP(), []int{1}
}

func (x *SignalIds) GetSignalId() []*SignalId {
	if x != nil {
		return x.SignalId
	}
	return nil
}

type Signals struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Signal []*Signal `protobuf:"bytes,1,rep,name=signal,proto3" json:"signal,omitempty"`
}

func (x *Signals) Reset() {
	*x = Signals{}
	if protoimpl.UnsafeEnabled {
		mi := &file_network_api_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Signals) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Signals) ProtoMessage() {}

func (x *Signals) ProtoReflect() protoreflect.Message {
	mi := &file_network_api_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Signals.ProtoReflect.Descriptor instead.
func (*Signals) Descriptor() ([]byte, []int) {
	return file_network_api_proto_rawDescGZIP(), []int{2}
}

func (x *Signals) GetSignal() []*Signal {
	if x != nil {
		return x.Signal
	}
	return nil
}

type PublisherConfig struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Signals   *Signals  `protobuf:"bytes,1,opt,name=signals,proto3" json:"signals,omitempty"`
	ClientId  *ClientId `protobuf:"bytes,2,opt,name=clientId,proto3" json:"clientId,omitempty"`
	Frequency int32     `protobuf:"varint,3,opt,name=frequency,proto3" json:"frequency,omitempty"`
}

func (x *PublisherConfig) Reset() {
	*x = PublisherConfig{}
	if protoimpl.UnsafeEnabled {
		mi := &file_network_api_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *PublisherConfig) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PublisherConfig) ProtoMessage() {}

func (x *PublisherConfig) ProtoReflect() protoreflect.Message {
	mi := &file_network_api_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PublisherConfig.ProtoReflect.Descriptor instead.
func (*PublisherConfig) Descriptor() ([]byte, []int) {
	return file_network_api_proto_rawDescGZIP(), []int{3}
}

func (x *PublisherConfig) GetSignals() *Signals {
	if x != nil {
		return x.Signals
	}
	return nil
}

func (x *PublisherConfig) GetClientId() *ClientId {
	if x != nil {
		return x.ClientId
	}
	return nil
}

func (x *PublisherConfig) GetFrequency() int32 {
	if x != nil {
		return x.Frequency
	}
	return 0
}

type Signal struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Id *SignalId `protobuf:"bytes,1,opt,name=id,proto3" json:"id,omitempty"`
	// Types that are assignable to Payload:
	//	*Signal_Integer
	//	*Signal_Double
	//	*Signal_Arbitration
	//	*Signal_Empty
	Payload   isSignal_Payload `protobuf_oneof:"payload"`
	Raw       []byte           `protobuf:"bytes,5,opt,name=raw,proto3" json:"raw,omitempty"`
	Timestamp int64            `protobuf:"varint,7,opt,name=timestamp,proto3" json:"timestamp,omitempty"`
}

func (x *Signal) Reset() {
	*x = Signal{}
	if protoimpl.UnsafeEnabled {
		mi := &file_network_api_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Signal) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Signal) ProtoMessage() {}

func (x *Signal) ProtoReflect() protoreflect.Message {
	mi := &file_network_api_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Signal.ProtoReflect.Descriptor instead.
func (*Signal) Descriptor() ([]byte, []int) {
	return file_network_api_proto_rawDescGZIP(), []int{4}
}

func (x *Signal) GetId() *SignalId {
	if x != nil {
		return x.Id
	}
	return nil
}

func (m *Signal) GetPayload() isSignal_Payload {
	if m != nil {
		return m.Payload
	}
	return nil
}

func (x *Signal) GetInteger() int64 {
	if x, ok := x.GetPayload().(*Signal_Integer); ok {
		return x.Integer
	}
	return 0
}

func (x *Signal) GetDouble() float64 {
	if x, ok := x.GetPayload().(*Signal_Double); ok {
		return x.Double
	}
	return 0
}

func (x *Signal) GetArbitration() bool {
	if x, ok := x.GetPayload().(*Signal_Arbitration); ok {
		return x.Arbitration
	}
	return false
}

func (x *Signal) GetEmpty() bool {
	if x, ok := x.GetPayload().(*Signal_Empty); ok {
		return x.Empty
	}
	return false
}

func (x *Signal) GetRaw() []byte {
	if x != nil {
		return x.Raw
	}
	return nil
}

func (x *Signal) GetTimestamp() int64 {
	if x != nil {
		return x.Timestamp
	}
	return 0
}

type isSignal_Payload interface {
	isSignal_Payload()
}

type Signal_Integer struct {
	Integer int64 `protobuf:"varint,2,opt,name=integer,proto3,oneof"`
}

type Signal_Double struct {
	Double float64 `protobuf:"fixed64,3,opt,name=double,proto3,oneof"`
}

type Signal_Arbitration struct {
	Arbitration bool `protobuf:"varint,4,opt,name=arbitration,proto3,oneof"`
}

type Signal_Empty struct {
	Empty bool `protobuf:"varint,6,opt,name=empty,proto3,oneof"`
}

func (*Signal_Integer) isSignal_Payload() {}

func (*Signal_Double) isSignal_Payload() {}

func (*Signal_Arbitration) isSignal_Payload() {}

func (*Signal_Empty) isSignal_Payload() {}

var File_network_api_proto protoreflect.FileDescriptor

var file_network_api_proto_rawDesc = []byte{
	0x0a, 0x11, 0x6e, 0x65, 0x74, 0x77, 0x6f, 0x72, 0x6b, 0x5f, 0x61, 0x70, 0x69, 0x2e, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x12, 0x04, 0x62, 0x61, 0x73, 0x65, 0x1a, 0x0c, 0x63, 0x6f, 0x6d, 0x6d, 0x6f,
	0x6e, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x85, 0x01, 0x0a, 0x10, 0x53, 0x75, 0x62, 0x73,
	0x63, 0x72, 0x69, 0x62, 0x65, 0x72, 0x43, 0x6f, 0x6e, 0x66, 0x69, 0x67, 0x12, 0x2a, 0x0a, 0x08,
	0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x49, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x0e,
	0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x43, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x49, 0x64, 0x52, 0x08,
	0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x49, 0x64, 0x12, 0x29, 0x0a, 0x07, 0x73, 0x69, 0x67, 0x6e,
	0x61, 0x6c, 0x73, 0x18, 0x02, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x0f, 0x2e, 0x62, 0x61, 0x73, 0x65,
	0x2e, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x49, 0x64, 0x73, 0x52, 0x07, 0x73, 0x69, 0x67, 0x6e,
	0x61, 0x6c, 0x73, 0x12, 0x1a, 0x0a, 0x08, 0x6f, 0x6e, 0x43, 0x68, 0x61, 0x6e, 0x67, 0x65, 0x18,
	0x03, 0x20, 0x01, 0x28, 0x08, 0x52, 0x08, 0x6f, 0x6e, 0x43, 0x68, 0x61, 0x6e, 0x67, 0x65, 0x22,
	0x37, 0x0a, 0x09, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x49, 0x64, 0x73, 0x12, 0x2a, 0x0a, 0x08,
	0x73, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x49, 0x64, 0x18, 0x01, 0x20, 0x03, 0x28, 0x0b, 0x32, 0x0e,
	0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x49, 0x64, 0x52, 0x08,
	0x73, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x49, 0x64, 0x22, 0x2f, 0x0a, 0x07, 0x53, 0x69, 0x67, 0x6e,
	0x61, 0x6c, 0x73, 0x12, 0x24, 0x0a, 0x06, 0x73, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x18, 0x01, 0x20,
	0x03, 0x28, 0x0b, 0x32, 0x0c, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53, 0x69, 0x67, 0x6e, 0x61,
	0x6c, 0x52, 0x06, 0x73, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x22, 0x84, 0x01, 0x0a, 0x0f, 0x50, 0x75,
	0x62, 0x6c, 0x69, 0x73, 0x68, 0x65, 0x72, 0x43, 0x6f, 0x6e, 0x66, 0x69, 0x67, 0x12, 0x27, 0x0a,
	0x07, 0x73, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x0d,
	0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x73, 0x52, 0x07, 0x73,
	0x69, 0x67, 0x6e, 0x61, 0x6c, 0x73, 0x12, 0x2a, 0x0a, 0x08, 0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74,
	0x49, 0x64, 0x18, 0x02, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x0e, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e,
	0x43, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x49, 0x64, 0x52, 0x08, 0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74,
	0x49, 0x64, 0x12, 0x1c, 0x0a, 0x09, 0x66, 0x72, 0x65, 0x71, 0x75, 0x65, 0x6e, 0x63, 0x79, 0x18,
	0x03, 0x20, 0x01, 0x28, 0x05, 0x52, 0x09, 0x66, 0x72, 0x65, 0x71, 0x75, 0x65, 0x6e, 0x63, 0x79,
	0x22, 0xd5, 0x01, 0x0a, 0x06, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x12, 0x1e, 0x0a, 0x02, 0x69,
	0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x0e, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53,
	0x69, 0x67, 0x6e, 0x61, 0x6c, 0x49, 0x64, 0x52, 0x02, 0x69, 0x64, 0x12, 0x1a, 0x0a, 0x07, 0x69,
	0x6e, 0x74, 0x65, 0x67, 0x65, 0x72, 0x18, 0x02, 0x20, 0x01, 0x28, 0x03, 0x48, 0x00, 0x52, 0x07,
	0x69, 0x6e, 0x74, 0x65, 0x67, 0x65, 0x72, 0x12, 0x18, 0x0a, 0x06, 0x64, 0x6f, 0x75, 0x62, 0x6c,
	0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x01, 0x48, 0x00, 0x52, 0x06, 0x64, 0x6f, 0x75, 0x62, 0x6c,
	0x65, 0x12, 0x22, 0x0a, 0x0b, 0x61, 0x72, 0x62, 0x69, 0x74, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e,
	0x18, 0x04, 0x20, 0x01, 0x28, 0x08, 0x48, 0x00, 0x52, 0x0b, 0x61, 0x72, 0x62, 0x69, 0x74, 0x72,
	0x61, 0x74, 0x69, 0x6f, 0x6e, 0x12, 0x16, 0x0a, 0x05, 0x65, 0x6d, 0x70, 0x74, 0x79, 0x18, 0x06,
	0x20, 0x01, 0x28, 0x08, 0x48, 0x00, 0x52, 0x05, 0x65, 0x6d, 0x70, 0x74, 0x79, 0x12, 0x10, 0x0a,
	0x03, 0x72, 0x61, 0x77, 0x18, 0x05, 0x20, 0x01, 0x28, 0x0c, 0x52, 0x03, 0x72, 0x61, 0x77, 0x12,
	0x1c, 0x0a, 0x09, 0x74, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x18, 0x07, 0x20, 0x01,
	0x28, 0x03, 0x52, 0x09, 0x74, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x42, 0x09, 0x0a,
	0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64, 0x32, 0xba, 0x01, 0x0a, 0x0e, 0x4e, 0x65, 0x74,
	0x77, 0x6f, 0x72, 0x6b, 0x53, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x12, 0x3f, 0x0a, 0x12, 0x53,
	0x75, 0x62, 0x73, 0x63, 0x72, 0x69, 0x62, 0x65, 0x54, 0x6f, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c,
	0x73, 0x12, 0x16, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53, 0x75, 0x62, 0x73, 0x63, 0x72, 0x69,
	0x62, 0x65, 0x72, 0x43, 0x6f, 0x6e, 0x66, 0x69, 0x67, 0x1a, 0x0d, 0x2e, 0x62, 0x61, 0x73, 0x65,
	0x2e, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x73, 0x22, 0x00, 0x30, 0x01, 0x12, 0x36, 0x0a, 0x0e,
	0x50, 0x75, 0x62, 0x6c, 0x69, 0x73, 0x68, 0x53, 0x69, 0x67, 0x6e, 0x61, 0x6c, 0x73, 0x12, 0x15,
	0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x50, 0x75, 0x62, 0x6c, 0x69, 0x73, 0x68, 0x65, 0x72, 0x43,
	0x6f, 0x6e, 0x66, 0x69, 0x67, 0x1a, 0x0b, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x45, 0x6d, 0x70,
	0x74, 0x79, 0x22, 0x00, 0x12, 0x2f, 0x0a, 0x0b, 0x52, 0x65, 0x61, 0x64, 0x53, 0x69, 0x67, 0x6e,
	0x61, 0x6c, 0x73, 0x12, 0x0f, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53, 0x69, 0x67, 0x6e, 0x61,
	0x6c, 0x49, 0x64, 0x73, 0x1a, 0x0d, 0x2e, 0x62, 0x61, 0x73, 0x65, 0x2e, 0x53, 0x69, 0x67, 0x6e,
	0x61, 0x6c, 0x73, 0x22, 0x00, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_network_api_proto_rawDescOnce sync.Once
	file_network_api_proto_rawDescData = file_network_api_proto_rawDesc
)

func file_network_api_proto_rawDescGZIP() []byte {
	file_network_api_proto_rawDescOnce.Do(func() {
		file_network_api_proto_rawDescData = protoimpl.X.CompressGZIP(file_network_api_proto_rawDescData)
	})
	return file_network_api_proto_rawDescData
}

var file_network_api_proto_msgTypes = make([]protoimpl.MessageInfo, 5)
var file_network_api_proto_goTypes = []interface{}{
	(*SubscriberConfig)(nil), // 0: base.SubscriberConfig
	(*SignalIds)(nil),        // 1: base.SignalIds
	(*Signals)(nil),          // 2: base.Signals
	(*PublisherConfig)(nil),  // 3: base.PublisherConfig
	(*Signal)(nil),           // 4: base.Signal
	(*ClientId)(nil),         // 5: base.ClientId
	(*SignalId)(nil),         // 6: base.SignalId
	(*Empty)(nil),            // 7: base.Empty
}
var file_network_api_proto_depIdxs = []int32{
	5,  // 0: base.SubscriberConfig.clientId:type_name -> base.ClientId
	1,  // 1: base.SubscriberConfig.signals:type_name -> base.SignalIds
	6,  // 2: base.SignalIds.signalId:type_name -> base.SignalId
	4,  // 3: base.Signals.signal:type_name -> base.Signal
	2,  // 4: base.PublisherConfig.signals:type_name -> base.Signals
	5,  // 5: base.PublisherConfig.clientId:type_name -> base.ClientId
	6,  // 6: base.Signal.id:type_name -> base.SignalId
	0,  // 7: base.NetworkService.SubscribeToSignals:input_type -> base.SubscriberConfig
	3,  // 8: base.NetworkService.PublishSignals:input_type -> base.PublisherConfig
	1,  // 9: base.NetworkService.ReadSignals:input_type -> base.SignalIds
	2,  // 10: base.NetworkService.SubscribeToSignals:output_type -> base.Signals
	7,  // 11: base.NetworkService.PublishSignals:output_type -> base.Empty
	2,  // 12: base.NetworkService.ReadSignals:output_type -> base.Signals
	10, // [10:13] is the sub-list for method output_type
	7,  // [7:10] is the sub-list for method input_type
	7,  // [7:7] is the sub-list for extension type_name
	7,  // [7:7] is the sub-list for extension extendee
	0,  // [0:7] is the sub-list for field type_name
}

func init() { file_network_api_proto_init() }
func file_network_api_proto_init() {
	if File_network_api_proto != nil {
		return
	}
	file_common_proto_init()
	if !protoimpl.UnsafeEnabled {
		file_network_api_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SubscriberConfig); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_network_api_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SignalIds); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_network_api_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Signals); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_network_api_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*PublisherConfig); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_network_api_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Signal); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	file_network_api_proto_msgTypes[4].OneofWrappers = []interface{}{
		(*Signal_Integer)(nil),
		(*Signal_Double)(nil),
		(*Signal_Arbitration)(nil),
		(*Signal_Empty)(nil),
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_network_api_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   5,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_network_api_proto_goTypes,
		DependencyIndexes: file_network_api_proto_depIdxs,
		MessageInfos:      file_network_api_proto_msgTypes,
	}.Build()
	File_network_api_proto = out.File
	file_network_api_proto_rawDesc = nil
	file_network_api_proto_goTypes = nil
	file_network_api_proto_depIdxs = nil
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConnInterface

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion6

// NetworkServiceClient is the client API for NetworkService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type NetworkServiceClient interface {
	SubscribeToSignals(ctx context.Context, in *SubscriberConfig, opts ...grpc.CallOption) (NetworkService_SubscribeToSignalsClient, error)
	PublishSignals(ctx context.Context, in *PublisherConfig, opts ...grpc.CallOption) (*Empty, error)
	ReadSignals(ctx context.Context, in *SignalIds, opts ...grpc.CallOption) (*Signals, error)
}

type networkServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewNetworkServiceClient(cc grpc.ClientConnInterface) NetworkServiceClient {
	return &networkServiceClient{cc}
}

func (c *networkServiceClient) SubscribeToSignals(ctx context.Context, in *SubscriberConfig, opts ...grpc.CallOption) (NetworkService_SubscribeToSignalsClient, error) {
	stream, err := c.cc.NewStream(ctx, &_NetworkService_serviceDesc.Streams[0], "/base.NetworkService/SubscribeToSignals", opts...)
	if err != nil {
		return nil, err
	}
	x := &networkServiceSubscribeToSignalsClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type NetworkService_SubscribeToSignalsClient interface {
	Recv() (*Signals, error)
	grpc.ClientStream
}

type networkServiceSubscribeToSignalsClient struct {
	grpc.ClientStream
}

func (x *networkServiceSubscribeToSignalsClient) Recv() (*Signals, error) {
	m := new(Signals)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *networkServiceClient) PublishSignals(ctx context.Context, in *PublisherConfig, opts ...grpc.CallOption) (*Empty, error) {
	out := new(Empty)
	err := c.cc.Invoke(ctx, "/base.NetworkService/PublishSignals", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *networkServiceClient) ReadSignals(ctx context.Context, in *SignalIds, opts ...grpc.CallOption) (*Signals, error) {
	out := new(Signals)
	err := c.cc.Invoke(ctx, "/base.NetworkService/ReadSignals", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// NetworkServiceServer is the server API for NetworkService service.
type NetworkServiceServer interface {
	SubscribeToSignals(*SubscriberConfig, NetworkService_SubscribeToSignalsServer) error
	PublishSignals(context.Context, *PublisherConfig) (*Empty, error)
	ReadSignals(context.Context, *SignalIds) (*Signals, error)
}

// UnimplementedNetworkServiceServer can be embedded to have forward compatible implementations.
type UnimplementedNetworkServiceServer struct {
}

func (*UnimplementedNetworkServiceServer) SubscribeToSignals(*SubscriberConfig, NetworkService_SubscribeToSignalsServer) error {
	return status.Errorf(codes.Unimplemented, "method SubscribeToSignals not implemented")
}
func (*UnimplementedNetworkServiceServer) PublishSignals(context.Context, *PublisherConfig) (*Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method PublishSignals not implemented")
}
func (*UnimplementedNetworkServiceServer) ReadSignals(context.Context, *SignalIds) (*Signals, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ReadSignals not implemented")
}

func RegisterNetworkServiceServer(s *grpc.Server, srv NetworkServiceServer) {
	s.RegisterService(&_NetworkService_serviceDesc, srv)
}

func _NetworkService_SubscribeToSignals_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(SubscriberConfig)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(NetworkServiceServer).SubscribeToSignals(m, &networkServiceSubscribeToSignalsServer{stream})
}

type NetworkService_SubscribeToSignalsServer interface {
	Send(*Signals) error
	grpc.ServerStream
}

type networkServiceSubscribeToSignalsServer struct {
	grpc.ServerStream
}

func (x *networkServiceSubscribeToSignalsServer) Send(m *Signals) error {
	return x.ServerStream.SendMsg(m)
}

func _NetworkService_PublishSignals_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PublisherConfig)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(NetworkServiceServer).PublishSignals(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/base.NetworkService/PublishSignals",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(NetworkServiceServer).PublishSignals(ctx, req.(*PublisherConfig))
	}
	return interceptor(ctx, in, info, handler)
}

func _NetworkService_ReadSignals_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SignalIds)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(NetworkServiceServer).ReadSignals(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/base.NetworkService/ReadSignals",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(NetworkServiceServer).ReadSignals(ctx, req.(*SignalIds))
	}
	return interceptor(ctx, in, info, handler)
}

var _NetworkService_serviceDesc = grpc.ServiceDesc{
	ServiceName: "base.NetworkService",
	HandlerType: (*NetworkServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "PublishSignals",
			Handler:    _NetworkService_PublishSignals_Handler,
		},
		{
			MethodName: "ReadSignals",
			Handler:    _NetworkService_ReadSignals_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "SubscribeToSignals",
			Handler:       _NetworkService_SubscribeToSignals_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "network_api.proto",
}
