function hourToc(tStart)
% FORMAT hourToc(tStart)
% A great way to see how long your scripts are taking when you're testing
% and streamlining them.
%
% tStart:   Result of tic (use tStart = tic to start timer).
% output:   Will print a string of the time elapsed since tStart was
%           created in hours, minutes, and seconds.

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
    fprintf('%d %s, %d %s, and %d %s\n', hrs, hrStr, mins, minStr, secs, secStr);
elseif mins > 0
    fprintf('%d %s and %d %s\n', mins, minStr, secs, secStr);
else
    fprintf('%d %s\n', secs, secStr);
end
end