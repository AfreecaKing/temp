import java.net.*;
import java.io.*;
import java.util.*;

public class Server28 {
     private static ServerSocket SSocket;
     private static int port;
     private Hashtable<Socket, DataOutputStream> ht = new Hashtable<>();
     private Socket socket;

     // FlagContainer 封裝了 flag 變數
     public static class FlagContainer {
          private boolean flag = true;

          public boolean getFlag() {
               return flag;
          }

          public void setFlag(boolean flag) {
               this.flag = flag;
          }
     }

     private FlagContainer flagContainer = new FlagContainer();

     public Server28() throws IOException {
          try {
               SSocket = new ServerSocket(port);
               System.out.println("Server created.");
               System.out.println("Waiting for clients to connect...");

               while (true) {
                    socket = SSocket.accept();
                    System.out.println("Connected from Client " + socket.getInetAddress().getHostAddress());
                    DataOutputStream outstream = new DataOutputStream(socket.getOutputStream());
                    ht.put(socket, outstream);

                    // 將 FlagContainer 實例傳遞給 ServerThread
                    Thread thread = new Thread(new ServerThread(socket, ht, flagContainer));
                    thread.start();
               }
          } catch (IOException ex) {
               ex.printStackTrace();
          }
     }

     public static void main(String[] args) throws Exception {
          port = 1235;
          Server28 ServerStart = new Server28();
     }
}

class ServerThread extends Thread implements Runnable {
     private Socket socket;
     private Hashtable<Socket, DataOutputStream> ht;
     private Server28.FlagContainer flagContainer;

     public ServerThread(Socket socket, Hashtable<Socket, DataOutputStream> ht, Server28.FlagContainer flagContainer) {
          this.socket = socket;
          this.ht = ht;
          this.flagContainer = flagContainer;
     }

     public void run() {
          DataInputStream instream;
          int wind;
          try {
               instream = new DataInputStream(socket.getInputStream());
               while (true) {
                    int client_number = instream.readInt();
                    int press_time = instream.readInt();
                    int time = 0;
                    System.out.println("Client: " + client_number);
                    Random random = new Random();
                    wind = random.nextInt(10 - (-10) + 1) - 10;
                    synchronized (ht) {
                         for (DataOutputStream outstream : ht.values()) {
                              try {

                                   // 使用 FlagContainer 中的 flag
                                   if (client_number == 1 && flagContainer.getFlag()) {
                                        if (time == 1)
                                             flagContainer.setFlag(false);
                                        outstream.writeUTF("1:" + press_time);
                                        outstream.flush();
                                        outstream.writeInt(wind);
                                        outstream.flush();
                                        System.out.println("Response sent");
                                   } else if (client_number == 2 && !flagContainer.getFlag()) {
                                        if (time == 1)
                                             flagContainer.setFlag(true);
                                        outstream.writeUTF("2:" + press_time);
                                        outstream.flush();
                                        outstream.writeInt(wind);
                                        outstream.flush();
                                        System.out.println("Response sent");
                                   }
                                   // System.out.println(time + " " + flagContainer.getFlag());

                              } catch (IOException ex) {
                                   ex.printStackTrace();
                              }
                              time++;
                         }
                    }
               }
          } catch (IOException ex) {
               // 處理 IOException
          } finally {
               synchronized (ht) {
                    System.out.println("Remove connection: " + socket);
                    ht.remove(socket);
                    try {
                         socket.close();
                    } catch (IOException ex) {
                         ex.printStackTrace();
                    }
               }
          }
     }
}
