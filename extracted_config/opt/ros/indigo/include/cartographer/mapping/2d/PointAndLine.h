#ifndef __PAL_CPP_
#define _PAL_CPP_
#include <cstdlib>
#include <cstddef>
#include<iostream>
#include "Eigen/Core"
namespace PointAndLine
{
    class Point
    {
    private:
        float x, y;
        friend class Line;
    public:
        Point() :x(0), y(0) {}
        Point(float _x, float _y);
        Point(const Point& p);
        Point& operator=(const Point& p);
        float getter_x()const;
        float getter_y()const;
        void setter(float _x, float _y);
        float getdis(const Point& p);
        friend std::ostream& operator<<(std::ostream& os, Point &p)
        {
            return os << "(" << p.getter_x() << ", " << p.getter_y() << ")";
        }
    };

    class Line
    {
    private:
        float a, b, c;
        Point start_p,end_p;
    public:
        Line():a(0),b(1),c(0){}
        Line(float _a,float _b,float _c);
        Line(const Line& l);
        Line& operator=(const Line& l);
        void getter(float& _a, float& _b,float& _c)const;
        float calcDistance(Point p)const;
        bool point_In_line(Point p) const;
        float GetSlope()const;
        float GetVerdictSlope()const;
        int ifaboveline(const Point &p)const;
        float GetY(const float &x) const;
        Eigen::Vector2f GetFoot(const Point &p) const;
        Line GetCrossLine(Point p) const;
        Line GetTransLine(const float &delta) const;
        Eigen::Vector2f GetInterPoint(const Line &ll) const;
        void SetEndPoint(const Eigen::Vector2f &start_p,const Eigen::Vector2f &end_p);
        void GetEndPoint(Eigen::Vector2f &start_p,Eigen::Vector2f &end_p) const;
    };
    class Area {
    public:
        static double GetTriangleArea(Eigen::Vector2f a, Eigen::Vector2f b,
                                      Eigen::Vector2f c) {
            return fabs((a[0] * b[1] + b[0] * c[1] + c[0] * a[1] - b[0] * a[1] -
                         c[0] * b[1] - a[0] * c[1]) /
                        2.0);
        }
        Area(Eigen::Vector2f a, Eigen::Vector2f b, Eigen::Vector2f c,
             Eigen::Vector2f d)
                : a_(a), b_(b), c_(c), d_(d) {
            area_s = GetTriangleArea(a_, b_, c_) + GetTriangleArea(a_, d_, c_);
            //std::cout << "四点面积：" << area_s << std::endl;
        }
        ~Area() {}

        bool IsInside(Eigen::Vector2f p) const {
            if (area_s <= 0.01) {
                return false;
            }
            double area_p = GetTriangleArea(a_, b_, p) + GetTriangleArea(b_, c_, p) +
                            GetTriangleArea(c_, d_, p) + GetTriangleArea(d_, a_, p);
            //std::cout << "计算面积：" << area_p << std::endl;
            return fabs(area_p - area_s) < 1e-6;
        }

    private:
        Eigen::Vector2f a_, b_, c_, d_;
        double area_s;
    };
}
#endif