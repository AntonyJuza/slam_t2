//leastSquare.h
#ifndef _LEASQU_H_
#define _LEASQU_H_
#include<iostream>
#include <vector>
#include"PointAndLine.h"
using namespace PointAndLine;
using namespace std;
namespace leastSquare
{
    vector<Point> GenRanPoint(Line l, int num);
    Line FitLine(vector<Point> ptr);
    bool PointsEvaluate(const vector<Point> & points);
    std::pair<float,float> CalcDistance(vector<Point> ptr, Line l);
    bool ErrorEvaluate(vector<Point> ptr, Line l);
}
#endif