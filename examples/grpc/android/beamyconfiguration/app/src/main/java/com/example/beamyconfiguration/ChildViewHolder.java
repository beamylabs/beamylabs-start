/**
 * Created by Peter Winzell, Volvo Cars(c) on 5/11/21.
 */
package com.example.beamyconfiguration;

import android.content.Context;
import android.graphics.Color;
import android.util.Log;
import android.util.TypedValue;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.TextView;

import androidx.core.content.ContextCompat;

import com.unnamed.b.atv.model.TreeNode;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ChildViewHolder extends TreeNode.BaseNodeViewHolder<String> {

    private TextView tvValue;
    private CheckBox nodeSelector;
    private SelectedDataModel dataSelection;


    public ChildViewHolder(Context context) {
        super(context);
         dataSelection = SelectedDataModel.getInstance();
    }


    @Override
    public View createNodeView(TreeNode node, String value) {

        final LayoutInflater inflater = LayoutInflater.from(context);
        final View view = inflater.inflate(R.layout.layout_selectable_item, null, false);

        tvValue = (TextView) view.findViewById(R.id.node_value);
        tvValue.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20f);
        tvValue.setTextColor( ContextCompat.getColorStateList(context, R.color.colorPrimaryDark));
        // tvValue.setBackgroundColor(ContextCompat.getColorStateList(context, R.color.colorGreen));
        tvValue.setText(value);


        nodeSelector = (CheckBox) view.findViewById(R.id.node_selector);
        nodeSelector.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                node.setSelected(isChecked);
                if (node.isSelected()){
                    if (node.isLeaf()) {
                        dataSelection.addValue(node.getValue());
                        Log.println(Log.INFO,"LEAF ", node.getValue().toString());
                    }
                }else{
                    dataSelection.removeValue(node.getValue());
                }
            }
        });
        nodeSelector.setChecked(node.isSelected());

       /* if (node.isLastChild()) {
            view.findViewById(R.id.bot_line).setVisibility(View.INVISIBLE);
        }*/

        return view;

       /* final TextView tv = new TextView(context);
        tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20f);
        tv.setTextColor( ContextCompat.getColorStateList(context, R.color.colorGreen));
        tv.setText(String.valueOf(value));



        return tv;*/
    }

    @Override
    public void toggleSelectionMode(boolean editModeEnabled) {
        // Log.println(Log.INFO,"tree view", "selection toggled" );
        nodeSelector.setVisibility(editModeEnabled ? View.VISIBLE : View.GONE);
        nodeSelector.setChecked(mNode.isSelected());
    }

}
