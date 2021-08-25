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

        aModel = BrokerDataModel.getInstance();
        aModel.addObserver(this);

        selectionModel = SelectedDataModel.getInstance();
        selectionModel.addObserver(this);
    }

    private void clearTreeView(){

        while (root.getChildren().size() > 0) {
            List<TreeNode> children = root.getChildren();
            TreeNode child = children.get(0);
            root.deleteChild(child);
        }

    }

    @Override
    public void update(Observable o, Object arg) {
        if (o instanceof BrokerDataModel) {
            clearTreeView();
            Log.println(Log.INFO, "update triggered", o.toString());

            TreeData listan = aModel.getConfData();

            if (listan == null){
                Log.println(Log.ERROR, " connection", " connecting to broker failed");
                return;
            }

            aModel.printTree(listan);

            if (listan.getChildren() != null) {
                List<TreeData> children = listan.getChildren();
                for (TreeData element : children) {
                    TreeNode pNode = new TreeNode(element.getName()).setViewHolder(new ChildViewHolder(this));
                    List<TreeData> granchildren = element.getChildren();
                    for (TreeData child : granchildren) {
                        TreeNode cNode = new TreeNode(child.getName()).setViewHolder(new ChildViewHolder(this));
                        List<TreeData> grangranchildren = child.getChildren();
                        for (TreeData childchild : grangranchildren){
                            TreeNode ccNode = new TreeNode(childchild.getName()).setViewHolder(new ChildViewHolder(this));
                            cNode.addChild(ccNode);
                        }
                        pNode.addChild(cNode);
                    }
                    root.addChild(pNode);
                }
            }

            tView.expandAll();
            tView.collapseAll();
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
