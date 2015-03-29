function writeCsv(data, outName, accessMode)
% FORMAT writeCsv(data, outName, accessMode)
% Accepts a data structure and and save location and file name e.g.
% /home/name/output.csv. The data structure is a sort of pseudo-standard.
% The structure should have an area for a .header and .col field. This is
% requisite. Essentially the format should mirror that of an excel file.
% I think this should work for any data set in the given format.
%
%
% Inputs:
% data:         Structure with .header and .col fields. Each header should be a
%		single cell. Each col should be a 1xN cell array.
% outName:	Output filename (with or without path). String.
% accessMode:   Access mode of outName. Optional. Default is 'w+'. String.
%
%
% writeCsv.m is the proprietary property of The Regents of the
% University of California (“The Regents.”)
% Copyright © 2012-14 The Regents of the University of California, Davis
% campus. All Rights Reserved.  
% Redistribution and use in source and binary forms, with or without
% modification, are permitted by nonprofit, research institutions for
% research use only, provided that the following conditions are met:
%   - Redistributions of source code must retain the above copyright
%     notice, this list of conditions and the following disclaimer. 
%   - Redistributions in binary form must reproduce the above copyright
%     notice, this list of conditions and the following disclaimer in the
%     documentation and/or other materials provided with the distribution. 
%   - The name of The Regents may not be used to endorse or promote
%     products derived from this software without specific prior written
%     permission. 
% The end-user understands that the program was developed for research
% purposes and is advised not to rely exclusively on the program for any
% reason.
% THE SOFTWARE PROVIDED IS ON AN "AS IS" BASIS, AND THE REGENTS HAVE NO 
% OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
% MODIFICATIONS. THE REGENTS SPECIFICALLY DISCLAIM ANY EXPRESS OR IMPLIED
% WARRANTIES, INCLUDING BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
% MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
% NO EVENT SHALL THE REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
% SPECIAL, INCIDENTAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES, INCLUDING BUT
% NOT LIMITED TO  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES, LOSS OF USE,
% DATA OR PROFITS, OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND UNDER ANY
% THEORY OF LIABILITY WHETHER IN CONTRACT, STRICT LIABILITY OR TORT
% (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
% THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY
% OF SUCH DAMAGE. 
% If you do not agree to these terms, do not download or use the software.
% This license may be modified only in a writing signed by authorized
% signatory of both parties.
% For commercial license information please contact copyright@ucdavis.edu.
%
%
% Created by Benjamin Geib 121010

nohead = 0;
if exist('accessMode', 'var')
    default = accessMode; 
    if ~exist(outName, 'file')
        nohead = 0;
        default = 'w+';
    else
        nohead = 1;
    end
else
    default = 'w+'; 
end
fid = fopen(outName, default);

% Print out the headers first (if it's a new file)
if ~nohead
    for iCol = 1:length(data)
        current_class = class(data{iCol}.header);
        switch current_class
            case 'cell'
                fprintf(fid, [char(data{iCol}.header) ',']);
            case 'char'
                fprintf(fid, [data{iCol}.header ',']);
            otherwise
                fprintf(fid, [num2str(data{iCol}.header) ',']);
        end
    end
    fprintf(fid, '\n');
end

% Examine the data structure
for iRow = 1:length(data{1}.col)
    for jCol = 1:length(data)
        if ~isfield(data{jCol}, 'col')
            fprintf(['Error writing: ' outName '\n']);
            fprintf('\tData does not have field "col"\n');
            return;
        end
        % Columns do not need to be the same length. If a column
        % is empty at the end we want it to just print as empty.
        nRows = length(data{jCol}.col);
        if iRow <= nRows
            % Determine the class of the {} or (), we don't know which it
            % should be
            current_class1 = class(data{jCol}.col(iRow));
            % Here we try out both classes, an error in one causes a
            % default occurance of the second.
            try
                % If the object is empty, print as such.
                if ~isempty(data{jCol}.col(iRow))
                    switch current_class1
                        case 'cell'
                            fprintf(fid, char(data{jCol}.col(iRow)));
                        case 'char'
                            fprintf(fid, data{jCol}.col(iRow));
                        otherwise
                            fprintf(fid, num2str(data{jCol}.col(iRow)));
                    end
                end
            catch err
                current_class2 = class(data{jCol}.col{iRow});
                if ~isempty(data{jCol}.col{iRow})
                    switch current_class2
                        case 'cell'
                            fprintf(fid, char(data{jCol}.col{iRow}));
                        case 'char'
                            fprintf(fid, data{jCol}.col{iRow});
                        otherwise
                            fprintf(fid, num2str(data{jCol}.col{iRow}));
                    end
                end
            end
        end
        fprintf(fid, ',');
    end
    fprintf(fid, '\n');
end

fclose(fid);
fprintf('Saved: %s\n', outName);
end
