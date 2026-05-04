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
public class ClientBean implements Serializable {
    @Inject
    private AuthBean authBean;

    @Inject
    private RentalService service;

    private Long selectedCarId;
    private int days = 1;

    public List<Rental> getMyRentals() {
        if (!authBean.isClient()) {
            return List.of();
        }
        return service.findClientRentals(authBean.getCurrentUser().getId());
    }

    public List<Car> getAvailableCars() {
        return service.findAvailableCars();
    }

    public String selectCar(Long carId) {
        selectedCarId = carId;
        days = 1;
        return null;
    }

    public String rentSelected() {
        try {
            service.rentCar(authBean.getCurrentUser().getId(), selectedCarId, days);
            selectedCarId = null;
            days = 1;
            addMessage(FacesMessage.SEVERITY_INFO, "Автомобиль арендован");
        } catch (RuntimeException ex) {
            addMessage(FacesMessage.SEVERITY_ERROR, ex.getMessage());
        }
        return null;
    }

    public String closeRental(Long rentalId) {
        try {
            service.closeRental(authBean.getCurrentUser().getId(), rentalId);
            addMessage(FacesMessage.SEVERITY_INFO, "Аренда завершена");
        } catch (RuntimeException ex) {
            addMessage(FacesMessage.SEVERITY_ERROR, ex.getMessage());
        }
        return null;
    }

    public Car getSelectedCar() {
        if (selectedCarId == null) {
            return null;
        }
        return service.findCar(selectedCarId);
    }

    public double getTotalPrice() {
        Car car = getSelectedCar();
        if (car == null) {
            return 0;
        }
        return car.getPricePerDay() * Math.max(days, 1);
    }

    private void addMessage(FacesMessage.Severity severity, String text) {
        FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(severity, text, text));
    }

    public Long getSelectedCarId() {
        return selectedCarId;
    }

    public void setSelectedCarId(Long selectedCarId) {
        this.selectedCarId = selectedCarId;
    }

    public int getDays() {
        return days;
    }

    public void setDays(int days) {
        this.days = days;
    }
}
