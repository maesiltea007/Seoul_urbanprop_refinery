import pandas as pd
import re

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




