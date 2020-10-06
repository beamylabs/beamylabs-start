#  Go grpc signal broker example

## Setup

Follow this steps before you continue

1. Download and install go: https://golang.org/dl/
2. Choose IDE (Recommended to use is Golang or VSCode+GoExtension)
	* Golang IDE: https://www.jetbrains.com/go/
	* GoExtension (VSCode) https://code.visualstudio.com/docs/languages/go
3. Install go extionsion below to be able to run the examples.

	```
	go get -u github.com/fogleman/gg
	go get -u github.com/sirupsen/logrus
	go get -u google.golang.org/grpc
	```
4. Include the generated grpc proto files in the folder proto_files, the go hook files (*.pb.go) is also generated in the folder proto_files.
	```
	protoc -I ../../../proto_files ../../../proto_files/*.proto  --go_out=plugins=grpc:./timeSync/proto_files/
	protoc -I ../../../proto_files ../../../proto_files/*.proto  --go_out=plugins=grpc:./linArbitrationSub/proto_files/
	```
> make sure to have `somepath/go/src/github.com/golang/protobuf/protoc-gen-go` in your PATH


## Go and the signal broker

In order to subscribe to vehicle signals we need to build a **base.SubscriberConfig struct** :
```
func subsignalDB() (*settings){
	data := &settings{
		Namespaces: []spaces{
			{Name: "UDPCanInterface",
				Frames: []framee{
					{Frameid: "missing_header_64",
						Sigids: []signalid{
							{Identifier: "Day"},
							{Identifier: "Hr"},
							{Identifier: "Mins"},
							{Identifier: "BenchC_a"},
							{Identifier: "TiAndDateIndcn_UB"},
							{Identifier: "TiAndDateVld"},
						}},
				},
			},
		},
	}


   return data
}
```
In here we subscribe to the signals
```
// set signals and namespaces to grpc subscriber configuration, see files under proto_files
func getSignals(data *settings)*base.SubscriberConfig{
	var signalids []*base.SignalId;
	var namespacename string

	for cindex := 0; cindex < len(data.Namespaces); cindex++{
		namespacename = data.Namespaces[cindex].Name;
		for _,frameelement := range data.Namespaces[cindex].Frames{
			for _,sigelement := range frameelement.Sigids{
				log.Info("subscribing to signal: " , sigelement);
				signalids = append(signalids,getSignaId(sigelement.Identifier,namespacename));
			}
		}
	}

	// add selected signals to subscriber configuration
	signals := &base.SubscriberConfig{
		ClientId: &base.ClientId{
			Id: "app_identifier",
		},
		Signals: &base.SignalIds{
			SignalId:signalids,
		},
		OnChange: false,
	}

	return signals
}
...
```

If you only want to subscribe to the arbitration, skip the last for-loop in the exmaple above, like this;

```
func getArbitration(data *settings) *base.SubscriberConfig {
	var signals []*base.SignalId

	// Subscribe to "missing_header_64"
	for _, selectedNamespace := range data.Namespaces {
		namespacename := selectedNamespace.Name
		for _, frameelement := range selectedNamespace.Frames {
			log.Info("Subscribing to frame arbitration: ", frameelement.Frameid)
			signals = append(signals, getSignaID(frameelement.Frameid, namespacename))
		}
	}

	// add selected signals to subscriber configuration
	return &base.SubscriberConfig{
		ClientId: &base.ClientId{
			Id: "app_identifier",
		},
		Signals: &base.SignalIds{
			SignalId: signals,
		},
		OnChange: false,
	}
}
```

Instead of using the hardcoded **base.SubscriberConfig struct**, we can use the function listSignals from the signalbroker server like below;

```
	channel, err := grpc.Dial("localhost:50051", grpc.WithInsecure())

	if err != nil {
		fmt.Println("Dialing error", err)
	}

	defer channel.Close()

	// Create the network stub
	networkStub := base.NewNetworkServiceClient(channel)

	// Create a system stub
	systemStub := base.NewSystemServiceClient(channel)

	// Create a namespace
	namespace := &base.NameSpace{Name: your-namespace-name}

	// Get all signals from .ldf file
	systemSignals, _ := systemStub.ListSignals(context.Background(), namespace)

```
We have now recieved a \*Frames object, from this object we can get all frames & signals from the .ldf file we have included in the *interfaces.json*

Together with some connection setup and a calls we are able to subcribe to the specified signals.
```
...
response, err := clientconnection.SubscribeToSignals(context.Background(),signals);
...
msg,err := response.Recv();
...
```

## Examples

[Time Sync](#Time-sync)

[LIN Arbitration Subscription](#LIN-Arbitration-Subscription)

### Time Sync

This go example connects to the signal broker using grpc and subscribes to a set of can vehicle signals that represent the system time. The result is continously published on http://localhost:9000.

![alt text](https://github.com/PeterWinzell/signalbroker-server/blob/go-example/examples/grpc/go/timeSync/printer/screen.png)

We have previously explained: https://github.com/beamylabs/signalbroker-server/blob/master/configuration/interfaces.json how the signal broker needs to be initialized through **interfaces.json**, and that the matching dbc file needs to be exposed to the signal broker at startup. We can through **canplayer**, https://github.com/linux-can/can-utils., record data from a real driving cycle and replay that with can player having defined a virtual can interface which is exposed to the broker.

Set up the virtual can interfaces vcan0 on linux:
```
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```    

Start the can log playback, assuming that we have a can log named can.log
```
canplayer -I can.log -l i vcan0=can0
```

## Start from prompt


Go to this directory and do
```
go run main.go pngprint.go
```

## LIN Arbitration Subscription

This go example connects to the signalbroker using grpc and subscribes to one/a set of LIN arbitrations.
Once we recevied an arbitration frame, we reply back to the master with the signals that belongs to that frame.

If you attempt to use the signal broker together with LIN, you should also use the [signalbroker LIN transceiver](https://github.com/AleksandarFilipov/signalbroker-lin-transceiver) (that is one branch for arduino and one for esp32). Please have a look in the README how you should config your interfaces.json file aswell. 

Configure the *configuration.json* so that one suits your needs.

Simply run the example 
```
go run main.go
```

## Cross-compiling

For cross-compiling go checkout: https://dave.cheney.net/2015/08/22/cross-compilation-with-go-1-5
Current example was built on mac os with the following settings to cross-compile for debian jessie and rpi3.
**GOOS=linux;GOARCH=arm;GOARM=5**
