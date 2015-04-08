function timeElapsed = hourToc(tStart, printOut)
% FORMAT timeElapsed = hourToc(tStart, printOut)
% A great way to see how long your scripts are taking when you're testing
% and streamlining them.
%
% tStart:   Result of tic (use tStart = tic to start timer).
% output:   Will print a string of the time elapsed since tStart was
%           created in hours, minutes, and seconds.

if ~exist('printOut', 'var')
    printOut = true;
end

tEnd = toc(tStart);

hrs = floor(tEnd / 3600);
mins = floor(rem(tEnd, 3600) / 60);
secs = floor(rem(rem(tEnd, 3600), 60));

hrStr = 'hours';
minStr = 'minutes';
secStr = 'seconds';

if hrs == 1
    hrStr = 'hour';
end
if mins == 1
    minStr = 'minute';
end
if secs == 1
    secStr = 'second';
end

if hrs > 0
    timeElapsed = sprintf('%d %s, %d %s, and %d %s', hrs, hrStr, mins, minStr, secs, secStr);
elseif mins > 0
    timeElapsed = sprintf('%d %s and %d %s', mins, minStr, secs, secStr);
else
    timeElapsed = sprintf('%d %s', secs, secStr);
end
if printOut
    fprintf('%s\n', timeElapsed);
end
end
