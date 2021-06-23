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

    SimpleSubscriptionExample subscribeToSpeedExample;
    public SelectedDataModel(){
        subscribeToSpeedExample = new SimpleSubscriptionExample();
    }

    private String note="";

    public void Subscribe(){
        subscribeToSpeedExample.addObserver(this);
        subscribeToSpeedExample.startSubscription();
    }

    @Override
    public void update(Observable o, Object arg){
        Log.println(Log.INFO,"sub","changed");
        note = subscribeToSpeedExample.getNote();
        setChanged();
        notifyObservers();
    }

    public String getNote(){
        return note;
    }

}
