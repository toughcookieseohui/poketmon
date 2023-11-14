### 스크래핑 데이터  구성


    key:: 키로 사용 할 수 있는 번호
    no:: 포켓몬 도감 번호
    
    name:: 포켓몬 이름
    
    type:: 타입(eg. 풀, 물)
    
    height:: 키
    
    sort:: 분류(eg. 화염포켓몬)
    
    sex:: 성별(eg. 양성, 수컷, 암컷, 불명)
    
    weight:: 몸무게
    
    ability:: 특성(eg. 날씨부정)
    
    description:: 포켓몬에 대한 설명
    
    evolution:: 진화 단계(eg. 파이리 > 리자드 > 리자몽)
    
    img_src:: 포켓몬 이미지 주소


### 특이사항

분류에서 '포켓몬'은 떼고 저장(eg. 화염포켓몬 >> 화염)

타입과 특성, 진화 단계 등 다중 값 속성의 경우 세미콜론(;)을 구분자로 하여 저장

성별에서 양성은 b(bi), 수컷은 m(mail), 암컷은 f(femail), 불명은 u(unkown) 으로 저장

몸무게가 '???'인 경우 INF(무한)로 저장
