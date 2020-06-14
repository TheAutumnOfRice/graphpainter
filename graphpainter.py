import warnings
warnings.filterwarnings("ignore")
from matplotlib.pyplot import figure, subplot, show
import matplotlib.pyplot as plt
from networkx import Graph, DiGraph, draw
import networkx as nx
import os
import random
import sys
from networkx.drawing.nx_pydot import graphviz_layout
def binary_tree_layout(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0., xcenter = 0.5,
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.
       each node has an attribute "left: or "right"'''
    if root is None:
        root = T.nodes.__iter__().__next__()
    if pos is None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    if parent != None:
        neighbors.remove(parent)
    if len(list(neighbors))!=0:
        dx = width/2.
        leftx = xcenter - dx/2
        rightx = xcenter + dx/2
        for neighbor in neighbors:
            if G.nodes[neighbor]['child_status'] == 'left':
                pos = binary_tree_layout(G,neighbor, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=leftx, pos=pos,
                    parent = root)
            elif G.nodes[neighbor]['child_status'] == 'right':
                pos = binary_tree_layout(G,neighbor, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=rightx, pos=pos,
                    parent = root)
    return pos

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
            else:
                root = random.choice(list(G.nodes))
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def hierarchy_pos2(G, root=None, levels=None, width=1., height=1.):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node
       levels: a dictionary
               key: level number (starting from 0)
               value: number of nodes in this level
       width: horizontal space allocated for drawing
       height: vertical space allocated for drawing'''
    TOTAL = "total"
    CURRENT = "current"
    def make_levels(levels, node=root, currentLevel=0, parent=None):
        """Compute the number of nodes for each level
        """
        if not currentLevel in levels:
            levels[currentLevel] = {TOTAL : 0, CURRENT : 0}
        levels[currentLevel][TOTAL] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                levels =  make_levels(levels, neighbor, currentLevel + 1, node)
        return levels

    def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
        dx = 1/levels[currentLevel][TOTAL]
        left = dx/2
        pos[node] = ((left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
        levels[currentLevel][CURRENT] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc-vert_gap)
        return pos
    if levels is None:
        levels = make_levels({})
    else:
        levels = {l:{TOTAL: levels[l], CURRENT:0} for l in levels}
    vert_gap = height / (max([l for l in levels])+1)
    return make_pos({})
if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    ## Read Info
    if len(sys.argv)<=1:
        filename = "data.txt"
    else:
        filename = sys.argv[1]
    if len(sys.argv)<=2:
        dcd="GBK"
    else:
        dcd=sys.argv[2]

    #filename="data.txt"
    mode = 0
    graphname = 'Graph'
    figureinfo = {}
    layoutinfo = {}
    drawinfo = {'with_labels': True, 'node_color': 'w'}
    nodeinfo = {}
    uselayout="graphviz"
    graphinfo = {}
    edgeinfo = []
    onenodeinfo={}
    curinfo = None
    curkey = None
    curvalue = None
    def Error(text, ecode=1):
        print(text)
        os.system('pause')
        sys.exit(ecode)


    def TryEval(str, text, ecode=1):
        try:
            return eval(str)
        except:
            Error(text, ecode)


    with (open(filename, 'r',encoding=dcd)) as f:
        for ss in f:
            s = ss.strip()
            if s == '%Graph%':
                graphname = 'Graph'
                curinfo = graphinfo
                uselayout = "graphviz"
                layoutinfo = {'prog': 'dot'}
                mode = 1
                graphinfo = {}
            elif s == '%DiGraph%':
                graphname = 'DiGraph'
                curinfo = graphinfo
                uselayout = "graphviz"
                layoutinfo = {'prog': 'dot'}
                mode = 1
                graphinfo = {}
            elif s == '%BT%':
                graphname = 'BT'
                curinfo = graphinfo
                uselayout = "bt"
                mode = 1
                graphinfo = {}
            elif s == "%none layout%":
                layoutinfo = {}
                uselayout = "none"
            elif s == "%bt layout%":
                layoutinfo = {}
                uselayout = "bt"
            elif s=="%graphviz layout%":
                layoutinfo = {'prog': 'dot'}
                uselayout = "graphviz"
            elif s=='%joel layout%':
                layoutinfo = {}
                uselayout = "joel"
            elif s=='%joel2 layout%':
                layoutinfo = {}
                uselayout = "joel2"
            elif s == '%figure%':
                mode = 1
                curinfo = figureinfo
            elif s == '%layout%':
                mode = 1
                curinfo = layoutinfo
            elif s == '%draw%':
                mode = 1
                curinfo = drawinfo
            elif s == '%node%':
                mode = 4
            elif s == '%edge%':
                mode = 5
            elif mode == 0:
                Error("Error Command: %s" % s, 1)
            elif mode == 1:
                if s[0] == '#' and s[-1] == '#':
                    curkey = s[1:-1]
                    mode = 2
                else:
                    Error("Error Key Format: %s" % s, 3)
            elif mode == 2:
                curvalue = TryEval(s, "Value Parse Error: %s" % s, 4)
                mode = 1
                curinfo[curkey] = curvalue
            elif mode == 4:
                if graphname != 'BT':
                    pos = s.find(':')
                    if pos != -1:
                        curkey = TryEval(s[:pos], 'Key Parse Error: %s' % s[:pos], 2)
                        curvalue = TryEval(s[pos + 1:], 'Value Parse Error: %s' % s[pos + 1:], 4)
                        nodeinfo[curkey] = curvalue
                    else:
                        curkey = TryEval(s, 'Key Parse Error: %s' % s, 2)
                        curvalue = str(curkey)
                        nodeinfo[curkey] = curvalue
                else:
                    bpos=s[0].upper()
                    if bpos!='L' and bpos!='R':
                        Error("BT Graph Node should be started with L or R.",5)
                    s=s[1:]
                    pos = s.find(':')
                    if pos != -1:
                        curkey = TryEval(s[:pos], 'Key Parse Error: %s' % s[:pos], 2)
                        curvalue = TryEval(s[pos + 1:], 'Value Parse Error: %s' % s[pos + 1:], 4)
                        nodeinfo[curkey] = (curvalue,'left' if bpos=='L' else 'right')
                    else:
                        curkey = TryEval(s, 'Key Parse Error: %s' % s, 2)
                        curvalue = str(curkey)
                        nodeinfo[curkey] = (curvalue,'left' if bpos=='L' else 'right')

            elif mode == 5:
                curvalue = TryEval(s, 'Value Parse Error: %s' % s, 4)
                edgeinfo += [curvalue]

    ## Generate Pic
    figure(**figureinfo)
    subplot(111)
    if graphname == 'Graph' or graphname == 'BST':
        T = Graph(**graphinfo)
    elif graphname == 'DiGraph':
        T = DiGraph(**graphinfo)
    else:
        T = Graph(**graphinfo)
    if graphname=='BT':
        for i in nodeinfo.keys():
            T.add_node(i,child_status=nodeinfo[i][1])
            nodeinfo[i]=nodeinfo[i][0]
    else:
        for i in nodeinfo.keys():
            T.add_node(i)
    for i in edgeinfo:
        T.add_edge(*i)
    if uselayout=='graphviz':
        pos = graphviz_layout(T, **layoutinfo)
    elif uselayout=='bt':
        pos = binary_tree_layout(T,**layoutinfo)
    elif uselayout=='joel':
        pos = hierarchy_pos(T, **layoutinfo)
    elif uselayout=='joel2':
        pos = hierarchy_pos2(T, **layoutinfo)
    else:
        pos=None
    draw(T, pos, labels=nodeinfo, **drawinfo)
    show()
    sys.exit(0)
