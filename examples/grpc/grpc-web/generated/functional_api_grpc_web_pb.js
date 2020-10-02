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
proto.base.FunctionalServicePromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!proto.base.FunctionalServiceClient} The delegate callback based client
   */
  this.delegateClient_ = new proto.base.FunctionalServiceClient(
      hostname, credentials, options);

};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.ClientId,
 *   !proto.base.Empty>}
 */
const methodInfo_FunctionalService_OpenPassWindow = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /** @param {!proto.base.ClientId} request */
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
      methodInfo_FunctionalService_OpenPassWindow,
      callback);
};


/**
 * @param {!proto.base.ClientId} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServicePromiseClient.prototype.openPassWindow =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.openPassWindow(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.ClientId,
 *   !proto.base.Empty>}
 */
const methodInfo_FunctionalService_ClosePassWindow = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /** @param {!proto.base.ClientId} request */
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
      methodInfo_FunctionalService_ClosePassWindow,
      callback);
};


/**
 * @param {!proto.base.ClientId} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServicePromiseClient.prototype.closePassWindow =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.closePassWindow(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SenderInfo,
 *   !proto.base.Empty>}
 */
const methodInfo_FunctionalService_SetFanSpeed = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Empty,
  /** @param {!proto.base.SenderInfo} request */
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
      methodInfo_FunctionalService_SetFanSpeed,
      callback);
};


/**
 * @param {!proto.base.SenderInfo} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Empty>}
 *     The XHR Node Readable Stream
 */
proto.base.FunctionalServicePromiseClient.prototype.setFanSpeed =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.setFanSpeed(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.SubscriberRequest,
 *   !proto.base.Value>}
 */
const methodInfo_FunctionalService_SubscribeToFanSpeed = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.Value,
  /** @param {!proto.base.SubscriberRequest} request */
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
      metadata,
      methodInfo_FunctionalService_SubscribeToFanSpeed);
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
  return this.delegateClient_.client_.serverStreaming(this.delegateClient_.hostname_ +
      '/base.FunctionalService/SubscribeToFanSpeed',
      request,
      metadata,
      methodInfo_FunctionalService_SubscribeToFanSpeed);
};


module.exports = proto.base;

