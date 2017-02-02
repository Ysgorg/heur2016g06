package districtobjects;

public class FamilyHome extends Residence {
	FamilyHome(){
		super(8.0, 8.0, 285000, 2, 0.03);
	}
	
	public FamilyHome(double x, double y){
		super(8.0, 8.0, 285000, 2, 0.03);
		setX(x);
		setY(y);
	}

	@Override
	public String getType() {
		return "FamilyHome";
	}
}