# Android gPRC example 

## Project Summary:
A Sample Android application that communicates with the Beamy broker. The
Android application retrieves current configuration information from the Beamy broker by calling the
proto defined SystemService:

```
...
service SystemService {
  rpc GetConfiguration (Empty) returns (Configuration) {}
  rpc ListSignals (NameSpace) returns (Frames) {}
}
...

```

It retrieves a list of vehicle network configurations that are available for a
vehicle.

## Introduction 
This application is using the io.grpc implementation: https://grpc.io/docs/tutorials/basic/android/
The Beamy proto files are stored in a folder under **src/main/proto** and the java generated files
are automatically built when syncing the project in android studio.

The project gradle file have the following dependencies added for grpc:
```
classpath 'com.google.protobuf:protobuf-gradle-plugin:0.8.16'
```

To the module gradle file we add at the top of the file.
```
apply plugin: 'com.google.protobuf'
```
 
The following takes care of the java proto generated files:
```
protobuf {
    protoc { artifact = 'com.google.protobuf:protoc:3.8.0' }
    plugins {
        javalite { artifact = "com.google.protobuf:protoc-gen-javalite:3.0.0" }
        grpc {
            artifact = 'io.grpc:protoc-gen-grpc-java:1.21.0' // CURRENT_GRPC_VERSION
        }
    }
    generateProtoTasks {
        all().each { task ->
            task.plugins {
                javalite {}
                grpc { // Options added to --grpc_out
                    option 'lite'
                }
            }
        }
    }
}


```

We also add these dependencies:

```
implementation 'io.grpc:grpc-okhttp:1.21.0' // CURRENT_GRPC_VERSION
implementation 'io.grpc:grpc-protobuf-lite:1.21.0' // CURRENT_GRPC_VERSION
implementation 'io.grpc:grpc-stub:1.21.0' // CURRENT_GRPC_VERSION
```
## Proto file settings
The proto files should be copied to */src/main/proto, and for the protogen to generate the service 
we need to edit in all of the proto files and add the following statement(s):

```
option java_generic_services = true;
```

To get a java qualified name we need to add these statements to our proto files -  in this case the 
**system_api.proto** - which then lets us interact with the Beamy broker server.
```
option java_package = "com.example.beamyconfiguration";
option java_outer_classname = "System";
```

like this:

```
...
SystemServiceGrpc.SystemServiceBlockingStub stub = SystemServiceGrpc.newBlockingStub(channel);
...
System.Configuration conf = stub.getConfiguration(request);
...

```


## Java protobuf call
To setup the connection with the signal broker we need to build a io.grpc.Managedchannel. Once the connection is established
we have basically two sets of services available a blocking service and a non-blocking when that makes sense. In this case
we use the blocking service call with an empty request to retrieve the vehicle configuration.

```
...
import io.grpc.ManagedChannelBuilder;
import io.grpc.ManagedChannel;
...
channel = ManagedChannelBuilder.forAddress("10.242.179.196",50051).usePlaintext().build();

SystemServiceGrpc.SystemServiceStub stub = SystemServiceGrpc.newStub(channel);
SystemServiceGrpc.SystemServiceBlockingStub stub = SystemServiceGrpc.newBlockingStub(channel);

Base.Empty request  = Base.Empty.newBuilder().build();
Base.Configuration conf = stub.getConfiguration(request);
...

```

![UI instructions](instr.PNG)
