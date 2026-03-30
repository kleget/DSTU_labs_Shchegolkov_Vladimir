package lab2;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CbrService {
    public record Quote(LocalDate date, double value) {}

    private static final DateTimeFormatter CBR_PARAM = DateTimeFormatter.ofPattern("dd/MM/yyyy");
    private static final DateTimeFormatter CBR_DATE = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    private static final HttpClient HTTP = HttpClient.newHttpClient();

    public List<Quote> currency(String code, LocalDate from, LocalDate to) throws Exception {
        Map<String, String> ids = new HashMap<>();
        ids.put("USD", "R01235");
        ids.put("EUR", "R01239");
        ids.put("CNY", "R01375");
        ids.put("GBP", "R01035");

        String id = ids.getOrDefault(code.toUpperCase(), "R01235");
        String url = "https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=" + enc(CBR_PARAM.format(from)) +
                "&date_req2=" + enc(CBR_PARAM.format(to)) + "&VAL_NM_RQ=" + enc(id);
        Document doc = load(url);

        List<Quote> out = new ArrayList<>();
        NodeList records = doc.getDocumentElement().getElementsByTagName("Record");
        for (int i = 0; i < records.getLength(); i++) {
            Element r = (Element) records.item(i);
            LocalDate date = LocalDate.parse(r.getAttribute("Date"), CBR_DATE);
            double nominal = Double.parseDouble(text(r, "Nominal").replace(',', '.'));
            double value = Double.parseDouble(text(r, "Value").replace(',', '.')) / nominal;
            out.add(new Quote(date, value));
        }
        return out;
    }

    public List<Quote> metal(String code, LocalDate from, LocalDate to) throws Exception {
        int idx = switch (code.toUpperCase()) {
            case "AU" -> 0;
            case "AG" -> 1;
            case "PT" -> 2;
            case "PD" -> 3;
            default -> 0;
        };

        String url = "https://www.cbr.ru/scripts/xml_metall.asp?date_req1=" + enc(CBR_PARAM.format(from)) +
                "&date_req2=" + enc(CBR_PARAM.format(to));
        Document doc = load(url);

        List<Quote> out = new ArrayList<>();
        NodeList records = doc.getDocumentElement().getElementsByTagName("Record");
        for (int i = 0; i < records.getLength(); i++) {
            Element r = (Element) records.item(i);
            LocalDate date = LocalDate.parse(r.getAttribute("Date"), CBR_DATE);
            NodeList buys = r.getElementsByTagName("Buy");
            if (buys.getLength() > idx) {
                String raw = buys.item(idx).getTextContent().trim().replace(',', '.');
                if (!raw.isEmpty()) {
                    out.add(new Quote(date, Double.parseDouble(raw)));
                }
            }
        }
        return out;
    }

    private static Document load(String url) throws Exception {
        HttpRequest req = HttpRequest.newBuilder(URI.create(url)).GET().build();
        byte[] body = HTTP.send(req, HttpResponse.BodyHandlers.ofByteArray()).body();
        return DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(new ByteArrayInputStream(body));
    }

    private static String text(Element e, String tag) {
        return e.getElementsByTagName(tag).item(0).getTextContent().trim();
    }

    private static String enc(String s) {
        return URLEncoder.encode(s, StandardCharsets.UTF_8);
    }
}
