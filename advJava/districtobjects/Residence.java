package districtobjects;

public abstract class Residence extends Placeable {
	private final double value;
	private final double minimumDistance;
	private final double addedValuePercentage;
	
	public Residence(double width, double height, double value, double minimumDistance, double addedValuePercentage) {
		super(-1, -1, width, height);
		this.value = value;
		this.minimumDistance = minimumDistance;
		this.addedValuePercentage = addedValuePercentage;
	}

	public double getValue() {
		return value;
	}

	public double getAddedValuePercentage() {
		return addedValuePercentage;
	}

	public double getMinimumDistance() {
		return minimumDistance;
	}
	
	public abstract String getType();
}