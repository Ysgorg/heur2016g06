package src;

import districtobjects.*;

public class AdvNoPlay {
	private static boolean PLAYGROUND = false;
	private static int NR_HOUSES = 888; // Whatever	

	GroundplanFrame frame;

	public AdvNoPlay() throws Exception {
		frame = new GroundplanFrame();
		Groundplan plan = planDistrict();

		int scale = 4;
		int marginleft = 10;
		int margintop = 10;
		plan.saveToImage(String.format(System.getProperty("user.dir") + "/images/plan" + System.currentTimeMillis() + ".png"), (int)Groundplan.WIDTH*scale + 4*marginleft, (int)Groundplan.HEIGHT*scale + 4*margintop, scale, 0, 0);
		frame.setPlan(plan);

		while (true) {
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
		double bungX = 3;
		double bungY = 170 - 3 - 10;
		double extraClearance = 0;

		for (int i = 0, count = 17; i < count; i++) { //////////// This places bottom row of bungalows.
			if (i > 12) {
				extraClearance = 1;

				bungY = 170 - 3 - 10 - extraClearance;
				bungX += extraClearance;
			}

			Bungalow bun = new Bungalow(bungX, bungY);
			plan.addResidence(bun);
			bun.flip();

			bungX += 7.5 + 3;
		}

		bungX = 200 - 3 - 10;
		bungY = 3;
		extraClearance = 0; // The extra clearance is to improve the usage of space in the bottom right
		// As there is unused space at Right of plan, these bungalows will fill up:
		for (int i = 0, count = 15; i < count; i++) { ///////// This places right row of bungalows TODO ORIGINAL 15 
			if (i > 7) {
				if (i < 9 || i > 10) {
					extraClearance = 1;
				} else {
					extraClearance = 2;
				}

				bungX = 200 - 3 - 10 - extraClearance;
				bungY += extraClearance;
			}

			Bungalow bun = new Bungalow(bungX, bungY);
			plan.addResidence(bun);

			bungY += 7.5 + 3;
		}

		System.out.println(plan.isValid() + " Value of plan is: " + plan.getPlanValue());


		x = 3; // 3 is minimum distance of bungalow
		y = 3;
		FamilyHome fam = new FamilyHome(0,0);
		while (x < maxX) { ///////////////// This places all family houses

			while (y < maxY) {
				fam = new FamilyHome(x,y);

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
			new AdvNoPlay();
		} catch (Exception e) {
			//Do nothing with exception...
		}
	}
}