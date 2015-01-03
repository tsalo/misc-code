function [outCellArray] = removeEmptyCells(cellArray)
% FORMAT [outCellArray] = removeEmptyCells(cellArray)
% A very simple function to remove empty cells from cell arrays. Great for
% subject lists.
%
% Inputs:
% cellArray:    Cell array or cell array of structures in format outputted
%               by readCsv.
%
% Outputs:
% outCellArray: cellArray without empty cells.
%
%
% 140804 Created by Taylor Salo

for iCell = 1:length(cellArray)
    cellArray{iCell} = cellArray{iCell}(~isspace(cellArray{iCell}));
    if isfield(cellArray{iCell}, 'col')
        cellArray{iCell}.col = removeEmptyCells(cellArray{iCell}.col);
    end
end

outCellArray = cellArray(~cellfun('isempty', cellArray));
end
