import java.awt.*;
import java.awt.event.*;
import java.awt.geom.AffineTransform;
import java.io.*;
import java.net.*;
import javax.swing.*;

public class Client1 extends JFrame {
    private Image cat, dog, power;
    private Image dog1, dog2;
    private Image background;
    private Image bone, fishbone;
    private Image direction;
    private long pressStartTime; // 紀錄按下的時間
    private Socket socket;
    private DataOutputStream outStream;
    private DataInputStream inStream;
    private Timer powerTimer;
    private Timer dogAnimationTimer;
    private Timer animationTimer;
    private int player, powerHeight, dog_state = 0;
    private int up_power, wind = 0, next_wind = 0;
    // private int cat_blood = 5, dog_blood = 5;
    private GamePanel gamePanel;
    private double initialVelocity;
    private double angle;
    private double time;
    private int boneX, boneY;
    // private boolean hitCat=false,hitDog=false;

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Client1());
    }

    public Client1() {
        super("work28_User1");
        setSize(700, 460);
        int width = 100, height = 100;

        // 載入圖片
        cat = Toolkit.getDefaultToolkit().getImage(getClass().getResource("cat.png"));
        dog = Toolkit.getDefaultToolkit().getImage(getClass().getResource("dog.png"));
        power = Toolkit.getDefaultToolkit().getImage(getClass().getResource("block.png"));
        dog1 = Toolkit.getDefaultToolkit().getImage(getClass().getResource("dog_throw_1.png"));
        dog2 = Toolkit.getDefaultToolkit().getImage(getClass().getResource("dog_throw_2.png"));
        background = Toolkit.getDefaultToolkit().getImage(getClass().getResource("background.png"));
        bone = Toolkit.getDefaultToolkit().getImage(getClass().getResource("bone.png"));
        fishbone = Toolkit.getDefaultToolkit().getImage(getClass().getResource("fishbone.png"));
        direction = Toolkit.getDefaultToolkit().getImage(getClass().getResource("direction.png"));
        // 調整圖片大小
        cat = cat.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        dog = dog.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        power = power.getScaledInstance(width / 2, height / 2, Image.SCALE_SMOOTH);
        dog1 = dog1.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        dog2 = dog2.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        background = background.getScaledInstance(700, 460, Image.SCALE_SMOOTH);
        bone = bone.getScaledInstance(width / 2, height / 2, Image.SCALE_SMOOTH);
        fishbone = fishbone.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        direction = direction.getScaledInstance(100, 50, Image.SCALE_SMOOTH);
        // 啟用滑鼠事件監聽
        enableEvents(AWTEvent.MOUSE_EVENT_MASK);

        try {
            // 連接伺服器
            socket = new Socket("127.0.0.1", 1235);
            outStream = new DataOutputStream(socket.getOutputStream());
            inStream = new DataInputStream(socket.getInputStream());
            System.out.println("Connected to server.");

        } catch (IOException e) {
            e.printStackTrace();
        }

        // 計時器處理動畫
        powerTimer = new Timer(200, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                powerHeight += 10;
                repaint();
            }
        });

        // 初始化 dogAnimationTimer
        dogAnimationTimer = new Timer(500, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                dog_state = 0; // 切換回原本的 dog 動畫
                gamePanel.repaint();
            }
        });
        dogAnimationTimer.setRepeats(false); // 設定 Timer 只執行一次

        // 初始化動畫計時器
        animationTimer = new Timer(15, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                gamePanel.repaint();
            }
        });

        // 啟動執行緒，處理接收伺服器回傳值
        Thread receiveThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        // 接收伺服器的回應並印出
                        String response = inStream.readUTF();
                        wind = inStream.readInt();
                        player = Character.getNumericValue(response.charAt(0));
                        up_power = Integer.parseInt(response.substring(2));
                        System.out.println("Server response: " + response);
                        System.out.println(wind);
                        // 設定拋物線相關參數
                        if (player == 1)
                            initialVelocity = Math
                                    .sqrt(Math.pow(up_power * 0.05, 2) + Math.pow(-next_wind * 5 + up_power * 0.05, 2));
                        else if (player == 2)
                            initialVelocity = Math
                                    .sqrt(Math.pow(up_power * 0.05, 2) + Math.pow(next_wind * 5 + up_power * 0.05, 2));
                        System.out.print(initialVelocity);
                        angle = Math.toRadians(45); // 45度角
                        time = 0;
                        if (player == 1)
                            boneX = 510; // 起始位置
                        else if (player == 2)
                            boneX = 80;
                        boneY = 300;
                        // 啟動動畫計時器
                        animationTimer.start();
                        next_wind = wind;

                    } catch (IOException ex) {
                        ex.printStackTrace();
                        break; // 當伺服器斷開連接時，跳出迴圈結束執行緒
                    }
                }
            }
        });
        receiveThread.start();

        // 創建遊戲面板
        gamePanel = new GamePanel();
        add(gamePanel);

        // 滑鼠事件處理
        addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                pressStartTime = System.currentTimeMillis();
                powerTimer.start();
                dog_state = 1; // 切換dog動畫
            }

            public void mouseReleased(MouseEvent e) {
                long pressDuration = System.currentTimeMillis() - pressStartTime;
                System.out.println("Mouse pressed duration: " + pressDuration + " milliseconds");

                try {
                    // 送出識別值至伺服器
                    outStream.writeInt(1);
                    outStream.flush();
                    // 送出整數時間至伺服器
                    outStream.writeInt((int) pressDuration);
                    outStream.flush();
                    System.out.println("Data sent to server.");

                } catch (IOException ex) {
                    ex.printStackTrace();
                } finally {
                    // 停止計時器並重設 power 的高度，重新繪製遊戲面板
                    powerTimer.stop();
                    powerHeight = 0;
                    dog_state = 2;// 切換dog動畫
                    gamePanel.repaint();

                    // 啟動 dogAnimationTimer，延遲 0.5 秒後切換回原本的 dog 動畫
                    dogAnimationTimer.restart();
                }
            }
        });

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    // 內部類，用於繪製遊戲元素
    private class GamePanel extends JPanel {

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;

            // 繪製圖片和動畫
            g.drawImage(background, 0, 0, this);
            g.drawImage(cat, 80, 300, this);
            if (dog_state == 1) { // 狗動畫處理
                g.drawImage(dog1, 510, 300, this);
            } else if (dog_state == 2) {
                g.drawImage(dog2, 510, 300, this);
            } else {
                g.drawImage(dog, 510, 300, this);
            }
            if (powerHeight > 0) {
                // 由下往上長的動畫
                g.drawImage(power, 610, 385 - powerHeight, 20, powerHeight, this);
            }
            // 拋物線動畫
            if (boneY <= 350 && boneY > 100 && player == 1) {
                g2d.drawImage(bone, boneX, boneY, this);

                // 根據物理模型計算新的位置
                double x = initialVelocity * Math.cos(angle) * time;
                double y = initialVelocity * Math.sin(angle) * time - 0.5 * 9.8 * time * time;
                boneX = 510 - (int) x; // 起始位置偏移
                boneY = 300 - (int) y;
                time += 0.1;
                // 檢查是否碰撞到 cat
                Rectangle boneRect = new Rectangle(boneX, boneY, bone.getWidth(null), bone.getHeight(null));
                Rectangle catRect = new Rectangle(80, 300, cat.getWidth(null), cat.getHeight(null));

                if (boneRect.intersects(catRect)) {
                    System.out.println("Bone hit the cat!");
                    // hitCat=true;
                }
            } else if (boneY <= 350 && boneY > 100 && player == 2) { // 魚刺飛行
                g2d.drawImage(fishbone, boneX, boneY, this);
                // 根據物理模型計算新的位置
                double x = initialVelocity * Math.cos(angle) * time;
                double y = initialVelocity * Math.sin(angle) * time - 0.5 * 9.8 * time * time;
                boneX = 80 + (int) x; // 起始位置偏移
                boneY = 300 - (int) y;
                time += 0.1;
                Rectangle fishboneRect = new Rectangle(boneX, boneY, fishbone.getWidth(null), fishbone.getHeight(null));
                Rectangle dogRect = new Rectangle(510, 300, dog.getWidth(null), dog.getHeight(null));

                if (fishboneRect.intersects(dogRect)) {
                    System.out.println("fishBone hit the dog!");
                    // hitDog=true;
                }

            } else {
                // 停止動畫計時器
                animationTimer.stop();
            }
            if (wind != 0) {
                // 設定變換
                AffineTransform transform = new AffineTransform();
                transform.translate(350, 100);
                if (wind < 0) {
                    transform.rotate(Math.toRadians(180));
                }

                // 根據 wind 動態調整圖片寬度
                double scale = Math.abs(wind) / (double) direction.getWidth(null) * 10;
                transform.scale(scale, 1.0);

                transform.translate(-direction.getWidth(null) / 2, -direction.getHeight(null) / 2);

                // 套用變換
                g2d.drawImage(direction, transform, null);
            }
            /*
             * if(hitCat){
             * cat_blood--;
             * System.out.println(cat_blood);
             * hitCat=false;
             * }
             * if(hitDog){
             * dog_blood--;
             * System.out.println(dog_blood);
             * hitDog=false;
             * }
             */

        }
    }
}
