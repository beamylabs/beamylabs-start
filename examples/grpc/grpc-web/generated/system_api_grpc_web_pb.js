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
proto.base.SystemServicePromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!proto.base.SystemServiceClient} The delegate callback based client
   */
  this.delegateClient_ = new proto.base.SystemServiceClient(
      hostname, credentials, options);

};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.Empty,
 *   !proto.base.Configuration>}
 */
const methodInfo_SystemService_GetConfiguration = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Configuration,
  /** @param {!proto.base.Empty} request */
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
      methodInfo_SystemService_GetConfiguration,
      callback);
};


/**
 * @param {!proto.base.Empty} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Configuration>}
 *     The XHR Node Readable Stream
 */
proto.base.SystemServicePromiseClient.prototype.getConfiguration =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.getConfiguration(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.NameSpace,
 *   !proto.base.Frames>}
 */
const methodInfo_SystemService_ListSignals = new grpc.web.AbstractClientBase.MethodInfo(
  common_pb.Frames,
  /** @param {!proto.base.NameSpace} request */
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
      methodInfo_SystemService_ListSignals,
      callback);
};


/**
 * @param {!proto.base.NameSpace} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.Frames>}
 *     The XHR Node Readable Stream
 */
proto.base.SystemServicePromiseClient.prototype.listSignals =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.listSignals(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


module.exports = proto.base;

