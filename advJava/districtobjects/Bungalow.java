package districtobjects;

public class Bungalow extends Residence {

	public Bungalow() {
		super(10.0, 7.5, 399000, 3, 0.04);
	}
	
	public Bungalow(double x, double y) {
		super(10.0, 7.5, 399000, 3, 0.04);
		setX(x);
		setY(y);
	}
	
	@Override
	public String getType() {
		return "Bungalow";
	}
}