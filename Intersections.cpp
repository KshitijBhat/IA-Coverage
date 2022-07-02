#include <CGAL/Circular_kernel_intersections.h>
#include <CGAL/Exact_circular_kernel_2.h>
#include <cmath>
#include <algorithm>
typedef CGAL::Exact_circular_kernel_2             Circular_k;
typedef CGAL::Point_2<Circular_k>                 Point_2;
typedef CGAL::Circle_2<Circular_k>                Circle_2;
typedef CGAL::Circular_arc_2<Circular_k>          Circular_arc_2;
typedef CGAL::Line_2<Circular_k>                  Line_2;
typedef CGAL::Line_arc_2<Circular_k>              Line_arc_2;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circle_2, Circle_2>::type circ_circ_intersection_result;
typedef CGAL::CK2_Intersection_traits<Circular_k, Circular_arc_2, Circular_arc_2>::type arc_arc_intersection_result;
typedef CGAL::CK2_Intersection_traits<Circular_k, Line_arc_2, Circular_arc_2>::type seg_arc_intersection_result;
typedef CGAL::CK2_Intersection_traits<Circular_k, Line_arc_2, Line_arc_2>::type seg_seg_intersection_result;
typedef CGAL::CK2_Intersection_traits<Circular_k, Line_2, Line_2>::type lin_lin_intersection_result;
typedef CGAL::Circular_arc_point_2<Circular_k>    Circular_arc_point_2;

using namespace std;
class Interval;
Point_2 polarToCartesian(double r, double phi, Point_2 o);
double * CartesianToPolar(Point_2 p, Point_2 o);
bool sortcol(const vector<double>& v1, const vector<double>& v2);
bool sortcol2(const vector<double>& v1, const vector<double>& v2);
double * cartesianToPolarArr(double points[28][2],int num_pts, Point_2 o);
bool pointIn(Interval I, Point_2 p);
void print(Point_2 p);
void print(Circular_arc_point_2 p);
void print(Circular_arc_2 ar);
void print(Line_arc_2 seg);
void print(double pts[]);


void print(Point_2 p){
    cout<<"("<<to_double(p.x())<<", "<<to_double(p.y())<<") ";
}
void print(Circular_arc_point_2 p){
    cout<<"("<<to_double(p.x())<<", "<<to_double(p.y())<<") ";
}
void print(Circular_arc_2 ar){
    cout<<"Arc:";
    print(ar.source());
    print(ar.target());
    cout<<"center "; print(ar.center());cout<<" ";
    cout<<"sqaured radius: "<<to_double(ar.squared_radius())<<endl;
}

void print(Line_arc_2 seg){
    cout<<"Seg:";
    print(seg.source());
    print(seg.target());
    cout<<endl;
}



void print(double pts[5]){
    cout<<"Points: (";
    for(int i=0; i<2*(int)pts[4];i++){
        cout<< pts[i];
        if(i%2 && i!=0){
            cout<<"),(";
        }
        else{
            cout<<",";
        }
    }
    cout<<(int)pts[4]<<" points)"<<endl;
}



double * arc_arc( Circular_arc_2 ar1, Circular_arc_2 ar2)
{
    double * pts = new double[5]{0,0,0,0,0};

    vector<arc_arc_intersection_result> res;
    if(do_intersect(ar1,ar2)){
        intersection(ar1,ar2,back_inserter(res));
        using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;
        int i = 0;
        
        try{
            for(const auto& element : res) {
                auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
                pts[i] = to_double(algPoint.x());
                pts[i+1] = to_double(algPoint.y());
                i = i+2;
            }
            if(i==2){
                pts[4] = 1.0; // disregard pts[2] and pts[3] (1 point of intersection)
            }
            if(i==4){
            pts[4] = 2.0;   // 2 unique points of intersection
            }
        }
        catch(boost::exception_detail::clone_impl<boost::exception_detail::error_info_injector<boost::bad_get> >){
            pts[4] = -1.0; // concurrent arcs
        }
    }
    return pts; //remember: pts is a pointer to the points array
} 


double * seg_seg( Line_arc_2 l1, Line_arc_2 l2)
{
    double * pts = new double[5]{0,0,0,0,0};
    vector<seg_seg_intersection_result> res;
    if(do_intersect(l1,l2)){
        intersection(l1,l2,back_inserter(res));
        using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;
        int i = 0;
        try{
            for( auto& element : res) {
            auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
            pts[i] = to_double(algPoint.x());
            pts[i+1] = to_double(algPoint.y());
            i = i+2;
            }
            pts[4] = 1.0; // (1 point of intersection)
        }
        catch(boost::exception_detail::clone_impl<boost::exception_detail::error_info_injector<boost::bad_get> >){
            pts[4] = -1.0; // coincident segments
        }
    }
    
    return pts; //remember: pts is a pointer to the points array
}


double * seg_arc( Line_arc_2 l, Circular_arc_2 ar)
{
    double * pts = new double[5]{0,0,0,0,0};
    vector<seg_arc_intersection_result> res;
    if(do_intersect(l,ar)){
        intersection(l,ar,back_inserter(res));
        using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;
        int i = 0;
        try{
            for( auto& element : res) {
            auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
            pts[i] = to_double(algPoint.x());
            pts[i+1] = to_double(algPoint.y());
            i = i+2;
            }
            if(i==2){
                pts[4] = 1.0; // disregard pts[2] and pts[3] (1 point of intersection)
            }
            if(i==4){
            pts[4] = 2.0;   // 2 unique points of intersection
            }
        }
        catch(boost::exception_detail::clone_impl<boost::exception_detail::error_info_injector<boost::bad_get> >){
            pts[4] = -1.0; // ignore case
        }
    }
    
    return pts; //remember: pts is a pointer to the points array
} 
  

double * tangency( Point_2 p, Circular_arc_2 ar)
{
    double * pts = new double[5]{0,0,0,0,0};
    vector<arc_arc_intersection_result> res;
    
    Point_2 c = ar.center();
    double squared_radius = to_double(ar.squared_radius());
    double sq_dist = to_double(CGAL::squared_distance(p,c));
    double f_radius = sq_dist - squared_radius;
    if(f_radius<0){
        return pts;
    }
    else if(f_radius == 0){
        pts[0] = to_double(p.x());
        pts[1] = to_double(p.y());
        pts[4] = 1.0; // one points of tangency, p on ar
        return pts;
    }
    Circle_2 constr(p,f_radius);    

    if (do_intersect(ar,constr)){
        intersection(ar,constr,back_inserter(res));
        using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;
        int i = 0;
        for( auto& element : res) {
        auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
        pts[i] = to_double(algPoint.x());
        pts[i+1] = to_double(algPoint.y());
        i = i+2;
        }
        pts[4] = 2.0; // two unique points of tangency  
    }
    
    return pts; //remember: pts is a pointer to the points array
}


double * normalcy( Point_2 p, Circular_arc_2 ar)
{
    double * pts = new double[5]{0,0,0,0,0};
    vector<seg_arc_intersection_result> res;
    Point_2 c = ar.center();
    Line_arc_2 constr(p,c);
    if (do_intersect(ar,constr)){
        intersection(ar,constr,back_inserter(res));
        using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;
        int i = 0;
        for( auto& element : res) {
        auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
        pts[i] = to_double(algPoint.x());
        pts[i+1] = to_double(algPoint.y());
        i = i+2;
        }
        pts[4] = 1.0; // one point of intersection, normalcy 
    }
    return pts;
}


typedef struct IntervalStruct{
    double radius1 = 69;
    double radius2 = 69;
    double theta1 = 69;
    double theta2 = 69;
    double origin1 = 69;
    double origin2 = 69;
}IntervalStruct;

class Interval{
    
    
    
    public:
    double radius1;
    double radius2;
    double theta1;
    double theta2;
    Point_2 origin;

    
    Line_arc_2 seg1, seg2;
    Circular_arc_2 arc1, arc2;

    Point_2 r1t1, r2t1, r1t2, r2t2;
    
    friend Point_2 polarToCartesian(double r, double phi, Point_2 o);
    friend double * cartesianToPolarArr(double points[28][2],int num_pts, Point_2 o);
    // friend struct IntervalStruct;
    
    Interval( double r1, double r2,  double t1, double t2,  Point_2 o)
    {
        
        radius1 = r1; radius2 = r2;
        theta1 = t1; theta2 = t2;
        origin = o;

        r1t1 = polarToCartesian(r1,t1,o);
        r2t1 = polarToCartesian(r2,t1,o);
        r1t2 = polarToCartesian(r1,t2,o);
        r2t2 = polarToCartesian(r2,t2,o);


        seg1 = Line_arc_2(r1t1,r2t1);
        seg2 = Line_arc_2(r1t2,r2t2);
        arc1 = Circular_arc_2(Circle_2(o,r1*r1),Circular_arc_point_2(r1t1),Circular_arc_point_2(r1t2));
        arc2 = Circular_arc_2(Circle_2(o,r2*r2),Circular_arc_point_2(r2t1),Circular_arc_point_2(r2t2));  
    }


    Interval(struct IntervalStruct IS)
    {

        Point_2 o = Point_2(IS.origin1,IS.origin2);
        radius1 = IS.radius1; radius2 = IS.radius2;
        theta1 = IS.theta1; theta2 = IS.theta2;
        origin = o;

        r1t1 = polarToCartesian(IS.radius1,IS.theta1,o);
        r2t1 = polarToCartesian(IS.radius2,IS.theta1,o);
        r1t2 = polarToCartesian(IS.radius1,IS.theta2,o);
        r2t2 = polarToCartesian(IS.radius2,IS.theta2,o);


        seg1 = Line_arc_2(r1t1,r2t1);
        seg2 = Line_arc_2(r1t2,r2t2);
        arc1 = Circular_arc_2(Circle_2(o,IS.radius1*IS.radius1),Circular_arc_point_2(r1t1),Circular_arc_point_2(r1t2));
        arc2 = Circular_arc_2(Circle_2(o,IS.radius2*IS.radius2),Circular_arc_point_2(r2t1),Circular_arc_point_2(r2t2));  
    }

    // void IntervalFromEndpoints(Point_2 r1t1, Point_2 r2t1, Point_2 r1t2, Point_2 r2t2){
    //     Line_2 l1 = Line_2(r1t1,r2t1);
    //     Line_2 l2 = Line_2(r1t2,r2t2);
    //     vector<lin_lin_intersection_result> res;
    //     intersection(l1,l2,back_inserter(res));
    //     using boostRetVal = std::pair<CGAL::Circular_arc_point_2<CGAL::Filtered_bbox_circular_kernel_2<CGAL::Circular_kernel_2<CGAL::Cartesian<CGAL::Gmpq>, CGAL::Algebraic_kernel_for_circles_2_2<CGAL::Gmpq> > > > , unsigned>;

    //     for( auto& element : res) {
    //     auto algPoint = std::get<0>( boost::get< boostRetVal >(element) );
    //     Point_2 o = Point_2(to_double(algPoint.x()),to_double(algPoint.y()));
    //     }
    // }    

};



IntervalStruct IntervalAnalysis(Interval I,Interval Iprime){
    Circular_arc_2 arcs[2] = {I.arc1,I.arc2};
    Circular_arc_2 arcprimes[2] = {Iprime.arc1,Iprime.arc2};
    Line_arc_2 segs[2] = {I.seg1,I.seg2};
    Line_arc_2 segprimes[2] = {Iprime.seg1,Iprime.seg2};
    double points[28][2];
    int num_pts = 0;

    // All arcs intersecting arcs
    for (Circular_arc_2 ar: arcs){
        for (Circular_arc_2 arprime: arcprimes){
            double *inter;
            inter = arc_arc(ar,arprime);
            if (inter[4]== 2.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                points[num_pts+1][0] = inter[2];
                points[num_pts+1][1] = inter[3];
                num_pts += 2;
            }
            else if(inter[4]== 1.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                num_pts += 1;
            }
        }
    }

    // All arcs intersecting segprimes
    for (Circular_arc_2 ar: arcs){
        for (Line_arc_2 segprime: segprimes){
            double *inter;
            inter = seg_arc(segprime,ar);
            if (inter[4]== 2.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                points[num_pts+1][0] = inter[2];
                points[num_pts+1][1] = inter[3];
                num_pts += 2;
            }
            else if(inter[4]== 1.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                num_pts += 1;
            }
        }
    }

    // All segs intersecting arcprimes
    for (Line_arc_2 seg: segs){
        for (Circular_arc_2 arcprime: arcprimes){
            double *inter;
            inter = seg_arc(seg,arcprime);
            if (inter[4]== 2.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                points[num_pts+1][0] = inter[2];
                points[num_pts+1][1] = inter[3];
                num_pts += 2;
            }
            else if(inter[4]== 1.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                num_pts += 1;
            }
        }
    }

    // All segs intersecting segprimes
    for (Line_arc_2 seg: segs){
        for (Line_arc_2 segprime: segprimes){
            double *inter;

            inter = seg_seg(seg,segprime);
            if(inter[4]== 1.0){
                
                points[num_pts][0] = inter[0];
                points[num_pts][1] = inter[1];
                num_pts += 1;
            }
        }
    }

    // Corner Cases
    Point_2 corners[4] = {Iprime.r1t1, Iprime.r2t1, Iprime.r1t2, Iprime.r2t2};

    for (int i=0;i<4;i++){
        if(pointIn(I,corners[i])){
            points[num_pts][0] = to_double(corners[i].x());
            points[num_pts][1] = to_double(corners[i].y());
            num_pts += 1;
        }
    }
    

    double *normal;
    normal = normalcy(I.origin,arcprimes[1]);
    
    if(normal[4]== 1.0 ){
        if (pointIn(I,Point_2(normal[0],normal[1]))){
            points[num_pts][0] = normal[0];
            points[num_pts][1] = normal[1];
            num_pts += 1;
        }    
    }

    double *tangents;
    tangents = tangency(I.origin,arcprimes[1]);
    // Added condition to ensure tangency lies in I
    if (tangents[4]== 2.0){
        if(pointIn(I,Point_2(tangents[0],tangents[1]))){
            points[num_pts][0] = tangents[0];
            points[num_pts][1] = tangents[1];
            num_pts += 1;
        }
        if(pointIn(I,Point_2(tangents[2],tangents[3]))){
            points[num_pts+1][0] = tangents[2];
            points[num_pts+1][1] = tangents[3];
            num_pts += 1;
        }
        
    }
    else if(tangents[4]== 1.0){
        if(pointIn(I,Point_2(tangents[0],tangents[1]))){
            points[num_pts][0] = tangents[0];
            points[num_pts][1] = tangents[1];
            num_pts += 1;
        }
    }


    // for(int ii=0;ii<num_pts;ii++){
    //     cout<<"("<<points[ii][0]<<","<<points[ii][1]<<")"<<endl;

    // }
    // cout<<"Num_pts: "<<num_pts<<endl;
    // for (int i=0;i<num_pts;i++){
    //     cout<<*points[i]<<*(points[i]+1)<<endl;
    // }
    double x0,y0;
    x0 = to_double(I.origin.x());y0 = to_double(I.origin.y());
    vector<vector<double>> cartez;
    for (int i=0;i<num_pts;i++){
        double x = *points[i]; double y = *(points[i]+1);
        cartez.push_back({sqrt((x-x0) * (x-x0) + (y-y0) * (y-y0)), atan2(y-y0 , x-x0)});
    }
    sort(cartez.begin(), cartez.end(), sortcol);
    vector<vector<double>> cartezt = cartez;
    sort(cartez.begin(), cartez.end(), sortcol2);

    double theta1 = cartezt[0][1]; double theta2 = cartezt[num_pts-1][1];
    double radius1 = cartez[0][0]; double radius2 = cartez[num_pts-1][0];
    
    // double * J = new double[6]{radius1,radius2,theta1,theta2,x0,y0};
    IntervalStruct J;
    J.radius1 = radius1;
    J.radius2 = radius2;
    J.theta1 = theta1;
    J.theta2 = theta2;
    J.origin1 = x0;
    J.origin2 = y0;
    return J;
}

bool sortcol(const vector<double>& v1, const vector<double>& v2)
{
    return v1[1] < v2[1];
}
bool sortcol2(const vector<double>& v1, const vector<double>& v2)
{
    return v1[0] < v2[0];
}

double * CartesianToPolar(Point_2 p, Point_2 o){
    double x = to_double(p.x())-to_double(o.x());
    double y = to_double(p.y())-to_double(o.y());
    double * pt = new double[2]{sqrt(x * x + y * y), atan2(y , x)};
    return pt;     
}

double * cartesianToPolarArr(double points[28][2],int num_pts,Point_2 o) {
    double x0,y0;
    x0 = to_double(o.x());y0 = to_double(o.y());
    vector<vector<double>> cartez;
    for (int i=0;i<num_pts;i++){
        double x = *points[i]; double y = *(points[i]+1);
        cartez.push_back({sqrt((x-x0) * (x-x0) + (y-y0) * (y-y0)), atan2(y-y0 , x-x0)});
    }
    sort(cartez.begin(), cartez.end(), sortcol);
    vector<vector<double>> cartezt = cartez;
    
    sort(cartez.begin(), cartez.end(), sortcol2);

    double theta1 = cartezt[0][1]; double theta2 = cartezt[num_pts-1][1];
    double radius1 = cartez[0][0]; double radius2 = cartezt[num_pts-1][0];

    double * I = new double[6]{radius1,radius2,theta1,theta2,x0,y0};
    return I;
}

Point_2 polarToCartesian(double r, double phi, Point_2 o) {
    double x = to_double(o.x())+r * cos(phi); double y = to_double(o.y())+r * sin(phi);
    return Point_2(x,y);
}

bool pointIn(Interval I, Point_2 p){
    double * arr;
    arr = CartesianToPolar(p,I.origin);
    if(arr[0]<=I.radius2 && arr[0]>=I.radius1){
        if(arr[1]<=I.theta2 && arr[1]>=I.theta1){
            return true;
        } 
        else{
            return false;
        }
    }
    else{
        return false;
    }
}
// void IntervalAnalysis(double I1r1,double I1r2, double I1t1, double I1t2, double I1ox,double I1oy,
//                       double I2r1,double I2r2, double I2t1, double I2t2, double I2ox,double I2oy){
//     Interval I1 = Interval(I1r1,I1r2,I1t1,I1t2, Point_2(I1ox,I1oy));
//     Interval I2 = Interval(I2r1,I2r2,I2t1,I2t2, Point_2(I2ox,I2oy));
//     // print(I1.arc2);
//     // print(I2.arc2);
//     Interval_analysis(I1,I2);

// }

int main() {

    
    // Interval I2 = Interval(0,1.732,-1.57,2,Point_2(-3,-3));


    // Interval I1 = Interval(0,3,3,5.5,Point_2(0,0));
    
    Interval I2 = Interval(1,2,2,3.5,Point_2(3,2));
    Interval I1 = Interval(1,2,0.5,1.7,Point_2(0,0));
    // print(I1.arc2);
    // print(I2.arc2);
    cout<<IntervalAnalysis(I1,I2).radius1;
    // print(IntervalAnalysis(I1,I2).arc1);
    
    // print(arc_arc(I1.arc2,I2.arc2));
    
    // print(polarToCartesian(5,1.57096));
}



extern "C" {
    // Geek* Geek_new(){ return new Geek(); }
    // void interval_analysis(double I1r1,double I1r2, double I1t1, double I1t2, double I1ox,double I1oy,double I2r1,double I2r2, double I2t1, double I2t2, double I2ox,double I2oy)
    // {IntervalAnalysis(I1r1,I1r2,I1t1,I1t2,I1ox,I1oy,I2r1,I2r2,I2t1,I2t2,I2ox,I2oy);}
    Interval* Interval_new(double r1, double r2,  double t1, double t2,  double originx, double originy){ return new Interval(r1, r2,  t1, t2,  Point_2(originx, originy)); }
    IntervalStruct* interval_analysis(IntervalStruct I1,IntervalStruct I2){return new IntervalStruct(IntervalAnalysis(Interval(I1),Interval(I2)));}
}