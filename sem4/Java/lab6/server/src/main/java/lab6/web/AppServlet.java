package lab6.web;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lab6.client.CompetitionApiClient;
import lab6.model.Competition;
import lab6.model.Participant;
import lab6.model.Stage;

import java.io.IOException;
import java.util.Comparator;
import java.util.List;

@WebServlet("/app")
public class AppServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html; charset=UTF-8");

        String role = role(request.getParameter("role"));
        StringBuilder body = new StringBuilder();
        body.append("<nav class=\"top-nav\">")
                .append("<a href=\"").append(request.getContextPath()).append("/\">Главная</a>")
                .append("<a href=\"").append(request.getContextPath()).append("/app?role=admin\">Администратор</a>")
                .append("<a href=\"").append(request.getContextPath()).append("/app?role=participant\">Участник</a>")
                .append("<a href=\"").append(request.getContextPath()).append("/app?role=spectator\">Зритель</a>")
                .append("</nav>");

        try (CompetitionApiClient client = new CompetitionApiClient(apiBase(request))) {
            List<Competition> competitions = client.getCompetitions();
            competitions.sort(Comparator.comparingLong(Competition::getId));
            Competition selected = selectCompetition(request, client, competitions);
            body.append("<h1>Соревнования</h1>");
            body.append(renderChooser(request, competitions, selected, role));
            if ("admin".equals(role)) {
                body.append(renderAdmin(request, selected));
            } else if ("participant".equals(role)) {
                body.append(renderParticipant(request, selected));
            } else {
                body.append(renderSpectator(selected));
            }
        } catch (RuntimeException ex) {
            body.append("<section class=\"notice error\">Ошибка Client API: ")
                    .append(Html.escape(ex.getMessage()))
                    .append("</section>");
        }

        response.getWriter().write(Html.page("Lab 6 competitions", body.toString()));
    }

    private static String renderChooser(HttpServletRequest request, List<Competition> competitions,
                                        Competition selected, String role) {
        StringBuilder html = new StringBuilder();
        html.append("<section><h2>Выбор соревнования</h2>");
        if (competitions.isEmpty()) {
            html.append("<p>Соревнований пока нет.</p>");
        } else {
            html.append("<form method=\"get\" action=\"").append(request.getContextPath()).append("/app\">")
                    .append("<input type=\"hidden\" name=\"role\" value=\"").append(Html.escape(role)).append("\">")
                    .append("<label>Соревнование<select name=\"competitionId\">");
            for (Competition competition : competitions) {
                html.append("<option value=\"").append(competition.getId()).append("\"");
                if (selected != null && selected.getId() == competition.getId()) {
                    html.append(" selected");
                }
                html.append(">")
                        .append(Html.escape(competition.getTitle()))
                        .append("</option>");
            }
            html.append("</select></label><button type=\"submit\">Открыть</button></form>");
        }
        html.append("</section>");
        return html.toString();
    }

    private static String renderAdmin(HttpServletRequest request, Competition selected) {
        StringBuilder html = new StringBuilder();
        html.append("<section><h2>Администратор</h2>")
                .append("<p>Задает тему, расписание и промежуточные результаты.</p>")
                .append("<form method=\"post\" action=\"").append(request.getContextPath()).append("/app/admin\">")
                .append("<input type=\"hidden\" name=\"action\" value=\"saveCompetition\">");
        if (selected != null) {
            html.append("<input type=\"hidden\" name=\"competitionId\" value=\"").append(selected.getId()).append("\">");
        }
        html.append("<label>Название<input name=\"title\" required")
                .append(Html.value(selected == null ? "" : selected.getTitle())).append("></label>")
                .append("<label>Дата и время<input type=\"datetime-local\" name=\"eventDateTime\"")
                .append(Html.value(selected == null ? "" : selected.getEventDateTime())).append("></label>")
                .append("<label>Организаторы<input name=\"organizers\"")
                .append(Html.value(selected == null ? "" : selected.getOrganizers())).append("></label>")
                .append("<label>Доп. информация<textarea name=\"extraInfo\">")
                .append(Html.escape(selected == null ? "" : selected.getExtraInfo())).append("</textarea></label>")
                .append("<button type=\"submit\">Сохранить соревнование</button></form>");

        if (selected != null) {
            html.append("<form method=\"post\" action=\"").append(request.getContextPath()).append("/app/admin\" class=\"inline-form\">")
                    .append("<input type=\"hidden\" name=\"action\" value=\"deleteCompetition\">")
                    .append("<input type=\"hidden\" name=\"competitionId\" value=\"").append(selected.getId()).append("\">")
                    .append("<button type=\"submit\" class=\"danger\">Удалить соревнование</button></form>");

            html.append("<h3>Добавить этап</h3><form method=\"post\" action=\"")
                    .append(request.getContextPath()).append("/app/admin\">")
                    .append("<input type=\"hidden\" name=\"action\" value=\"addStage\">")
                    .append("<input type=\"hidden\" name=\"competitionId\" value=\"").append(selected.getId()).append("\">")
                    .append("<label>Название этапа<input name=\"stageName\" required></label>")
                    .append("<label>Время<input type=\"datetime-local\" name=\"stageTime\"></label>")
                    .append("<button type=\"submit\">Добавить этап</button></form>");

            html.append("<h3>Внести результат</h3><form method=\"post\" action=\"")
                    .append(request.getContextPath()).append("/app/admin\">")
                    .append("<input type=\"hidden\" name=\"action\" value=\"addParticipant\">")
                    .append("<input type=\"hidden\" name=\"competitionId\" value=\"").append(selected.getId()).append("\">")
                    .append("<label>Участник<input name=\"participantName\" required></label>")
                    .append("<label>E-mail<input name=\"participantEmail\"></label>")
                    .append("<label>Этап<input name=\"stageName\"></label>")
                    .append("<label>Результат<input name=\"result\"></label>")
                    .append("<button type=\"submit\">Сохранить результат</button></form>");
            html.append(renderDetails(selected));
        }
        html.append("</section>");
        return html.toString();
    }

    private static String renderParticipant(HttpServletRequest request, Competition selected) {
        StringBuilder html = new StringBuilder();
        html.append("<section><h2>Участник</h2>");
        if (selected == null) {
            html.append("<p>Нет доступных соревнований.</p></section>");
            return html.toString();
        }
        html.append("<p>Регистрируется и отправляет результат выбранного этапа.</p>")
                .append("<form method=\"post\" action=\"").append(request.getContextPath()).append("/app/participant\">")
                .append("<input type=\"hidden\" name=\"competitionId\" value=\"").append(selected.getId()).append("\">")
                .append("<label>Имя<input name=\"participantName\" required></label>")
                .append("<label>E-mail<input type=\"email\" name=\"participantEmail\"></label>")
                .append("<label>Этап<input name=\"stageName\" placeholder=\"Например, отборочный этап\"></label>")
                .append("<label>Результат<input name=\"result\" placeholder=\"Например, 70 баллов\"></label>")
                .append("<button type=\"submit\">Зарегистрироваться / отправить</button></form>")
                .append(renderDetails(selected))
                .append("</section>");
        return html.toString();
    }

    private static String renderSpectator(Competition selected) {
        StringBuilder html = new StringBuilder();
        html.append("<section><h2>Зритель</h2><p>Просмотр расписания и результатов без регистрации.</p>");
        if (selected == null) {
            html.append("<p>Нет доступных соревнований.</p>");
        } else {
            html.append(renderDetails(selected));
        }
        html.append("</section>");
        return html.toString();
    }

    private static String renderDetails(Competition competition) {
        StringBuilder html = new StringBuilder();
        html.append("<article class=\"details\"><h3>")
                .append(Html.escape(competition.getTitle()))
                .append("</h3><dl>")
                .append("<dt>Дата и время</dt><dd>").append(Html.escape(competition.getEventDateTime())).append("</dd>")
                .append("<dt>Организаторы</dt><dd>").append(Html.escape(competition.getOrganizers())).append("</dd>")
                .append("<dt>Доп. информация</dt><dd>").append(Html.escape(competition.getExtraInfo())).append("</dd>")
                .append("</dl>");

        html.append("<h4>Этапы</h4><table><thead><tr><th>ID</th><th>Название</th><th>Время</th></tr></thead><tbody>");
        for (Stage stage : competition.getStages()) {
            html.append("<tr><td>").append(stage.getId()).append("</td><td>")
                    .append(Html.escape(stage.getName())).append("</td><td>")
                    .append(Html.escape(stage.getStartsAt())).append("</td></tr>");
        }
        html.append("</tbody></table>");

        html.append("<h4>Участники и результаты</h4><table><thead><tr><th>ID</th><th>Участник</th><th>E-mail</th><th>Этап</th><th>Результат</th></tr></thead><tbody>");
        for (Participant participant : competition.getParticipants()) {
            html.append("<tr><td>").append(participant.getId()).append("</td><td>")
                    .append(Html.escape(participant.getName())).append("</td><td>")
                    .append(Html.escape(participant.getEmail())).append("</td><td>")
                    .append(Html.escape(participant.getStageName())).append("</td><td>")
                    .append(Html.escape(participant.getResult())).append("</td></tr>");
        }
        html.append("</tbody></table></article>");
        return html.toString();
    }

    private static Competition selectCompetition(HttpServletRequest request, CompetitionApiClient client,
                                                 List<Competition> competitions) {
        long requestedId = parseLong(request.getParameter("competitionId"), -1);
        if (requestedId > 0) {
            return client.getCompetition(requestedId);
        }
        return competitions.isEmpty() ? null : competitions.get(0);
    }

    private static String apiBase(HttpServletRequest request) {
        return request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort()
                + request.getContextPath() + "/api";
    }

    private static String role(String role) {
        if ("admin".equals(role) || "participant".equals(role) || "spectator".equals(role)) {
            return role;
        }
        return "spectator";
    }

    private static long parseLong(String value, long defaultValue) {
        try {
            return value == null || value.isBlank() ? defaultValue : Long.parseLong(value);
        } catch (NumberFormatException ex) {
            return defaultValue;
        }
    }
}
