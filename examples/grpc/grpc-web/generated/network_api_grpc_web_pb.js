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
proto.base = require('./network_api_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.base.NetworkServiceClient =
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
proto.base.NetworkServicePromiseClient =
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
 *   !proto.base.SubscriberConfig,
 *   !proto.base.Signals>}
 */
const methodDescriptor_NetworkService_SubscribeToSignals = new grpc.web.MethodDescriptor(
  '/base.NetworkService/SubscribeToSignals',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.base.SubscriberConfig,
  proto.base.Signals,
  /**
   * @param {!proto.base.SubscriberConfig} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.Signals.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SubscriberConfig,
 *   !proto.base.Signals>}
 */
const methodInfo_NetworkService_SubscribeToSignals = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.Signals,
  /**
   * @param {!proto.base.SubscriberConfig} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.Signals.deserializeBinary
);


/**
 * @param {!proto.base.SubscriberConfig} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.base.Signals>}
 *     The XHR Node Readable Stream
 */
proto.base.NetworkServiceClient.prototype.subscribeToSignals =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/base.NetworkService/SubscribeToSignals',
      request,
      metadata || {},
      methodDescriptor_NetworkService_SubscribeToSignals);
};


/**
 * @param {!proto.base.SubscriberConfig} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.base.Signals>}
 *     The XHR Node Readable Stream
 */
proto.base.NetworkServicePromiseClient.prototype.subscribeToSignals =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/base.NetworkService/SubscribeToSignals',
      request,
      metadata || {},
      methodDescriptor_NetworkService_SubscribeToSignals);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.PublisherConfig,
 *   !proto.base.Empty>}
 */
const methodDescriptor_NetworkService_PublishSignals = new grpc.web.MethodDescriptor(
  '/base.NetworkService/PublishSignals',
  grpc.web.MethodType.UNARY,
  proto.base.PublisherConfig,
  common_pb.Empty,
  /**
   * @param {!proto.base.PublisherConfig} request
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
 *   !proto.base.PublisherConfig,
 *   !proto.base.Empty>}
 */
const methodInfo_NetworkService_PublishSignals = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /**
   * @param {!proto.base.PublisherConfig} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  common_pb.Empty.deserializeBinary
);


/**
 * @param {!proto.base.PublisherConfig} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Empty)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Empty>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.NetworkServiceClient.prototype.publishSignals =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.NetworkService/PublishSignals',
      request,
      metadata || {},
      methodDescriptor_NetworkService_PublishSignals,
      callback);
};


/**
 * @param {!proto.base.PublisherConfig} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     Promise that resolves to the response
 */
proto.base.NetworkServicePromiseClient.prototype.publishSignals =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.NetworkService/PublishSignals',
      request,
      metadata || {},
      methodDescriptor_NetworkService_PublishSignals);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.base.SignalIds,
 *   !proto.base.Signals>}
 */
const methodDescriptor_NetworkService_ReadSignals = new grpc.web.MethodDescriptor(
  '/base.NetworkService/ReadSignals',
  grpc.web.MethodType.UNARY,
  proto.base.SignalIds,
  proto.base.Signals,
  /**
   * @param {!proto.base.SignalIds} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.Signals.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SignalIds,
 *   !proto.base.Signals>}
 */
const methodInfo_NetworkService_ReadSignals = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.Signals,
  /**
   * @param {!proto.base.SignalIds} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.Signals.deserializeBinary
);


/**
 * @param {!proto.base.SignalIds} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.Signals)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.Signals>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.NetworkServiceClient.prototype.readSignals =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.NetworkService/ReadSignals',
      request,
      metadata || {},
      methodDescriptor_NetworkService_ReadSignals,
      callback);
};


/**
 * @param {!proto.base.SignalIds} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Signals>}
 *     Promise that resolves to the response
 */
proto.base.NetworkServicePromiseClient.prototype.readSignals =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/base.NetworkService/ReadSignals',
      request,
      metadata || {},
      methodDescriptor_NetworkService_ReadSignals);
};


module.exports = proto.base;

