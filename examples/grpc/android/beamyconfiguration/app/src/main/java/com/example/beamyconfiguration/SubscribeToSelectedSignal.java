/**
 * Created by Peter Winzell, Volvo Cars(c) on 6/28/21.
 */
package com.example.beamyconfiguration;

import android.util.Log;

import java.util.Observable;

public class SubscribeToSelectedSignal extends Observable {

    private Base.ClientId clientId;
    private Base.NameSpace namespace;
    private Base.SignalId sigId;

    private Network.SignalIds signalS;
    private Network.SubscriberConfig subConfig;

    private String subscription_notification_string = "";
    private Object sync = new Object();



    private  NetworkServiceGrpc.NetworkServiceBlockingStub stub;

    SubscribeToSelectedSignal(){
        if (BrokerDataModel.channel == null){
            Log.println(Log.INFO,"channel error", " need to connect to broker first");
        }
    }

    class SubScription implements Runnable {

        Thread thread;
        TreeData selectedNode;

        SubScription(TreeData node) {
            // Retrieve the network service ...
            selectedNode = node;
            if (BrokerDataModel.channel == null){
                Log.println(Log.INFO,"channel error", " need to connect to broker first");
                return;
            }
            stub = NetworkServiceGrpc.newBlockingStub(BrokerDataModel.channel);
            // build a clientId, the broker uses this id for handling its clients
            Base.ClientId clientId  = Base.ClientId.newBuilder().setId("android_client").build();
            // build a namespace, e.g where does the signal you want come form
            String Anamespacename = node.getParent().getParent().getName();
            Base.NameSpace namespace = Base.NameSpace.newBuilder().setName(Anamespacename).build();
            //build a signal id for a signal which belongs to namespace
            String signalName = node.getName();
            Base.SignalId sigId = Base.SignalId.newBuilder().setNamespace(namespace).setName(signalName).build();

            //build a list of signals to subscribe to
            signalS = Network.SignalIds.newBuilder().addSignalId(sigId).build();
            subConfig = Network.SubscriberConfig.newBuilder().setClientId(clientId).setSignals(signalS).build();

        }

        public void run() {
            while (true){
                // subscribe to the signals defined in constuctor.
                java.util.Iterator<Network.Signals> response = stub.subscribeToSignals(subConfig);


                try{
                    while (response.hasNext()) {
                        Network.Signals sigs = response.next();
                        for (int i = 0; i < sigs.getSignalCount(); i++) {
                            // retrieve the signal value
                            Network.Signal aSignal = sigs.getSignal(i);
                            if (aSignal.getId().getName().equals(selectedNode.getName())) {
                                setNote(selectedNode.getName() + " = " + new Double(aSignal.getDouble()).toString());
                                Log.println(Log.INFO,selectedNode.getName() + "is: " , new Double(aSignal.getDouble()).toString());
                            }

                        }
                    }
                }catch(io.grpc.StatusRuntimeException ex){
                    Log.println(Log.ERROR,"subscribe error", ex.toString());
                }
                Thread.yield();
            }
        }

        public void start(){
            if (thread == null){
                thread = new Thread(this);
                thread.start();
            }
        }
    }

    public void startSubscription(TreeData node){

        if (node != null) {
            SubscribeToSelectedSignal.SubScription sub = new SubscribeToSelectedSignal.SubScription(node);
            sub.start();
        }else{
            Log.println(Log.ERROR, "signal name", " not found ");
        }


    }

    public String getNote(){
        synchronized (sync) {
            return subscription_notification_string;
        }
    }

    public void setNote(String note){
        synchronized (sync)  {
            subscription_notification_string = note;
        }
        setChanged();
        notifyObservers();
    }


}
