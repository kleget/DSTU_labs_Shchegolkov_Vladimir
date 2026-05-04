package lab5.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.io.Serializable;

@Entity
@Table(name = "car")
public class Car implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String color;

    @Column(nullable = false, unique = true)
    private String serialNumber;

    @Column(nullable = false)
    private String conditionInfo;

    @Column(nullable = false)
    private double pricePerDay;

    public Car() {
    }

    public Car(String name, String color, String serialNumber, String conditionInfo, double pricePerDay) {
        this.name = name;
        this.color = color;
        this.serialNumber = serialNumber;
        this.conditionInfo = conditionInfo;
        this.pricePerDay = pricePerDay;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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
