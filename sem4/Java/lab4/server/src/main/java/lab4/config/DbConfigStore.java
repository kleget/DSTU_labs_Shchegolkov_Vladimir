package lab4.config;

import jakarta.servlet.ServletContext;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;

public class DbConfigStore {
    private final File file;

    public DbConfigStore(ServletContext context) {
        String realPath = context.getRealPath("/WEB-INF/db-config.xml");
        this.file = realPath == null ? new File("db-config.xml") : new File(realPath);
    }

    public synchronized DbConfig load() throws Exception {
        if (!file.exists()) {
            DbConfig config = new DbConfig();
            save(config);
            return config;
        }
        Document document = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(file);
        Element root = document.getDocumentElement();
        DbConfig config = new DbConfig();
        config.setDriver(text(root, "driver"));
        config.setUrl(text(root, "url"));
        config.setUser(text(root, "user"));
        config.setPassword(text(root, "password"));
        return config;
    }

    public synchronized void save(DbConfig config) throws Exception {
        Document document = DocumentBuilderFactory.newInstance().newDocumentBuilder().newDocument();
        Element root = document.createElement("database");
        document.appendChild(root);
        append(document, root, "driver", config.getDriver());
        append(document, root, "url", config.getUrl());
        append(document, root, "user", config.getUser());
        append(document, root, "password", config.getPassword());

        var transformer = TransformerFactory.newInstance().newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.transform(new DOMSource(document), new StreamResult(file));
    }

    private static void append(Document document, Element root, String name, String value) {
        Element element = document.createElement(name);
        element.setTextContent(value == null ? "" : value);
        root.appendChild(element);
    }

    private static String text(Element root, String name) {
        var nodes = root.getElementsByTagName(name);
        if (nodes.getLength() == 0) {
            return "";
        }
        return nodes.item(0).getTextContent();
    }
}
