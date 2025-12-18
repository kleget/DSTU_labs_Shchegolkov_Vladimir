package lab4;

import java.util.Objects;

public final class Complex {
    private final double real;
    private final double imag;

    public Complex() {
        this(0.0, 0.0);
    }

    public Complex(double real) {
        this(real, 0.0);
    }

    public Complex(double real, double imag) {
        this.real = real;
        this.imag = imag;
    }

    public double real() {
        return real;
    }

    public double imag() {
        return imag;
    }

    public double modulus() {
        return Math.hypot(real, imag);
    }

    public double argument() {
        return Math.atan2(imag, real);
    }

    public Complex conjugate() {
        return new Complex(real, -imag);
    }

    public Complex add(Complex other) {
        Objects.requireNonNull(other);
        return new Complex(real + other.real, imag + other.imag);
    }

    public Complex add(double value) {
        return new Complex(real + value, imag);
    }

    public Complex subtract(Complex other) {
        Objects.requireNonNull(other);
        return new Complex(real - other.real, imag - other.imag);
    }

    public Complex subtract(double value) {
        return new Complex(real - value, imag);
    }

    public Complex multiply(Complex other) {
        Objects.requireNonNull(other);
        double r = real * other.real - imag * other.imag;
        double i = real * other.imag + other.real * imag;
        return new Complex(r, i);
    }

    public Complex multiply(double value) {
        return new Complex(real * value, imag * value);
    }

    public Complex divide(Complex other) {
        Objects.requireNonNull(other);
        double denom = other.real * other.real + other.imag * other.imag;
        if (denom == 0.0) {
            throw new ArithmeticException("Division by zero modulus");
        }
        double r = (real * other.real + imag * other.imag) / denom;
        double i = (imag * other.real - real * other.imag) / denom;
        return new Complex(r, i);
    }

    public Complex divide(double value) {
        if (value == 0.0) {
            throw new ArithmeticException("Division by zero");
        }
        return new Complex(real / value, imag / value);
    }

    public String toTrigonometricString() {
        double r = modulus();
        double phi = argument();
        return String.format("%.4f*(cos(%.4f)+i*sin(%.4f))", r, phi, phi);
    }

    @Override
    public String toString() {
        String sign = imag >= 0 ? "+" : "-";
        return String.format("%.4f %s %.4fi", real, sign, Math.abs(imag));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof Complex)) {
            return false;
        }
        Complex complex = (Complex) o;
        return Double.compare(complex.real, real) == 0
            && Double.compare(complex.imag, imag) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(real, imag);
    }
}
