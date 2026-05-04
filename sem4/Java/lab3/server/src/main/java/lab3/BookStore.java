package lab3;

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
import java.util.ArrayList;
import java.util.List;

public class BookStore {
    private static final String TITLE_RE = "^[\\p{L}\\p{N} .,'\"«»:\\-()!?]{1,80}$";
    private static final String AUTHOR_RE = "^[\\p{L} .'-]{2,60}$";
    private static final String GENRE_RE = "^[\\p{L} -]{2,30}$";
    private static final String YEAR_RE = "^(1[5-9]\\d{2}|20\\d{2})$";

    private final File file;

    public BookStore(ServletContext context) {
        this.file = new File(context.getRealPath("/WEB-INF/books.xml"));
    }

    public synchronized List<Book> list(String genre) throws Exception {
        String filter = value(genre).toLowerCase();
        Document doc = load();
        NodeList nodes = doc.getDocumentElement().getElementsByTagName("book");
        List<Book> books = new ArrayList<>();
        for (int i = 0; i < nodes.getLength(); i++) {
            Element e = (Element) nodes.item(i);
            Book book = new Book(
                    e.getAttribute("id"),
                    e.getAttribute("title"),
                    e.getAttribute("author"),
                    e.getAttribute("genre"),
                    e.getAttribute("year")
            );
            if (filter.isEmpty() || book.getGenre().equalsIgnoreCase(filter)) {
                books.add(book);
            }
        }
        return books;
    }

    public synchronized void add(Book book) throws Exception {
        validate(book);
        Document doc = load();
        Element e = doc.createElement("book");
        e.setAttribute("id", String.valueOf(System.currentTimeMillis()));
        e.setAttribute("title", value(book.getTitle()));
        e.setAttribute("author", value(book.getAuthor()));
        e.setAttribute("genre", value(book.getGenre()));
        e.setAttribute("year", value(book.getYear()));
        doc.getDocumentElement().appendChild(e);
        save(doc);
    }

    public synchronized boolean delete(String id) throws Exception {
        Document doc = load();
        NodeList nodes = doc.getDocumentElement().getElementsByTagName("book");
        for (int i = 0; i < nodes.getLength(); i++) {
            Element e = (Element) nodes.item(i);
            if (value(id).equals(e.getAttribute("id"))) {
                e.getParentNode().removeChild(e);
                save(doc);
                return true;
            }
        }
        return false;
    }

    private static void validate(Book book) {
        if (!value(book.getTitle()).matches(TITLE_RE)) {
            throw new IllegalArgumentException("Название: 1-80 символов, только буквы, цифры, пробелы и простые знаки.");
        }
        if (!value(book.getAuthor()).matches(AUTHOR_RE)) {
            throw new IllegalArgumentException("Автор: 2-60 символов, только буквы, пробел, точка, апостроф или дефис.");
        }
        if (!value(book.getGenre()).matches(GENRE_RE)) {
            throw new IllegalArgumentException("Жанр: 2-30 символов, только буквы, пробел или дефис.");
        }
        if (!value(book.getYear()).matches(YEAR_RE)) {
            throw new IllegalArgumentException("Год должен быть числом от 1500 до 2099.");
        }
    }

    private Document load() throws Exception {
        return DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(file);
    }

    private void save(Document doc) throws Exception {
        var transformer = TransformerFactory.newInstance().newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.transform(new DOMSource(doc), new StreamResult(file));
    }

    private static String value(String s) {
        return s == null ? "" : s.trim();
    }
}
