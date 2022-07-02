#include <CGAL/Circular_kernel_intersections.h>
#include <CGAL/Exact_circular_kernel_2.h>

typedef CGAL::Exact_circular_kernel_2             Circular_k;
typedef CGAL::Point_2<Circular_k>                 Point_2;
typedef CGAL::Circle_2<Circular_k>                Circle_2;
typedef CGAL::Circular_arc_2<Circular_k>          Circular_arc_2;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circle_2, Circle_2>::type Intersection_result;

using namespace std;

int main() {

    Point_2 p(0,0), r(2,0);
    Circle_2 c1(p,4), c2(r,1);

    vector<Intersection_result> res;
    intersection(c1,c2,back_inserter(res));
    using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;

    for(const auto& element : res) {
    auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
    auto point = Point_2(to_double(algPoint.x()), to_double(algPoint.y()));
    std::cout << point << std::endl;
    }
}