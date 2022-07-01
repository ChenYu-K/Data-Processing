reader = VideoReader('C0079.MP4');
writer = VideoWriter('transcoded_C0072_test.avi', ...
                        'Grayscale AVI');

% Uncompressed (https://ww2.mathworks.cn/help/matlab/ref/videowriter.html?searchHighlight=videowriter&s_tid=srchtitle_videowriter_1#d123e1491750) option
writer.FrameRate = reader.FrameRate;
%writer.FrameCount = 3;
frame = 1;

open(writer);
while hasFrame(reader)
   %if mod(frame,8) == 0 
    img = readFrame(reader);
    img_gray = rgb2gray(img);
    writeVideo(writer,img_gray);
   %end
   frame = frame + 1;
end

close(writer);
