package Vision;

import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;

public class VisionServer extends Thread {

    public static final int PORT = 5801;

    ServerSocket srvSocket;

    public static void main(String[] args)
    {
        new VisionServer();
    }

    public VisionServer() {       
        start();
    }

    @Override
    public void run() {
        InetAddress addr;
        try {
            addr = InetAddress.getLocalHost();
        } catch (UnknownHostException e2) {
            addr = null;
            e2.printStackTrace();
		}
        while(true) {
           try {
                srvSocket = new ServerSocket(PORT,2,addr);
                System.out.println("Server listen on " + addr + " on port " + PORT);
                while(true) {
                    Socket s = srvSocket.accept();
                    System.out.println("Server accept " + s.getInetAddress());
                    new SocketHandlerTask(s);
                }
            } catch (Exception e) {
                try {
                    srvSocket.close();
                } catch (Exception e1) {}
            }
        }
    }
}