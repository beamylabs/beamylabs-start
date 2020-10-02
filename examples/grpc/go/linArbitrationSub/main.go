package main

/*
	@author: Niclas Lind (nlind1@volvocars.com)
	@date: 31-01-2020

	@description:
		In this example we subscribe to an arbitration frame in a LIN-enviroment
		Once we recive an arbitration frame, we respond with the signals belonging to that frame

*/

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	log "github.com/sirupsen/logrus"
	"google.golang.org/grpc"

	base "./proto_files"
)

// json file for connection specifics.
type Configuration struct {
	BrokerIP   string
	BrokerPort string
}

var conf Configuration

// define signal data
type signalid struct {
	Identifier string
}

type framee struct {
	Frameid string     `json:"frameid"`
	Sigids  []signalid `json:"sigids"`
}

type spaces struct {
	Name   string   `json:"name"`
	Frames []framee `json:"framee"`
}

type settings struct {
	Namespaces []spaces `json:"namespaces"`
}

type VehiclesList struct {
	Vehicles []settings `json:"vehicles"`
}

func initConfiguration() bool {
	file, err := os.Open("configuration.json")
	defer file.Close()

	if err != nil {
		log.Error("Could not open configuration.json ", err)
		return false
	} else {
		decoder := json.NewDecoder(file)
		conf = Configuration{}
		err2 := decoder.Decode(&conf)
		if err2 != nil {
			log.Error("Could not parse configuration.json ", err2)
			return false
		}

	}
	return true
}

// hard coded predefined signal settings used for this example.
func signalDB() *settings {
	data := &settings{
		Namespaces: []spaces{
			{Name: "Virtual_LIN",
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

// set signal name and namespace to grpc generated data strcuture
func getSignaID(signalName string, namespaceName string) *base.SignalId {
	return &base.SignalId{
		Name: signalName,
		Namespace: &base.NameSpace{
			Name: namespaceName},
	}
}

// generate a signal with signalName & namespaceName and return the generated signal
func generateSignal(signalName string, namespaceName string) *base.Signal {
	signalPayload := &base.Signal_Integer{Integer: 1}

	// Just for test, if signalname is Day then set payload to 2...
	if signalName == "Day" {
		signalPayload = &base.Signal_Integer{Integer: 2}
	}

	return &base.Signal{
		Id:      getSignaID(signalName, namespaceName),
		Payload: signalPayload,
	}
}

// set signals and namespaces to grpc subscriber configuration, see files under proto_files
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

// publish signals that belongs to the frame that we received the arbitraion from
func publishSignals(data *settings, frameName string) *base.PublisherConfig {
	var signals []*base.Signal

	// add selected signals to publisher configuration
	for _, namespaceelement := range data.Namespaces {
		namespacename := namespaceelement.Name
		for _, frameelement := range namespaceelement.Frames {
			if frameName == frameelement.Frameid {
				for _, sigelement := range frameelement.Sigids {
					log.Info("Publishing signal: ", sigelement)
					signals = append(signals, generateSignal(sigelement.Identifier, namespacename))
				}
			}
		}
	}

	// publish all signals
	return &base.PublisherConfig{
		ClientId: &base.ClientId{
			Id: "publisher",
		},
		Signals: &base.Signals{
			Signal: signals,
		},
		Frequency: 0,
	}
}

func subscribeToArbitration(networkStub base.NetworkServiceClient, arbitration chan struct {
	string
	bool
}) {
	// Get arbitration name from our database
	subSignals := getArbitration(signalDB())

	fmt.Println("Subscribe to: ", subSignals.Signals)

	// Subscribe
	subscription, err := networkStub.SubscribeToSignals(context.Background(), subSignals)

	if err != nil {
		fmt.Println("Subscription error", err)
	} else {
		for {
			recvSignals, err := subscription.Recv() // wait for a subscription msg

			if err != nil {
				fmt.Println("Reception error", err)
				break
			}

			for _, recvSignal := range recvSignals.GetSignal() {
				arbitrationName := recvSignal.Id.Name
				arbitrationValue := recvSignal.GetArbitration()

				arbitration <- struct {
					string
					bool
				}{arbitrationName, arbitrationValue}
			}
		}
	}
}

func init() {
	fmt.Println("Init Go-example of LIN arbitration subscribtion")

	initConfiguration()
}

func main() {
	channel, err := grpc.Dial(conf.BrokerIP+":"+string(conf.BrokerPort), grpc.WithInsecure())
	if err != nil {
		log.Debugf("Didn't connect: %v", err)
	}
	defer channel.Close()

	// Create the network stub
	networkStub := base.NewNetworkServiceClient(channel)

	// Create a channel that
	arbitration := make(chan struct {
		string // Arbitrationframe (name)
		bool   // IsArbitration (true or false)
	})

	go subscribeToArbitration(networkStub, arbitration)

	// Check if an arbitration is received on grpc...
	for {
		select {
		case masterPull := <-arbitration:
			// If arbitration, send the signals that belongs to frame
			if masterPull.bool {
				frameID := masterPull.string
				signals := publishSignals(signalDB(), frameID)
				networkStub.PublishSignals(context.Background(), signals)
			}
		}
	}
}
