#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/intersections.h>
#include <iostream>
typedef CGAL::Exact_predicates_exact_constructions_kernel K;
typedef K::Point_2 Point_2;
typedef K::Segment_2 Segment_2;
typedef K::Intersect_2 Intersect_2;

int main()
{
  Segment_2 seg(Point_2(0,0), Point_2(1,1));
  Segment_2 seg2(Point_2(-1,1), Point_2(1,-1));
  const auto result = intersection(seg, seg2);
  std::cout<<"Point: "<<result<<std::endl;
  return 0;
}