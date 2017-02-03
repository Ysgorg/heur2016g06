package districtobjects;

public class Waterbody extends Placeable {

	public Waterbody(double x, double y, double width, double height) {
		super(x, y, width, height);
	}

	public Waterbody(Waterbody water) {
		super(water.getX(), water.getY(), water.getWidth(), water.getHeight());
	}
	
	public boolean correctRatio() {
		double longSide = Math.max(getWidth(), getHeight());
		double shortSide = Math.min(getWidth(), getHeight());
		
		return shortSide * 4 >= longSide; 
	}
}