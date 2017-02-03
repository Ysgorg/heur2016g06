package src;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.color.ColorSpace;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;

import districtobjects.Bungalow;
import districtobjects.FamilyHome;
import districtobjects.Ground;
import districtobjects.Mansion;
import districtobjects.Placeable;
import districtobjects.Playground;
import districtobjects.Residence;
import districtobjects.Waterbody;

public class Groundplan {
	public static final double	WIDTH 						= 200;
	public static final double	HEIGHT 						= 170;
	private static final double	AREA 						= WIDTH * HEIGHT;
	private static final double	MINIMUM_WATER_PERCENTAGE 	= 0.2;
	private static final int	MAXIMUM_WATER_BODIES 		= 4;
	private static final double	FAMILYHOME_PERCENTAGE 		= 0.5;
	private static final double	BUNGALOW_PERCENTAGE 		= 0.3;
	private static final double	MANSION_PERCENTAGE			= 0.2;
	private static final double MAXIMUM_PLAYGROUND_DISTANCE = 50;

	private Ground ground;

	private ArrayList<Residence> residences;
	private ArrayList<Waterbody> waterbodies;
	private ArrayList<Playground> playgrounds;

	private int nFamilyHomes, nBungalows, nMansions, nHouses;
	private boolean playground;

	public Groundplan(int nrHouses, boolean playground){
		ground = new Ground(0, 0, WIDTH, HEIGHT);
		this.playground = playground;

		residences = new ArrayList<Residence>();
		waterbodies = new ArrayList<Waterbody>();
		playgrounds = new ArrayList<Playground>();

		nFamilyHomes = nBungalows = nMansions = 0;
		nHouses = nrHouses;
	}

	public double nHouses() {
		return nHouses;
	}

	public double getWidth() {
		return WIDTH;
	}

	public double getHeight() {
		return HEIGHT;
	}

	public void addResidence(Residence residence){
		if(residence.getType().equals("FamilyHome")){
			nFamilyHomes++;
		}else if(residence.getType().equals("Bungalow")){
			nBungalows++;
		}else if(residence.getType().equals("Mansion")){
			nMansions++;
		}
		residences.add(residence);
	}

	public void removeResidence(Residence residence) {
		if(residence.getType().equals("FamilyHome")){
			nFamilyHomes--;
		}else if(residence.getType().equals("Bungalow")){
			nBungalows--;
		}else if(residence.getType().equals("Mansion")){
			nMansions--;
		}
		residences.remove(residence);
	}

	@SuppressWarnings("unchecked")
	public ArrayList<Residence> getResidences(){
		return (ArrayList<Residence>) residences.clone();
	}

	public void addWaterBody(Waterbody waterBody){
		waterbodies.add(waterBody);
	}

	public void removeWaterBody(Waterbody water) {
		waterbodies.remove(water);
	}

	@SuppressWarnings("unchecked")
	public ArrayList<Waterbody> getWaterBodies(){
		return (ArrayList<Waterbody>) waterbodies.clone();
	}

	public void addPlayground(Playground playground){
		playgrounds.add(playground);
	}

	public void removePlayground(Playground playground) {
		playgrounds.remove(playground);
	}

	@SuppressWarnings("unchecked")
	public ArrayList<Playground> getPlaygrounds(){
		return (ArrayList<Playground>) playgrounds.clone();
	}

	public boolean checkPlaygrounds() {
		return playground;
	}

	public boolean isValid(){
		if(waterbodies.size() > MAXIMUM_WATER_BODIES /*|| 
		   ((double) nFamilyHomes / nHouses) != FAMILYHOME_PERCENTAGE ||
		   ((double) nBungalows / nHouses) != BUNGALOW_PERCENTAGE || 
		   ((double) nMansions / nHouses) != MANSION_PERCENTAGE*/) {
			return false;
		}else{
			double waterSurfaceArea = 0;

			for(Waterbody waterbody : waterbodies) {
				if(!waterbody.correctRatio() || !isCorrectlyPlaced(waterbody)) {
					return false;
				} else {
					waterSurfaceArea += waterbody.getWidth() * waterbody.getHeight();
				}
			}

			if((double) waterSurfaceArea / AREA < MINIMUM_WATER_PERCENTAGE){
				return false;
			}

			for(Residence residence : residences){
				if(!isCorrectlyPlaced(residence)){
					return false;
				}
			}
		}
		return true;
	}

	public boolean isCorrectlyPlaced(Placeable placeable){
		if(isOutOfBounds(placeable)){
			return false;
		}

		if(placeable instanceof Residence){
			if(placeable.leftEdge() < ((Residence) placeable).getMinimumDistance() || 
					placeable.rightEdge() > ground.rightEdge() - ((Residence) placeable).getMinimumDistance() || 
					placeable.topEdge() < ((Residence) placeable).getMinimumDistance() || 
					placeable.bottomEdge() > ground.bottomEdge() - ((Residence) placeable).getMinimumDistance()){
				return false;
			}
		}

		for(Waterbody waterBody : waterbodies){
			if(placeable != waterBody && 
					placeable.leftEdge() < waterBody.rightEdge() && 
					placeable.rightEdge() > waterBody.leftEdge() && 
					placeable.topEdge() < waterBody.bottomEdge() && 
					placeable.bottomEdge() > waterBody.topEdge()){
				return false;
			}
		}

		boolean inRange = false;
		for(Playground playground : playgrounds){
			if(placeable != playground && 
					placeable.leftEdge() < playground.rightEdge() && 
					placeable.rightEdge() > playground.leftEdge() && 
					placeable.topEdge() < playground.bottomEdge() && 
					placeable.bottomEdge() > playground.topEdge()){
				return false;
			} else if(placeable instanceof Residence && 
					placeable != playground){
				if(getDistance(placeable, playground) < ((Residence) placeable).getMinimumDistance()){
					return false;	
				}else if(getDistance(placeable, playground) < MAXIMUM_PLAYGROUND_DISTANCE){
					inRange = true;
				}
			}
		}

		if(playground && placeable instanceof Residence && !inRange){
			return false;
		}

		for(Residence other : residences){
			if(placeable != other && 
					placeable.leftEdge() < other.rightEdge() && 
					placeable.rightEdge() > other.leftEdge() && 
					placeable.topEdge() < other.bottomEdge() && 
					placeable.bottomEdge() > other.topEdge()){
				return false;
			} else if(placeable instanceof Residence && 
					placeable != other && 
					(getDistance((Residence) placeable, other) < ((Residence) placeable).getMinimumDistance() || 
							getDistance(other,(Residence) placeable) < other.getMinimumDistance())){
				return false;
			}
		}
		return true;
	}

	public double getResidenceValue(Residence residence){
		double value = 0;

		if(!isOutOfBounds(residence)){
			value += residence.getValue();
		}

		double distance = getValueDistance(residence);
		double valueIncrease = residence.getAddedValuePercentage() * value;

		value += (Math.max((int)distance - residence.getMinimumDistance(),0)) * valueIncrease;

		return value;
	}

	public double getPlanValue(){
		double value = 0;

		try {
			for(Residence residence : residences){
				if(!isOutOfBounds(residence)){
					value += getResidenceValue(residence);
				}
			}

			for(Playground playground : playgrounds){
				value -= playground.getCost();
			}

		} catch (Exception e) {System.out.println("Caught uncaught exception...");}

		return value;
	}

	public boolean isCheckPlaygrounds() {
		return playground;
	}

	public boolean isOutOfBounds(Placeable placeable) {
		if(placeable.rightEdge() > ground.rightEdge() || 
				placeable.leftEdge() < ground.leftEdge() || 
				placeable.topEdge() < ground.topEdge() || 
				placeable.bottomEdge() > ground.bottomEdge()){
			return true;	
		}
		return false;
	}

	public double getPlanCummulativeDistance(){
		double value = 0;
		for(Residence residence : residences){
			value += getValueDistance(residence);
		}
		return value;
	}

	public double getValueDistance(Residence residence){
		double minimum = residence.leftEdge();

		if(residence.topEdge() < minimum){
			minimum = residence.topEdge();
		}
		if(ground.rightEdge() - residence.rightEdge() < minimum){
			minimum = ground.rightEdge() - residence.rightEdge();
		}
		if(ground.bottomEdge() - residence.bottomEdge() < minimum){
			minimum = ground.bottomEdge() - residence.bottomEdge();
		}

		for(Residence other : residences){
			if(residence != other){
				double d = getDistance(residence, other);
				if(d < minimum){
					minimum = d;
				}
			}
		}

		for(Playground other : playgrounds){
			double d = getDistance(residence, other);
			if(d < minimum){
				minimum = d;
			}
		}

		return minimum;
	}

	public double getDistance(Placeable residence, Placeable other){
		double distance = 0;
		if(residence != other){
			if(residence.leftEdge() <= other.rightEdge()
					&& residence.rightEdge() >= other.leftEdge()
					&& residence.topEdge() <= other.bottomEdge()
					&& residence.bottomEdge() >= other.topEdge()){
				return 0;
			}else if(residence.leftEdge() < other.rightEdge()
					&& residence.rightEdge() > other.leftEdge()
					&& residence.topEdge() > other.bottomEdge()){
				distance = residence.topEdge() - other.bottomEdge();
			}else if(residence.leftEdge() < other.rightEdge()
					&& residence.rightEdge() > other.leftEdge()
					&& residence.bottomEdge() < other.topEdge()){
				distance = other.topEdge() - residence.bottomEdge();
			}else if(residence.bottomEdge() > other.topEdge()
					&& residence.topEdge() < other.bottomEdge()
					&& residence.rightEdge() < other.leftEdge()){
				distance = other.leftEdge() - residence.rightEdge();
			}else if(residence.bottomEdge() > other.topEdge()
					&& residence.topEdge() < other.bottomEdge()
					&& residence.leftEdge() > other.rightEdge()){
				distance = residence.leftEdge() - other.rightEdge();
			}else if(residence.rightEdge() > other.leftEdge()
					&& residence.topEdge() < other.bottomEdge()){
				distance = Math.sqrt(Math.pow(residence.leftEdge() - other.rightEdge(),2) + Math.pow(other.topEdge() - residence.bottomEdge(),2));
			}else if(residence.leftEdge() < other.rightEdge()
					&& residence.topEdge() < other.bottomEdge()){
				distance = Math.sqrt(Math.pow(other.leftEdge() - residence.rightEdge(),2) + Math.pow(other.topEdge() - residence.bottomEdge(),2));
			}else if(residence.rightEdge() > other.leftEdge()
					&& residence.bottomEdge() > other.topEdge()){
				distance = Math.sqrt(Math.pow(residence.leftEdge() - other.rightEdge(),2) + Math.pow(residence.topEdge() - other.bottomEdge(),2));
			}else if(residence.leftEdge() < other.rightEdge()
					&& residence.bottomEdge() > other.topEdge()){
				distance = Math.sqrt(Math.pow(other.leftEdge() - residence.rightEdge(),2) + Math.pow(residence.topEdge() - other.bottomEdge(),2));
			}
		}else{
			distance = java.lang.Double.MAX_VALUE;
		}
		return distance;
	}

	public void saveToImage(String filename, int width, int height, int scale, int marginleft, int margintop){
		Image image = new BufferedImage(width, height, ColorSpace.TYPE_RGB);

		Graphics g = image.getGraphics();
		g.setColor(Color.WHITE);
		g.fillRect(0, 0, width, height);

		g.setColor(Color.DARK_GRAY);
		g.drawRect(marginleft-1, margintop-1, (int)(width * scale) +2, (int)(height * scale) +2);
		g.drawRect(marginleft-2, margintop-2, (int)(width * scale) +4, (int)(height * scale) +4);
		setPlan(g, scale, marginleft, margintop);

		File outputFile;
		if(filename.isEmpty()){
			outputFile = new File("images/groundplan-"+System.currentTimeMillis()+".png");
		}else{
			outputFile = new File(filename);
		}
		try {
			ImageIO.write((RenderedImage) image, "png", outputFile);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected void setPlan(Graphics g, int scale, int marginleft, int margintop){
		Graphics2D g2d = (Graphics2D) g;
		for(Waterbody waterbody : this.getWaterBodies()){
			g2d.setColor(Color.BLUE);
			g2d.fillRect((int)((waterbody.getX()*scale)+0.5+marginleft),(int)((waterbody.getY()*scale)+0.5+margintop), (int)((waterbody.getWidth()*scale)+0.5), (int)((waterbody.getHeight()*scale)+0.5));
			g2d.setColor(Color.BLUE.darker());
			g2d.drawRect((int)((waterbody.getX()*scale)+0.5+marginleft),(int)((waterbody.getY()*scale)+0.5+margintop), (int)((waterbody.getWidth()*scale)+0.5), (int)((waterbody.getHeight()*scale)+0.5));
		}
		for(Playground playground : this.getPlaygrounds()){
			g2d.setColor(Color.GREEN);
			g2d.fillRect((int)((playground.getX()*scale)+0.5+marginleft),(int)((playground.getY()*scale)+0.5+margintop), (int)((playground.getWidth()*scale)+0.5), (int)((playground.getHeight()*scale)+0.5));
			g2d.setColor(Color.GREEN.darker());
			g2d.drawRect((int)((playground.getX()*scale)+0.5+marginleft),(int)((playground.getY()*scale)+0.5+margintop), (int)((playground.getWidth()*scale)+0.5), (int)((playground.getHeight()*scale)+0.5));
		}

		for(Residence residence : this.getResidences()){
			if(residence instanceof Mansion){
				g2d.setColor(Color.CYAN);
				g2d.fillRect((int)((residence.getX()*scale)+0.5+marginleft),(int)((residence.getY()*scale)+0.5+margintop), (int)((residence.getWidth()*scale)+0.5), (int)((residence.getHeight()*scale)+0.5));
				g2d.setColor(Color.CYAN.darker());
				g2d.drawRect((int)((residence.getX()*scale)+0.5+marginleft),(int)((residence.getY()*scale)+0.5+margintop), (int)((residence.getWidth()*scale)+0.5), (int)((residence.getHeight()*scale)+0.5));
			}
		}

		for(Residence residence : this.getResidences()){
			if(residence instanceof Bungalow){
				g2d.setColor(Color.MAGENTA);
				g2d.fillRect((int)((residence.getX()*scale)+0.5+marginleft),(int)((residence.getY()*scale)+0.5+margintop), (int)((residence.getWidth()*scale)+0.5), (int)((residence.getHeight()*scale)+0.5));
				g2d.setColor(Color.MAGENTA.darker());
				g2d.drawRect((int)((residence.getX()*scale)+0.5+marginleft),(int)((residence.getY()*scale)+0.5+margintop), (int)((residence.getWidth()*scale)+0.5), (int)((residence.getHeight()*scale)+0.5));
			}
		}

		for(Residence residence : this.getResidences()){
			if(residence instanceof FamilyHome){
				g2d.setColor(Color.ORANGE);
				g2d.fillRect((int)((residence.getX()*scale)+0.5+marginleft),(int)((residence.getY()*scale)+0.5+margintop), (int)((residence.getWidth()*scale)+0.5), (int)((residence.getHeight()*scale)+0.5));
				g2d.setColor(Color.ORANGE.darker());
				g2d.drawRect((int)((residence.getX()*scale)+0.5+marginleft),(int)((residence.getY()*scale)+0.5+margintop), (int)((residence.getWidth()*scale)+0.5), (int)((residence.getHeight()*scale)+0.5));
			}
		}
	}
}
