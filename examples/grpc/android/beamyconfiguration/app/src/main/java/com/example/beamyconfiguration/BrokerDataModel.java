/**
 * Created by Peter Winzell, Volvo Cars(c) on 5/11/21.
 */
package com.example.beamyconfiguration;

import android.os.AsyncTask;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;
import java.util.Observable;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;


public class BrokerDataModel extends Observable {

    public static ManagedChannel channel;
    private String serverAdress;
    private int port;

    private  List<Base.NetworkInfo> networkinfo = null;
    private  List<TreeData> beamyConfData =  null;

    public BrokerDataModel() {

    }

    public List getConfData(){
        return this.beamyConfData;
    }

    private int parsePort(String serverA){
        Log.println(Log.INFO,serverA,"this is it");

        try{
            return Integer.parseInt(serverA);
        }catch(NumberFormatException ex){
            Log.println(Log.INFO,"PORTERROR:",ex.toString());
        }

        return -1;
    }

    public void connect(String serverAdr){
        try {
            this.serverAdress = serverAdr.substring(0, serverAdr.lastIndexOf(":"));
            this.port = parsePort(serverAdr.substring(serverAdr.lastIndexOf(":")+1, serverAdr.length()));

            new LongOperation().execute("");

        }catch(Exception ex){
            Log.println(Log.ERROR," could not parse url ", ex.toString());
        }
    }

    private class LongOperation extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {

            if (port > -1) {
                try {
                    // Interact with Beamy broker generated gRPC bridge
                    channel = ManagedChannelBuilder.forAddress(serverAdress, port).usePlaintext().build();
                    SystemServiceGrpc.SystemServiceBlockingStub stub = SystemServiceGrpc.newBlockingStub(channel);

                    // Retrieve the current configuration.
                    Base.Empty request = Base.Empty.newBuilder().build();
                    System.Configuration conf = stub.getConfiguration(request);

                    // Retrieve information on current Beamy configuration.
                    networkinfo = conf.getNetworkInfoList();
                    for (Base.NetworkInfo i : networkinfo) {

                        // retrieve network info
                        String description = i.getDescription();
                        String typeStr = i.getType();
                        Log.println(Log.INFO,"retrieve Beamy conf.","Network description: " + description + " network type: " + typeStr);

                        // list all signals per namespace
                        String namespacename =  i.getNamespace().getName();
                        Base.Frames signals = stub.listSignals(i.getNamespace());

                        // log frame names per namespace
                        TreeData dataPoint = new TreeData();
                        Log.println(Log.INFO, "signals", namespacename);
                        dataPoint.setParent(namespacename);

                        // add the signal name within the frame to a list of available signals
                        for (int findex = 0; findex < signals.getFrameCount(); findex++) {
                            dataPoint.addChild(signals.getFrame(findex).getSignalInfo().getId().getName());
                            Log.println(Log.INFO, "SIG: ", signals.getFrame(findex).getSignalInfo().getId().getName());
                        }

                        if (!beamyConfData.contains(dataPoint)) {
                            beamyConfData.add(dataPoint);
                        }
                    }

                }catch(Exception ex){
                    Log.println(Log.ERROR,"gRPC connection", "could not connect to " + serverAdress + ":" + port);
                }
            }
            return "Executed";
        }

        @Override
        protected void onPostExecute(String result) {
            Log.println(Log.INFO,"no of observers: ",String.valueOf(countObservers()));
            setChanged();
            notifyObservers();
        }

        @Override
        protected void onPreExecute() {
            beamyConfData = new ArrayList<TreeData>(10);
        }

        @Override
        protected void onProgressUpdate(Void... values) {

        }
    }

}
