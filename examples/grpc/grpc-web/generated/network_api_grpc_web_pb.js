/**
 * @fileoverview gRPC-Web generated client stub for base
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



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

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
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
   * @private @const {!proto.base.NetworkServiceClient} The delegate callback based client
   */
  this.delegateClient_ = new proto.base.NetworkServiceClient(
      hostname, credentials, options);

};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SubscriberConfig,
 *   !proto.base.Signals>}
 */
const methodInfo_NetworkService_SubscribeToSignals = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.Signals,
  /** @param {!proto.base.SubscriberConfig} request */
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
      metadata,
      methodInfo_NetworkService_SubscribeToSignals);
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
  return this.delegateClient_.client_.serverStreaming(this.delegateClient_.hostname_ +
      '/base.NetworkService/SubscribeToSignals',
      request,
      metadata,
      methodInfo_NetworkService_SubscribeToSignals);
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.PublisherConfig,
 *   !proto.base.Empty>}
 */
const methodInfo_NetworkService_PublishSignals = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /** @param {!proto.base.PublisherConfig} request */
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
      methodInfo_NetworkService_PublishSignals,
      callback);
};


/**
 * @param {!proto.base.PublisherConfig} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     The XHR Node Readable Stream
 */
proto.base.NetworkServicePromiseClient.prototype.publishSignals =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.publishSignals(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SignalIds,
 *   !proto.base.Signals>}
 */
const methodInfo_NetworkService_ReadSignals = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.Signals,
  /** @param {!proto.base.SignalIds} request */
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
      methodInfo_NetworkService_ReadSignals,
      callback);
};


/**
 * @param {!proto.base.SignalIds} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Signals>}
 *     The XHR Node Readable Stream
 */
proto.base.NetworkServicePromiseClient.prototype.readSignals =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.readSignals(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


module.exports = proto.base;

