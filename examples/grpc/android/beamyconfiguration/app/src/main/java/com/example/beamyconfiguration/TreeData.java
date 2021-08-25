/**
 * Created by Peter Winzell, Volvo Cars(c) on 5/11/21.
 */
package com.example.beamyconfiguration;

import org.w3c.dom.Node;

import java.util.ArrayList;
import java.util.List;


enum NodeType{
    UNKNOWN,
    SPACE,
    FRAME,
    SIGNAL
}

public class TreeData {

    private TreeData parent = null;
    private List<TreeData> children = null;
    private String name;
    private NodeType type = NodeType.UNKNOWN;

    public TreeData(String name, NodeType type){
        this.type = type;
        this.name = name;
        children = new ArrayList<TreeData>(100);
    }
    public void setParent(TreeData parent){

        this.parent = parent;
    }

    public TreeData addChild(TreeData child){
        children.add(child);
        return child;
    }

    public TreeData getParent(){
        return parent;
    }

    public List getChildren(){
        return children;
    }

    public boolean equals(Object obj){
        boolean ret = ((TreeData)obj).name.equals(parent.getName());
        return ret;
    }

    public void setName(String name){
        this.name = name;
    }

    public String getName(){
        return name;
    }

    public NodeType getNodeType() {
        return this.type;
    }
}

