import java.net.*;
import java.io.*;

public class TestSOAPClient {

    public final static String DEFAULT_SERVER = "http://sicredi.fluidsystem.com.br/homologacao/webservice/process";
    public final static String SOAP_ACTION = "http://sicredi.fluidsystem.com.br/homologacao/webservice/process/#dados";
    public final static String CHARSET = "UTF-8";

    public static void main(String[] args) {

        if (args.length == 0) {
            System.out.println("Usage: java TestSOAPClient processo chave url");
            return;
        }
        String input = args[0];
        String chave = args[1];
        String server = DEFAULT_SERVER;
        if (args.length >= 3)
            server = args[2];

        try {
            URL u = new URL(server);
            URLConnection uc = u.openConnection();
            HttpURLConnection connection = (HttpURLConnection) uc;

            connection.setDoOutput(true);
            connection.setDoInput(true);
            connection.setRequestProperty("Accept-Charset", CHARSET);
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded;charset=" + CHARSET);
            connection.setRequestProperty("User-Agent", "FluidnowSOAPClient 1.0");
            connection.setRequestMethod("POST");
            connection.setRequestProperty("SOAPAction", SOAP_ACTION);

            OutputStream out = connection.getOutputStream();
            Writer wout = new OutputStreamWriter(out);

            wout.write("<?xml version='1.0'?>\r\n");
            wout.write("<SOAP-ENV:Envelope ");
            wout.write("xmlns:SOAP-ENV=");
            wout.write("'http://schemas.xmlsoap.org/soap/envelope/'");
            wout.write("xmlns:xsi=");
            wout.write("'http://www.w3.org/2001/XMLSchema-instance'>\r\n");
            wout.write("  <SOAP-ENV:Body>\r\n");
            wout.write("    <dados><processo>" + input + "</processo><chave>" + chave + "</chave></dados>\r\n");
            wout.write("  </SOAP-ENV:Body>\r\n");
            wout.write("</SOAP-ENV:Envelope>\r\n");

            wout.flush();
            wout.close();

            InputStream in = connection.getInputStream();
            int c;
            while ((c = in.read()) != -1)
                System.out.write(c);
            in.close();

        } catch (IOException e) {
            System.err.println(e);
        }

    } // end main

} // end FluidnowSOAPClient
