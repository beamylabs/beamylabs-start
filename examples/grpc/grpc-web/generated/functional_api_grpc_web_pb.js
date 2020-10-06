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
proto.base = require('./functional_api_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.base.FunctionalServiceClient =
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
proto.base.FunctionalServicePromiseClient =
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
 *   !proto.base.ClientId,
 *   !proto.base.Empty>}
 */
const methodDescriptor_FunctionalService_OpenPassWindow = new grpc.web.MethodDescriptor(
  '/base.FunctionalService/OpenPassWindow',
  grpc.web.MethodType.UNARY,
  common_pb.ClientId,
  common_pb.Empty,
  /**
   * @param {!proto.base.ClientId} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.ClientId,
 *   !proto.base.Empty>}
 */
const methodInfo_FunctionalService_OpenPassWindow = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /**
   * @param {!proto.base.ClientId} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @param {!proto.base.ClientId} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Empty)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Empty>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServiceClient.prototype.openPassWindow =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.FunctionalService/OpenPassWindow',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_OpenPassWindow,
      callback);
};


/**
 * @param {!proto.base.ClientId} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     Promise that resolves to the response
 */
proto.base.FunctionalServicePromiseClient.prototype.openPassWindow =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.FunctionalService/OpenPassWindow',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_OpenPassWindow);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.ClientId,
 *   !proto.base.Empty>}
 */
const methodDescriptor_FunctionalService_ClosePassWindow = new grpc.web.MethodDescriptor(
  '/base.FunctionalService/ClosePassWindow',
  grpc.web.MethodType.UNARY,
  common_pb.ClientId,
  common_pb.Empty,
  /**
   * @param {!proto.base.ClientId} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.ClientId,
 *   !proto.base.Empty>}
 */
const methodInfo_FunctionalService_ClosePassWindow = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /**
   * @param {!proto.base.ClientId} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @param {!proto.base.ClientId} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Empty)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Empty>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServiceClient.prototype.closePassWindow =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.FunctionalService/ClosePassWindow',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_ClosePassWindow,
      callback);
};


/**
 * @param {!proto.base.ClientId} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     Promise that resolves to the response
 */
proto.base.FunctionalServicePromiseClient.prototype.closePassWindow =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.FunctionalService/ClosePassWindow',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_ClosePassWindow);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.SenderInfo,
 *   !proto.base.Empty>}
 */
const methodDescriptor_FunctionalService_SetFanSpeed = new grpc.web.MethodDescriptor(
  '/base.FunctionalService/SetFanSpeed',
  grpc.web.MethodType.UNARY,
  proto.base.SenderInfo,
  common_pb.Empty,
  /**
   * @param {!proto.base.SenderInfo} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SenderInfo,
 *   !proto.base.Empty>}
 */
const methodInfo_FunctionalService_SetFanSpeed = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /**
   * @param {!proto.base.SenderInfo} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @param {!proto.base.SenderInfo} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Empty)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Empty>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServiceClient.prototype.setFanSpeed =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.FunctionalService/SetFanSpeed',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_SetFanSpeed,
      callback);
};


/**
 * @param {!proto.base.SenderInfo} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     Promise that resolves to the response
 */
proto.base.FunctionalServicePromiseClient.prototype.setFanSpeed =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.FunctionalService/SetFanSpeed',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_SetFanSpeed);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.SubscriberRequest,
 *   !proto.base.Value>}
 */
const methodDescriptor_FunctionalService_SubscribeToFanSpeed = new grpc.web.MethodDescriptor(
  '/base.FunctionalService/SubscribeToFanSpeed',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.base.SubscriberRequest,
  proto.base.Value,
  /**
   * @param {!proto.base.SubscriberRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.Value.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SubscriberRequest,
 *   !proto.base.Value>}
 */
const methodInfo_FunctionalService_SubscribeToFanSpeed = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.Value,
  /**
   * @param {!proto.base.SubscriberRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.Value.deserializeBinary
);


/**
 * @param {!proto.base.SubscriberRequest} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.base.Value>}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServiceClient.prototype.subscribeToFanSpeed =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/base.FunctionalService/SubscribeToFanSpeed',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_SubscribeToFanSpeed);
};


/**
 * @param {!proto.base.SubscriberRequest} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.base.Value>}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServicePromiseClient.prototype.subscribeToFanSpeed =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/base.FunctionalService/SubscribeToFanSpeed',
      request,
      metadata || {},
      methodDescriptor_FunctionalService_SubscribeToFanSpeed);
};


module.exports = proto.base;

