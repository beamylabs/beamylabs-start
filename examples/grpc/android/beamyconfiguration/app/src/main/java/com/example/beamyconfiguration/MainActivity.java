/**
 * Created by Peter Winzell, Volvo Cars(c) on 5/11/21.
 */
package com.example.beamyconfiguration;


import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import com.unnamed.b.atv.model.TreeNode;
import com.unnamed.b.atv.view.AndroidTreeView;

import java.util.List;
import java.util.Observable;
import java.util.Observer;



public class MainActivity extends AppCompatActivity implements Observer, View.OnClickListener {

    private BrokerDataModel aModel;
    private SelectedDataModel  selectionModel;

    private Button connectButton;
    private Button subscribeButton;
    private TextView serverAdr;
    private TextView notificationTV;
    private TreeNode root;
    private AndroidTreeView tView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ViewGroup rootV = (ViewGroup) findViewById(R.id.brokeraddress);
        ViewGroup containerView = (ViewGroup) findViewById(R.id.idTreeView);

        notificationTV = findViewById(R.id.subscription);
        serverAdr = findViewById(R.id.beamyurl);
        connectButton = findViewById(R.id.connectbutton);

        subscribeButton = findViewById(R.id.connectbutton);
        subscribeButton.setActivated(false);

        root = new TreeNode("Beamy-Configuration");
        tView = new AndroidTreeView(this, root);

        tView.setDefaultAnimation(true);
        tView.setSelectionModeEnabled(true);
        tView.setDefaultContainerStyle(R.style.TreeNodeStyleDivided, true);

        containerView.addView(tView.getView());

        aModel = new BrokerDataModel();
        aModel.addObserver(this);

        selectionModel = new SelectedDataModel();
        selectionModel.addObserver(this);
    }

    @Override
    public void update(Observable o, Object arg) {
        if (o instanceof BrokerDataModel) {
            Log.println(Log.INFO, "update triggered", o.toString());

            List<TreeData> listan = aModel.getConfData();
            if (listan.size() > 0) {

                for (TreeData element : listan) {
                    String parent = element.getParent();
                    TreeNode pNode = new TreeNode(parent).setViewHolder(new TreeViewHolder(this));
                    List<String> children = element.getChildren();
                    for (String child : children) {
                        TreeNode cNode = new TreeNode(child).setViewHolder(new ChildViewHolder(this));
                        pNode.addChild(cNode);
                    }
                    root.addChild(pNode);
                }
            }

            tView.expandAll();
            subscribeButton.setActivated(true);
        }
        else if (o instanceof SelectedDataModel){
            notificationTV.setText(((SelectedDataModel) o).getNote());
        }
    }

    @Override
    public void onClick(View v) {
            switch (v.getId()) {
                case R.id.connectbutton:
                    aModel.connect(serverAdr.getText().toString());
                    break;
                case R.id.subscribebutton:
                    if (BrokerDataModel.channel != null) {
                        selectionModel.Subscribe();
                    }
                    else{
                        Log.println(Log.ERROR,"subscribe", "trying to subscribe without connected to broker");
                    }
                    break;
            }
    }

}
