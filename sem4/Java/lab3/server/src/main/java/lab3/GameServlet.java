package lab3;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;

public class GameServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        show(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        GameBean game = game(req.getSession(true));
        if ("reset".equals(req.getParameter("action"))) {
            game.reset();
        } else {
            game.playerMove(parse(req.getParameter("row")), parse(req.getParameter("col")));
        }
        show(req, resp);
    }

    private void show(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setAttribute("game", game(req.getSession(true)));
        req.getRequestDispatcher("/WEB-INF/jsp/game.jsp").forward(req, resp);
    }

    private GameBean game(HttpSession session) {
        GameBean game = (GameBean) session.getAttribute("game");
        if (game == null) {
            game = new GameBean();
            session.setAttribute("game", game);
        }
        return game;
    }

    private static int parse(String value) {
        try {
            return Integer.parseInt(value);
        } catch (Exception e) {
            return -1;
        }
    }
}
