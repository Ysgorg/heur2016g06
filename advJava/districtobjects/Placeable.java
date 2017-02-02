package districtobjects;

public abstract class Placeable {
	private double x;
	private double y;
	private double width;
	private double height;
	private boolean flipped = false;

	public Placeable(double x, double y, double width, double height) {
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
	}

	public double getX() {
		return x;
	}
	
	public void setX(double x) {
		this.x = x;
	}
	
	public double getY() {
		return y;
	}
	
	public void setY(double y) {
		this.y = y;
	}
	
	public void setWidth(double width) {
		this.width = width;
	}

	public double getWidth() {
		return width;
	}
	
	public void setHeight(double height) {
		this.height = height;
	}
	
	public double getHeight() {
		return height;
	}
	
	public double leftEdge(){
		return x;
	}
	
	public double rightEdge(){
		return x + width;
	}
	
	public double topEdge(){
		return y;
	}
	
	public double bottomEdge(){
		return y + height;
	}

	public boolean getOrientation() {
		return flipped;
	}

	public void flip() {
		if(flipped){
			flipped = false;
		}else{
			flipped = true;
		}
		
		double tmp = width;
		width = height;
		height = tmp;
	}
}