#pragma once
#ifndef __GRAPHPAINTER__
#define __GRAPHPAINTER__
#include <cstdlib>
#include <string.h>
#include <fstream>
#include <stdexcept>
#include <sstream>
#include <iostream>
using namespace std;
enum GraphType { Graph = 0, DiGraph = 1 ,BT=2};
enum LayoutType {none=0,bt=1,graphviz=2,joel=3,joel2=4,auto_=5};
class graphpainter
{
public:
	char filename[256]; //输出地址
	char exeaddr[256]; //graphpainter执行文件地址
	graphpainter(const char* addr = "python graphpainter.py");
	bool newpainter(const char* filename, const GraphType gtype, const LayoutType ltype=auto_);
	void close();
	void setgraph(const char* attr, const char* value);
	void setfigure(const char *attr, const char* value);
	void setlayout(const char *attr, const char* value);
	void setdraw(const char *attr, const char* value);
	void setnode(const char *nodeid, const char* label = "");
	void setedge(const char *uid, const char* vid);
	void setbtnode(char bind, const char * nodeid, const char * label);
	void draw(const char* tip = "Drawing...\n");
private:
	int mode;
	fstream fout;
};
#endif
