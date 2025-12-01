/**
 * Хэш-функция, суммирующая коды символов фамилии.
 */
public class PersonHashFunction extends HashFunction<String> {

    public PersonHashFunction(int tableSize) {
        super(tableSize);
    }

    @Override
    protected int hash(String key) {
        int sum = 0;
        for (char ch : key.toCharArray()) {
            sum += ch;
        }
        return sum;
    }
}
