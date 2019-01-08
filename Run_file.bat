move mmdata.txt "C:\Users\Amanda Barker\Desktop\PrDM"
move Litter_size.txt "C:\Users\Amanda Barker\Desktop\PrDM"
cd "C:\Users\Amanda Barker\Desktop\PrDM"
del Results_1.txt Results_parsed.txt
PrDM.exe < Litter_size.txt > Results.txt
type Results.txt| findstr /r [0-9].[0-9][0-9][0-9] > Results_1.txt
for /f "tokens=1,2 delims== " %%a in (Results_1.txt) do (
if "%%a"=="%PrDM %" set var = %%b
echo:%%b> Results_parsed.txt
)
del Results.txt
copy Results_parsed.txt "C:\Users\Amanda Barker\Dropbox\Python_Bnose\"
cd "C:\Users\Amanda Barker\Dropbox\Python_Bnose\"
del Done.txt