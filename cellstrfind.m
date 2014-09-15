function K = cellstrfind(string, patternCells, setting)
% FORMAT K = cellstrfind(string, patternCells, setting)
% Just tells you if any of the string patterns in a cell array are in a
% string.
% 
%
% string:           String to be checked.
% patternCells:     Cell array of strings to be compared against string.
% setting:          "Exact" or anything else. String. Determines if
%                   cellstrfind will use strmatch or strfind.
%
% K (output):       0 if no match, 1 if match.
K = 0;
for iPattern = 1:length(patternCells)
    if strcmp(setting, 'exact')
        if strcmp(string, patternCells{iPattern})
            K = 1;
        end
    else
        if strfind(string, patternCells{iPattern})
            K = 1;
        end
    end
end
end
