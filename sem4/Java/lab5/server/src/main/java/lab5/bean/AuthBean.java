package lab5.bean;

import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import lab5.model.Role;
import lab5.model.User;
import lab5.service.RentalService;

import java.io.Serializable;

@Named
@SessionScoped
public class AuthBean implements Serializable {
    @Inject
    private RentalService service;

    private String name;
    private String password;
    private User currentUser;

    public String login() {
        currentUser = service.login(name, password);
        if (currentUser == null) {
            addMessage(FacesMessage.SEVERITY_ERROR, "Неверное имя пользователя или пароль");
            return null;
        }

        if (currentUser.getRole() == Role.MANAGER) {
            return "/manager.xhtml?faces-redirect=true";
        }
        return "/client.xhtml?faces-redirect=true";
    }

    public String logout() {
        FacesContext.getCurrentInstance().getExternalContext().invalidateSession();
        return "/index.xhtml?faces-redirect=true";
    }

    public boolean isLoggedIn() {
        return currentUser != null;
    }

    public boolean isManager() {
        return currentUser != null && currentUser.getRole() == Role.MANAGER;
    }

    public boolean isClient() {
        return currentUser != null && currentUser.getRole() == Role.CLIENT;
    }

    public String requireManager() {
        if (!isManager()) {
            return "/index.xhtml?faces-redirect=true";
        }
        return null;
    }

    public String requireClient() {
        if (!isClient()) {
            return "/index.xhtml?faces-redirect=true";
        }
        return null;
    }

    private void addMessage(FacesMessage.Severity severity, String text) {
        FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(severity, text, text));
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public User getCurrentUser() {
        return currentUser;
    }

    public void setCurrentUser(User currentUser) {
        this.currentUser = currentUser;
    }
}
