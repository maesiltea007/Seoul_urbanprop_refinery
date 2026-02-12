import pandas as pd
import re

from utils.column_merge_utils import merge_cols_and_place

def parse_legal_addr(
    addr : str      # 파싱할 주소
    ) -> list[str]: # 리스트로 파싱
    
    if addr is None or pd.isna(addr): return(pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA)    
    addr = addr.strip()
    if not addr: return(pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA)     # 주소값이 없을 경우에 널값 리턴
    
    시도 = pd.NA
    군구 = pd.NA
    동리= pd.NA
    번지= pd.NA
    상세= pd.NA
    중복주소= pd.NA
    addr_rest = addr
    
    # 주소 파싱
    match_groups = re.match(r"(.+?시)\s*(.*)", addr)
    if match_groups:
        시도 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
    
    match_groups = re.match(r"(.+?구)\s*(.*)", addr_rest)
    if match_groups:
        군구 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
        
    match_groups = re.match(r"(\S+)\s*(.*)", addr_rest)
    if match_groups:
        동리 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
        
    match_groups = re.match(r"(\d+(?:-\d+)?)(?:번지)?-?\s*(.*)", addr_rest)
    if match_groups:
        번지 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
    
    match_groups = re.match(r"([^,]*)\s*(?:,\s*(.*))", addr_rest)
    if match_groups:
        상세 = match_groups.group(1)
        중복주소 = match_groups.group(2).strip() if match_groups.group(2) else pd.NA
    return (시도, 군구, 동리, 번지, 상세, 중복주소)




def parse_street_addr(
    addr: str       # 파싱할 주소
    ) -> list[str]: # 리스트로 파싱
    
    if addr is None or pd.isna(addr): return(pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA)
    addr = addr.strip()
    if not addr: return(pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA)
    
    시도 = pd.NA
    군구 = pd.NA
    도로명 = pd.NA
    건물번호 = pd.NA
    상세 = pd.NA
    중복주소 = pd.NA
    addr_rest = addr
    
    match_groups = re.match(r"(.+?시)\s*(.*)", addr)
    if match_groups:
        시도 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
    
    match_groups = re.match(r"(.+?구)\s*(.*)", addr_rest)
    if match_groups:
        군구 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
        
    match_groups = re.match(r"(\S+(?:로|길))\s*(.*)", addr_rest)
    if match_groups:
        도로명 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
        
    match_groups = re.match(r"(\d+(?:-\d+)?)\s*(.*)", addr_rest)
    if match_groups:
        건물번호 = match_groups.group(1)
        addr_rest = match_groups.group(2).strip()
    
    match_groups = re.match(r"([^,]*)\s*(?:,\s*(.*))", addr_rest)
    if match_groups:
        상세 = match_groups.group(1)
        중복주소 = match_groups.group(2).strip() if match_groups.group(2) else pd.NA
        
    return (시도, 군구, 도로명, 건물번호, 상세, 중복주소)




def merge_two_df(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    on_list: list[str]
    ):
    suffix = 'suffix'
    
    merged = df1.merge( # OUTER JOIN
        df2,
        on = on_list,
        how='outer',
        suffixes=('',suffix),   # 컬럼명이 같은 경우 suffix 붙임
        indicator=True          # ['_merge'] 컬럼 추가
    )
    
    cols_to_column_merge = {c.removesuffix(suffix):c for c in merged.columns if c.endswith(suffix)}
    for col1, col2 in cols_to_column_merge.items():
        merged = merge_cols_and_place(merged, [col1,col2],[col1])
    
    matched = ( # 양쪽 매칭에 성공한 것
        merged.loc[merged['_merge']=='both']
        .drop(columns=['_merge'])
        .copy()
    )
    left_merged = ( # LEFT JOIN
        merged.loc[merged['_merge']=='left']
        .drop(columns=['_merge'])
        .copy()
    )
    right_merged = (# RIGHT JOIN
        merged.loc[merged['_merge']=='right']
        .drop(columns=['_merge'])
        .copy()
    )
    
    unmatched_df1 = (   # 매칭에 실패한 데이터
        merged.loc[merged['_merge']=='left_only']
        .copy()
    )
    unmatched_df1 = unmatched_df1.drop( # 원본 테이블의 형식으로 되돌리기
        columns=[c for c in unmatched_df1.columns if c not in df1.columns]
    )
    unmatched_df2 = (
        merged.loc[merged['_merge']=='right_only']
        .copy()
    )
    unmatched_df2 = unmatched_df2.drop(
        columns=[c for c in unmatched_df2.columns if c not in df2.columns]
    )
    
    return merged, matched, left_merged, right_merged, unmatched_df1, unmatched_df2