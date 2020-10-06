/**
 * @fileoverview gRPC-Web generated client stub for base
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!


/* eslint-disable */
// @ts-nocheck



const grpc = {};
grpc.web = require('grpc-web');


var common_pb = require('./common_pb.js')
const proto = {};
proto.base = require('./system_api_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.base.SystemServiceClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.base.SystemServicePromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.Empty,
 *   !proto.base.Configuration>}
 */
const methodDescriptor_SystemService_GetConfiguration = new grpc.web.MethodDescriptor(
  '/base.SystemService/GetConfiguration',
  grpc.web.MethodType.UNARY,
  common_pb.Empty,
  common_pb.Configuration,
  /**
   * @param {!proto.base.Empty} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Configuration.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.Empty,
 *   !proto.base.Configuration>}
 */
const methodInfo_SystemService_GetConfiguration = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Configuration,
  /**
   * @param {!proto.base.Empty} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Configuration.deserializeBinary
);


/**
 * @param {!proto.base.Empty} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Configuration)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Configuration>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.SystemServiceClient.prototype.getConfiguration =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.SystemService/GetConfiguration',
      request,
      metadata || {},
      methodDescriptor_SystemService_GetConfiguration,
      callback);
};


/**
 * @param {!proto.base.Empty} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Configuration>}
 *     Promise that resolves to the response
 */
proto.base.SystemServicePromiseClient.prototype.getConfiguration =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.SystemService/GetConfiguration',
      request,
      metadata || {},
      methodDescriptor_SystemService_GetConfiguration);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.NameSpace,
 *   !proto.base.Frames>}
 */
const methodDescriptor_SystemService_ListSignals = new grpc.web.MethodDescriptor(
  '/base.SystemService/ListSignals',
  grpc.web.MethodType.UNARY,
  common_pb.NameSpace,
  common_pb.Frames,
  /**
   * @param {!proto.base.NameSpace} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Frames.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.NameSpace,
 *   !proto.base.Frames>}
 */
const methodInfo_SystemService_ListSignals = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Frames,
  /**
   * @param {!proto.base.NameSpace} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Frames.deserializeBinary
);


/**
 * @param {!proto.base.NameSpace} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Frames)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Frames>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.SystemServiceClient.prototype.listSignals =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.SystemService/ListSignals',
      request,
      metadata || {},
      methodDescriptor_SystemService_ListSignals,
      callback);
};


/**
 * @param {!proto.base.NameSpace} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Frames>}
 *     Promise that resolves to the response
 */
proto.base.SystemServicePromiseClient.prototype.listSignals =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.SystemService/ListSignals',
      request,
      metadata || {},
      methodDescriptor_SystemService_ListSignals);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.FileUploadChunkRequest,
 *   !proto.base.FileUploadResponse>}
 */
const methodDescriptor_SystemService_UploadFileChunk = new grpc.web.MethodDescriptor(
  '/base.SystemService/UploadFileChunk',
  grpc.web.MethodType.UNARY,
  proto.base.FileUploadChunkRequest,
  proto.base.FileUploadResponse,
  /**
   * @param {!proto.base.FileUploadChunkRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.FileUploadResponse.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.FileUploadChunkRequest,
 *   !proto.base.FileUploadResponse>}
 */
const methodInfo_SystemService_UploadFileChunk = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.FileUploadResponse,
  /**
   * @param {!proto.base.FileUploadChunkRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.FileUploadResponse.deserializeBinary
);


/**
 * @param {!proto.base.FileUploadChunkRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.FileUploadResponse)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.FileUploadResponse>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.SystemServiceClient.prototype.uploadFileChunk =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.SystemService/UploadFileChunk',
      request,
      metadata || {},
      methodDescriptor_SystemService_UploadFileChunk,
      callback);
};


/**
 * @param {!proto.base.FileUploadChunkRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.FileUploadResponse>}
 *     Promise that resolves to the response
 */
proto.base.SystemServicePromiseClient.prototype.uploadFileChunk =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.SystemService/UploadFileChunk',
      request,
      metadata || {},
      methodDescriptor_SystemService_UploadFileChunk);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.Empty,
 *   !proto.base.ReloadMessage>}
 */
const methodDescriptor_SystemService_ReloadConfiguration = new grpc.web.MethodDescriptor(
  '/base.SystemService/ReloadConfiguration',
  grpc.web.MethodType.UNARY,
  common_pb.Empty,
  proto.base.ReloadMessage,
  /**
   * @param {!proto.base.Empty} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.ReloadMessage.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.Empty,
 *   !proto.base.ReloadMessage>}
 */
const methodInfo_SystemService_ReloadConfiguration = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.ReloadMessage,
  /**
   * @param {!proto.base.Empty} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.ReloadMessage.deserializeBinary
);


/**
 * @param {!proto.base.Empty} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.ReloadMessage)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.ReloadMessage>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.SystemServiceClient.prototype.reloadConfiguration =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.SystemService/ReloadConfiguration',
      request,
      metadata || {},
      methodDescriptor_SystemService_ReloadConfiguration,
      callback);
};


/**
 * @param {!proto.base.Empty} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.ReloadMessage>}
 *     Promise that resolves to the response
 */
proto.base.SystemServicePromiseClient.prototype.reloadConfiguration =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.SystemService/ReloadConfiguration',
      request,
      metadata || {},
      methodDescriptor_SystemService_ReloadConfiguration);
};


module.exports = proto.base;

