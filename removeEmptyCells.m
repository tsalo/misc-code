function [outCellArray] = removeEmptyCells(cellArray)
% FORMAT [outCellArray] = removeEmptyCells(cellArray)
% A very simple function to remove empty cells from cell arrays. Great for
% subject lists.

for iCell = 1:length(cellArray)
    cellArray{iCell} = cellArray{iCell}(~isspace(cellArray{iCell}));
    if isfield(cellArray{iCell}, 'col')
        cellArray{iCell}.col = removeEmptyCells(cellArray{iCell}.col);
    end
end

outCellArray = cellArray(~cellfun('isempty', cellArray));
end