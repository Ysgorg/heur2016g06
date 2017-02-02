package src;

public class DistrictPlanner {
	private static boolean PLAYGROUND = false;
	private static int NR_HOUSES = 40;	
	
	GroundplanFrame frame;
	
	public DistrictPlanner() {
		frame = new GroundplanFrame();
		Groundplan plan = new Groundplan(NR_HOUSES, PLAYGROUND);
		
		// your code
		
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

	public static void main(String[] args) {
		new DistrictPlanner();
	}
}
