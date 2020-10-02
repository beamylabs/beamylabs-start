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
proto.base = require('./diagnostics_api_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.base.DiagnosticsServiceClient =
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
proto.base.DiagnosticsServicePromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!proto.base.DiagnosticsServiceClient} The delegate callback based client
   */
  this.delegateClient_ = new proto.base.DiagnosticsServiceClient(
      hostname, credentials, options);

};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.base.DiagnosticsRequest,
 *   !proto.base.DiagnosticsResponse>}
 */
const methodInfo_DiagnosticsService_SendDiagnosticsQuery = new grpc.web.AbstractClientBase.MethodInfo(
  proto.base.DiagnosticsResponse,
  /** @param {!proto.base.DiagnosticsRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.base.DiagnosticsResponse.deserializeBinary
);


/**
 * @param {!proto.base.DiagnosticsRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.base.DiagnosticsResponse)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.base.DiagnosticsResponse>|undefined}
 *     The XHR Node Readable Stream
 */
proto.base.DiagnosticsServiceClient.prototype.sendDiagnosticsQuery =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/base.DiagnosticsService/SendDiagnosticsQuery',
      request,
      metadata || {},
      methodInfo_DiagnosticsService_SendDiagnosticsQuery,
      callback);
};


/**
 * @param {!proto.base.DiagnosticsRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.base.DiagnosticsResponse>}
 *     The XHR Node Readable Stream
 */
proto.base.DiagnosticsServicePromiseClient.prototype.sendDiagnosticsQuery =
    function(request, metadata) {
  var _this = this;
  return new Promise(function (resolve, reject) {
    _this.delegateClient_.sendDiagnosticsQuery(
      request, metadata, function (error, response) {
        error ? reject(error) : resolve(response);
      });
  });
};


module.exports = proto.base;

