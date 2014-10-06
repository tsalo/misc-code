

system(['fsl_ev2csv.sh ' featDir ' ' vectorCSV]);
data = excel_reader(vectorCSV);
names = data{1}.col;
for iCond = 1:length(data{2}.col)
    condData = importdata(data{2}.col{iCond});
    onsets{iCond} = condData(:, 1);
    durations{iCond} = condData(:, 3) - 3;
end
save(vectorMat, 'names', 'onsets', 'durations');