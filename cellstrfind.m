function K = cellstrfind(string, patternCells)
% FORMAT K = cellstrfind(string, patternCells)
% Just tells you if any of the string patterns in a cell array are in a
% string.
% K (output): 0 if no match, 1 if match.
K = 0;
for iPattern = 1:length(patternCells)
    if strfind(string, patternCells{iPattern})
        K = 1;
    end
end
end

