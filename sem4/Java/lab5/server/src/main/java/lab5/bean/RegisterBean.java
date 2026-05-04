package lab5.bean;

import jakarta.enterprise.context.RequestScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import lab5.model.Role;
import lab5.service.RentalService;

import java.io.Serializable;

@Named
@RequestScoped
public class RegisterBean implements Serializable {
    @Inject
    private RentalService service;

    private String name;
    private String email;
    private String phone;
    private String password;
    private Role role = Role.CLIENT;

    public String register() {
        try {
            service.register(name, email, phone, password, role);
            FacesContext.getCurrentInstance().getExternalContext().getFlash()
                    .put("info", "Регистрация выполнена. Теперь войдите под своим именем.");
            return "/index.xhtml?faces-redirect=true";
        } catch (IllegalArgumentException ex) {
            addMessage(FacesMessage.SEVERITY_ERROR, ex.getMessage());
            return null;
        }
    }

    private void addMessage(FacesMessage.Severity severity, String text) {
        FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(severity, text, text));
    }

    public Role[] getRoles() {
        return Role.values();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }
}
