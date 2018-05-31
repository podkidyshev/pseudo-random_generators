clc;
clearvars;
gen_type = 'add'; 

M = dlmread(strcat('.\\analysis\\rnd_', gen_type, '.dat'));
fileID = fopen(strcat('.\\analysis\\report_', gen_type, '.txt'),'w');

mx = mean(M);
fprintf(fileID, 'Математическое ожидание = %f\r\n', mx);
sx = std(M) ^ 2;
fprintf(fileID, 'Среднеквадратическое отклонение = %f\r\n', sx);
counts = [10 100 1000 3000 7000 10000];
means = zeros(1, length(counts));
deviations = zeros(1, length(counts));
for i = 1:length(counts)
   sample = M(1:counts(i));
   fprintf(fileID, '\r\nВыборка размером %d:\r\n', counts(i));
   means(i) = mean(sample);
   fprintf(fileID, 'Мат. ожидание = %f\r\n', means(i));
   deviations(i) = std(sample) ^ 2;
   fprintf(fileID, 'Среднеквадрат. отклонение = %f\r\n', deviations(i));
end

plot(counts, means, '-o');
title('Зависимость мат. ожидания от объёма выборки');
ylim([0.4 0.6]);
figure;
plot(counts, deviations, '-o');
title('Зависимость среднеквадрат. отклонения от объёма выборки');
ylim([0.076 0.084]);

% теоретические значения для стандартного нормального распределения
mean_true = 0.5;
deviation_true = 1 / 12;
sample_num = 2; % в массиве counts это 100
fprintf(fileID, '\r\nОтносительная погрешность для выборки размером %d:\r\n', counts(sample_num));
mean_dev = abs(means(sample_num) - mean_true) / means(sample_num) * 100;
fprintf(fileID, 'Для мат. ожидания: %f%%\r\n', mean_dev);
deviation_dev = abs(deviations(sample_num) - deviation_true) / deviations(sample_num);
fprintf(fileID, 'Для среднеквадрат. отклонения: %f%%\r\n', deviation_dev);

fclose(fileID);