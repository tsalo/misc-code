function convertPs(filename, outType)
% FORMAT convertPs(filename, outType)
% A small function that calls GhostScript to convert postscript files to
% other formats. The default is pdf.
%
%
% filename: The .ps file to convert (include .ps extension). String.
% outType: The format to which the postscript file will be converted.
%           String. Possible values: jpg, pdf. Others will need to be
%           added to the code.

if ~exist('outType', 'var')
    outType = 'pdf';
end
[~, filenameShort, ~] = fileparts(filename);

if strcmp(outType, 'jpg')
    device = 'jpeg';
elseif strcmp(outType, 'pdf')
    device = 'pdfwrite';
end

system(['gs -dBATCH -dNOPAUSE -sDEVICE=' device ' -sOutputFile=' filename_short '.' out_type ' -r100 ' filename])
fprintf('Converted %s to %s.%s\n', filename, filenameShort, outType);
end
