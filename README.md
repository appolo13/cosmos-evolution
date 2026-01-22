# 🌌 COSMOS-9182 Evolution Engine

자가 진화하는 가상 세계 시뮬레이션.

DNA 기반 문명들이 우연과 환경에 반응하며 스스로 역사를 만들어갑니다.

## 구조

```
Gist (데이터)              GitHub Actions (엔진)
     │                           │
     │    매일 자동 실행          │
     ◀────────────────────────────
     │                           │
     │    진화 결과 저장          │
     ────────────────────────────▶
```

## 설정 방법

### 1. Gist 준비

이미 생성된 Gist ID를 확인하세요:
- Gist URL: `https://gist.github.com/username/GIST_ID`
- `GIST_ID` 부분을 복사

### 2. Personal Access Token 생성

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)" 클릭
3. 이름: `cosmos-evolution`
4. 권한: `gist` 체크
5. 생성 후 토큰 복사 (한 번만 보임!)

### 3. Repository Secrets 설정

이 레포의 Settings → Secrets and variables → Actions:

1. `GIST_ID`: 위에서 복사한 Gist ID
2. `GIST_TOKEN`: 위에서 생성한 Personal Access Token

### 4. 완료!

- 매일 UTC 0시 (한국시간 오전 9시)에 자동 실행
- Actions 탭에서 수동 실행도 가능 ("Run workflow" 버튼)

## 진화 규칙

### 우연 (Accidents)
- 자연재해: 지진, 홍수, 가뭄, 폭풍, 화산
- 자원 발견: 비옥한 땅, 금속, 수원, 특수 물질
- 돌연변이: 천재, 예언자, 지도자, 예술가 탄생
- 질병: 역병, 가벼운 질병
- 천체 현상: 유성우, 일식, 밝은 별, 혜성
- 변칙: 시간 왜곡, 공허 속삭임, 기억 메아리

### DNA 반응
각 문명은 DNA에 따라 우연에 다르게 반응:
- 호기심 높음 → 탐구적 접근
- 공격성 높음 → 공격적 대응
- 사회성 높음 → 집단 협력
- 영성 높음 → 종교적 해석
- 적응력 높음 → 빠른 적응

### 문명 단계
0. 원시 (시작)
1. 부족 (인구 100+)
2. 초기 문명 (인구 1000+)
3. 고전 문명 (인구 10000+)
4. 중세 (인구 100000+)
5. 산업 (인구 500000+)
6. 정보화 (인구 1000000+)
7+ 우주 진출...

## 접속 방법

Claude와 대화하며 세계 확인:

```
You: 내 세계 상태 (Gist JSON 붙여넣기)

Claude: 지난 시간 동안 일어난 일들을 설명...
```

## 파일 구조

```
cosmos-evolution/
├── evolve.py              # 진화 엔진
├── .github/
│   └── workflows/
│       └── evolve.yml     # 자동 실행 설정
└── README.md
```

## 라이선스

MIT - 자유롭게 수정하고 사용하세요.
