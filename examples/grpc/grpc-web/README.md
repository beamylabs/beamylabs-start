# grpc-web example

The signalserver-web-client uses web grpc to interface the server

## Reference, re-generate web-grp js files

inspiration from
https://github.com/grpc/grpc-web/ and https://hackernoon.com/interface-grpc-with-web-using-grpc-web-and-envoy-possibly-the-best-way-forward-3ae9671af67


proto files are available in: [proto_files/](/proto_files)

to re-generate files - or just grab the files from the generated folder

- git clone https://github.com/grpc/grpc-web.git
- make plugin
- make sure to copy protoc-gen-grpc-web to a discoverable path such as /user/local/bin
- mkdir generated

Run the command from "this" directory!

```bash
protoc ../../../proto_files/* -I../../../proto_files --js_out=import_style=commonjs:generated --grpc-web_out=import_style=commonjs,mode=grpcwebtext:generated
```
