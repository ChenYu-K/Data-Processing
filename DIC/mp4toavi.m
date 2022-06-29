reader = VideoReader('C0072.MP4');
writer = VideoWriter('transcoded_C0072.avi', ...
                        'Uncompressed AVI');

writer.FrameRate = reader.FrameRate;

open(writer);
while hasFrame(reader)
   img = readFrame(reader);
   writeVideo(writer,img);
end
close(writer);
