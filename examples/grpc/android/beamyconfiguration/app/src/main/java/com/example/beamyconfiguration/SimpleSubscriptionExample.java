    /**
     * Created by Peter Winzell, Volvo Cars(c) on 6/22/21.
     */
    package com.example.beamyconfiguration;

    import android.util.Log;

    import java.util.Observable;

    public class SimpleSubscriptionExample extends Observable {
        private Base.ClientId clientId;
        private Base.NameSpace namespace;
        private Base.SignalId sigId;

        private Network.SignalIds signalS;
        private Network.SubscriberConfig subConfig;

        private String subscription_notification_string = "";
        private Object sync = new Object();

        private  NetworkServiceGrpc.NetworkServiceBlockingStub stub;

        class SubScription implements Runnable {

            Thread thread;

            SubScription() {
                // Retrieve the network service ...
                if (BrokerDataModel.channel == null){
                    Log.println(Log.INFO,"channel error", " need to connect to broker first");
                }
                stub = NetworkServiceGrpc.newBlockingStub(BrokerDataModel.channel);
                // build a clientId, the broker uses this id for handling its clients
                Base.ClientId clientId  = Base.ClientId.newBuilder().setId("android_client").build();
                // build a namespace, e.g where does the signal you want come form
                Base.NameSpace namespace = Base.NameSpace.newBuilder().setName("custom_can").build();
                //build a signal id for a signal which belongs to namespace
                Base.SignalId sigId = Base.SignalId.newBuilder().setNamespace(namespace).setName("VehicleSpeed").build();

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
                            if (aSignal.getId().getName().equals("VehicleSpeed")) {
                                setNote(new Double(aSignal.getDouble()).toString());

                                Log.println(Log.INFO,"speed is: " , new Double(aSignal.getDouble()).toString());
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

        public void startSubscription(){
            SubScription sub = new SubScription();
            sub.start();
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
