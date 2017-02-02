package src;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;

import javax.swing.JPanel;

public class GroundplanCanvas extends JPanel {
	private static final long serialVersionUID = 2544621875608225004L;
	public static final int MARGINLEFT = 25, MARGINTOP = 25;
	public static final int SCALE = 3;
	private Groundplan plan = null;
	private final JPanel canvas;
	
	private static int mouseX, mouseY;
	
	public GroundplanCanvas(Groundplan plan){
		this.setLayout(null);
		this.setPreferredSize(getPreferredSize());
		this.setSize(getPreferredSize());
		
		this.plan = plan;
		mouseX = 0;
		mouseY = 0;
		
		canvas = this;
		this.addMouseMotionListener(new MouseMotionAdapter(){

			@Override
			public void mouseMoved(MouseEvent e) {
				super.mouseMoved(e);
				GroundplanCanvas.mouseX = (e.getX() - MARGINLEFT) / SCALE;
				GroundplanCanvas.mouseY = (e.getY() - MARGINTOP) / SCALE;
				
				if(GroundplanCanvas.mouseX < 0
					|| GroundplanCanvas.mouseY < 0
					|| GroundplanCanvas.mouseX > Groundplan.WIDTH
					|| GroundplanCanvas.mouseY > Groundplan.HEIGHT){
					GroundplanCanvas.mouseX = -1;
					GroundplanCanvas.mouseY = -1;
				}
				
				canvas.invalidate();
			}
		});
			}
	
	@Override
	public Dimension getPreferredSize() {
		 return new Dimension((int)Groundplan.WIDTH*SCALE + 2*MARGINLEFT, (int)Groundplan.HEIGHT*SCALE+2*MARGINTOP);
	}
	
	public void paintComponent(Graphics g){
		super.paintComponent(g);
		Image image = createImage(this.getWidth(), this.getHeight());
		
		Graphics g2 = image.getGraphics();
		setBackground(Color.white);
		g2.setColor(Color.DARK_GRAY);
		g2.drawRect(GroundplanCanvas.MARGINLEFT-1, GroundplanCanvas.MARGINTOP-1, (int)(Groundplan.WIDTH * SCALE) +2, (int)(Groundplan.HEIGHT * SCALE) +2);
		g2.drawRect(GroundplanCanvas.MARGINLEFT-2, GroundplanCanvas.MARGINTOP-2, (int)(Groundplan.WIDTH * SCALE) +4, (int)(Groundplan.HEIGHT * SCALE) +4);
	    plan.setPlan(g2,SCALE,MARGINLEFT,MARGINTOP);
	    
	    g2.setColor(Color.black);
	    g2.setFont(Font.getFont("Verdana"));
	    String mX = mouseX >= 0 ? Integer.toString(mouseX) : "*";
	    String mY = mouseY >= 0 ? Integer.toString(mouseY) : "*";
	    g2.drawString("Mouse at: "+mX+", "+mY, 10, 20);
	    
	    double value = plan.getPlanValue();
	    g2.drawString("Plan Value: "+value, 150, 20);
	    
	    g.drawImage(image, 0, 0, this);
	}
}
