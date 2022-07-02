#include <CGAL/Circular_kernel_intersections.h>
#include <CGAL/Exact_circular_kernel_2.h>

typedef CGAL::Exact_circular_kernel_2                  Circular_k;
typedef CGAL::Point_2<Circular_k>                      Point_2;
typedef CGAL::Circular_arc_point_2<Circular_k>         CircularArcPoint_2;
typedef CGAL::Direction_2<Circular_k>                  Direction_2;
typedef CGAL::Line_2<Circular_k>                       Line_2;
typedef CGAL::Circle_2<Circular_k>                     Circle_2;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circle_2, Circle_2>::type Intersection_cc_result;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circle_2, Line_2>::type Intersection_cl_result;
int main() {
    Point_2 a(0.15, 0.15), b(-0.15, -0.15), c(-0.15, 0.15), d(0.15, -0.15);
    double u = 0.5;
    double theta = atan(u);
    Line_2 r2(b, Direction_2(sin(-1.5708+theta),cos(-1.5708+theta)));
    Circle_2 cir(Point_2 (0,0), 4);
    using boostRetVal = std::pair<CGAL::Circular_arc_point_2< CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq>>>> , unsigned >;
    std::vector<Intersection_cl_result> out1s;
    intersection(cir,r2,back_inserter(out1s));
    const auto v1_s =std::get<0>( boost::get<boostRetVal>(out1s[0]));
    const auto v1s =Point_2(to_double(v1_s.x()), to_double(v1_s.y()));
    std::cout <<"v1s = "<< v1s << std::endl;
    return 0;
}