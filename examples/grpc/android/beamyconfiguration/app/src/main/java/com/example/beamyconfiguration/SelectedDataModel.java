/**
 * Created by Peter Winzell, Volvo Cars(c) on 6/22/21.
 */
package com.example.beamyconfiguration;

import android.util.Log;

import com.google.common.eventbus.Subscribe;

import java.util.HashMap;
import java.util.Map;
import java.util.Observable;

public class SelectedDataModel extends Observable {

    SimpleSubscriptionExample subscribeToSpeedExample;
    public SelectedDataModel(){
        subscribeToSpeedExample = new SimpleSubscriptionExample();
    }

    public void Subscribe(){
        subscribeToSpeedExample.startSubscription();
    }
}
