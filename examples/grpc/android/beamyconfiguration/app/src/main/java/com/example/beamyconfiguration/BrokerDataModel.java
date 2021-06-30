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

    public static ManagedChannel channel = null;
    private String serverAdress;
    private int port;

    private  List<Base.NetworkInfo> networkinfo = null;
    private  TreeData beamyConfData =  null;
    private static BrokerDataModel currentInstance = null;

    private BrokerDataModel() {

    }


    public static BrokerDataModel getInstance(){
        if (currentInstance  == null){
            currentInstance = new BrokerDataModel();
        }
        return currentInstance;
    }


    public TreeData getConfData(){
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

    public void PrintTree(TreeData data){
        if (data != null) {
            Log.println(Log.INFO," Tree" , data.getName());
            if (data.getChildren() != null){
                List<TreeData> children = data.getChildren();
                for (TreeData i: children ) {
                    PrintTree(i);
                    Log.println(Log.INFO," -------- " , "----------");
                }
            }
        }
    }

    private TreeData found = null;
    private void Search(TreeData data,String signalName){
        String name1 = data.getName();
        Log.println(Log.INFO,"compare ", name1 + " " + signalName);
        if (data.getName().equals(signalName)){
            found = data;
        }else if(data.getChildren() != null){
            List<TreeData> children = data.getChildren();
            for (TreeData child : children ){
                Search(child,signalName);
            }
        }
    }

    public TreeData FindNameSpace(String signalName){
        if (beamyConfData != null){
            Search(beamyConfData,signalName);
            if (found != null){
                return found;
            }
        }

        return null;
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

                    TreeData root = new TreeData("Beamy-Signal-Tree",NodeType.UNKNOWN);
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
                        TreeData dataPoint = new TreeData(namespacename,NodeType.SPACE);
                        dataPoint.setParent(root);
                        root.addChild(dataPoint);
                        Log.println(Log.INFO, "signals", namespacename);

                        // add the signal name within the frame to a list of available signals
                        for (int findex = 0; findex < signals.getFrameCount(); findex++) {
                            TreeData child = dataPoint.addChild(new TreeData(signals.getFrame(
                                    findex).getSignalInfo().getId().getName(),NodeType.FRAME));
                            child.setParent(dataPoint);
                            Log.println(Log.INFO, "SIG: ", signals.getFrame(findex).getSignalInfo().getId().getName());
                            List<Base.SignalInfo> signalsperframe = signals.getFrame(findex).getChildInfoList();
                            for (int framesignalindex = 0; framesignalindex < signalsperframe.size(); framesignalindex++){
                                Base.SignalInfo sInfo = signalsperframe.get(framesignalindex);
                                TreeData granChild = new TreeData(sInfo.getId().getName(),NodeType.SIGNAL);
                                granChild.setParent(child);
                                child.addChild(granChild);
                                Log.println(Log.INFO,"signal info ", " " + sInfo.getId().getName());
                            }
                        }

                    }

                    beamyConfData = root;

                }catch(Exception ex){
                    ex.printStackTrace();
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
            // beamyConfData = new ArrayList<TreeData>(10);
        }

        @Override
        protected void onProgressUpdate(Void... values) {

        }

    }

}
