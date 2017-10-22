function csv2kml(mainDir,data2WorkOn,class2show,lines2show,nedOrigin,openFileWhenDone)
%%%%
% mainDir - Dir where train/test data is
% data2WorkOn - Name of the data CSV file
% class2show - Which class in CSV file to draw, or (-1) if using test set or lines2show parameter
% lines2show - Which lines in CSV file to draw
% nedOrigin - Geo coordinates where XYZ = 0
% openFileWhenDone - Open KML after it is ready (KML files have to be associated with Google Earth)
%%%%
if nargin == 0
	mainDir = 'D:\DataHack2017\';
	%data2WorkOn = 'test';
	data2WorkOn = 'train';	
	class2show = -1;  %for 'train' only
	lines2show = 1:300; %for 'test' (or 'train if class2show == -1)
	nedOrigin = [31.784491,35.214245,0];
	openFileWhenDone = 1;
end



name = 'Rocket_Data_Science';
if class2show > 0
    name = [name '_' num2str(class2show)];
end
kmlStrHeader = ['<kml xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://www.opengis.net/kml/2.2"> \n' ...
'  <Document> \n' ...
'    <name>' name '</name> \n'];

kmlStrFooter = '  </Document></kml>';
strUP = '';
strDN = '';

disp('Loading...');
csvSetTable = readtable([mainDir data2WorkOn '.csv']);
csvSet = table2array(csvSetTable(:,1:211));

disp('Working...');
if strfind(data2WorkOn,'train') && class2show > 0
    lines2show = find(csvSet(:,end) == class2show);
end

for lll = lines2show(:)'
    lla_str = ned2geodetic2String(csvSet,lll,nedOrigin);
    velVal = round((norm( csvSet(lll,6:8) )/1500) * 255 );
    velColor = dec2hex(velVal,2);
    if  csvSet(lll,8) > 0
      clr_str = ['FF' velColor '0000'];
      strUP = addPlacemark(strUP,['line_' num2str(lll-1)],lla_str,clr_str);
    else
      clr_str = ['FF0000' velColor];
      strDN = addPlacemark(strDN,['line_' num2str(lll-1)],lla_str,clr_str);      
    end
end

finalStr = [kmlStrHeader '<Folder>\n <name>UP</name> \n' strUP ...
    '</Folder><Folder>\n <name>DOWN</name> \n' strDN '</Folder>' kmlStrFooter];

disp('Saving...');
fid = fopen([mainDir name '_MATLAB.kml'],'w');
fprintf(fid,finalStr);
fclose(fid);

disp('Done!');
if openFileWhenDone
   winopen( [mainDir name '_MATLAB.kml']);
end

end

function str = addPlacemark(str,name,lla_str,clr_str)

strTMP = [ ...
'    <Placemark> \n' ...
'      <name>' name '</name>  \n' ...
'      <Style>  \n' ...
'        <LineStyle>  \n' ...
'          <color>' clr_str '</color> \n' ...
'          <width>4</width> \n' ...
'        </LineStyle>  \n' ...
'      </Style> \n' ...
'      <LineString> \n' ...
'        <altitudeMode>absolute</altitudeMode> \n' ...
'        <coordinates>'  lla_str '</coordinates> \n' ...
'      </LineString> \n' ...
'    </Placemark>     \n' ...
];

str = [str strTMP];

end


function lla_str = ned2geodetic2String(csvSet,line,nedOrigin)
lla_str = '';
for iii = 1:15
    northCoor = csvSet(line,3+7*(iii-1));
    eastCoor = csvSet(line,4+7*(iii-1));
    downCoor = -csvSet(line,5+7*(iii-1));
    if isnan(northCoor)
       continue 
    end
    [lat,lon,h] = ned2geodetic(northCoor,eastCoor,downCoor,nedOrigin(1),nedOrigin(2),nedOrigin(3),referenceEllipsoid('GRS 80'));
    lla_str = [lla_str num2str([lon lat h],'%.10f,%.10f,%.10f') ' '];
end

end
