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

    private Button connectButton;
    private TextView serverAdr;
    private TreeNode root;
    private AndroidTreeView tView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ViewGroup rootV = (ViewGroup) findViewById(R.id.brokeraddress);
        ViewGroup containerView = (ViewGroup) findViewById(R.id.idTreeView);


        serverAdr = findViewById(R.id.beamyurl);
        connectButton = findViewById(R.id.connectbutton);

        root = new TreeNode("Beamy-Configuration");
        tView = new AndroidTreeView(this, root);

        tView.setDefaultAnimation(true);
        tView.setSelectionModeEnabled(true);
        tView.setDefaultContainerStyle(R.style.TreeNodeStyleDivided, true);

        containerView.addView(tView.getView());

        aModel = new BrokerDataModel();
        aModel.addObserver(this);


    }

    @Override
    public void update(Observable o, Object arg) {

       Log.println(Log.INFO,"update triggered",o.toString());

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
    }

    @Override
    public void onClick(View v) {
            switch (v.getId()) {
                case R.id.connectbutton:
                    aModel.connect(serverAdr.getText().toString());
                    break;
            }
    }


}
