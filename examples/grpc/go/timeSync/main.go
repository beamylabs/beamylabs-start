package main

import (
	"context"
	"encoding/json"
	"fmt"
	log "github.com/sirupsen/logrus"
	"os"
	utils "./util"
	"strconv"
	"strings"
)
import "google.golang.org/grpc"
import "./proto_files"


// json file for connection specifics.
type Configuration struct{
	Brokerip string
	Brokerport string
}

var conf Configuration

// define signal data

type signalid struct{
	Identifier string
}


type framee struct{
	Frameid string `json:frameid`
	Sigids []signalid `json:sigids`
}

type spaces struct{
	Name  string `json:name`
	Frames []framee `json:framee`
}

type settings struct{
	Namespaces []spaces `json:namespaces`
}

type VehiclesList struct{
	Vehicles []settings `json:vehicles`
}

const(
	ddindex = 0
	hhindex = 2
	mmindex = 4
	ssindex = 6
)
func display_subscribedvalues(signals []*base.Signal){

	timestrings := []string{"00",":","00",":","00",":","00"}

	// collect the output string
	for _,asignal := range signals{
		zerofiller := ""
		if asignal.GetInteger() < 10 {
			zerofiller = "0"
		}
		switch asignal.Id.Name{
		case "Day":
			timestrings[ddindex] = zerofiller + strconv.FormatInt(asignal.GetInteger(),10)
		case "Hr":
			timestrings[hhindex] = zerofiller + strconv.FormatInt(asignal.GetInteger(),10)
		case "Mins":
			timestrings[mmindex] = zerofiller + strconv.FormatInt(asignal.GetInteger(),10)
		case "Sec":
			timestrings[ssindex] = zerofiller + strconv.FormatInt(asignal.GetInteger(),10)
		}
	}

	print(strings.Join(timestrings,""))
}

func subcribe_to_signal_set(clientconnection base.NetworkServiceClient,signals *base.SubscriberConfig,ch chan int) {

	response, err := clientconnection.SubscribeToSignals(context.Background(),signals);

	if (err != nil){
		log.Debug(" error in subscrition to signals ", err);
	} else {
		for {
			msg,err := response.Recv(); // wait for a subscription msg
			if (err != nil){
				log.Debug(" error ", err);
				break;
			}

			display_subscribedvalues(msg.GetSignal())
		}
	}

	log.Info(" Done subcribing ...")
	ch <- 1 // don't block any more.
}

func initConfiguration()(bool){
	file,err := os.Open("configuration.json")
	defer file.Close()

	if  err != nil {
		log.Error("could not open configuration.json ", err)
		return false
	} else{
		decoder := json.NewDecoder(file)
		conf = Configuration{}
		err2 := decoder.Decode(&conf)
		if err2 != nil{
			log.Error("could not parse configuration.json ", err2)
			return false
		}

	}

	inializePlotter()
	return true
}




// print current configuration to the console
func printSignalTree(clientconnection *grpc.ClientConn) {
	systemServiceClient := base.NewSystemServiceClient(clientconnection);
	configuration,err := systemServiceClient.GetConfiguration(context.Background(),&base.Empty{})

	infos := configuration.GetNetworkInfo();
	for _,element := range infos{
		printSignals(element.Namespace.Name,clientconnection);
	}

	if err != nil{
		log.Debug("could not retrieve configuration " , err);
	}

}

// print signal tree(s) to console , using fmt for this.
func printSpaces(number int){
	for k := 1; k < number; k++ {
		fmt.Print(" ");
	}
}

func printTreeBranch(){
	fmt.Print("|");
}

func getFirstNameSpace(frames []*base.FrameInfo) string{
	element := frames[0];
	return element.SignalInfo.Id.Name;
}

func printSignals(zenamespace string,clientconnection *grpc.ClientConn){
	systemServiceClient := base.NewSystemServiceClient(clientconnection)
	signallist, err := systemServiceClient.ListSignals(context.Background(),&base.NameSpace{Name : zenamespace})

	frames := signallist.GetFrame();

	rootstring := "|[" + zenamespace + "]---|";
	rootstringlength := len(rootstring);
	fmt.Println(rootstring);

	for _,element := range frames{

		printTreeBranch();
		printSpaces(rootstringlength -1);

		framestring := "|---[" + element.SignalInfo.Id.Name + "]---|";
		framestringlength := len(framestring);

		fmt.Println(framestring);
		childs := element.ChildInfo;

		for _,childelement := range childs{
			outstr := childelement.Id.Name;
			printTreeBranch();
			printSpaces(rootstringlength -1);
			printTreeBranch();
			printSpaces(framestringlength - 1);
			fmt.Println("|---{", outstr, "}");
		}
	}

	if err != nil {
		log.Debug(" could not list signals ", err);
	}
}

// hard coded predefined sigbal settings used for this example.
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

// set signal name and namespace to grpc generated data strcuture
func getSignaId(signalName string,namespaceName string) *base.SignalId{
	return &base.SignalId{
		Name: signalName,
		Namespace:&base.NameSpace{
			Name:namespaceName},
	}
}

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

func main(){
	fmt.Println(" we are trying go with the volvo signal broker")

	// http server for output
	go utils.ServePrinter()

	initConfiguration()
	conn, err := grpc.Dial(conf.Brokerip + ":"+ string(conf.Brokerport), grpc.WithInsecure())
	if err != nil {
		log.Debug("did not connect: %v", err)
	}
	defer conn.Close()

	// get system and basic signal information from broker
	printSignalTree(conn)
	c := base.NewNetworkServiceClient(conn)

	// prevents main thread from finishing
	var ch chan int = make(chan int)

	signals := getSignals(subsignalDB())
	// start subscription thread
	go subcribe_to_signal_set(c,signals,ch);
	log.Info(" Waiting for subscription to end ...")
	fmt.Println(<-ch);
}
