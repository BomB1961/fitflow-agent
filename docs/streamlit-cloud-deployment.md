# Streamlit Community Cloud 배포 준비 가이드

## 목적

이 문서는 FitFlow Agent의 Streamlit UI를 사용자가 직접 Streamlit Community Cloud에 배포할 때 필요한 준비 사항을 정리합니다.

- 리뷰어가 브라우저에서 포트폴리오 데모를 확인할 수 있게 합니다.
- Streamlit UI는 이미 배포된 Render FastAPI backend를 호출합니다.
- 이 단계는 배포 준비만 다루며, 로그인, OAuth, 2FA, billing, password, API key, secret credential 처리는 포함하지 않습니다.
- 실제 Streamlit UI URL은 사용자가 수동 배포 후 확인하기 전까지 문서에 추가하지 않습니다.

## 현재 backend URL

- Live API: https://fitflow-agent-api.onrender.com
- Swagger UI: https://fitflow-agent-api.onrender.com/docs
- Health check: https://fitflow-agent-api.onrender.com/health

현재 배포된 API는 기본 `mock` provider를 사용하므로 API key 없이 데모를 확인할 수 있습니다.

## 수동 배포 절차

Streamlit Community Cloud에서 아래 값을 사용해 직접 배포합니다.

1. Streamlit Community Cloud에 접속합니다.
2. GitHub 계정을 사용자가 직접 연결합니다.
3. Repository로 `BomB1961/fitflow-agent`를 선택합니다.
4. Branch는 이 변경이 병합된 뒤 `main`을 선택합니다.
5. Main file path는 `ui/streamlit_app.py`로 지정합니다.
6. App URL은 사용자가 원하는 값으로 선택합니다.

이 저장소의 Streamlit UI는 기본적으로 로컬 API인 `http://localhost:8000`을 호출합니다. Cloud 배포에서는 아래 환경 변수를 설정해 Render API를 호출하게 만듭니다.

## 환경 변수 설정

Streamlit Cloud의 app 설정에서 다음 값을 추가합니다.

```text
FITFLOW_API_URL=https://fitflow-agent-api.onrender.com
```

`FITFLOW_API_URL`은 secret credential이 아니라 공개된 backend URL입니다. 이 mock provider 데모에는 API key를 추가하지 않습니다.

## Render free plan 참고

Render free plan은 비활성 상태가 길어지면 API가 sleep 상태가 될 수 있습니다. 이 경우 첫 요청은 cold start 때문에 느릴 수 있습니다.

포트폴리오 데모에서는 정상적인 제한 사항으로 보고, 첫 요청이 느리면 잠시 기다린 뒤 다시 시도합니다.

## 수동 배포 후 확인 체크리스트

1. Streamlit app URL을 엽니다.
2. 샘플 job posting과 profile 내용을 그대로 제출합니다.
3. API 응답이 UI에 표시되는지 확인합니다.
4. 첫 요청이 느리면 https://fitflow-agent-api.onrender.com/health 를 열어 Render API를 깨웁니다.
5. Streamlit UI URL이 확정된 뒤에만 README 업데이트 여부를 검토합니다.

## 문제 해결

- UI가 API에 연결하지 못하면 Streamlit Cloud 설정의 `FITFLOW_API_URL` 값을 확인합니다.
- API 응답이 느리면 Render cold start가 끝날 때까지 기다립니다.
- dependency 설치가 실패하면 `requirements.txt`와 `pyproject.toml`의 dependency 설정을 확인합니다.
- mock provider 데모에는 secrets, API key, OAuth 설정을 추가하지 않습니다.
- 이 배포는 포트폴리오 데모 확인용이며 production-ready 운영 환경을 의미하지 않습니다.

## Dependency 참고

Streamlit Community Cloud는 Python dependency file을 사용해 앱 의존성을 설치합니다. 공식 문서는 `requirements.txt` 사용을 권장하며, dependency file은 repository root 또는 app entrypoint 파일이 있는 디렉터리에 둘 수 있다고 설명합니다.

이 저장소는 root의 `requirements.txt`에 Streamlit UI 실행에 필요한 최소 dependency만 둡니다.

- Streamlit Community Cloud app dependencies: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
