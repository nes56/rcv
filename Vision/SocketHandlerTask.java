package Vision;

import java.io.EOFException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonStreamParser;

public class SocketHandlerTask extends Thread {

    public Socket socket;
    public boolean isFront;

    Gson gson;
    JsonStreamParser parser;
    InputStream is;

    VisionData visionData;
    static final boolean USE_JSON = false;

    public SocketHandlerTask(Socket socket) {
        super();
        this.socket = socket;
        try {
            socket.setSoTimeout(0);
        } catch (Exception e) {
        }
        gson = new Gson();
        try {
            is = socket.getInputStream();
            // parser = new JsonStreamParser(new
            // InputStreamReader(socket.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }
        start();
    }

    void processWithOPrint() throws Exception {
        char[] buf = new char[1024];
        int nCurl = 0;
        int pos = 0;
        while(true) {
            int i = is.read();
            char c = (char)i;
            System.out.print(c);
            if(c == '{') {
                nCurl++;
            }
            if(nCurl > 0) {
                buf[pos++] = c;
            }
            if(c == '}') {
                nCurl --;
                if(nCurl == 0) {
                    String str = new String(buf,0,pos);
//                    System.out.println("VIS: " + str);
                    parser = new JsonStreamParser(str);
                    JsonElement element = parser.next();
                    visionData = gson.fromJson(element, VisionData.class);
                    // change distance to mm from cm
                    visionData.p1.d *= 10;
                    visionData.p2.d *= 10;
                    isFront = visionData.front;                    
                    visionData.set();
                    return;
                }
            }  
        }
    }

    @Override
    public void run() {
        System.out.println("is connected = " + socket.isConnected());
        boolean isFront = true;
        while (socket != null && socket.isConnected()) {
            try {
                // processJson();
                processWithOPrint();
            } catch (Exception ex) {
                System.out.println("error in parse data  " + ex);
                if (socket.isInputShutdown() || socket.isClosed() || !socket.isConnected()
                        || ex instanceof EOFException) {                    
                    try {
                        socket.close();
                    } catch (Exception e2) {
                    }
                    break;
                }
            }
        }
    }

    void processJson() {
        JsonElement element = parser.next();
        visionData = gson.fromJson(element, VisionData.class);
        isFront = visionData.front;        
        visionData.set();
    }
}