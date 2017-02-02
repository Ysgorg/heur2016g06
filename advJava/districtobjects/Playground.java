package districtobjects;

public class Playground extends Placeable {
	public static final double COST = 500000;
	
	public Playground(){
		super(-1, -1, 30, 20);
	}
	
	public Playground(double x, double y) {
		super(x, y, 30, 20);
	}

	public Playground(Playground playground) {
		super(playground.getX(), playground.getY(), 30, 20);
	}

	public double getCost() {
		return COST;
	}
}
