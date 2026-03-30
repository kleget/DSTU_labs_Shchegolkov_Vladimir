package lab2;

import jakarta.servlet.ServletContext;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class UserStore {
    private final File file;

    public UserStore(ServletContext context) {
        this.file = new File(context.getRealPath("/WEB-INF/users.xml"));
    }

    public synchronized boolean verify(String login, String password) throws Exception {
        Element user = findUser(load(), login);
        return user != null && hash(password).equals(user.getAttribute("hash"));
    }

    public synchronized boolean register(String login, String password) throws Exception {
        Document doc = load();
        if (findUser(doc, login) != null) {
            return false;
        }
        Element user = doc.createElement("user");
        user.setAttribute("login", login);
        user.setAttribute("hash", hash(password));
        doc.getDocumentElement().appendChild(user);
        save(doc);
        return true;
    }

    private Document load() throws Exception {
        return DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(file);
    }

    private void save(Document doc) throws Exception {
        var tf = TransformerFactory.newInstance().newTransformer();
        tf.setOutputProperty(OutputKeys.INDENT, "yes");
        tf.transform(new DOMSource(doc), new StreamResult(file));
    }

    private Element findUser(Document doc, String login) {
        NodeList users = doc.getDocumentElement().getElementsByTagName("user");
        for (int i = 0; i < users.getLength(); i++) {
            Element e = (Element) users.item(i);
            if (login.equals(e.getAttribute("login"))) {
                return e;
            }
        }
        return null;
    }

    public static String hash(String value) throws Exception {
        byte[] bytes = MessageDigest.getInstance("SHA-256").digest(value.getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
