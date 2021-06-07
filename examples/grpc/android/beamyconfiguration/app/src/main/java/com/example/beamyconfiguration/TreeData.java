/**
 * Created by Peter Winzell, Volvo Cars(c) on 5/11/21.
 */
package com.example.beamyconfiguration;

import java.util.ArrayList;
import java.util.List;

public class TreeData {

    private String parent;
    private List children = null;

    public TreeData(){
        children = new ArrayList<String>(100);
    }

    public void setParent(String parent){
        this.parent = parent;
    }

    public void addChild(String child){
        children.add(child);
    }

    public String getParent(){
        return parent;
    }

    public List getChildren(){
        return children;
    }

    public boolean equals(Object obj){
        boolean ret = ((TreeData)obj).parent.equals(parent);
        return ret;
    }
}
