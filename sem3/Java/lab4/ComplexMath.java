package lab4;

public final class ComplexMath {
    private static final Complex I = new Complex(0, 1);

    private ComplexMath() {
    }

    public static Complex exp(Complex z) {
        double exp = Math.exp(z.real());
        return new Complex(exp * Math.cos(z.imag()), exp * Math.sin(z.imag()));
    }

    public static Complex sin(Complex z) {
        double a = z.real();
        double b = z.imag();
        return new Complex(Math.sin(a) * Math.cosh(b), Math.cos(a) * Math.sinh(b));
    }

    public static Complex cos(Complex z) {
        double a = z.real();
        double b = z.imag();
        return new Complex(Math.cos(a) * Math.cosh(b), -Math.sin(a) * Math.sinh(b));
    }

    public static Complex tan(Complex z) {
        return sin(z).divide(cos(z));
    }

    public static Complex sinh(Complex z) {
        double a = z.real();
        double b = z.imag();
        return new Complex(Math.sinh(a) * Math.cos(b), Math.cosh(a) * Math.sin(b));
    }

    public static Complex cosh(Complex z) {
        double a = z.real();
        double b = z.imag();
        return new Complex(Math.cosh(a) * Math.cos(b), Math.sinh(a) * Math.sin(b));
    }

    public static Complex tanh(Complex z) {
        return sinh(z).divide(cosh(z));
    }

    public static Complex coth(Complex z) {
        return cosh(z).divide(sinh(z));
    }

    public static Complex log(Complex z) {
        double r = z.modulus();
        double phi = z.argument();
        return new Complex(Math.log(r), phi);
    }

    public static Complex atan(Complex z) {
        // 0.5i * (ln(1 - i z) - ln(1 + i z))
        Complex one = new Complex(1, 0);
        Complex ln1MinusIZ = log(one.subtract(I.multiply(z)));
        Complex ln1PlusIZ = log(one.add(I.multiply(z)));
        Complex diff = ln1MinusIZ.subtract(ln1PlusIZ);
        return diff.multiply(new Complex(0, 0.5));
    }
}
