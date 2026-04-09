# 가이드


## 실행순서
### 1. concat_표제부_총괄표제부
| 원본  | 파일명 |
| ------------- |:-------------:|
| 일반 표제부      | input/일반.txt   |
| 총괄 표제부     |  input/총괄.txt   |
| 폐쇄대장    | input/closed_blds.csv  |

파일명을 위와 같이 설정한 후 concat_표제부_총괄표제부 폴더 내 코드를 일괄적으로 실행하면 output/blds.csv에 결과 파일 생성\
실행 순서 : (1)->(1-2)->(2)->(3)->(4)
<br><br><br><br>

### 2. merge_kapt_서울시공공주택정보
| 원본  | 파일명 |
| ------------- |:-------------:|
| 2번(K-apt 관리비공개의무단지 기본정보)  | input/kapt.xlsx   |
| 3번(서울시 공동주택 아파트 정보)     |  input/서울시 공동주택 아파트 정보.csv   |

파일명을 위와 같이 설정한 후 merge_kapt_sapt.ipynb 실행하면 output/apt.csv에 결과 파일 생성
<br><br><br><br>

### 3. merge_apt_건축물대장
| 원본  | 파일명 |
| ------------- |:-------------:|
| output/blds.csv (1번 과정 결과 파일) | input/blds.csv|
| output/apt.csv (2번 과정 결과 파일) |  input/apt.csv  |

앞의 1번 과정과 2번 과정의 결과파일을 input 폴더로 이동시킨 후 merge_apt_건축물대장.ipynb 실행해면 output/apt_blds_병합.csv에 결과파일 생성
<br><br><br><br>

### 4. merge_master_공동주택현황
| 원본  | 파일명 |
| ------------- |:-------------:|
| output/apt_blds_병합.csv (3번 과정 결과파일) | input/blds.csv|
| 서룰시공공주택아파트정보  |  input/units_summary.xlsx  |

파일명을 위와 같이 변경한 후 코드 실행하면 output/final.csv 파일 생성

### 5(optional). post_processing
최종 파일(final.csv)에서 1번(blds.csv)이 포함되지 않은 row는 전부 드랍