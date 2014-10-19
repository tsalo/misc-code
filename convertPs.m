function convertPs(filename, out_type)
% FORMAT convertPs(filename, out_type)
% A small function that calls GhostScript to convert postscript files to
% other formats. The default is pdf.
%
%
% filename: The .ps file to convert (include .ps extension). String.
% out_type: The format to which the postscript file will be converted.
%           String. Possible values: jpg, pdf. Others will need to be
%           added to the code.

if ~exist('out_type', 'var')
    out_type = 'pdf';
    device = 'pdfwrite';
end
[~,filename_short,~] = fileparts(filename);

if strcmp(out_type, 'jpg')
    device = 'jpeg';
elseif strcmp(out_type, 'pdf')
    device = 'pdfwrite';
end

disp(['gs -dBATCH -dNOPAUSE -sDEVICE=' device ' -sOutputFile=' filename_short '.' out_type ' -r100 ' filename]);
system(['gs -dBATCH -dNOPAUSE -sDEVICE=' device ' -sOutputFile=' filename_short '.' out_type ' -r100 ' filename]);
fprintf('Converted %s to %s.%s\n', filename, filename_short, out_type);

end
