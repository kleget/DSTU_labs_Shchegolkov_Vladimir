package lab5.bean;

import jakarta.enterprise.context.RequestScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import lab5.model.Car;
import lab5.model.Rental;
import lab5.service.RentalService;

import java.io.Serializable;
import java.util.List;

@Named
@RequestScoped
public class ManagerBean implements Serializable {
    @Inject
    private RentalService service;

    private Long editId;
    private String name;
    private String color;
    private String serialNumber;
    private String conditionInfo;
    private double pricePerDay;

    public List<Car> getAvailableCars() {
        return service.findAvailableCars();
    }

    public List<Rental> getActiveRentals() {
        return service.findActiveRentals();
    }

    public String edit(Car car) {
        editId = car.getId();
        name = car.getName();
        color = car.getColor();
        serialNumber = car.getSerialNumber();
        conditionInfo = car.getConditionInfo();
        pricePerDay = car.getPricePerDay();
        return null;
    }

    public String save() {
        try {
            service.saveCar(editId, name, color, serialNumber, conditionInfo, pricePerDay);
            clearForm();
            addMessage(FacesMessage.SEVERITY_INFO, "Автомобиль сохранен");
        } catch (RuntimeException ex) {
            addMessage(FacesMessage.SEVERITY_ERROR, ex.getMessage());
        }
        return null;
    }

    public String delete(Long carId) {
        try {
            service.deleteCar(carId);
            addMessage(FacesMessage.SEVERITY_INFO, "Автомобиль удален");
        } catch (RuntimeException ex) {
            addMessage(FacesMessage.SEVERITY_ERROR, ex.getMessage());
        }
        return null;
    }

    public String clearForm() {
        editId = null;
        name = "";
        color = "";
        serialNumber = "";
        conditionInfo = "";
        pricePerDay = 0;
        return null;
    }

    private void addMessage(FacesMessage.Severity severity, String text) {
        FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(severity, text, text));
    }

    public Long getEditId() {
        return editId;
    }

    public void setEditId(Long editId) {
        this.editId = editId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String getSerialNumber() {
        return serialNumber;
    }

    public void setSerialNumber(String serialNumber) {
        this.serialNumber = serialNumber;
    }

    public String getConditionInfo() {
        return conditionInfo;
    }

    public void setConditionInfo(String conditionInfo) {
        this.conditionInfo = conditionInfo;
    }

    public double getPricePerDay() {
        return pricePerDay;
    }

    public void setPricePerDay(double pricePerDay) {
        this.pricePerDay = pricePerDay;
    }
}
