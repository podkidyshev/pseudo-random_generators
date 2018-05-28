import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigInteger;
import java.util.*;



public class Solution {

    static double n = 10000.0;

    public static void main(String[] args) {
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            ArrayList<Double> numbers = new ArrayList<>();
            String s;
            while ((s = br.readLine()) != null) {
                s = s.replaceAll(",", ".");
                numbers.add(Math.abs(Double.parseDouble(s)) / 1000);
            }
            double max = Double.MIN_VALUE;
            for(Double d : numbers){
                if(d > max){
                    max = d;
                }
            }

            chi_square(numbers);
            System.out.println();
            series(numbers);
            System.out.println();
            interval(numbers);
            System.out.println();
            splitting(numbers);
            System.out.println();
            reverse(numbers);
            System.out.println();
            monotone(numbers);
            System.out.println();
            conflicts(numbers);
            System.out.println();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void monotone(ArrayList<Double> numbers) {
        System.out.println("Критерий монотонности:");
        int step = 1;
        int[] ni = new int[7];
        for (int i = 1; i < numbers.size(); i++) {
            if (1000*numbers.get(i) > 1000*numbers.get(i - 1)) {
                step++;
                if (step == 6) {
                    ni[6]++;
                    step = 0;
                }
            } else {
                ni[step]++;
                step = 0;
            }
        }
        double[][] a = new double[][]{
                {4529.4, 9044.9, 13568, 18091, 22615, 27892},
                {9044.9, 18097, 27139, 36187, 45234, 55789},
                {13568, 27139, 40721, 54281, 67852, 83685},
                {18091, 36187, 54281, 72414, 90470, 111580},
                {22615, 45234, 67852, 90470, 113262, 139476},
                {27892, 55789, 838685, 111580, 139476, 172860}
        };
        double[] b = new double[]{(double) 1 / 6, (double) 5 / 24, (double) 11 / 120, (double) 19 / 720, (double) 29 / 5040, (double) 1 / 840};
        double v = 0.0;
        for (int i = 0; i < b.length; i++) {
            for (int j = 0; j < b.length; j++) {
                double result = ni[i + 1] - numbers.size() * b[i];
                result *= (ni[j + 1] - numbers.size() * b[j]);
                result *= a[i][j];
                v += result;
            }
        }
        v /= (numbers.size() - b.length);
        v /= 10000000;
        double crit = 12.59;
        System.out.println("Полученное: " + v);
        System.out.println("Критическое: " + crit);
        if (v > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    private static void conflicts(ArrayList<Double> numbers) {
        System.out.println("Критерий конфликтов:");
        ArrayList<Integer> num = new ArrayList<>();
        for(Double x : numbers){
            num.add((int)(x*1000));
        }
        byte[] bytes = new byte[30000];
        int i = 0;
        for (Integer number1 : num) {

            int number = number1;
            int first = number / 100;
            int second = number % 100 / 10;
            int third = number % 10;
            if (first < 5) {
                bytes[i] = 0;
                i++;
            } else {
                bytes[i] = 1;
                i++;
            }
            if (second < 5) {
                bytes[i] = 0;
                i++;
            } else {
                bytes[i] = 1;
                i++;
            }
            if (third < 5) {
                bytes[i] = 0;
                i++;
            } else {
                bytes[i] = 1;
                i++;
            }
        }
        ArrayList<BigInteger> values = new ArrayList<>();
        int count = 0;
        for (int j = 0; j < bytes.length; j += 20) {
            byte[] part = new byte[20];
            System.arraycopy(bytes, j, part, 0, 20);
            BigInteger value = new BigInteger(part);
            if (values.contains(value)) {
                count++;
            } else {
                values.add(value);
            }
        }
        double crit = 1.07;
        System.out.println("Полученное: " + count);
        System.out.println("Ожидаемое: " + crit);
        if (count > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    private static void reverse(ArrayList<Double> numbers) {
        System.out.println("Критерий перестановок:");
        int t = 4;
        List<String> values = Arrays.asList("1234", "1243", "1324", "1342", "1423", "1432",
                "2134", "2143", "2314", "2341", "2413", "2431",
                "3124", "3142", "3214", "3241", "3412", "3421",
                "4123", "4132", "4213", "4231", "4312", "4321");
        int[] ni = new int[24];
        for (int i = 0; i < ni.length; i++) {
            ni[i] = 0;
        }
        List<Double> cur;
        List<Double> sorted = new ArrayList<>();
        boolean[] isChecked = new boolean[t];
        String s = "";
        for (int i = 0; i < numbers.size() - 3; i += t) {
            cur = Arrays.asList(1000*numbers.get(i), 1000*numbers.get(i + 1), 1000*numbers.get(i + 2), 1000*numbers.get(i + 3));
            sorted.addAll(cur);
            Collections.sort(sorted);
            for (Double aCur : cur) {
                for (int k = 0; k < sorted.size(); k++) {
                    if (aCur.equals(sorted.get(k)) && !isChecked[k]) {
                        isChecked[k] = true;
                        s += k + 1;
                        break;
                    }
                }
            }
            ni[values.indexOf(s)]++;
            s = "";
            sorted.clear();
            isChecked = new boolean[t];
        }
        double ej = numbers.size() / 125.0;
        double chi = 0.0;
        for (int j = 0; j < values.size(); j++) {
            chi += (ni[j] - ej) * (ni[j] - ej) / ej;
        }
        double crit = 35.17;
        chi /= 1000;
        System.out.println("Полученное: " + chi);
        System.out.println("Критическое: " + crit);
        if (chi > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    private static void splitting(ArrayList<Double> numbers) {
        System.out.println("Критерий разбиений:");
        int step = 7;
        int[] ni = new int[7];
        for (int i = 0; i < 7; i++) {
            ni[i] = 0;
        }
        HashMap<Integer, HashSet<Integer>> values = new HashMap<>();
        for (int i = 0; i < step; i++) {
            values.put(i, new HashSet<Integer>());
        }
        for (Double number : numbers) {
            int result = 1000*number.intValue() / step;
            if(result >= ni.length) result = ni.length - 1;
            ni[result]++;
            values.get(result).add(1000*number.intValue() % step);
        }
        double[] er = new double[7];
        int[] stirlingNumbers = {0, 720, 1764, 1624, 735, 175, 21, 1};
        for (int i = 1; i < er.length; i++) {
            er[i] = step * stirlingNumbers[i];
        }
        double chi = 0.0;
        for (int i = 1; i < er.length; i++) {
            chi += (ni[i] - er[i]) * (ni[i] - er[i]) / er[i];
        }
        double crit = 12.59;
        chi /= 1000000;
        System.out.println("Полученное: " + chi);
        System.out.println("Критическое: " + crit);
        if (chi > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    private static void interval(ArrayList<Double> numbers) {
        System.out.println("Критерий интервалов:");
        ArrayList<Double> num = new ArrayList<>(numbers.size());
        for (Double x : numbers){
            num.add(x);
        }
        Collections.sort(num);
        double a = 0.5;
        double b = 1;
        int t = 5;
        int n = 500;
        int s = 0;
        int j = -1;
        double[] p = new double[t + 1];
        int[] count = new int[t + 1];
        while (s < n){
            int r = 0;
            while (j + 1 < num.size() && num.get(++j) < a || num.get(j) >= b){
                r++;
            }
            if (r >= t){
                count[t]++;
            }
            else{
                count[r]++;
            }
            s++;
        }
        for (int r = 0; r < p.length; r++){
            if (r == t)
                p[t] = Math.pow(1 - (b - a), t);
            else
                p[r] = (b - a) * Math.pow(1 - (b - a), r);
        }
        double crit = 14.06;
        double chi = 0.0;
        for (int i = 0; i < count.length; i++){
            chi+=(count[i] - n*p[i]) * (count[i] - n*p[i]) / (n*p[i]);
        }
        chi/=10000;
        System.out.println("Полученное: " + chi);
        System.out.println("Критическое: " + crit);
        if (chi > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    private static void series(ArrayList<Double> numbers) {
        int d = 10;
        ArrayList<Integer> num = new ArrayList<>();
        for(Double x : numbers){
            num.add((int)(x*d));
        }
        System.out.println("Критерий серий:");
        int k = d*d;
        int[] ni = new int[k + 10000];
        for (int j = 0; j < k; j++) {
            ni[j] = 0;
        }
        for (int i = 0; i < num.size() - 1; i++) {
            Integer first = num.get(i);
            Integer second = num.get(i + 1);
            ni[first*d + second]++;
        }

        double ej = (double) num.size() / (2*d*d);
        double chi = 0.0;
        for (int j = 0; j < k; j++) {
            chi += (ni[j] - ej) * (ni[j] - ej) / ej;
        }
        chi/=10000;
        double crit = 123.22;
        System.out.println("Полученное: " + chi);
        System.out.println("Критическое: " + crit);
        if (chi > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    private static void chi_square(ArrayList<Double> numbers) {
        int d = 1000;
        ArrayList<Integer> num = new ArrayList<>();
        for(Double x : numbers){
            num.add((int)(x*d));
        }
        System.out.println("Критерий хи-квадрат:");
        int k = 14;
        double step = 1000 / 14.0;
        int[] ni = new int[k];
        for (int j = 0; j < k; j++) {
            ni[j] = 0;
        }
        for (Integer number : num) {
            int result = (int) (number / step);
            if(result >= ni.length)
                result = ni.length - 1;
            ni[result]++;
        }
        double ej = (double) numbers.size() / k;
        double chi = 0.0;
        for (int j = 0; j < k; j++) {
            chi += (ni[j] - ej) * (ni[j] - ej) / ej;
        }
        double crit = 22.36;
        chi /= 10000;
        System.out.println("Полученное: " + chi);
        System.out.println("Критическое: " + crit);
        if (chi > crit) {
            System.out.println("Не пройден!");
        } else {
            System.out.println("Пройден!");
        }
    }

    class Pair {
        public int a;
        public int b;

        public Pair(int a, int b) {
            this.a = a;
            this.b = b;
        }
    }
}
