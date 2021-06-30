/**
 * Created by Peter Winzell, Volvo Cars(c) on 6/22/21.
 */
package com.example.beamyconfiguration;

import android.util.Log;

import com.google.common.eventbus.Subscribe;

import java.util.HashMap;
import java.util.Map;
import java.util.Observable;
import java.util.Observer;

public class SelectedDataModel extends Observable implements Observer {

    private static SelectedDataModel  currentInstance = null;

    SimpleSubscriptionExample subscribeToSpeedExample;
    SubscribeToSelectedSignal subscribeToSelectedSignal;

    private  SelectedDataModel(){

        subscribeToSpeedExample = new SimpleSubscriptionExample();
        subscribeToSelectedSignal = new SubscribeToSelectedSignal();

    }

    private Object nodeName = null;

    public static SelectedDataModel getInstance(){
        if (currentInstance  == null){
            currentInstance = new SelectedDataModel();
        }
        return currentInstance;
    }

    private String note="";

    public void Subscribe(){
        // uncomment if you want to listen to speed hardcoded to custom_can namespace
        // subscribeToSpeedExample.addObserver(this);
        // subscribeToSpeedExample.startSubscription();

        // comment out if you want to uncomment the above.
        subscribeToSelectedSignal.addObserver(this);
        if (nodeName != null) {
            TreeData signalNode = BrokerDataModel.getInstance().FindNameSpace(nodeName.toString());
            subscribeToSelectedSignal.startSubscription(signalNode);
        }
    }

    @Override
    public void update(Observable o, Object arg){
        Log.println(Log.INFO,"sub","changed");
        // uncomment if you want to run hardcoded against vehicle speed
        // note = subscribeToSpeedExample.getNote();
        note = subscribeToSelectedSignal.getNote();
        setChanged();
        notifyObservers();
    }

    public String getNote(){
        return note;
    }

    public void AddValue(Object value){
        nodeName = value.toString();
        Log.println(Log.INFO,"select data model", value.toString() + " added " );
    }

    public void RemoveValue(Object value){
        Log.println(Log.INFO,"select data model", value.toString() + " removed " );
        nodeName = null;
    }
}
