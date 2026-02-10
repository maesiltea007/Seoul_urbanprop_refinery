import pandas as pd
import re
from itertools import chain



def norm_to_str(val):
    return '' if pd.isna(val) else str(val).strip()



############ 컬럼병합 함수 ############
def merge_col_values(
    vals: list      # 병합할 컬럼값 리스트
    ) -> list[str]: # 병합된 컬럼값 리스트
    
    vals = [norm_to_str(c) for c in vals]
    
    uniq = []  # 유일한 값만 보관
    seen = set()                   
    for val in vals:
        if val !='' and val not in seen:
            uniq.append(val)
            seen.add(val)
    
    return uniq + [''] * (len(vals) - len(uniq)) # 인풋한 리스트 길이만큼 패딩해서 리턴



def merge_cols_and_place(
    df: pd.DataFrame,
    source_cols: list,  # 병합할 컬럼명 리스트
    merged_cols: list   # 결과 컬럼명 리스트
    ) -> pd.DataFrame:

    cols_to_remain = merged_cols.copy()             # 병합된 컬럼 중 결과 테이블에 남길 컬럼명 리스트
    anchor_idx = df.columns.get_loc(source_cols[0]) # 병합된 컬럼들을 위치시킬 곳

    if len(source_cols)>len(merged_cols):   # merged_cols의 사이즈를 source_cols와 같게
        merged_cols = merged_cols+['']*(len(source_cols)-len(merged_cols))
    for i,col in enumerate(merged_cols):
        if col=='':
            merged_cols[i] = f"보조_{source_cols[0]}{i+1}"  # merged_cols에 새로 생성한 컬럼명은 암의로 작명

    source_cols_df = df[source_cols].copy() # 병합할 컬럼들은 별개의 df에 보관
    df = df.drop(columns=source_cols)       # 원본 테이블의 병합할 컬럼들은 삭제
    
    df[merged_cols] = source_cols_df.apply( # 병합
        lambda row: merge_col_values([row[col] for col in source_cols]),
        axis=1,
        result_type='expand'
    )
    
    for i,col in enumerate(merged_cols):    # 병합된 컬럼 위치 조정
        col_to_move = df.pop(col)
        df.insert(anchor_idx+i, col, col_to_move)
    
    cols_to_drop = list(set(merged_cols)-set(cols_to_remain))
    df = df.drop(columns=(cols_to_drop))
    return df



def column_merge(df, column_merge_rules):
    for source_column_rule, merged_columns in column_merge_rules:
        source_columns = list(chain.from_iterable(source_column_rule))
        df = merge_cols_and_place(df,  source_columns, merged_columns)
    return df




############ 병합종류 컬럼병합 ############
def merge_병합종류_values(
    vals1: str,
    vals2: str
    ) -> str:
    vals1, vals2 = norm_to_str(vals1), norm_to_str(vals2)
    
    if vals1=='': return vals2
    if vals2=='': return vals1
    
    set1 = {v.strip() for v in vals1.split(',') if v.strip()}
    set2 = {v.strip() for v in vals2.split(',') if v.strip()}
    merged_vals = set1|set2 # 합집합
    merged_vals = sorted(   # sort
        merged_vals,
        key=lambda val: int(val.replace('번', ''))
    )
    
    return ','.join(merged_vals)

def merge_병합종류(
    df: pd.DataFrame,
    col1: str,
    col2: str
    ) -> pd.DataFrame:
    
    df['병합종류'] = df.apply(  # 두 테이블의 병합종류 컬럼을 병합, 새로운 병합종류 컬럼 생성
        lambda row: merge_병합종류_values(row[col1], row[col2]),
        axis=1
    )
    
    # 일관성을 위해 여기서 컬럼의 위치를 조정하거나 드랍하지 않음
    
    return df