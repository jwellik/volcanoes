function  [vfile,efile,vfile2,efile2] = getVOTWfromGVPlink(odir)

%% volcanoes
% l = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes&maxFeatures=50&outputFormat=csv';
l = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes&outputFormat=csv';

options = weboptions;
options.Timeout = 60;
% options.CertificateFilename=('');

str = datestr(now,'yyyymmdd');

vfile = fullfile(odir,['Smithsonian_VOTW_Holocene_Volcanoes_',str,'.csv']);
vfile = websave(vfile,l,options);

if ~exist(vfile,'file')
    warning('problem with comcat wget command')
    disp(result)
end
ls(vfile)

T = readtable(vfile);
vname = fixStringName(T.Volcano_Name);
T2 = table(T.Latitude,T.Longitude,T.Elevation,T.Volcano_Number,vname',T.Country,T.Region);
vfile2 = fullfile(odir,['Smithsonian_VOTW_Holocene_Volcanoes.csv']);
T2.Properties.VariableNames = {'Lat','Lon','Elev','Vnum','Volcano','Country','Region'};

%% add old region names in for US swarm plots and FIG 1: Alaska, etc
vc = table2struct(T2);
volcDB = '/Users/jpesicek/JDP/EFIS/DB/volcDB';
oldVolcCat = fullfile(volcDB,...
    'Smithsonian_VOTW_Holocene_Volcanoes_20240426_keep4regions.csv'); %last with old regions
vc = getOldRegions(vc,oldVolcCat);
T2 = struct2table(vc);
%%

writetable(T2,vfile2)
ls(vfile2)

%% eruptions
% l = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Holocene_Eruptions&maxFeatures=50&outputFormat=csv';
l = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Holocene_Eruptions&outputFormat=csv';

efile = fullfile(odir,['Smithsonian_VOTW_Holocene_Eruptions_',str,'.csv']);
efile = websave(efile,l,options);

if ~exist(efile,'file')
    warning('problem with comcat wget command')
    disp(result)
end
ls(efile)
%%
l = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Pleistocene_Volcanoes&outputFormat=csv';

vfile2 = fullfile(odir,['Smithsonian_VOTW_Pleistocene_Volcanoes_',str,'.csv']);
vfile2 = websave(vfile2,l,options);

if ~exist(vfile2,'file')
    warning('problem with comcat wget command')
    disp(result)
end
ls(vfile2)
%%
l = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Pleistocene_Eruptions&outputFormat=csv';

efile2 = fullfile(odir,['Smithsonian_VOTW_Pleistocene_Eruptions_',str,'.csv']);
efile2 = websave(efile2,l,options);

if ~exist(efile2,'file')
    warning('problem with comcat wget command')
    disp(result)
end
ls(efile2)

end