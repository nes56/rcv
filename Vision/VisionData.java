package Vision;

public class VisionData{

    // contains the data from the Raspberry Pi


    public static VisionData frontData = new VisionData(true);
    public static VisionData backData = new VisionData(false);

    public String name;


    public VisionData(boolean front){
        this.front = front;
        p1 = new point();
        p2 = new point();       
    }  
    public class point {
        public double a; // angle
        public double d; // distance

        point() {
            a = 0;
            d = 0;
        }
    }

    public volatile point p1;
    public volatile point p2;
    public volatile boolean front;
    public volatile boolean found = false;
    public long time = 0;

    

    public void set(VisionData vd){
        p1.a = vd.p1.a;
        p1.d = vd.p1.d;
        p2.a = vd.p2.a;
        p2.d = vd.p2.d;
        front = vd.front;
        found = vd.found;
        time = vd.time;

//        System.out.println("point front : start - angle = " + frontData.p1.a + " length = " + 
//        frontData.p1.d + " / end - angle = " + frontData.p2.a + " length = " + frontData.p2.d);
//        System.out.println("point back : start - angle = " + backData.p1.a + " length = " + 
//        backData.p1.d + " / end - angle = " + backData.p2.a + " length = " + backData.p2.d);
    }
    public void set() {
        time = System.currentTimeMillis();
        if(front) {
            frontData.set(this);
        } else {
            backData.set(this);
        }
    }
    public boolean found() { 
        return found;
    }
    public double a1() {
        return p1.a;
    }
    public double d1() {
        return p1.d;
    }
    public double a2() {
        return p2.a;
    }
    public double d2() {
        return p2.d;
    }

    public long time() {
        return time;
    }
}
