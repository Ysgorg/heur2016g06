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
		int sleepTime = 500; // Time between 
		double ss = 0.5; // StepSize

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

		Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly

		double maxX = 200 - 7.5; // 7.5 minimum house dimension.
		double maxY = 170 - 7.5;
		double y = maxY;
		x = 3;

		// As there is unused space at bottom of plan, these bungalows will fill up:
		while (y > 0) { //////////// This places bottom row of bungalows.
			boolean rowPlaced = false;

			while (x < maxX) {
				Bungalow bun = new Bungalow(x,y);
				bun.flip();

				if (plan.isCorrectlyPlaced(bun)) {
					plan.addResidence(bun);
					rowPlaced = true;

					//Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly
				}

				x += ss;
			}

			if (rowPlaced) {
				Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly
				break;
			}

			x = 3;
			y -= ss;
		}

		y = 0;
		x = maxX;

		// As there is unused space at bottom of plan, these bungalows will fill up:
		while (x > 0) { ///////// This palces right row of bungalows
			boolean rowPlaced = false;

			while (y < maxY) {
				Bungalow bun = new Bungalow(x,y);

				if (plan.isCorrectlyPlaced(bun)) {
					plan.addResidence(bun);
					rowPlaced = true;

					//Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly
				}

				y += ss;
			}

			if (rowPlaced)
				break;

			Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly
			y = 3;
			x -= ss;
		}


		x = 3; // 3 is minimum distance of bungalow
		y = 3;

		while (x < maxX) { ///////////////// This places all family houses

			while (y < maxY) {
				FamilyHome fam = new FamilyHome(x,y);

				if (plan.isCorrectlyPlaced(fam)) {
					plan.addResidence(fam);

					//Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly
				}

				y += ss;
			}

			Thread.sleep(sleepTime);frame.repaint(); // Repainting can throw errors when done too quickly
			y = 0;
			x += ss;
		}

		if (plan.isValid())
		{
			System.out.println("Plan is valid.");
			System.out.println("Plan value: " + plan.getPlanValue());
		} else {
			System.out.println("Plan is invalid!");
		}

		frame.setPlan(plan);
		Thread.sleep(2000); // Sleep enough to make sure plan is finished setting.
		frame.repaint();

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