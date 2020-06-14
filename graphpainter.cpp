#include "graphpainter.h"
graphpainter::graphpainter(const char * addr)
{
	strcpy(exeaddr, addr);
}

bool graphpainter::newpainter(const char * filename, const GraphType gtype,const LayoutType ltype)
{
	fout.open(filename, ios::out);
	mode = 0;
	if (fout.good())
	{
		strcpy(this->filename, filename);
		switch (gtype)
		{
		case Graph:
			fout << "%Graph%" << endl; break;
		case BT:
			fout << "%BT%" << endl; break;
		case DiGraph:
			fout << "%DiGraph%" << endl; break;
		}
		switch (ltype)
		{
		case none:
			fout << "%none layout%" << endl; break;
		case bt:
			fout << "%bst layout%" << endl; break;
		case graphviz:
			fout << "%graphviz layout%" << endl; break;
		case joel:
			fout << "%joel layout%" << endl; break;
		case joel2:
			fout << "%joel2 layout%" << endl; break;
		}
		return true;
	}
	return false;
}

void graphpainter::close()
{
	fout.close();
}

void graphpainter::setgraph(const char * attr, const char * value)
{
	if (mode != 0)
		throw logic_error("Set Graph Just After New Painter.");
	fout << '#' << attr << '#' << endl << value << endl;
}

void graphpainter::setfigure(const char * attr, const char * value)
{
	if (mode != 1)
	{
		mode = 1;
		fout << "%figure%" << endl;
	}
	fout << '#' << attr << '#' << endl << value << endl;
}

void graphpainter::setlayout(const char * attr, const char * value)
{
	if (mode != 2)
	{
		mode = 2;
		fout << "%layout%" << endl;
	}
	fout << '#' << attr << '#' << endl << value << endl;
}

void graphpainter::setdraw(const char * attr, const char * value)
{
	if (mode != 3)
	{
		mode = 3;
		fout << "%draw%" << endl;
	}
	fout << '#' << attr << '#' << endl << value << endl;
}

void graphpainter::setnode(const char * nodeid, const char * label)
{

	if (mode != 4)
	{
		mode = 4;
		fout << "%node%" << endl;
	}
	if (label != "")
		fout << nodeid << ':' << label << endl;
	else
		fout << nodeid << endl;
}
void graphpainter::setbtnode(char bind,const char * nodeid, const char * label)
{

	if (mode != 4)
	{
		mode = 4;
		fout << "%node%" << endl;
	}
	fout << bind << " ";
	if (label != "")
		fout << nodeid << ':' << label << endl;
	else
		fout << nodeid << endl;
}

void graphpainter::setedge(const char * uid, const char * vid)
{

	if (mode != 5)
	{
		mode = 5;
		fout << "%edge%" << endl;
	}
	fout << uid << "," << vid << endl;
}

void graphpainter::draw(const char * tip)
{

	stringstream str;
	cout << tip;
	str << exeaddr << " " << filename;
	system(str.str().c_str());
}
