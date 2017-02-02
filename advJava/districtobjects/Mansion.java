package districtobjects;

public class Mansion extends Residence {
	public Mansion(){
		super(11.0, 10.5, 610000, 6, 0.06);
	}

	public Mansion(double x, double y){
		super(11.0, 10.5, 610000, 6, 0.06);
		setX(x);
		setY(y);
	}
	
	@Override
	public String getType() {
		return "Mansion";
	}
}