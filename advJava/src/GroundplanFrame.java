package src;

import java.awt.BorderLayout;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JScrollPane;

public class GroundplanFrame extends JFrame {
	private static final long serialVersionUID = -360885512080963508L;
	private Groundplan plan = null;
	private GroundplanCanvas groundplanCanvas = null;
	private JScrollPane scrollPane = null;

	public GroundplanFrame(){
		setTitle("Heuristieken 2016 - Amstelhaege!");
		setLayout(new BorderLayout());
		setSize(1024,768);
		setVisible(true);
		
		this.addWindowListener(new WindowAdapter(){
			@Override
			public void windowClosing(WindowEvent e) {
				super.windowClosing(e);
				System.exit(0);
			}
		});
		
		this.addKeyListener(new KeyAdapter() {
			
			@Override
			public void keyPressed(KeyEvent e) {
				super.keyPressed(e);
				if(e.getKeyCode() == KeyEvent.VK_ESCAPE){
					System.exit(0);
				}
			}
		});
	}
	
	public void repaint(){
		super.repaint();
		invalidate();
		validate();
	}

	public void setPlan(Groundplan plan) {
		this.plan = plan;
		if(scrollPane != null){
			remove(scrollPane);
		}
		
		groundplanCanvas = new GroundplanCanvas(plan);
		scrollPane = new JScrollPane(groundplanCanvas);
		scrollPane.setAutoscrolls(true);
		this.getContentPane().add(scrollPane);
		
		this.pack();
		
		this.invalidate();
		this.validate();
	}
}