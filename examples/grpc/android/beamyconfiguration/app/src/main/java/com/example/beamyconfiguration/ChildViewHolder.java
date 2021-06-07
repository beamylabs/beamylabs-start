/**
 * Created by Peter Winzell, Volvo Cars(c) on 5/11/21.
 */
package com.example.beamyconfiguration;

import android.content.Context;
import android.util.TypedValue;
import android.view.View;
import android.widget.TextView;

import androidx.core.content.ContextCompat;

import com.unnamed.b.atv.model.TreeNode;

public class ChildViewHolder extends TreeNode.BaseNodeViewHolder<Object> {

    public ChildViewHolder(Context context) {
        super(context);
    }


    @Override
    public View createNodeView(TreeNode node, Object value) {

        final TextView tv = new TextView(context);
        tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20f);
        tv.setTextColor( ContextCompat.getColorStateList(context, R.color.colorGreen));
        tv.setText(String.valueOf(value));

        return tv;
    }

    @Override
    public void toggle(boolean active) {

    }
}
