#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Empty {}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ClientId {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SignalId {
    #[prost(string, tag = "1")]
    pub name: ::prost::alloc::string::String,
    #[prost(message, optional, tag = "2")]
    pub namespace: ::core::option::Option<NameSpace>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SignalInfo {
    #[prost(message, optional, tag = "1")]
    pub id: ::core::option::Option<SignalId>,
    #[prost(message, optional, tag = "2")]
    pub meta_data: ::core::option::Option<MetaData>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MetaData {
    #[prost(string, tag = "4")]
    pub description: ::prost::alloc::string::String,
    #[prost(int32, tag = "5")]
    pub max: i32,
    #[prost(int32, tag = "6")]
    pub min: i32,
    #[prost(string, tag = "7")]
    pub unit: ::prost::alloc::string::String,
    #[prost(int32, tag = "8")]
    pub size: i32,
    #[prost(bool, tag = "9")]
    pub is_raw: bool,
    #[prost(double, tag = "10")]
    pub factor: f64,
    #[prost(double, tag = "11")]
    pub offset: f64,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct NameSpace {
    #[prost(string, tag = "1")]
    pub name: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct NetworkInfo {
    #[prost(message, optional, tag = "1")]
    pub namespace: ::core::option::Option<NameSpace>,
    #[prost(string, tag = "2")]
    pub r#type: ::prost::alloc::string::String,
    #[prost(string, tag = "3")]
    pub description: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FrameInfo {
    #[prost(message, optional, tag = "1")]
    pub signal_info: ::core::option::Option<SignalInfo>,
    #[prost(message, repeated, tag = "2")]
    pub child_info: ::prost::alloc::vec::Vec<SignalInfo>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Frames {
    #[prost(message, repeated, tag = "1")]
    pub frame: ::prost::alloc::vec::Vec<FrameInfo>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DiagnosticsRequest {
    #[prost(message, optional, tag = "1")]
    pub up_link: ::core::option::Option<SignalId>,
    #[prost(message, optional, tag = "2")]
    pub down_link: ::core::option::Option<SignalId>,
    #[prost(bytes = "vec", tag = "3")]
    pub service_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "4")]
    pub data_identifier: ::prost::alloc::vec::Vec<u8>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DiagnosticsResponse {
    #[prost(bytes = "vec", tag = "5")]
    pub raw: ::prost::alloc::vec::Vec<u8>,
}
#[doc = r" Generated client implementations."]
pub mod diagnostics_service_client {
    #![allow(unused_variables, dead_code, missing_docs, clippy::let_unit_value)]
    use tonic::codegen::*;
    #[derive(Debug, Clone)]
    pub struct DiagnosticsServiceClient<T> {
        inner: tonic::client::Grpc<T>,
    }
    impl DiagnosticsServiceClient<tonic::transport::Channel> {
        #[doc = r" Attempt to create a new client by connecting to a given endpoint."]
        pub async fn connect<D>(dst: D) -> Result<Self, tonic::transport::Error>
        where
            D: std::convert::TryInto<tonic::transport::Endpoint>,
            D::Error: Into<StdError>,
        {
            let conn = tonic::transport::Endpoint::new(dst)?.connect().await?;
            Ok(Self::new(conn))
        }
    }
    impl<T> DiagnosticsServiceClient<T>
    where
        T: tonic::client::GrpcService<tonic::body::BoxBody>,
        T::ResponseBody: Body + Send + 'static,
        T::Error: Into<StdError>,
        <T::ResponseBody as Body>::Error: Into<StdError> + Send,
    {
        pub fn new(inner: T) -> Self {
            let inner = tonic::client::Grpc::new(inner);
            Self { inner }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> DiagnosticsServiceClient<InterceptedService<T, F>>
        where
            F: tonic::service::Interceptor,
            T: tonic::codegen::Service<
                http::Request<tonic::body::BoxBody>,
                Response = http::Response<
                    <T as tonic::client::GrpcService<tonic::body::BoxBody>>::ResponseBody,
                >,
            >,
            <T as tonic::codegen::Service<http::Request<tonic::body::BoxBody>>>::Error:
                Into<StdError> + Send + Sync,
        {
            DiagnosticsServiceClient::new(InterceptedService::new(inner, interceptor))
        }
        #[doc = r" Compress requests with `gzip`."]
        #[doc = r""]
        #[doc = r" This requires the server to support it otherwise it might respond with an"]
        #[doc = r" error."]
        pub fn send_gzip(mut self) -> Self {
            self.inner = self.inner.send_gzip();
            self
        }
        #[doc = r" Enable decompressing responses with `gzip`."]
        pub fn accept_gzip(mut self) -> Self {
            self.inner = self.inner.accept_gzip();
            self
        }
        pub async fn send_diagnostics_query(
            &mut self,
            request: impl tonic::IntoRequest<super::DiagnosticsRequest>,
        ) -> Result<tonic::Response<super::DiagnosticsResponse>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static(
                "/base.DiagnosticsService/SendDiagnosticsQuery",
            );
            self.inner.unary(request.into_request(), path, codec).await
        }
    }
}
/// to stop hammering make same call with frequency 0
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SenderInfo {
    #[prost(message, optional, tag = "1")]
    pub client_id: ::core::option::Option<ClientId>,
    #[prost(message, optional, tag = "2")]
    pub value: ::core::option::Option<Value>,
    #[prost(int32, tag = "3")]
    pub frequency: i32,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SubscriberRequest {
    #[prost(message, optional, tag = "1")]
    pub client_id: ::core::option::Option<ClientId>,
    #[prost(bool, tag = "2")]
    pub on_change: bool,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Value {
    #[prost(int32, tag = "1")]
    pub payload: i32,
}
#[doc = r" Generated client implementations."]
pub mod functional_service_client {
    #![allow(unused_variables, dead_code, missing_docs, clippy::let_unit_value)]
    use tonic::codegen::*;
    #[derive(Debug, Clone)]
    pub struct FunctionalServiceClient<T> {
        inner: tonic::client::Grpc<T>,
    }
    impl FunctionalServiceClient<tonic::transport::Channel> {
        #[doc = r" Attempt to create a new client by connecting to a given endpoint."]
        pub async fn connect<D>(dst: D) -> Result<Self, tonic::transport::Error>
        where
            D: std::convert::TryInto<tonic::transport::Endpoint>,
            D::Error: Into<StdError>,
        {
            let conn = tonic::transport::Endpoint::new(dst)?.connect().await?;
            Ok(Self::new(conn))
        }
    }
    impl<T> FunctionalServiceClient<T>
    where
        T: tonic::client::GrpcService<tonic::body::BoxBody>,
        T::ResponseBody: Body + Send + 'static,
        T::Error: Into<StdError>,
        <T::ResponseBody as Body>::Error: Into<StdError> + Send,
    {
        pub fn new(inner: T) -> Self {
            let inner = tonic::client::Grpc::new(inner);
            Self { inner }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> FunctionalServiceClient<InterceptedService<T, F>>
        where
            F: tonic::service::Interceptor,
            T: tonic::codegen::Service<
                http::Request<tonic::body::BoxBody>,
                Response = http::Response<
                    <T as tonic::client::GrpcService<tonic::body::BoxBody>>::ResponseBody,
                >,
            >,
            <T as tonic::codegen::Service<http::Request<tonic::body::BoxBody>>>::Error:
                Into<StdError> + Send + Sync,
        {
            FunctionalServiceClient::new(InterceptedService::new(inner, interceptor))
        }
        #[doc = r" Compress requests with `gzip`."]
        #[doc = r""]
        #[doc = r" This requires the server to support it otherwise it might respond with an"]
        #[doc = r" error."]
        pub fn send_gzip(mut self) -> Self {
            self.inner = self.inner.send_gzip();
            self
        }
        #[doc = r" Enable decompressing responses with `gzip`."]
        pub fn accept_gzip(mut self) -> Self {
            self.inner = self.inner.accept_gzip();
            self
        }
        pub async fn open_pass_window(
            &mut self,
            request: impl tonic::IntoRequest<super::ClientId>,
        ) -> Result<tonic::Response<super::Empty>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path =
                http::uri::PathAndQuery::from_static("/base.FunctionalService/OpenPassWindow");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn close_pass_window(
            &mut self,
            request: impl tonic::IntoRequest<super::ClientId>,
        ) -> Result<tonic::Response<super::Empty>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path =
                http::uri::PathAndQuery::from_static("/base.FunctionalService/ClosePassWindow");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn set_fan_speed(
            &mut self,
            request: impl tonic::IntoRequest<super::SenderInfo>,
        ) -> Result<tonic::Response<super::Empty>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.FunctionalService/SetFanSpeed");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn subscribe_to_fan_speed(
            &mut self,
            request: impl tonic::IntoRequest<super::SubscriberRequest>,
        ) -> Result<tonic::Response<tonic::codec::Streaming<super::Value>>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path =
                http::uri::PathAndQuery::from_static("/base.FunctionalService/SubscribeToFanSpeed");
            self.inner
                .server_streaming(request.into_request(), path, codec)
                .await
        }
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SubscriberConfig {
    #[prost(message, optional, tag = "1")]
    pub client_id: ::core::option::Option<ClientId>,
    #[prost(message, optional, tag = "2")]
    pub signals: ::core::option::Option<SignalIds>,
    #[prost(bool, tag = "3")]
    pub on_change: bool,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SignalIds {
    #[prost(message, repeated, tag = "1")]
    pub signal_id: ::prost::alloc::vec::Vec<SignalId>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Signals {
    #[prost(message, repeated, tag = "1")]
    pub signal: ::prost::alloc::vec::Vec<Signal>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublisherConfig {
    #[prost(message, optional, tag = "1")]
    pub signals: ::core::option::Option<Signals>,
    #[prost(message, optional, tag = "2")]
    pub client_id: ::core::option::Option<ClientId>,
    #[prost(int32, tag = "3")]
    pub frequency: i32,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Signal {
    #[prost(message, optional, tag = "1")]
    pub id: ::core::option::Option<SignalId>,
    #[prost(bytes = "vec", tag = "5")]
    pub raw: ::prost::alloc::vec::Vec<u8>,
    #[prost(int64, tag = "7")]
    pub timestamp: i64,
    #[prost(oneof = "signal::Payload", tags = "2, 3, 4, 6")]
    pub payload: ::core::option::Option<signal::Payload>,
}
/// Nested message and enum types in `Signal`.
pub mod signal {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Payload {
        #[prost(int64, tag = "2")]
        Integer(i64),
        #[prost(double, tag = "3")]
        Double(f64),
        #[prost(bool, tag = "4")]
        Arbitration(bool),
        #[prost(bool, tag = "6")]
        Empty(bool),
    }
}
#[doc = r" Generated client implementations."]
pub mod network_service_client {
    #![allow(unused_variables, dead_code, missing_docs, clippy::let_unit_value)]
    use tonic::codegen::*;
    #[derive(Debug, Clone)]
    pub struct NetworkServiceClient<T> {
        inner: tonic::client::Grpc<T>,
    }
    impl NetworkServiceClient<tonic::transport::Channel> {
        #[doc = r" Attempt to create a new client by connecting to a given endpoint."]
        pub async fn connect<D>(dst: D) -> Result<Self, tonic::transport::Error>
        where
            D: std::convert::TryInto<tonic::transport::Endpoint>,
            D::Error: Into<StdError>,
        {
            let conn = tonic::transport::Endpoint::new(dst)?.connect().await?;
            Ok(Self::new(conn))
        }
    }
    impl<T> NetworkServiceClient<T>
    where
        T: tonic::client::GrpcService<tonic::body::BoxBody>,
        T::ResponseBody: Body + Send + 'static,
        T::Error: Into<StdError>,
        <T::ResponseBody as Body>::Error: Into<StdError> + Send,
    {
        pub fn new(inner: T) -> Self {
            let inner = tonic::client::Grpc::new(inner);
            Self { inner }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> NetworkServiceClient<InterceptedService<T, F>>
        where
            F: tonic::service::Interceptor,
            T: tonic::codegen::Service<
                http::Request<tonic::body::BoxBody>,
                Response = http::Response<
                    <T as tonic::client::GrpcService<tonic::body::BoxBody>>::ResponseBody,
                >,
            >,
            <T as tonic::codegen::Service<http::Request<tonic::body::BoxBody>>>::Error:
                Into<StdError> + Send + Sync,
        {
            NetworkServiceClient::new(InterceptedService::new(inner, interceptor))
        }
        #[doc = r" Compress requests with `gzip`."]
        #[doc = r""]
        #[doc = r" This requires the server to support it otherwise it might respond with an"]
        #[doc = r" error."]
        pub fn send_gzip(mut self) -> Self {
            self.inner = self.inner.send_gzip();
            self
        }
        #[doc = r" Enable decompressing responses with `gzip`."]
        pub fn accept_gzip(mut self) -> Self {
            self.inner = self.inner.accept_gzip();
            self
        }
        pub async fn subscribe_to_signals(
            &mut self,
            request: impl tonic::IntoRequest<super::SubscriberConfig>,
        ) -> Result<tonic::Response<tonic::codec::Streaming<super::Signals>>, tonic::Status>
        {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path =
                http::uri::PathAndQuery::from_static("/base.NetworkService/SubscribeToSignals");
            self.inner
                .server_streaming(request.into_request(), path, codec)
                .await
        }
        pub async fn publish_signals(
            &mut self,
            request: impl tonic::IntoRequest<super::PublisherConfig>,
        ) -> Result<tonic::Response<super::Empty>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.NetworkService/PublishSignals");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn read_signals(
            &mut self,
            request: impl tonic::IntoRequest<super::SignalIds>,
        ) -> Result<tonic::Response<super::Signals>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.NetworkService/ReadSignals");
            self.inner.unary(request.into_request(), path, codec).await
        }
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Configuration {
    #[prost(message, repeated, tag = "1")]
    pub network_info: ::prost::alloc::vec::Vec<NetworkInfo>,
    #[prost(bytes = "vec", tag = "2")]
    pub interfaces_json: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, tag = "4")]
    pub public_address: ::prost::alloc::string::String,
    #[prost(string, tag = "5")]
    pub server_version: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ReloadMessage {
    #[prost(oneof = "reload_message::Status", tags = "1, 2")]
    pub status: ::core::option::Option<reload_message::Status>,
}
/// Nested message and enum types in `ReloadMessage`.
pub mod reload_message {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Status {
        #[prost(message, tag = "1")]
        Configuration(super::Configuration),
        #[prost(string, tag = "2")]
        ErrorMessage(::prost::alloc::string::String),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FileDescription {
    ///  sha256 is base16 encoded and not relevant when downloading
    #[prost(string, tag = "1")]
    pub sha256: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub path: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FileUploadRequest {
    #[prost(oneof = "file_upload_request::Data", tags = "1, 2")]
    pub data: ::core::option::Option<file_upload_request::Data>,
}
/// Nested message and enum types in `FileUploadRequest`.
pub mod file_upload_request {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Data {
        #[prost(message, tag = "1")]
        FileDescription(super::FileDescription),
        #[prost(bytes, tag = "2")]
        Chunk(::prost::alloc::vec::Vec<u8>),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FileUploadChunkRequest {
    #[prost(message, optional, tag = "1")]
    pub file_description: ::core::option::Option<FileDescription>,
    #[prost(uint32, tag = "2")]
    pub chunks: u32,
    #[prost(uint32, tag = "3")]
    pub chunk_id: u32,
    #[prost(bytes = "vec", tag = "4")]
    pub chunk: ::prost::alloc::vec::Vec<u8>,
    #[prost(bool, tag = "5")]
    pub cancel_upload: bool,
    #[prost(uint32, tag = "6")]
    pub upload_timeout: u32,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FileUploadResponse {
    #[prost(oneof = "file_upload_response::Data", tags = "1, 2, 3")]
    pub data: ::core::option::Option<file_upload_response::Data>,
}
/// Nested message and enum types in `FileUploadResponse`.
pub mod file_upload_response {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Data {
        #[prost(bool, tag = "1")]
        Finished(bool),
        #[prost(bool, tag = "2")]
        Cancelled(bool),
        #[prost(string, tag = "3")]
        ErrorMessage(::prost::alloc::string::String),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FileDownloadResponse {
    #[prost(oneof = "file_download_response::Data", tags = "1, 2")]
    pub data: ::core::option::Option<file_download_response::Data>,
}
/// Nested message and enum types in `FileDownloadResponse`.
pub mod file_download_response {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Data {
        #[prost(bytes, tag = "1")]
        Chunk(::prost::alloc::vec::Vec<u8>),
        #[prost(string, tag = "2")]
        ErrorMessage(::prost::alloc::string::String),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct LicenseInfo {
    #[prost(enumeration = "LicenseStatus", tag = "1")]
    pub status: i32,
    /// verbatim json from the license data (if base64-decodable)
    #[prost(bytes = "vec", tag = "2")]
    pub json: ::prost::alloc::vec::Vec<u8>,
    /// extracted from json for convenience
    #[prost(string, tag = "3")]
    pub expires: ::prost::alloc::string::String,
    /// info to use when requesting a new license
    #[prost(string, tag = "4")]
    pub request_id: ::prost::alloc::string::String,
    #[prost(bytes = "vec", tag = "5")]
    pub request_machine_id: ::prost::alloc::vec::Vec<u8>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct License {
    #[prost(bytes = "vec", tag = "1")]
    pub data: ::prost::alloc::vec::Vec<u8>,
    #[prost(bool, tag = "2")]
    pub terms_agreement: bool,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum LicenseStatus {
    Unset = 0,
    Valid = 1,
    Expired = 2,
    Baddate = 3,
    Wrongmachine = 4,
    Incompletejson = 5,
    Invalidjson = 6,
    Badsignature = 7,
    Malformed = 8,
    Servererror = 9,
    Notermsagreement = 10,
}
#[doc = r" Generated client implementations."]
pub mod system_service_client {
    #![allow(unused_variables, dead_code, missing_docs, clippy::let_unit_value)]
    use tonic::codegen::*;
    #[derive(Debug, Clone)]
    pub struct SystemServiceClient<T> {
        inner: tonic::client::Grpc<T>,
    }
    impl SystemServiceClient<tonic::transport::Channel> {
        #[doc = r" Attempt to create a new client by connecting to a given endpoint."]
        pub async fn connect<D>(dst: D) -> Result<Self, tonic::transport::Error>
        where
            D: std::convert::TryInto<tonic::transport::Endpoint>,
            D::Error: Into<StdError>,
        {
            let conn = tonic::transport::Endpoint::new(dst)?.connect().await?;
            Ok(Self::new(conn))
        }
    }
    impl<T> SystemServiceClient<T>
    where
        T: tonic::client::GrpcService<tonic::body::BoxBody>,
        T::ResponseBody: Body + Send + 'static,
        T::Error: Into<StdError>,
        <T::ResponseBody as Body>::Error: Into<StdError> + Send,
    {
        pub fn new(inner: T) -> Self {
            let inner = tonic::client::Grpc::new(inner);
            Self { inner }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> SystemServiceClient<InterceptedService<T, F>>
        where
            F: tonic::service::Interceptor,
            T: tonic::codegen::Service<
                http::Request<tonic::body::BoxBody>,
                Response = http::Response<
                    <T as tonic::client::GrpcService<tonic::body::BoxBody>>::ResponseBody,
                >,
            >,
            <T as tonic::codegen::Service<http::Request<tonic::body::BoxBody>>>::Error:
                Into<StdError> + Send + Sync,
        {
            SystemServiceClient::new(InterceptedService::new(inner, interceptor))
        }
        #[doc = r" Compress requests with `gzip`."]
        #[doc = r""]
        #[doc = r" This requires the server to support it otherwise it might respond with an"]
        #[doc = r" error."]
        pub fn send_gzip(mut self) -> Self {
            self.inner = self.inner.send_gzip();
            self
        }
        #[doc = r" Enable decompressing responses with `gzip`."]
        pub fn accept_gzip(mut self) -> Self {
            self.inner = self.inner.accept_gzip();
            self
        }
        pub async fn get_configuration(
            &mut self,
            request: impl tonic::IntoRequest<super::Empty>,
        ) -> Result<tonic::Response<super::Configuration>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/GetConfiguration");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn list_signals(
            &mut self,
            request: impl tonic::IntoRequest<super::NameSpace>,
        ) -> Result<tonic::Response<super::Frames>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/ListSignals");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn upload_file_chunk(
            &mut self,
            request: impl tonic::IntoRequest<super::FileUploadChunkRequest>,
        ) -> Result<tonic::Response<super::FileUploadResponse>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/UploadFileChunk");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn upload_file(
            &mut self,
            request: impl tonic::IntoStreamingRequest<Message = super::FileUploadRequest>,
        ) -> Result<tonic::Response<super::FileUploadResponse>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/UploadFile");
            self.inner
                .client_streaming(request.into_streaming_request(), path, codec)
                .await
        }
        pub async fn download_file(
            &mut self,
            request: impl tonic::IntoRequest<super::FileDescription>,
        ) -> Result<
            tonic::Response<tonic::codec::Streaming<super::FileDownloadResponse>>,
            tonic::Status,
        > {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/DownloadFile");
            self.inner
                .server_streaming(request.into_request(), path, codec)
                .await
        }
        #[doc = " will not return until new configuration is tested an active, make sure to set timeout to a large value. (fibex on pi > 50s)"]
        pub async fn reload_configuration(
            &mut self,
            request: impl tonic::IntoRequest<super::Empty>,
        ) -> Result<tonic::Response<super::ReloadMessage>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path =
                http::uri::PathAndQuery::from_static("/base.SystemService/ReloadConfiguration");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn get_license_info(
            &mut self,
            request: impl tonic::IntoRequest<super::Empty>,
        ) -> Result<tonic::Response<super::LicenseInfo>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/GetLicenseInfo");
            self.inner.unary(request.into_request(), path, codec).await
        }
        pub async fn set_license(
            &mut self,
            request: impl tonic::IntoRequest<super::License>,
        ) -> Result<tonic::Response<super::LicenseInfo>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.SystemService/SetLicense");
            self.inner.unary(request.into_request(), path, codec).await
        }
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PlaybackMode {
    #[prost(oneof = "playback_mode::Status", tags = "2, 3, 4")]
    pub status: ::core::option::Option<playback_mode::Status>,
}
/// Nested message and enum types in `PlaybackMode`.
pub mod playback_mode {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Status {
        #[prost(string, tag = "2")]
        ErrorMessage(::prost::alloc::string::String),
        #[prost(string, tag = "3")]
        Eof(::prost::alloc::string::String),
        #[prost(enumeration = "super::Mode", tag = "4")]
        Mode(i32),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PlaybackInfos {
    #[prost(message, repeated, tag = "1")]
    pub playback_info: ::prost::alloc::vec::Vec<PlaybackInfo>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PlaybackConfig {
    #[prost(message, optional, tag = "1")]
    pub file_description: ::core::option::Option<FileDescription>,
    #[prost(message, optional, tag = "2")]
    pub namespace: ::core::option::Option<NameSpace>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PlaybackInfo {
    #[prost(message, optional, tag = "1")]
    pub playback_config: ::core::option::Option<PlaybackConfig>,
    #[prost(message, optional, tag = "2")]
    pub playback_mode: ::core::option::Option<PlaybackMode>,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum Mode {
    Play = 0,
    Pause = 1,
    Stop = 2,
    Record = 3,
}
#[doc = r" Generated client implementations."]
pub mod traffic_service_client {
    #![allow(unused_variables, dead_code, missing_docs, clippy::let_unit_value)]
    use tonic::codegen::*;
    #[derive(Debug, Clone)]
    pub struct TrafficServiceClient<T> {
        inner: tonic::client::Grpc<T>,
    }
    impl TrafficServiceClient<tonic::transport::Channel> {
        #[doc = r" Attempt to create a new client by connecting to a given endpoint."]
        pub async fn connect<D>(dst: D) -> Result<Self, tonic::transport::Error>
        where
            D: std::convert::TryInto<tonic::transport::Endpoint>,
            D::Error: Into<StdError>,
        {
            let conn = tonic::transport::Endpoint::new(dst)?.connect().await?;
            Ok(Self::new(conn))
        }
    }
    impl<T> TrafficServiceClient<T>
    where
        T: tonic::client::GrpcService<tonic::body::BoxBody>,
        T::ResponseBody: Body + Send + 'static,
        T::Error: Into<StdError>,
        <T::ResponseBody as Body>::Error: Into<StdError> + Send,
    {
        pub fn new(inner: T) -> Self {
            let inner = tonic::client::Grpc::new(inner);
            Self { inner }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> TrafficServiceClient<InterceptedService<T, F>>
        where
            F: tonic::service::Interceptor,
            T: tonic::codegen::Service<
                http::Request<tonic::body::BoxBody>,
                Response = http::Response<
                    <T as tonic::client::GrpcService<tonic::body::BoxBody>>::ResponseBody,
                >,
            >,
            <T as tonic::codegen::Service<http::Request<tonic::body::BoxBody>>>::Error:
                Into<StdError> + Send + Sync,
        {
            TrafficServiceClient::new(InterceptedService::new(inner, interceptor))
        }
        #[doc = r" Compress requests with `gzip`."]
        #[doc = r""]
        #[doc = r" This requires the server to support it otherwise it might respond with an"]
        #[doc = r" error."]
        pub fn send_gzip(mut self) -> Self {
            self.inner = self.inner.send_gzip();
            self
        }
        #[doc = r" Enable decompressing responses with `gzip`."]
        pub fn accept_gzip(mut self) -> Self {
            self.inner = self.inner.accept_gzip();
            self
        }
        pub async fn play_traffic(
            &mut self,
            request: impl tonic::IntoRequest<super::PlaybackInfos>,
        ) -> Result<tonic::Response<super::PlaybackInfos>, tonic::Status> {
            self.inner.ready().await.map_err(|e| {
                tonic::Status::new(
                    tonic::Code::Unknown,
                    format!("Service was not ready: {}", e.into()),
                )
            })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static("/base.TrafficService/PlayTraffic");
            self.inner.unary(request.into_request(), path, codec).await
        }
    }
}
