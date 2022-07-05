classdef APP_MP4toAVI_exported < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                      matlab.ui.Figure
        LoadButton                    matlab.ui.control.Button
        ProgressBarGaugeLabel         matlab.ui.control.Label
        ProgressBarGauge              matlab.ui.control.LinearGauge
        StatusLampLabel               matlab.ui.control.Label
        StatusLamp                    matlab.ui.control.Lamp
        ExecuteButton                 matlab.ui.control.Button
        FilenameLabel                 matlab.ui.control.Label
        Fnameout                      matlab.ui.control.EditField
        TotalFramenumberLabel         matlab.ui.control.Label
        Framenumber                   matlab.ui.control.NumericEditField
        BrStreamConverter_Ver10Label  matlab.ui.control.Label
        Therehave4Class1AVIULabel_2   matlab.ui.control.Label
        OutputParameterPanel          matlab.ui.container.Panel
        Output_TypeDropDownLabel      matlab.ui.control.Label
        OutputType                    matlab.ui.control.DropDown
        fpsLabel                      matlab.ui.control.Label
        Frame_RateEditField_2Label    matlab.ui.control.Label
        FrameRate                     matlab.ui.control.NumericEditField
        OriginalFrameOrDownsamplingegLabel  matlab.ui.control.Label
        TabGroup                      matlab.ui.container.TabGroup
        UserManualTab                 matlab.ui.container.Tab
        Therehave4Class1AVIULabel_3   matlab.ui.control.Label
        OutputtypeTab                 matlab.ui.container.Tab
        Therehave4Class1AVIULabel     matlab.ui.control.Label
        ImageAxes                     matlab.ui.control.UIAxes
    end

    
    methods (Access = private)
        
        function streamconverter(app,filename)
                       
        end
    end
    

    % Callbacks that handle component events
    methods (Access = private)

        % Button pushed function: LoadButton
        function LoadButtonPushed(app, event)
            % Display uigetfile dialog
            filterspec = {'*.mp4;ng','MP4 File'};
            [f, p] = uigetfile(filterspec);
            % Make sure user didn't cancel uigetfile dialog
            % Configure image axes
            app.ImageAxes.Visible = 'off';
            app.ImageAxes.Colormap = gray(256);
            axis(app.ImageAxes, 'image');
            if (ischar(p))
               fname = fullfile(p,f);
               app.Fnameout.Value=fname;
               reader = VideoReader(fname);
               app.Framenumber.Value=reader.NumberOfFrame;
               app.FrameRate.Value = reader.FrameRate;
               app.StatusLamp.Color='1.00,0.00,0.00';
               imagesc(app.ImageAxes,read(reader,1));
            end
        end

        % Button pushed function: ExecuteButton
        function ExecuteButtonPushed(app, event)
            outputname = [app.Fnameout.Value,'_',app.OutputType.Value];
            type = app.OutputType.Value;
            if strcmp(type,'GS-MJPEG')
                writer = VideoWriter(outputname, 'Motion JPEG AVI');
            else
                writer = VideoWriter(outputname, type);
            end

            % Uncompressed AVI;Grayscale AVI'
            writer.FrameRate = round(app.FrameRate.Value);
            %writer.FrameCount = 3;
            reader = VideoReader(app.Fnameout.Value);
            nFrame = reader.NumberOfFrame;
            a =  round(reader.FrameRate) / writer.FrameRate;
            app.ProgressBarGauge.Value = 1;
            times = 1;
            
            
            
            open(writer);
            
            for frame = 1:nFrame
                
                if mod(frame,a) == 0
                %only read part of frame. (number = original fps / target fps = 24 / 8 =3)
                    img = read(reader,frame);
                    
                    %%%%-GrayScal Option-%%%%%%%
                    if strcmp(type,'Grayscale AVI') || strcmp(type,'GS-MJPEG')
                        img_gray = rgb2gray(img);
                        imagesc(app.ImageAxes,img_gray);
                        writeVideo(writer,img_gray);
                    else
                        imagesc(app.ImageAxes,img);
                        writeVideo(writer,img);
                    end
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    
                end
                times = times + 1 ;
               app.ProgressBarGauge.Value = times*100/nFrame;
               app.StatusLamp.Color='0.00,1.00,1.00';
            end
            close(writer);
            
            app.StatusLamp.Color='0.00,1.00,0.00';
            
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Position = [100 100 649 763];
            app.UIFigure.Name = 'MATLAB App';

            % Create LoadButton
            app.LoadButton = uibutton(app.UIFigure, 'push');
            app.LoadButton.ButtonPushedFcn = createCallbackFcn(app, @LoadButtonPushed, true);
            app.LoadButton.Position = [36 659 100 22];
            app.LoadButton.Text = '1. Load MP4';

            % Create ProgressBarGaugeLabel
            app.ProgressBarGaugeLabel = uilabel(app.UIFigure);
            app.ProgressBarGaugeLabel.HorizontalAlignment = 'center';
            app.ProgressBarGaugeLabel.Position = [477 361 75 22];
            app.ProgressBarGaugeLabel.Text = 'Progress Bar';

            % Create ProgressBarGauge
            app.ProgressBarGauge = uigauge(app.UIFigure, 'linear');
            app.ProgressBarGauge.Position = [429 398 170 48];

            % Create StatusLampLabel
            app.StatusLampLabel = uilabel(app.UIFigure);
            app.StatusLampLabel.HorizontalAlignment = 'right';
            app.StatusLampLabel.Position = [326 411 39 22];
            app.StatusLampLabel.Text = 'Status';

            % Create StatusLamp
            app.StatusLamp = uilamp(app.UIFigure);
            app.StatusLamp.Position = [380 411 20 20];
            app.StatusLamp.Color = [1 0 0];

            % Create ExecuteButton
            app.ExecuteButton = uibutton(app.UIFigure, 'push');
            app.ExecuteButton.ButtonPushedFcn = createCallbackFcn(app, @ExecuteButtonPushed, true);
            app.ExecuteButton.FontSize = 14;
            app.ExecuteButton.Position = [399 313 100 26];
            app.ExecuteButton.Text = 'Execute';

            % Create FilenameLabel
            app.FilenameLabel = uilabel(app.UIFigure);
            app.FilenameLabel.HorizontalAlignment = 'right';
            app.FilenameLabel.Position = [41 638 65 22];
            app.FilenameLabel.Text = 'File name: ';

            % Create Fnameout
            app.Fnameout = uieditfield(app.UIFigure, 'text');
            app.Fnameout.Position = [41 617 239 22];

            % Create TotalFramenumberLabel
            app.TotalFramenumberLabel = uilabel(app.UIFigure);
            app.TotalFramenumberLabel.HorizontalAlignment = 'right';
            app.TotalFramenumberLabel.Position = [45 585 113 22];
            app.TotalFramenumberLabel.Text = 'Total Frame number';

            % Create Framenumber
            app.Framenumber = uieditfield(app.UIFigure, 'numeric');
            app.Framenumber.Position = [173 585 100 22];

            % Create BrStreamConverter_Ver10Label
            app.BrStreamConverter_Ver10Label = uilabel(app.UIFigure);
            app.BrStreamConverter_Ver10Label.FontSize = 18;
            app.BrStreamConverter_Ver10Label.FontWeight = 'bold';
            app.BrStreamConverter_Ver10Label.Position = [200 714 242 22];
            app.BrStreamConverter_Ver10Label.Text = 'Br-StreamConverter_Ver1.0';

            % Create Therehave4Class1AVIULabel_2
            app.Therehave4Class1AVIULabel_2 = uilabel(app.UIFigure);
            app.Therehave4Class1AVIULabel_2.Position = [127 10 425 22];
            app.Therehave4Class1AVIULabel_2.Text = 'Copyright @2022 OMU_Bridge Engineering Lab. Yu Chen., All rights reservet';

            % Create OutputParameterPanel
            app.OutputParameterPanel = uipanel(app.UIFigure);
            app.OutputParameterPanel.ForegroundColor = [0 0.4471 0.7412];
            app.OutputParameterPanel.Title = 'Output Parameter';
            app.OutputParameterPanel.BackgroundColor = [0.9412 0.9412 0.9412];
            app.OutputParameterPanel.FontWeight = 'bold';
            app.OutputParameterPanel.FontSize = 14;
            app.OutputParameterPanel.Position = [29 313 260 221];

            % Create Output_TypeDropDownLabel
            app.Output_TypeDropDownLabel = uilabel(app.OutputParameterPanel);
            app.Output_TypeDropDownLabel.HorizontalAlignment = 'right';
            app.Output_TypeDropDownLabel.Position = [15 159 74 22];
            app.Output_TypeDropDownLabel.Text = 'Output_Type';

            % Create OutputType
            app.OutputType = uidropdown(app.OutputParameterPanel);
            app.OutputType.Items = {'U-AVI', 'U-AVI+Grayscal', 'MJPEG', 'MJPEG+GrayS'};
            app.OutputType.ItemsData = {'Uncompressed AVI', 'Grayscale AVI', 'Motion JPEG AVI', 'GS-MJPEG'};
            app.OutputType.Position = [104 159 100 22];
            app.OutputType.Value = 'Uncompressed AVI';

            % Create fpsLabel
            app.fpsLabel = uilabel(app.OutputParameterPanel);
            app.fpsLabel.Position = [171 107 25 22];
            app.fpsLabel.Text = 'fps';

            % Create Frame_RateEditField_2Label
            app.Frame_RateEditField_2Label = uilabel(app.OutputParameterPanel);
            app.Frame_RateEditField_2Label.HorizontalAlignment = 'right';
            app.Frame_RateEditField_2Label.Position = [15 107 72 22];
            app.Frame_RateEditField_2Label.Text = 'Frame_Rate';

            % Create FrameRate
            app.FrameRate = uieditfield(app.OutputParameterPanel, 'numeric');
            app.FrameRate.Position = [102 107 64 22];

            % Create OriginalFrameOrDownsamplingegLabel
            app.OriginalFrameOrDownsamplingegLabel = uilabel(app.OutputParameterPanel);
            app.OriginalFrameOrDownsamplingegLabel.Position = [102 45 141 54];
            app.OriginalFrameOrDownsamplingegLabel.Text = {'*Original Frame '; '  Or Down sampling'; '  (If Original Frame is 24, '; '     outfile Recommend 8)'};

            % Create TabGroup
            app.TabGroup = uitabgroup(app.UIFigure);
            app.TabGroup.Position = [31 74 586 205];

            % Create UserManualTab
            app.UserManualTab = uitab(app.TabGroup);
            app.UserManualTab.Title = 'User Manual';

            % Create Therehave4Class1AVIULabel_3
            app.Therehave4Class1AVIULabel_3 = uilabel(app.UserManualTab);
            app.Therehave4Class1AVIULabel_3.VerticalAlignment = 'top';
            app.Therehave4Class1AVIULabel_3.Position = [12 96 223 73];
            app.Therehave4Class1AVIULabel_3.Text = {' 1. Load MP4.'; ' 2. Select Output type'; ' 3. Define the Frame Rate of outputfile'; ' 4. Execute'};

            % Create OutputtypeTab
            app.OutputtypeTab = uitab(app.TabGroup);
            app.OutputtypeTab.Title = 'Output type ';

            % Create Therehave4Class1AVIULabel
            app.Therehave4Class1AVIULabel = uilabel(app.OutputtypeTab);
            app.Therehave4Class1AVIULabel.BackgroundColor = [0.9412 0.9412 0.9412];
            app.Therehave4Class1AVIULabel.VerticalAlignment = 'top';
            app.Therehave4Class1AVIULabel.Position = [6 28 562 141];
            app.Therehave4Class1AVIULabel.Text = {' 1. U-AVI: 非圧縮+AVI (Uncompressed AVI)'; ' 2. U-AVI + Grayscale: グレースケール+非圧縮AVI (U-AVI + Grayscale)'; ' 3. MJPEG: Motion JPEG AVI'; ' 4. MJPEG+GrayS: Grayscal + MJPEG AVI'};

            % Create ImageAxes
            app.ImageAxes = uiaxes(app.UIFigure);
            app.ImageAxes.XTick = [];
            app.ImageAxes.YTick = [];
            app.ImageAxes.Position = [298 453 332 254];

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = APP_MP4toAVI_exported

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end