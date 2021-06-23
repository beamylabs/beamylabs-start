    /**
     * Created by Peter Winzell, Volvo Cars(c) on 6/22/21.
     */
    package com.example.beamyconfiguration;

    import android.util.Log;

    public class SimpleSubscriptionExample {
        private Base.ClientId clientId;
        private Base.NameSpace namespace;
        private Base.SignalId sigId;

        private Network.SignalIds signalS;
        private Network.SubscriberConfig subConfig;

        private  NetworkServiceGrpc.NetworkServiceBlockingStub stub;

        class SubScription implements Runnable {

            Thread thread;

            SubScription() {
                stub = NetworkServiceGrpc.newBlockingStub(BrokerDataModel.channel);
                // set the clientID
                Base.ClientId clientId  = Base.ClientId.newBuilder().setId("android_client").build();
                Base.NameSpace namespace = Base.NameSpace.newBuilder().setName("custom_can").build();
                Base.SignalId sigId = Base.SignalId.newBuilder().setNamespace(namespace).setName("VehicleSpeed").build();

                signalS = Network.SignalIds.newBuilder().addSignalId(sigId).build();
                subConfig = Network.SubscriberConfig.newBuilder().setClientId(clientId).setSignals(signalS).build();

            }

            public void run() {
                while (true){
                    java.util.Iterator<Network.Signals> response = stub.subscribeToSignals(subConfig);
                    try{
                    while (response.hasNext()) {
                        Network.Signals sigs = response.next();
                        for (int i = 0; i < sigs.getSignalCount(); i++) {
                            Network.Signal aSignal = sigs.getSignal(i);
                            if (aSignal.getId().getName().equals("VehicleSpeed")) {
                                Log.println(Log.INFO, "signal subscription", aSignal.toString());
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
    }
