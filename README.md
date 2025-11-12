# Seoul_urbanprop_refinery

A data pipeline for cleaning and integrating **MOLIT (Ministry of Land, Infrastructure and Transport)** building register datasets — **표제부 (Main Register)** and **총괄표제부 (Comprehensive Register)** files.



## Usage

1. input/ 폴더에 해당 파일들을 아래와 같이 저장합니다
   - 표제부 : '일반{년도}.txt'
   - 종합표제부 : '총괄{년도}.txt'
   example) '총괄25.txt'

2. ipynb 파일을 실행하면 output/ 폴더에 엑셀 형식으로 병합된 파일이 저장됩니다.



## Notebooks

'1.국토부-표제부-총괄표제부-병합.ipynb'

'2.병합된-건축물대장-정제.ipynb'

'3.그룹종류-따라-디자인-추가.ipynb



## Reference

This project is hardly based on the original code by GwanBin Park (Chung-Ang University, SoftWare Department)
