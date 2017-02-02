package src;

import districtobjects.*;

public class Example {
	private static boolean PLAYGROUND = false;
	private static int NR_HOUSES = 888; // Whatever	

	GroundplanFrame frame;

	public Example() throws Exception {
		frame = new GroundplanFrame();
		Groundplan plan = planDistrict();

		int scale = 4;
		int marginleft = 10;
		int margintop = 10;
		plan.saveToImage(String.format(System.getProperty("user.dir") + "/images/plan" + System.currentTimeMillis() + ".png"), (int)Groundplan.WIDTH*scale + 4*marginleft, (int)Groundplan.HEIGHT*scale + 4*margintop, scale, 0, 0);
		frame.setPlan(plan);

		while(true){
			try {
				frame.repaint();
				Thread.sleep(50);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	public Groundplan planDistrict() throws Exception {
		Groundplan plan = new Groundplan(NR_HOUSES, PLAYGROUND);
		frame.setPlan(plan);

		double wBSize = Math.sqrt(170*200*0.2/4/4); // Size of ratio 1 of 4 water bodies

		double wB4Size = 4* wBSize; // Size of ratio 4

		double x = 0;
		double bunY = 3; // Minimum distance of bungalow

		for (int i = 0, count = 4; i < count; i++) { // Creates the 4 water bodies + bungalows in between
			Waterbody wb = new Waterbody(x, 0, wBSize, wB4Size);
			plan.isCorrectlyPlaced(wb);
			plan.addWaterBody(wb);

			Bungalow bun = new Bungalow(wBSize + x, bunY);

			if (i < 3) { // Disable the last bungalow row
				for( int j = 0, countJ = 6; j < countJ; j++) { // Place bungalows between water
					bun = new Bungalow(wBSize + x, bunY);
					bun.flip();
					plan.addResidence(bun);

					bunY += 10 + 3;
				}
			}

			x = bun.getX()+bun.getWidth();
			bunY = 3;
		}

		frame.repaint(); Thread.sleep(100); // Repainting can throw errors when done too quickly

		double ss = 0.5; // StepSize
		x = 3;
		double y = 3;
		double maxX = 200 - 7.9;
		double maxY = 170 - 7.9;

		while (x < maxX) {

			while (y < maxY) {
				FamilyHome fam = new FamilyHome(x,y);

				if (plan.isCorrectlyPlaced(fam)) {
					plan.addResidence(fam);

					Thread.sleep(100);frame.repaint(); // Repainting can throw errors when done too quickly
				}

				y += ss;
			}

			//try {Thread.sleep(50);frame.repaint();} catch (InterruptedException e) {} // Repainting can throw errors when done too quickly
			y = 0;
			x += ss;
		}

		System.out.println("Is Plan Valid? " + plan.isValid());

		frame.setPlan(plan);
		try {
			frame.repaint();
			Thread.sleep(100);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		return plan;
	}

	public static void main(String[] args) {
		try {
			new Example();
		} catch (Exception e) {
			//Do nothing with exception...
		}
	}
}