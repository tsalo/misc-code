function K = cellstrfind(string, patternCells, setting)
% FORMAT K = cellstrfind(string, patternCells, setting)
% Just tells you if any of the string patterns in a cell array are in a
% string.
% 
% Inputs:
% string:           String to be checked.
% patternCells:     Cell array of strings to be compared against string.
% setting:          "Exact" or anything else. String. Determines if
%                   cellstrfind will use strmatch or strfind.
%
% Outputs:
% K:                0 if no match, 1 if match.
%
% 140101 Created by Taylor Salo
K = 0;
for iPattern = 1:length(patternCells)
    if exist('setting', 'var') && strcmp(setting, 'exact')
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
