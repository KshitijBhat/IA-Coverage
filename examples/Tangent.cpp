#include <CGAL/Circular_kernel_intersections.h>
#include <CGAL/Exact_circular_kernel_2.h>
#include <CGAL/squared_distance_2.h>


typedef CGAL::Exact_circular_kernel_2             Circular_k;
typedef CGAL::Point_2<Circular_k>                 Point_2;
typedef CGAL::Circle_2<Circular_k>                Circle_2;
typedef CGAL::Circular_arc_2<Circular_k>          Circular_arc_2;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circle_2, Circle_2>::type Intersection_result_1;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circular_arc_2, Circular_arc_2>::type Intersection_result;
typedef CGAL::Circular_arc_point_2<Circular_k>    Circular_arc_point_2;
using namespace std;



int main() {
    // input arc: center(CGAL::Point_2<Circular_k>),double squared_radius, Point_2 start, Point_2 end
    Point_2 center(0,0);
    double squared_radius = 1;
    Circle_2 c(center,squared_radius);
    Point_2 start(0,-1), end(0,1);
    Circular_arc_point_2 s(start), e(end);
    Circular_arc_2 given(c,s,e);
    
    // input given point Point_2 pt
    Point_2 given_pt(2,0); 
    
    CGAL::internal::NT1 sq_dist = CGAL::squared_distance(given_pt,center);
    CGAL::internal::NT1 f_radius = sq_dist - squared_radius;
    Circle_2 constr(given_pt,f_radius);


    vector<Intersection_result> res;
    intersection(given,constr,back_inserter(res));
    using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;

    for(const auto& element : res) {
    auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
    auto point = Point_2(to_double(algPoint.x()), to_double(algPoint.y()));
    std::cout << point << std::endl;
    }
}